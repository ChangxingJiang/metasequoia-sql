"""
REPAIR TABLE 语句（repair table statement）
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.fixed_enum import EnumRepairType

__all__ = [
    "RepairTableStatement"
]


class RepairTableStatement(Statement):
    """REPAIR TABLE 语句"""

    __slots__ = (
        "_no_write_to_binlog",
        "_table_list",
        "_repair_type"
    )

    def __init__(self, no_write_to_binlog: bool, table_list: List["Identifier"], repair_type: "EnumRepairType"):
        self._no_write_to_binlog = no_write_to_binlog
        self._table_list = table_list
        self._repair_type = repair_type

    @property
    def no_write_to_binlog(self) -> bool:
        """
        是否不写入二进制日志

        Returns
        -------
        bool
            是否不写入二进制日志
        """
        return self._no_write_to_binlog

    @property
    def table_list(self) -> List["Identifier"]:
        """
        表列表

        Returns
        -------
        List[Identifier]
            表列表
        """
        return self._table_list

    @property
    def repair_type(self) -> "EnumRepairType":
        """
        修复类型

        Returns
        -------
        EnumRepairType
            修复类型
        """
        return self._repair_type
