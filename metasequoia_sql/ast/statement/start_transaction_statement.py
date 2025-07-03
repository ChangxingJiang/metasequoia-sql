"""
START TRANSACTION 语句（start transaction statement）
"""

from enum import IntFlag

from metasequoia_sql.ast.base import Statement

__all__ = [
    "StartTransactionOption",
    "StartTransactionStatement"
]


class StartTransactionOption(IntFlag):
    """START TRANSACTION 语句的选项"""

    DEFAULT = 0
    WITH_CONSISTENT_SNAPSHOT = 1  # WITH CONSISTENT SNAPSHOT
    READ_ONLY = 2  # READ ONLY
    READ_WRITE = 4  # READ WRITE


class StartTransactionStatement(Statement):
    """START TRANSACTION 语句"""

    __slots__ = (
        "_options",
    )

    def __init__(self, options: StartTransactionOption):
        """
        初始化 START TRANSACTION 语句

        Parameters
        ----------
        options : StartTransactionOption
            事务选项
        """
        self._options = options

    @property
    def options(self) -> StartTransactionOption:
        """
        事务选项

        Returns
        -------
        StartTransactionOption
            事务选项
        """
        return self._options
