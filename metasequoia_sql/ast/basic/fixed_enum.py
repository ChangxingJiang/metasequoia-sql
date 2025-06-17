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
    "EnumResourceGroupType",
    "EnumSignalConditionType",
    "EnumFlushOptionType",
    "EnumFlushLockType",
    "EnumAclType",
    "EnumXaJoinOrResume",
    "EnumXaSuspend",
    "EnumEnableDisable",
    "EnumViewCheckOption",
    "EnumSqlSecurity",
    "EnumEventStatusType",
    "EnumHandlerType",
    "EnumEventCompletionType",
    "EnumDiagnosticsAreaType",
    "EnumStatementInformationType",
    "EnumConditionInformationType",
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


class EnumResourceGroupType(IntEnum):
    """资源组类型的枚举值"""

    USER = 1  # USER
    SYSTEM = 2  # SYSTEM


class EnumSignalConditionType(IntEnum):
    """`SIGNAL` 和 `RESIGNAL` 语句中条件信息项名称的枚举值"""

    CLASS_ORIGIN = 1  # CLASS_ORIGIN
    SUBCLASS_ORIGIN = 2  # SUBCLASS_ORIGIN
    CONSTRAINT_CATALOG = 3  # CONSTRAINT_CATALOG
    CONSTRAINT_SCHEMA = 4  # CONSTRAINT_SCHEMA
    CONSTRAINT_NAME = 5  # CONSTRAINT_NAME
    CATALOG_NAME = 6  # CATALOG_NAME
    SCHEMA_NAME = 7  # SCHEMA_NAME
    TABLE_NAME = 8  # TABLE_NAME
    COLUMN_NAME = 9  # COLUMN_NAME
    CURSOR_NAME = 10  # CURSOR_NAME
    MESSAGE_TEXT = 11  # MESSAGE_TEXT
    MYSQL_ERRNO = 12  # MYSQL_ERRNO


class EnumFlushOptionType(IntFlag):
    """`FLUSH` 语句选项的枚举值"""

    DEFAULT = 0  # 默认值
    ERROR_LOGS = (1 << 0)  # ERROR LOGS
    ENGINE_LOGS = (1 << 1)  # ENGINE LOGS  
    GENERAL_LOGS = (1 << 2)  # GENERAL LOGS
    SLOW_LOGS = (1 << 3)  # SLOW LOGS
    BINARY_LOGS = (1 << 4)  # BINARY LOGS
    RELAY_LOGS = (1 << 5)  # RELAY LOGS
    PRIVILEGES = (1 << 6)  # PRIVILEGES
    LOGS = (1 << 7)  # LOGS
    STATUS = (1 << 8)  # STATUS
    RESOURCES = (1 << 9)  # RESOURCES
    OPTIMIZER_COSTS = (1 << 10)  # OPTIMIZER_COSTS


class EnumFlushLockType(IntEnum):
    """`FLUSH` 语句锁定选项的枚举值"""

    DEFAULT = 0  # 默认值
    WITH_READ_LOCK = 1  # WITH READ LOCK
    FOR_EXPORT = 2  # FOR EXPORT


class EnumAclType(IntEnum):
    """ACL 类型的枚举值"""

    DEFAULT = 0  # %empty
    TABLE = 1  # TABLE
    FUNCTION = 2  # FUNCTION
    PROCEDURE = 3  # PROCEDURE


class EnumXaJoinOrResume(IntEnum):
    """XA 事务中的 JOIN/RESUME 选项枚举值"""

    NONE = 0  # %empty
    JOIN = 1  # JOIN
    RESUME = 2  # RESUME


class EnumXaSuspend(IntEnum):
    """XA 事务中的 SUSPEND 选项枚举值"""

    NONE = 0  # %empty
    SUSPEND = 1  # SUSPEND
    FOR_MIGRATE = 2  # SUSPEND FOR MIGRATE


class EnumEnableDisable(IntEnum):
    """资源组启用 / 禁用状态的枚举值"""

    DEFAULT = 0  # %empty
    ENABLE = 1  # ENABLE
    DISABLE = 2  # DISABLE


class EnumViewCheckOption(IntEnum):
    """视图检查选项的枚举值"""

    DEFAULT = 0  # %empty
    WITH_CHECK_OPTION = 1  # WITH CHECK OPTION
    WITH_CASCADED_CHECK_OPTION = 2  # WITH CASCADED CHECK OPTION
    WITH_LOCAL_CHECK_OPTION = 3  # WITH LOCAL CHECK OPTION


class EnumSqlSecurity(IntEnum):
    """SQL 安全模式的枚举值"""

    DEFAULT = 0
    DEFINER = 1  # DEFINER：使用定义者权限执行
    INVOKER = 2  # INVOKER：使用调用者权限执行


class EnumEventStatusType(IntEnum):
    """事件状态类型的枚举值"""

    DEFAULT = 0
    ENABLE = 1  # ENABLE
    DISABLE_ON_SLAVE = 2  # DISABLE ON SLAVE
    DISABLE_ON_REPLICA = 3  # DISABLE ON REPLICA
    DISABLE = 4  # DISABLE


class EnumHandlerType(IntEnum):
    """处理器类型的枚举值"""

    EXIT = 1  # EXIT
    CONTINUE = 2  # CONTINUE


class EnumEventCompletionType(IntEnum):
    """事件完成类型的枚举值"""

    DEFAULT = 0  # %empty
    ON_COMPLETION_PRESERVE = 1  # ON COMPLETION PRESERVE
    ON_COMPLETION_NOT_PRESERVE = 2  # ON COMPLETION NOT PRESERVE


class EnumDiagnosticsAreaType(IntEnum):
    """诊断区域的枚举值"""

    DEFAULT = 0
    CURRENT_AREA = 1  # CURRENT
    STACKED_AREA = 2  # STACKED


class EnumStatementInformationType(IntEnum):
    """语句诊断信息项名称的枚举值"""

    NUMBER = 1  # NUMBER
    ROW_COUNT = 2  # ROW_COUNT


class EnumConditionInformationType(IntEnum):
    """条件诊断信息项名称的枚举值"""

    CLASS_ORIGIN = 1  # CLASS_ORIGIN
    SUBCLASS_ORIGIN = 2  # SUBCLASS_ORIGIN
    CONSTRAINT_CATALOG = 3  # CONSTRAINT_CATALOG
    CONSTRAINT_SCHEMA = 4  # CONSTRAINT_SCHEMA
    CONSTRAINT_NAME = 5  # CONSTRAINT_NAME
    CATALOG_NAME = 6  # CATALOG_NAME
    SCHEMA_NAME = 7  # SCHEMA_NAME
    TABLE_NAME = 8  # TABLE_NAME
    COLUMN_NAME = 9  # COLUMN_NAME
    CURSOR_NAME = 10  # CURSOR_NAME
    MESSAGE_TEXT = 11  # MESSAGE_TEXT
    MYSQL_ERRNO = 12  # MYSQL_ERRNO
    RETURNED_SQLSTATE = 13  # RETURNED_SQLSTATE
