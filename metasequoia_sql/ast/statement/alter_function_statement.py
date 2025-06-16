"""
ALTER FUNCTION 语句（alter function statement）
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.phrase.function_option import FunctionOption

__all__ = [
    "AlterFunctionStatement",
]


class AlterFunctionStatement(Statement):
    """ALTER FUNCTION 语句"""

    __slots__ = (
        "_function_name",
        "_option_list",
    )

    def __init__(self, function_name: "Identifier", option_list: List["FunctionOption"]):
        self._function_name = function_name
        self._option_list = option_list

    @property
    def function_name(self) -> "Identifier":
        return self._function_name

    @property
    def option_list(self) -> List["FunctionOption"]:
        return self._option_list 