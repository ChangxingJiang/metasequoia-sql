"""
CALL 语句（call statement）
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier

__all__ = [
    "CallStatement"
]


class CallStatement(Statement):
    """CALL 语句"""

    __slots__ = (
        "_function_name",
        "_arguments"
    )

    def __init__(self, function_name: "Identifier", arguments: List[Expression]):
        self._function_name = function_name
        self._arguments = arguments

    @property
    def function_name(self) -> "Identifier":
        """
        函数名标识符

        Returns
        -------
        Identifier
            函数名标识符
        """
        return self._function_name

    @property
    def arguments(self) -> List[Expression]:
        """
        函数参数列表

        Returns
        -------
        List[Expression]
            函数参数列表
        """
        return self._arguments
