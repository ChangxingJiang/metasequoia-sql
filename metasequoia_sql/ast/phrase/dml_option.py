"""
DML 语句选项（dml option）
"""

from enum import IntFlag

__all__ = [
    "DmlOption"
]


class DmlOption(IntFlag):
    """DML 语句选项"""

    DEFAULT = 0  # %empty
    IGNORE = (1 << 0)  # IGNORE（适用于 UPDATE、DELETE 语句）
    LOW_PRIORITY = (1 << 1)  # LOW_PRIORITY（适用于 UPDATE、DELETE、INSERT、REPLACE 语句）
    DELAYED = (1 << 2)  # DELAYED（适用于 INSERT、REPLACE 语句）
    QUICK = (1 << 3)  # QUICK（适用于 DELETE 语句）
    HIGH_PRIORITY = (1 << 4)  # HIGH_PRIORITY（适用于 INSERT 语句）
