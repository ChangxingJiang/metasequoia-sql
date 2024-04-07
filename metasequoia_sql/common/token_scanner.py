"""
TODO 多语句解析支持
"""

from typing import List, Optional

from metasequoia_sql import ast
from metasequoia_sql.errors import ScannerError
from metasequoia_sql.errors import SqlParseError


class TokenScanner:
    """Token 扫描器"""

    def __init__(self,
                 elements: List[ast.AST],
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
        if pos < 0:
            raise ScannerError(f"初始化的指针小于 0: pos={pos}")
        if pos > len(elements):
            raise ScannerError(f"初始化指针大于字符串长度: len(text)={len(elements)}, pos={pos}")

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

        self._elements = filtered_elements
        self._pos = pos
        self._len = len(self._elements)

        self._last = elements[pos - 1] if pos > 0 else None  # 上一个元素

    @property
    def elements(self) -> List[ast.AST]:
        return self._elements

    @property
    def pos(self) -> int:
        return self._pos

    @property
    def last(self) -> Optional[ast.AST]:
        """当前指针位置的上一个字符"""
        return self._last

    @property
    def now(self) -> Optional[ast.AST]:
        """当前指针位置的字符"""
        return self.get()

    @property
    def next1(self) -> Optional[ast.AST]:
        """当前指针位置的下一个字符"""
        return self._get_by_offset(1)

    @property
    def next2(self) -> Optional[ast.AST]:
        """设当前指针位置为 idx，则返回 idx+2 位置的元素"""
        return self._get_by_offset(2)

    @property
    def next3(self) -> Optional[ast.AST]:
        """设当前指针位置为 idx，则返回 idx+2 位置的元素"""
        return self._get_by_offset(3)

    @property
    def next4(self) -> Optional[ast.AST]:
        """设当前指针位置为 idx，则返回 idx+2 位置的元素"""
        return self._get_by_offset(4)

    def get(self) -> Optional[ast.AST]:
        """获取当前指针位置元素，但不移动指针

        - 如果指针已到达字符串末尾，则返回 None
        - 如果指针超出字符串长度，则抛出异常
        """
        if self._pos > self._len:
            raise ScannerError(f"要获取的指针大于等于字符串长度: len={self._len}, pos={self._pos}")
        if self._pos == self._len:
            return None
        return self._elements[self._pos]

    def pop(self) -> ast.AST:
        """获取当前指针位置元素，并移动指针

        - 如果要移动到的指针位置超出字符串长度，则抛出异常
        """
        if self._pos >= self._len:
            raise ScannerError(f"要移动到的指针下标大于字符串长度: len={self._len}, pos={self._pos + 1} {self}")

        self._last = self.get()  # 更新上一个元素
        result = self._elements[self._pos]
        self._pos += 1  # 移动指针
        return result

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

    def _get_by_offset(self, idx: int) -> Optional[ast.AST]:
        """获取当前指针位置 + idx 位置的元素，但不一定指针
        """
        if self._pos + idx >= self._len:
            return None
        return self._elements[self._pos + idx]

    def __repr__(self):
        return f"<TokenScanner tokens={self.elements[self.pos:]}, pos={self.pos}>"


def build_scanner(sql: str, ignore_space=True, ignore_comment=True):
    """根据 sql 语句构造扫描器"""
    return TokenScanner(ast.parse_as_tokens(sql), ignore_space=ignore_space, ignore_comment=ignore_comment)
