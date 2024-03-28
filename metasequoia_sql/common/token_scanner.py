from typing import List, Optional

from metasequoia_sql import ast
from metasequoia_sql.errors import ScannerError
from metasequoia_sql.errors import SqlParseError


class TokenScanner:
    """Token 扫描器"""

    def __init__(self, elements: List[ast.AST], pos: int = 0, ignore_space: bool = False):
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

        if ignore_space is True:  # 忽略空白字符的模式
            elements = [element for element in elements if element.is_space is False]

        self._elements = elements
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
        return self.get_next()

    @property
    def next2(self) -> Optional[ast.AST]:
        """设当前指针位置为 idx，则返回 idx+2 位置的元素"""
        return self.get_next(2)

    @property
    def next3(self) -> Optional[ast.AST]:
        """设当前指针位置为 idx，则返回 idx+2 位置的元素"""
        return self.get_next(3)

    @property
    def next4(self) -> Optional[ast.AST]:
        """设当前指针位置为 idx，则返回 idx+2 位置的元素"""
        return self.get_next(4)

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

    def get_next(self, idx: int = 1) -> Optional[ast.AST]:
        """获取当前指针下一个位置的元素，但不一定指针
        """
        if self._pos + idx >= self._len:
            return None
        return self._elements[self._pos + idx]

    def pop(self) -> ast.AST:
        """获取当前指针位置元素，并移动指针

        - 如果要移动到的指针位置超出字符串长度，则抛出异常
        """
        if self._pos >= self._len:
            raise ScannerError(f"要移动到的指针下标大于字符串长度: len={self._len}, pos={self._pos + 1}")

        self._last = self.get()  # 更新上一个元素
        result = self._elements[self._pos]
        self._pos += 1  # 移动指针
        return result

    def pop_as_source(self) -> str:
        """将指针向后移动 1 个元素并返回当前元素的 source"""
        return self.pop().source

    def pop_as_children_scanner(self) -> "TokenScanner":
        """【移动指针】返回当前指针位置的插入语节点的子节点的扫描器"""
        return TokenScanner(self.pop().children)

    def pop_as_children_scanner_list_split_by_comma(self, ignore_space: bool = False) -> List["TokenScanner"]:
        """【移动指针】返回当前指针位置的插入语结点的子节点使用逗号分隔的扫描器列表"""
        result = []
        tokens = []
        for token in self.pop().children:
            if token.is_comma:
                if len(tokens) > 0:
                    result.append(TokenScanner(tokens, ignore_space=ignore_space))
                    tokens = []
            else:
                tokens.append(token)
        if len(tokens) > 0:
            result.append(TokenScanner(tokens, ignore_space=ignore_space))
        return result

    def match_token(self, word: str) -> None:
        """尝试从当前指针位置开始匹配 word，如果匹配失败则抛出异常"""
        if not self.pop().equals(word):
            raise SqlParseError(f"tokens={self._elements}, words={word}")

    def match_tokens(self, words: List[str]) -> None:
        """尝试从当前指针位置开始匹配 words，如果匹配失败则抛出异常"""
        for word in words:
            if not self.pop().equals(word):
                raise SqlParseError(f"tokens={self._elements}, words={words}")

    @property
    def is_finish(self) -> bool:
        """返回是否已匹配结束"""
        return not self._pos < self._len

    def __repr__(self):
        return f"<TokenScanner tokens={self._elements}, pos={self._pos}>"
