from typing import List, Type

from metasequoia_sql import ast
from metasequoia_sql.errors import TokenIdxOutOfRangeError, SqlParseError
from metasequoia_sql.statements.common import SqlFunction


class TokenScanner:
    """Token 扫描器"""

    def __init__(self, tokens: List[ast.AST], pos: int = 0):
        """

        Parameters
        ----------
        tokens : List[ast.AST]
            当前层级的抽象语法树节点列表
        pos : int, default = 0
            当前正在处理的抽象语法树节点下标
        """
        self._tokens = tokens
        self._pos = pos
        self._n_token = len(self._tokens)

    @property
    def tokens(self) -> List[ast.AST]:
        return self._tokens

    @property
    def pos(self) -> int:
        return self._pos

    def get(self) -> ast.AST:
        """返回当前元素但不移动指针"""
        self._check_has_next(1)
        return self._tokens[self._pos]

    def move(self) -> ast.AST:
        """将指针向后移动 1 个元素并返回当前元素"""
        self._check_has_next(1)
        result = self._tokens[self._pos]
        self._pos += 1
        return result

    def move_as_source(self) -> str:
        """将指针向后移动 1 个元素并返回当前元素的 source"""
        return self.move().source

    def move_as_parenthesis(self) -> ast.ASTParenthesis:
        """将指针向后移动 1 个元素并返回当前元素（视作 ASTParenthesis 类型）"""
        element = self.move()
        if isinstance(element, ast.ASTParenthesis):
            return element
        raise SqlParseError(f"element.__class__.__name__={element.__class__.__name__}")

    def is_finish(self) -> bool:
        """返回是否已匹配结束"""
        return not self._pos < self._n_token

    def match_words(self, words: List[str]) -> None:
        """尝试从当前指针位置开始匹配 words，如果匹配失败则抛出异常"""
        for word in words:
            if not self.move().equals(word):
                raise SqlParseError(f"tokens={self._tokens}, words={words}")

    def match_function(self, aim_class: Type[SqlFunction]) -> SqlFunction:
        """匹配 SQL 函数，构造并返回 aim_class 类型的函数对象，同时移动指针"""
        function_name = self.move().source
        if not self.is_finish() and isinstance(self.get(), ast.ASTParenthesis):  # 函数包含参数
            function_param = [sub_node.source for sub_node in self.move_as_parenthesis().children]
            return aim_class(function_name, function_param)
        else:
            return aim_class(function_name)

    def _check_has_next(self, cnt: int) -> None:
        """检查当前指针及之前之后是否包含大于等于 cnt 个元素，如果不存在则抛出异常"""
        if self._pos + cnt > self._n_token:
            raise TokenIdxOutOfRangeError(f"tokens={self._tokens}, pos={self._pos}, cnt={cnt}")
