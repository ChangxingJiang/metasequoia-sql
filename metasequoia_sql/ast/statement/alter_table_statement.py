"""
ALTER TABLE 语句（alter table statement）
"""

from typing import List, TYPE_CHECKING, Union

from metasequoia_sql.ast.base import Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.phrase.alter_command import AlterCommand
    from metasequoia_sql.ast.phrase.ddl_alter_option import AlterOption
    from metasequoia_sql.ast.phrase.ddl_option import DdlOption

__all__ = [
    "AlterTableStatement"
]


class AlterTableStatement(Node):
    """`ALTER TABLE` 语句"""

    __slots__ = (
        "_table_ident",
        "_command_list"
    )

    def __init__(self,
                 table_ident: "Identifier",
                 command_list: List[Union[AlterCommand, AlterOption, DdlOption]]) -> None:
        self._table_ident = table_ident
        self._command_list = command_list

    @property
    def table_ident(self) -> "Identifier":
        return self._table_ident

    @property
    def command_list(self) -> List[Union[AlterCommand, AlterOption, DdlOption]]:
        return self._command_list
