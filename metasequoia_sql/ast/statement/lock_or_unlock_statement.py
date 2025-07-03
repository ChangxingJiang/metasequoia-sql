"""
LOCK/UNLOCK 语句（lock/unlock statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.fixed_enum import EnumLockOptionType
    from metasequoia_sql.ast.basic.ident import Identifier

__all__ = [
    "TableLock",
    "LockStatement",
    "LockTablesStatement",
    "LockInstanceStatement",
    "UnlockStatement",
    "UnlockTablesStatement",
    "UnlockInstanceStatement",
]


class TableLock:
    """表锁定信息"""

    __slots__ = (
        "_table_name",
        "_alias",
        "_lock_option",
    )

    def __init__(self, table_name: "Identifier", alias: Optional[str], lock_option: "EnumLockOptionType"):
        self._table_name = table_name
        self._alias = alias
        self._lock_option = lock_option

    @property
    def table_name(self) -> "Identifier":
        """
        表名称

        Returns
        -------
        Identifier
            表名称
        """
        return self._table_name

    @property
    def alias(self) -> Optional[str]:
        """
        表别名

        Returns
        -------
        Optional[str]
            表别名
        """
        return self._alias

    @property
    def lock_option(self) -> "EnumLockOptionType":
        """
        锁选项

        Returns
        -------
        EnumLockOptionType
            锁选项
        """
        return self._lock_option


class LockStatement(Statement):
    """LOCK 语句基类"""


class LockTablesStatement(LockStatement):
    """LOCK TABLES 语句"""

    __slots__ = (
        "_table_lock_list",
    )

    def __init__(self, table_lock_list: List[TableLock]):
        self._table_lock_list = table_lock_list

    @property
    def table_lock_list(self) -> List[TableLock]:
        """
        表锁列表

        Returns
        -------
        List[TableLock]
            表锁列表
        """
        return self._table_lock_list


class LockInstanceStatement(LockStatement):
    """LOCK INSTANCE FOR BACKUP 语句"""


class UnlockStatement(Statement):
    """UNLOCK 语句基类"""


class UnlockTablesStatement(UnlockStatement):
    """UNLOCK TABLES 语句"""


class UnlockInstanceStatement(UnlockStatement):
    """UNLOCK INSTANCE 语句"""
