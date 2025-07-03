"""
OPTIMIZE TABLE 语句（optimize table statement）
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier

__all__ = [
    "OptimizeTableStatement",
]


class OptimizeTableStatement(Statement):
    """OPTIMIZE TABLE 语句"""

    def __init__(self, no_write_to_binlog: bool, table_list: List["Identifier"]):
        self._no_write_to_binlog = no_write_to_binlog
        self._table_list = table_list

    @property
    def no_write_to_binlog(self) -> bool:
        """是否不写入二进制日志"""
        return self._no_write_to_binlog

    @property
    def table_list(self) -> List["Identifier"]:
        """表名列表"""
        return self._table_list
