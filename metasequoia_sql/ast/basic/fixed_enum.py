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
    "EnumRowFormatType",
    "EnumMergeInsertType",
    "EnumUndoTablespaceState",
    "EnumViewAlgorithmType",
    "EnumViewSuidType",
    "EnumReplicaThreadType",
    "EnumDataType",
    "EnumLoadDataLock",
    "EnumLoadSourceType",
    "EnumTablePrimaryKeyCheckType",
    "EnumAssignGtidsType",
    "EnumHandlerScanFunction",
    "EnumHandlerRkeyFunction",
    "EnumHandlerRkeyMode",
    "EnumTransactionAccessModeType",
    "EnumIsolationType",
    "EnumSetOptionType",
    "EnumTriggerActionTimeType",
    "EnumTriggerEventType",
    "EnumTriggerActionOrderType",
    "EnumProcedureParamMode",
    "EnumUdfReturnType",
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


class EnumRowFormatType(IntEnum):
    """行格式类型的枚举值"""

    DEFAULT = 0  # DEFAULT
    FIXED = 1  # FIXED
    DYNAMIC = 2  # DYNAMIC
    COMPRESSED = 3  # COMPRESSED
    REDUNDANT = 4  # REDUNDANT
    COMPACT = 5  # COMPACT


class EnumMergeInsertType(IntEnum):
    """向 MERGE 表插入数据的类型的枚举值"""

    NO = 1  # NO：不允许向 MERGE 表插入数据，尝试插入会报错
    FIRST = 2  # FIRST：将新记录插入到第一个底层的 MyISAM 表中
    LAST = 3  # LAST：将新记录插入到最后一个底层的 MyISAM 表中


class EnumUndoTablespaceState(IntEnum):
    """UNDO TABLESPACE 状态的枚举值"""

    ACTIVE = 1  # ACTIVE：启用状态
    INACTIVE = 2  # INACTIVE：禁用状态


class EnumViewAlgorithmType(IntEnum):
    """视图算法类型的枚举值"""

    DEFAULT = 0
    UNDEFINED = 1  # ALGORITHM = UNDEFINED
    MERGE = 2  # ALGORITHM = MERGE
    TEMPTABLE = 3  # ALGORITHM = TEMPTABLE


class EnumViewSuidType(IntEnum):
    """视图 SUID 类型的枚举值"""

    DEFAULT = 0  # %empty
    DEFINER = 1  # SQL SECURITY DEFINER
    INVOKER = 2  # SQL SECURITY INVOKER


class EnumReplicaThreadType(IntFlag):
    """副本线程选项的枚举值"""

    DEFAULT = 0
    SQL_THREAD = (1 << 0)
    RELAY_THREAD = (1 << 1)


class EnumDataType(IntEnum):
    """LOAD 语句中数据类型的枚举值"""

    CSV = 1  # DATA
    XML = 2  # XML


class EnumLoadDataLock(IntEnum):
    """LOAD 语句中锁定类型的枚举值"""

    DEFAULT = 0  # %empty
    CONCURRENT = 1  # CONCURRENT
    LOW_PRIORITY = 2  # LOW_PRIORITY


class EnumLoadSourceType(IntEnum):
    """LOAD 语句中数据源类型的枚举值"""

    FILE = 1  # INFILE
    URL = 2  # URL
    S3 = 3  # S3


class EnumTablePrimaryKeyCheckType(IntEnum):
    """表主键检查类型的枚举值"""

    STREAM = 1  # STREAM
    ON = 2  # ON
    OFF = 3  # OFF
    GENERATE = 4  # GENERATE


class EnumHandlerScanFunction(IntEnum):
    """HANDLER 语句扫描函数的枚举值"""

    FIRST = 1  # FIRST
    NEXT = 2  # NEXT


class EnumHandlerRkeyFunction(IntEnum):
    """HANDLER 语句索引键函数的枚举值"""

    FIRST = 1  # FIRST
    NEXT = 2  # NEXT
    PREV = 3  # PREV
    LAST = 4  # LAST


class EnumHandlerRkeyMode(IntEnum):
    """HANDLER 语句索引键模式的枚举值"""

    EQ = 1  # = (等于)
    GE = 2  # >= (大于等于)
    LE = 3  # <= (小于等于)
    GT = 4  # > (大于)
    LT = 5  # < (小于)


class EnumAssignGtidsType(IntEnum):
    """分配 GTID 类型的枚举值"""

    OFF = 1  # OFF
    LOCAL = 2  # LOCAL
    AUTOMATIC = 3  # AUTOMATIC


class EnumTransactionAccessModeType(IntEnum):
    """事务访问模式类型的枚举值"""

    READ_ONLY = 1  # READ ONLY
    READ_WRITE = 2  # READ WRITE


class EnumIsolationType(IntEnum):
    """事务隔离级别类型的枚举值"""

    READ_UNCOMMITTED = 1  # READ UNCOMMITTED
    READ_COMMITTED = 2  # READ COMMITTED
    REPEATABLE_READ = 3  # REPEATABLE READ
    SERIALIZABLE = 4  # SERIALIZABLE


class EnumSetOptionType(IntEnum):
    """SET 语句选项"""

    DEFAULT = 0  # %empty
    GLOBAL = 1  # GLOBAL
    PERSIST = 2  # PERSIST
    PERSIST_ONLY = 3  # PERSIST ONLY
    LOCAL = 4  # LOCAL
    SESSION = 5  # SESSION


class EnumTriggerActionTimeType(IntEnum):
    """触发器动作时间类型的枚举值"""

    BEFORE = 1  # BEFORE
    AFTER = 2  # AFTER


class EnumTriggerEventType(IntEnum):
    """触发器事件类型的枚举值"""

    INSERT = 1  # INSERT
    UPDATE = 2  # UPDATE
    DELETE = 3  # DELETE


class EnumTriggerActionOrderType(IntEnum):
    """触发器动作顺序类型的枚举值"""

    FOLLOWS = 1  # FOLLOWS
    PRECEDES = 2  # PRECEDES


class EnumProcedureParamMode(IntEnum):
    """存储过程参数模式的枚举值"""

    IN = 1  # IN
    OUT = 2  # OUT
    INOUT = 3  # INOUT


class EnumUdfReturnType(IntEnum):
    """UDF 函数返回值类型的枚举值"""

    STRING = 1  # STRING
    REAL = 2  # REAL
    DECIMAL = 3  # DECIMAL
    INT = 4  # INT
