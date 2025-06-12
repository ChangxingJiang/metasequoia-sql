"""
固定的枚举类型（fixed enum）
"""

from enum import IntEnum, IntFlag

__all__ = [
    "EnumDropRestrict",
    "EnumShowCommandType",
    "EnumRepairType",
    "EnumCheckType",
]


class EnumDropRestrict(IntEnum):
    """枚举类型：DROP 语句中的 RESTRICT 选项"""

    DEFAULT = 0
    CASCADE = 1  # 如果尝试删除一个有其他对象依赖的对象，则删除该对象的同时删除依赖该对象的其他对象
    RESTRICT = 2  # 如果尝试删除一个有其他对象依赖的对象，则会报错


class EnumShowCommandType(IntEnum):
    """枚举类型：SHOW 语句的命令类型"""

    DEFAULT = 0
    FULL = 1  # FULL
    EXTENDED = 2  # EXTENDED
    EXTENDED_FULL = 3  # EXTENDED FULL


class EnumRepairType(IntFlag):
    """枚举类型：REPAIR 语句的命令类型"""

    DEFAULT = 0
    QUICK = (1 << 0)  # QUICK
    EXTENDED = (1 << 1)  # EXTENDED
    USE = (1 << 2)  # USE


class EnumCheckType(IntFlag):
    """枚举类型：CHECK 语句的命令类型"""

    DEFAULT = 0
    QUICK = (1 << 0)  # QUICK
    FAST = (1 << 1)  # FAST
    MEDIUM = (1 << 2)  # MEDIUM
    EXTENDED = (1 << 3)  # EXTENDED
    CHANGED = (1 << 4)  # CHANGED
    FOR_UPGRADE = (1 << 5)  # FOR UPGRADE
