"""
固定的枚举类型（fixed enum）
"""

from enum import IntEnum, IntFlag

__all__ = [
    "EnumDropRestrict",
    "EnumShowCommandType",
    "EnumRepairType",
    "EnumCheckType",
    "EnumChecksumType",
    "EnumProfileType",
    "EnumVariableType",
    "EnumInstallOptionType",
    "EnumKillOptionType",
    "EnumLockOptionType",
    "EnumOpenSslType",
    "EnumChainType",
    "EnumReleaseType",
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


class EnumChecksumType(IntEnum):
    """`CHECKSUM` 语句命令类型的枚举值"""

    DEFAULT = 0
    QUICK = 1  # QUICK
    EXTENDED = 2  # EXTENDED


class EnumProfileType(IntFlag):
    """`SHOW PROFILE` 语句中性能分析指标的枚举值"""

    DEFAULT = 0
    CPU = (1 << 0)  # CPU
    MEMORY = (1 << 1)  # MEMORY
    BLOCK_IO = (1 << 2)  # BLOCK IO
    CONTEXT_SWITCHES = (1 << 3)  # CONTEXT SWITCHES
    PAGE_FAULTS = (1 << 4)  # PAGE FAULTS
    IPC = (1 << 5)  # IPC
    SWAPS = (1 << 6)  # SWAPS
    SOURCE = (1 << 7)  # SOURCE
    ALL = (1 << 8)  # ALL


class EnumVariableType(IntEnum):
    """变量类型的枚举值"""

    DEFAULT = 0
    GLOBAL = 1
    LOCAL = 2
    SESSION = 3


class EnumInstallOptionType(IntEnum):
    """`INSTALL` 语句的安装选项的枚举值"""

    DEFAULT = 0
    GLOBAL = 1
    PERSIST = 2


class EnumKillOptionType(IntEnum):
    """KILL 语句的选项的枚举值"""

    DEFAULT = 0  # 默认值
    CONNECTION = 1  # CONNECTION
    QUERY = 2  # QUERY


class EnumLockOptionType(IntEnum):
    """LOCK 语句的锁定选项的枚举值"""

    DEFAULT = 0  # 默认值
    READ = 1  # READ
    WRITE = 2  # WRITE
    LOW_PRIORITY_WRITE = 3  # LOW_PRIORITY WRITE
    READ_LOCAL = 4  # READ LOCAL


class EnumOpenSslType(IntEnum):
    """SSL 选项的枚举值"""

    DEFAULT = 0  # 默认值
    REQUIRED = 1  # REQUIRE SSL
    REQUIRED_NO_SSL = 2  # REQUIRE NO SSL


class EnumChainType(IntEnum):
    """CHAIN 选项的枚举值"""

    DEFAULT = 0  # 默认值
    YES = 1  # AND CHAIN
    NO = 2  # AND NO CHAIN


class EnumReleaseType(IntEnum):
    """RELEASE 选项的枚举值"""

    DEFAULT = 0  # 默认值
    YES = 1  # RELEASE
    NO = 2  # NO RELEASE
