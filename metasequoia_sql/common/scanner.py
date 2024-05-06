"""
抽象语法树扫描器
"""

from typing import List, Union, Optional

from metasequoia_sql.errors import ScannerError
from metasequoia_sql.lexical import AMTBase, AMTMark

__all__ = ["TokenScanner"]


class TokenScanner:
    """Token 扫描器"""

    def __init__(self, elements: List[AMTBase],
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
            if element.equals(AMTMark.SPACE):
                if ignore_space is False:  # 关闭忽略空白字符的模式
                    filtered_elements.append(element)
            elif element.equals(AMTMark.COMMENT):
                if ignore_comment is False:  # 关闭忽略注释的模式
                    filtered_elements.append(element)
            else:
                filtered_elements.append(element)

        if pos < 0:
            raise ScannerError(f"初始化的指针小于 0: pos={pos}")
        if pos > len(elements):
            raise ScannerError(f"初始化指针大于字符串长度: len(text)={len(elements)}, pos={pos}")

        self._elements = filtered_elements
        self._pos = pos
        self._len = len(filtered_elements)

    @property
    def elements(self) -> List[AMTBase]:
        """返回扫描器中的所有元素"""
        return self._elements

    @property
    def pos(self) -> int:
        """返回当前扫描指针"""
        return self._pos

    def get(self) -> Optional[AMTBase]:
        """获取当前指针位置元素，但不移动指针

        - 如果指针已到达字符串末尾，则返回 None
        - 如果指针超出字符串长度，则抛出异常
        """
        if self.pos > self._len:
            raise ScannerError(f"要获取的指针大于等于字符串长度: len={self._len}, pos={self.pos}")
        if self.pos == self._len:
            return None
        return self._elements[self._pos]

    def pop(self) -> AMTBase:
        """获取当前指针位置元素，并移动指针

        - 如果要移动到的指针位置超出字符串长度，则抛出异常
        """
        if self.pos >= self._len:
            raise ScannerError(f"要移动到的指针下标大于字符串长度: len={self._len}, pos={self.pos + 1} {self}")

        result = self._elements[self.pos]
        self._pos += 1  # 移动指针
        return result

    def _get_by_offset(self, idx: int) -> Optional[AMTBase]:
        """获取当前指针位置 + idx 位置的元素，但不一定指针
        """
        if self.pos + idx >= self._len or self.pos + idx < 0:
            return None
        return self._elements[self.pos + idx]

    def close(self) -> None:
        """关闭扫描器，如果扫描器没有遍历完成则抛出异常"""
        if not self.is_finish:
            raise ScannerError(f"关闭了没有遍历完成的扫描器 {self}")

    def __repr__(self):
        return f"<{self.__class__.__name__} tokens={self.elements[self.pos:]}, pos={self.pos}>"

    def search(self, *tokens: Union[str, AMTMark]) -> bool:
        """从当前配置开始匹配 tokens

        - 如果匹配成功，则返回 True
        - 如果匹配失败，则返回 False
        """
        for idx, token in enumerate(tokens):
            refer = self._get_by_offset(idx)
            if refer is None or not refer.equals(token):
                return False
        return True

    def search_and_move(self, *tokens: Union[str, AMTMark]) -> bool:
        """从当前配置开始匹配 tokens

        - 如果匹配成功，则将指针移动到 tokens 后的下一个元素并返回 True
        - 如果匹配失败，则不移动指针并返回 False
        """
        for idx, token in enumerate(tokens):
            refer = self._get_by_offset(idx)
            if refer is None or not refer.equals(token):
                return False
        for _ in range(len(tokens)):
            self.pop()
        return True

    def match(self, *tokens: Union[str, AMTMark]) -> None:
        """从当前配置开始匹配 tokens

        - 如果匹配成功，则将指针移动到 tokens 后的下一个元素
        - 如果匹配失败，则抛出异常
        """
        for word in tokens:
            if not self.pop().equals(word):
                raise ScannerError(f"没有解析到目标词语:目标词={tokens} - {self}")

    def get_as_source(self) -> str:
        """将指针向后移动 1 个元素并返回当前元素的 source"""
        return self.get().source

    def pop_as_source(self) -> str:
        """将指针向后移动 1 个元素并返回当前元素的 source"""
        return self.pop().source

    def get_as_children_scanner(self, ignore_space: bool = True, ignore_comment: bool = True) -> "TokenScanner":
        """【不移动指针】返回当前指针位置的插入语节点的子节点的扫描器"""
        return TokenScanner(self.get().children(), ignore_space=ignore_space, ignore_comment=ignore_comment)

    def pop_as_children_scanner(self, ignore_space: bool = True, ignore_comment: bool = True) -> "TokenScanner":
        """【移动指针】返回当前指针位置的插入语节点的子节点的扫描器"""
        return TokenScanner(self.pop().children(), ignore_space=ignore_space, ignore_comment=ignore_comment)

    def split_by(self,
                 source: str,
                 ignore_space: bool = True,
                 ignore_comment: bool = True) -> List["TokenScanner"]:
        """【移动指针（到末尾）】将后续元素拆分为使用 source 分隔的扫描器列表"""
        result = []
        tokens = []
        while not self.is_finish:
            token: AMTBase = self.pop()
            if token.equals(source):
                if len(tokens) > 0:
                    result.append(TokenScanner(tokens, ignore_space=ignore_space, ignore_comment=ignore_comment))
                    tokens = []
            else:
                tokens.append(token)
        if len(tokens) > 0:
            result.append(TokenScanner(tokens, ignore_space=ignore_space, ignore_comment=ignore_comment))
        return result

    def pop_as_children_scanner_list_split_by(self,
                                              source: str,
                                              ignore_space: bool = True,
                                              ignore_comment: bool = True) -> List["TokenScanner"]:
        """【移动指针】返回当前指针位置的插入语结点的子节点使用 source 分隔的扫描器列表"""
        result = []
        tokens = []
        for token in self.pop().children():
            if token.equals(source):
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
        return self._pos >= self._len
