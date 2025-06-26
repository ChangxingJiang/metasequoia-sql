"""
FLUSH 语句（flush statement）
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.fixed_enum import EnumFlushOptionType, EnumFlushLockType
    from metasequoia_sql.ast.basic.ident import Identifier

__all__ = [
    "FlushStatement",
    "FlushTablesStatement",
    "FlushOptionsStatement",
]


class FlushStatement(Statement):
    """FLUSH 语句基类"""

    __slots__ = (
        "_no_write_to_binlog",
    )

    def __init__(self, no_write_to_binlog: bool):
        self._no_write_to_binlog = no_write_to_binlog

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


class FlushTablesStatement(FlushStatement):
    """FLUSH TABLES 语句"""

    __slots__ = (
        "_table_list",
        "_flush_lock_type",
    )

    def __init__(self,
                 no_write_to_binlog: bool,
                 table_list: List["Identifier"],
                 flush_lock_type: "EnumFlushLockType"):
        super().__init__(no_write_to_binlog)
        self._table_list = table_list
        self._flush_lock_type = flush_lock_type

    @property
    def table_list(self) -> List["Identifier"]:
        """
        表名称列表

        Returns
        -------
        List[Identifier]
            表名称列表
        """
        return self._table_list

    @property
    def flush_lock_type(self) -> "EnumFlushLockType":
        """
        刷新锁类型

        Returns
        -------
        EnumFlushLockType
            刷新锁类型
        """
        return self._flush_lock_type


class FlushOptionsStatement(FlushStatement):
    """FLUSH 选项语句"""

    __slots__ = (
        "_flush_options",
    )

    def __init__(self, no_write_to_binlog: bool, flush_options: "EnumFlushOptionType"):
        super().__init__(no_write_to_binlog)
        self._flush_options = flush_options

    @property
    def flush_options(self) -> "EnumFlushOptionType":
        """
        刷新选项类型

        Returns
        -------
        EnumFlushOptionType
            刷新选项类型
        """
        return self._flush_options
