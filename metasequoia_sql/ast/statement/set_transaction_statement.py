"""
SET TRANSACTION 语句
"""

from typing import Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.fixed_enum import EnumTransactionAccessModeType, EnumIsolationType, EnumSetOptionType

__all__ = (
    "SetTransactionStatement"
)


class SetTransactionStatement(Statement):
    """SET TRANSACTION 语句"""

    __slots__ = (
        "_set_option",
        "_transaction_access_mode",
        "_isolation_level"
    )

    def __init__(self,
                 set_option: "EnumSetOptionType",
                 transaction_access_mode: Optional["EnumTransactionAccessModeType"],
                 isolation_level: Optional["EnumIsolationType"]):
        self._set_option = set_option
        self._transaction_access_mode = transaction_access_mode
        self._isolation_level = isolation_level

    @property
    def set_option(self) -> "EnumSetOptionType":
        """设置选项"""
        return self._set_option

    @property
    def transaction_access_mode(self) -> Optional["EnumTransactionAccessModeType"]:
        """事务访问模式"""
        return self._transaction_access_mode

    @property
    def isolation_level(self) -> Optional["EnumIsolationType"]:
        """事务隔离级别"""
        return self._isolation_level
