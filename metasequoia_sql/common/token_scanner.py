"""
TODO 多语句解析支持
"""

from typing import List, Optional

from metasequoia_sql import ast
from metasequoia_sql.common.base_scanner import BaseScanner
from metasequoia_sql.errors import ScannerError
from metasequoia_sql.errors import SqlParseError


class TokenScanner(BaseScanner):
    """Token 扫描器"""

    def __init__(self, elements: List[ast.AST],
                 pos: int = 0,
                 ignore_space: bool = False,
                 ignore_comment: bool = False):
        """

        Parameters
        ----------
        elements : List[ast.AST]
            当前层级的抽象语法树节点列表
        pos : int, default = 0
            当前正在处理的抽象语法树节点下标
        """
        # 根据要求筛选输入元素
        filtered_elements = []
        for element in elements:
            if element.is_space:
                if ignore_space is False:  # 关闭忽略空白字符的模式
                    filtered_elements.append(element)
            elif element.is_comment:
                if ignore_comment is False:  # 关闭忽略注释的模式
                    filtered_elements.append(element)
            else:
                filtered_elements.append(element)

        super().__init__(filtered_elements, pos)

    def search(self, *tokens: str) -> bool:
        """从当前配置开始匹配 tokens

        - 如果匹配成功，则返回 True
        - 如果匹配失败，则返回 False
        """
        for idx, token in enumerate(tokens):
            refer = self._get_by_offset(idx)
            if refer is None or not refer.equals(token):
                return False
        return True

    def search_and_move(self, *tokens: str) -> bool:
        """从当前配置开始匹配 tokens

        - 如果匹配成功，则将指针移动到 tokens 后的下一个元素并返回 True
        - 如果匹配失败，则不移动指针并返回 False
        """
        for idx, token in enumerate(tokens):
            refer = self._get_by_offset(idx)
            if refer is None or not refer.equals(token):
                return False
        else:
            for _ in range(len(tokens)):
                self.pop()
            return True

    def match(self, *tokens: str) -> None:
        """从当前配置开始匹配 tokens

        - 如果匹配成功，则将指针移动到 tokens 后的下一个元素
        - 如果匹配失败，则抛出异常
        """
        for word in tokens:
            if not self.pop().equals(word):
                raise SqlParseError(f"没有解析到目标词语:{self._elements}, 目标词={tokens}")

    def pop_as_source(self) -> str:
        """将指针向后移动 1 个元素并返回当前元素的 source"""
        return self.pop().source

    def get_as_children_scanner(self, ignore_space: bool = True, ignore_comment: bool = True) -> "TokenScanner":
        """【不移动指针】返回当前指针位置的插入语节点的子节点的扫描器"""
        return TokenScanner(self.now.children, ignore_space=ignore_space, ignore_comment=ignore_comment)

    def pop_as_children_scanner(self, ignore_space: bool = True, ignore_comment: bool = True) -> "TokenScanner":
        """【移动指针】返回当前指针位置的插入语节点的子节点的扫描器"""
        return TokenScanner(self.pop().children, ignore_space=ignore_space, ignore_comment=ignore_comment)

    def split_by_comma(self) -> List["TokenScanner"]:
        """【移动指针（到末尾）】将后续元素拆分为使用逗号分隔的扫描器列表"""
        result = []
        tokens = []
        while not self.is_finish:
            token = self.pop()
            if token.is_comma:
                if len(tokens) > 0:
                    result.append(TokenScanner(tokens))
                    tokens = []
            else:
                tokens.append(token)
        if len(tokens) > 0:
            result.append(TokenScanner(tokens))
        return result

    def pop_as_children_scanner_list_split_by_comma(self,
                                                    ignore_space: bool = True,
                                                    ignore_comment: bool = True) -> List["TokenScanner"]:
        """【移动指针】返回当前指针位置的插入语结点的子节点使用逗号分隔的扫描器列表"""
        result = []
        tokens = []
        for token in self.pop().children:
            if token.is_comma:
                if len(tokens) > 0:
                    result.append(TokenScanner(tokens, ignore_space=ignore_space, ignore_comment=ignore_comment))
                    tokens = []
            else:
                tokens.append(token)
        if len(tokens) > 0:
            result.append(TokenScanner(tokens, ignore_space=ignore_space, ignore_comment=ignore_comment))
        return result

    @property
    def is_finish(self) -> bool:
        """返回是否已匹配结束"""
        return not self._pos < self._len or self.now.is_semicolon


def build_token_scanner(sql: str, ignore_space=True, ignore_comment=True):
    """根据 sql 语句构造扫描器"""
    return TokenScanner(ast.parse_as_tokens(sql), ignore_space=ignore_space, ignore_comment=ignore_comment)
