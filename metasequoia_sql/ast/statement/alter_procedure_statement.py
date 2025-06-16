"""
ALTER PROCEDURE 语句（alter procedure statement）
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.phrase.function_option import FunctionOption

__all__ = [
    "AlterProcedureStatement",
]


class AlterProcedureStatement(Statement):
    """ALTER PROCEDURE 语句"""

    __slots__ = (
        "_procedure_name",
        "_option_list",
    )

    def __init__(self, procedure_name: "Identifier", option_list: List["FunctionOption"]):
        self._procedure_name = procedure_name
        self._option_list = option_list

    @property
    def procedure_name(self) -> "Identifier":
        return self._procedure_name

    @property
    def option_list(self) -> List["FunctionOption"]:
        return self._option_list 