"""
抽象语法树扫描器
"""

from typing import List, Union, Optional, Set

from metasequoia_sql.errors import ScannerError
from metasequoia_sql.lexical import AMTBase, AMTMark

__all__ = ["TokenScanner"]


class TokenScanner:
    """抽象词法树节点扫描器"""

    def __init__(self, elements: List[AMTBase]):
        """抽象词法树扫描器的构造方法

        Parameters
        ----------
        elements : List[ast.AST]
            当前层级的抽象语法树节点列表
        """
        self._elements = elements
        self._pos = 0
        self._len = len(elements)

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
        if self._pos > self._len:
            raise ScannerError(f"要获取的指针大于等于字符串长度: len={self._len}, pos={self._pos}")
        if self._pos == self._len:
            return None
        return self._elements[self._pos]

    def pop(self) -> AMTBase:
        """获取当前指针位置元素，并移动指针

        - 如果要移动到的指针位置超出字符串长度，则抛出异常
        """
        if self._pos >= self._len:
            raise ScannerError(f"要移动到的指针下标大于字符串长度: len={self._len}, pos={self._pos + 1} {self}")

        result = self._elements[self._pos]
        self._pos += 1  # 移动指针
        return result

    def move(self, idx: int = 1) -> None:
        """移动指针"""
        self._pos += idx

    def close(self) -> None:
        """关闭扫描器，如果扫描器没有遍历完成则抛出异常"""
        if not self.is_finish:
            raise ScannerError(f"关闭了没有遍历完成的扫描器 {self}")

    def __repr__(self):
        return f"<{self.__class__.__name__} tokens={self._elements[self._pos:]}, pos={self._pos}>"

    def search(self, *tokens: Union[str, AMTMark]) -> bool:
        """从当前配置开始匹配 tokens

        - 如果匹配成功，则返回 True
        - 如果匹配失败，则返回 False
        """
        if self._pos + len(tokens) > self._len:
            return False
        for idx, token in enumerate(tokens):
            refer = self._elements[self._pos + idx]
            if refer is None or not refer.equals(token):
                return False
        return True

    def rich_search(self, *tokens: Union[str, AMTMark, Set[str]]) -> bool:
        """从当前配置开始匹配 tokens

        集合中不支持 AMTMark 类型

        - 如果匹配成功，则返回 True
        - 如果匹配失败，则返回 False
        """
        if self._pos + len(tokens) > self._len:
            return False
        for idx, token in enumerate(tokens):
            refer = self._elements[self._pos + idx]
            if refer is None:
                return False
            if isinstance(token, (AMTMark, str)):
                if not refer.equals(token):
                    return False
            elif isinstance(token, set):
                if refer.source.upper() not in token:
                    return False
            else:
                raise KeyError(f"不支持的参数类型: {token} (type={type(token)})")
        return True

    def search_and_move(self, *tokens: Union[str, AMTMark]) -> bool:
        """从当前配置开始匹配 tokens

        - 如果匹配成功，则将指针移动到 tokens 后的下一个元素并返回 True
        - 如果匹配失败，则不移动指针并返回 False
        """
        if not self.search(*tokens):
            return False
        self.move(len(tokens))
        return True

    def rich_search_and_move(self, *tokens: Union[str, AMTMark, Set[str]]) -> bool:
        """从当前配置开始匹配 tokens

        当 token 为 str 类型或 AMTMark 类型时，判断当前元素是否与 token 一致；
        当 token 为 set 类型时，判断当前元素是否在 set 集合中
        集合中不支持 AMTMark 类型

        - 如果匹配成功，则将指针移动到 tokens 后的下一个元素并返回 True
        - 如果匹配失败，则不移动指针并返回 False
        """
        if not self.rich_search(*tokens):
            return False
        self.move(len(tokens))
        return True

    def match(self, *tokens: Union[str, AMTMark]) -> None:
        """从当前配置开始匹配 tokens

        - 如果匹配成功，则将指针移动到 tokens 后的下一个元素
        - 如果匹配失败，则抛出异常
        """
        for word in tokens:
            if not self.pop().equals(word):
                raise ScannerError(f"没有解析到目标词语:目标词={tokens} - {self}")

    def get_as_source(self) -> Optional[str]:
        """不移动指针，并返回当前元素的 source"""
        element = self.get()
        if element is not None:
            return self.get().source
        return None

    def pop_as_source(self) -> str:
        """将指针向后移动 1 个元素，并返回当前元素的 source"""
        return self.pop().source

    def get_as_children_scanner(self) -> "TokenScanner":
        """不移动指针，并返回当前指针位置的插入语节点的子节点的扫描器"""
        return TokenScanner(self.get().children())

    def pop_as_children_scanner(self) -> "TokenScanner":
        """将指针向后移动 1 个元素，并返回当前指针位置的插入语节点的子节点的扫描器"""
        return TokenScanner(self.pop().children())

    def split_by(self, source: str) -> List["TokenScanner"]:
        """将指针移动到末尾，并将后续元素拆分为使用 source 分隔的扫描器列表"""
        result = []
        tokens = []
        while not self.is_finish:
            token: AMTBase = self.pop()
            if token.equals(source):
                if len(tokens) > 0:
                    result.append(TokenScanner(tokens))
                    tokens = []
            else:
                tokens.append(token)
        if len(tokens) > 0:
            result.append(TokenScanner(tokens))
        return result

    def pop_as_children_scanner_list_split_by(self, source: str) -> List["TokenScanner"]:
        """将指针向后移动一个元素，并返回当前指针位置的插入语结点的子节点使用 source 分隔的扫描器列表"""
        result = []
        tokens = []
        for token in self.pop().children():
            if token.equals(source):
                if len(tokens) > 0:
                    result.append(TokenScanner(tokens))
                    tokens = []
            else:
                tokens.append(token)
        if len(tokens) > 0:
            result.append(TokenScanner(tokens))
        return result

    @property
    def is_finish(self) -> bool:
        """返回是否已匹配结束"""
        return self._pos >= self._len
