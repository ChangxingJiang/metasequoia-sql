"""
ALTER UNDO TABLESPACE 语句（alter undo tablespace statement）
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.fixed_enum import EnumUndoTablespaceState
    from metasequoia_sql.ast.phrase.ddl_option import DdlOption

__all__ = [
    "AlterUndoTablespaceStatement",
]


class AlterUndoTablespaceStatement(Statement):
    """ALTER UNDO TABLESPACE 语句"""

    __slots__ = ["_tablespace_name", "_state", "_option_list"]

    def __init__(self,
                 tablespace_name: str,
                 state: "EnumUndoTablespaceState",
                 option_list: List["DdlOption"]):
        self._tablespace_name = tablespace_name
        self._state = state
        self._option_list = option_list

    @property
    def tablespace_name(self) -> str:
        """
        撤销表空间名称

        Returns
        -------
        str
            撤销表空间名称
        """
        return self._tablespace_name

    @property
    def state(self) -> "EnumUndoTablespaceState":
        """
        撤销表空间状态

        Returns
        -------
        EnumUndoTablespaceState
            撤销表空间状态
        """
        return self._state

    @property
    def option_list(self) -> List["DdlOption"]:
        """
        DDL 选项列表

        Returns
        -------
        List["DdlOption"]
            DDL 选项列表
        """
        return self._option_list
