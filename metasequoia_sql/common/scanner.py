"""
抽象语法树扫描器
"""

from typing import List, Union, Optional, Set

from metasequoia_sql.errors import ScannerError, ScannerNotMatchError
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

    def get_offset(self, offset: int = 0) -> AMTBase:
        """【不移动指针】获取 self._pos（当前指针）+ offset 位置的元素，如果当前元素不存在，则抛出异常"""
        return self._elements[self._pos + offset]

    def get_offset_or_null(self, offset: int = 0) -> Optional[AMTBase]:
        """【不移动指针】获取 self._pos（当前指针）+ offset 位置的元素，如果当前元素不存在，则返回 None"""
        if self._pos + offset >= self._len:
            return None
        return self._elements[self._pos + offset]

    def get_or_null(self) -> Optional[AMTBase]:
        """获取当前指针位置元素，但不移动指针

        - 如果指针已到达字符串末尾，则返回 None
        - 如果指针超出字符串长度，则抛出异常
        """
        if self._pos >= self._len:
            return None
        return self._elements[self._pos]

    def pop(self) -> AMTBase:
        """获取当前指针位置元素，并移动指针

        - 如果要移动到的指针位置超出字符串长度，则抛出异常  TODO 在异常处理机制中提取并处理
        """
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

        需要注意的是：
        1. 插入语仅能用 ASTMark.PARENTHESIS 进行匹配，而不能使用源码进行匹配
        """
        if self._pos + len(tokens) > self._len:
            return False
        for idx, token in enumerate(tokens):
            refer = self._elements[self._pos + idx]
            if not refer.equals(token):
                return False
        return True

    def search_one_type_mark(self, token: AMTMark):
        """【不移动指针】判断当前抽象语法树节点是否包含 token 标签"""
        if self._pos >= self._len:
            return False
        return self._elements[self._pos].has_mark(token)

    def search_one_type_str(self, token: str):
        """【不移动指针】判断当前抽象词法树节点源代码的是否与 token 相同"""
        if self._pos >= self._len:
            return False
        return self._elements[self._pos].source_equal(token)

    def search_one_type_str_use_upper(self, token: str):
        """【不移动指针】判断当前抽象词法树节点源代码的 **大写形式** 是否与 token 相同"""
        if self._pos >= self._len:
            return False
        return self._elements[self._pos].source_equal_use_upper(token)

    def search_two_type_str_use_upper(self, token_1: str, token_2: str):
        """【不移动指针】判断当前抽象词法树节点源代码的 **大写形式** 是否与 token 相同"""
        if self._pos + 1 >= self._len:
            return False
        return (self._elements[self._pos].source_equal_use_upper(token_1)
                and self._elements[self._pos + 1].source_equal_use_upper(token_2))

    def search_three_type_str_use_upper(self, token_1: str, token_2: str, token_3: str):
        """【不移动指针】判断当前抽象词法树节点源代码的 **大写形式** 是否与 token 相同"""
        if self._pos + 2 >= self._len:
            return False
        return (self._elements[self._pos].source_equal_use_upper(token_1)
                and self._elements[self._pos + 1].source_equal_use_upper(token_2)
                and self._elements[self._pos + 2].source_equal_use_upper(token_3))

    def search_one_type_set(self, token: Set[str]) -> bool:
        """【不移动指针】判断当前抽象词法树节点源代码的是否在 token 的字典之中"""
        if self._pos >= self._len:
            return False
        return self._elements[self._pos].source in token

    def search_one_type_set_use_upper(self, token: Set[str]) -> bool:
        """【不移动指针】判断当前抽象词法树节点源代码的 **大写形式** 是否在 token 的字典之中"""
        if self._pos >= self._len:
            return False
        return self._elements[self._pos].source.upper() in token

    def search_and_move(self, *tokens: Union[str, AMTMark]) -> bool:
        """从当前配置开始匹配 tokens

        - 如果匹配成功，则将指针移动到 tokens 后的下一个元素并返回 True
        - 如果匹配失败，则不移动指针并返回 False
        """
        if not self.search(*tokens):
            return False
        self.move(len(tokens))
        return True

    def search_and_move_one_type_str(self, token: str):
        """【移动指针】判断当前抽象词法树节点源代码是否与 token 相同，如相同返回 True 并移动指针，否则返回 False 且不移动指针"""
        if not self.search_one_type_str(token):
            return False
        self.move()
        return True

    def search_and_move_one_type_str_use_upper(self, token: str):
        """【移动指针】判断当前抽象词法树节点源代码的 **大写形式** 是否与 token 相同，如相同返回 True 并移动指针，否则返回 False 且不移动指针"""
        if not self.search_one_type_str_use_upper(token):
            return False
        self.move()
        return True

    def search_and_move_two_type_str_use_upper(self, token_1: str, token_2: str):
        """【移动指针】判断当前抽象词法树节点源代码的 **大写形式** 是否与 token 相同，如相同返回 True 并移动指针，否则返回 False 且不移动指针"""
        if not self.search_two_type_str_use_upper(token_1, token_2):
            return False
        self.move(2)
        return True

    def search_and_move_three_type_str_use_upper(self, token_1: str, token_2: str, token_3: str):
        """【移动指针】判断当前抽象词法树节点源代码的 **大写形式** 是否与 token 相同，如相同返回 True 并移动指针，否则返回 False 且不移动指针"""
        if not self.search_three_type_str_use_upper(token_1, token_2, token_3):
            return False
        self.move(3)
        return True

    def search_and_move_one_type_set(self, token: Set[str]) -> bool:
        """【移动指针】判断当前抽象词法树节点源代码的是否在 token 的字典之中，如果存在返回 True 并移动指针，否则返回 False 且不移动指针"""
        if not self.search_one_type_set(token):
            return False
        self.move()
        return True

    def search_and_move_one_type_set_use_upper(self, token: Set[str]) -> bool:
        """【移动指针】判断当前抽象词法树节点源代码的 **大写形式** 是否在 token 的字典之中，如果存在返回 True 并移动指针，否则返回 False 且不移动指针"""
        if not self.search_one_type_set_use_upper(token):
            return False
        self.move()
        return True

    def match(self, *tokens: Union[str, AMTMark]) -> None:
        """从当前配置开始匹配 tokens

        - 如果匹配成功，则将指针移动到 tokens 后的下一个元素
        - 如果匹配失败，则抛出异常
        """
        for token in tokens:
            if not self.pop().equals(token):
                raise ScannerNotMatchError(token, tokens, self)

    def get_as_source_or_null(self) -> Optional[str]:
        """不移动指针，并返回当前元素的 source"""
        if self._pos >= self._len:
            return None
        return self._elements[self._pos].source

    def pop_as_source(self) -> str:
        """将指针向后移动 1 个元素，并返回当前元素的 source"""
        return self.pop().source

    def get_as_children_scanner(self) -> "TokenScanner":
        """不移动指针，并返回当前指针位置的插入语节点的子节点的扫描器"""
        return TokenScanner(self.get_or_null().children)

    def pop_as_children_scanner(self) -> "TokenScanner":
        """将指针向后移动 1 个元素，并返回当前指针位置的插入语节点的子节点的扫描器"""
        return TokenScanner(self.pop().children)

    def pop_as_children_scanner_list_split_by(self, source: str) -> List["TokenScanner"]:
        """将指针向后移动一个元素，并返回当前指针位置的插入语结点的子节点使用 source 分隔的扫描器列表"""
        result = []
        tokens = []
        for token in self.pop().children:
            if token.equals(source):
                if len(tokens) > 0:
                    result.append(TokenScanner(tokens))
                    tokens = []
            else:
                tokens.append(token)
        if len(tokens) > 0:
            result.append(TokenScanner(tokens))
        return result

    def get_recent_source(self, n_word: int = 10) -> str:
        """获取当前位置之前的 1 个元素开始的 n_word 个词法树节点（如果不足 n_word 个则全部返回）"""
        elements = self._elements[self._pos - 1: min(self._pos + n_word - 1, len(self._elements))]
        return " ".join([element.source for element in elements])

    @property
    def is_finish(self) -> bool:
        """返回是否已匹配结束"""
        return self._pos >= self._len
