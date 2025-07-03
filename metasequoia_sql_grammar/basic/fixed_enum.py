# pylint: disable=C0302

"""
固定的枚举类型（fixed enum）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_DROP_RESTRICT",
    "OPT_SHOW_COMMAND_TYPE",
    "OPT_REPAIR_TYPE_LIST",
    "REPAIR_TYPE_LIST",
    "REPAIR_TYPE",
    "OPT_CHECK_TYPE_LIST",
    "CHECK_TYPE_LIST",
    "CHECK_TYPE",
    "OPT_CHECKSUM_TYPE",
    "OPT_PROFILE_TYPE_LIST",
    "PROFILE_TYPE_LIST",
    "PROFILE_TYPE",
    "OPT_VARIABLE_TYPE",
    "INSTALL_OPTION_TYPE",
    "KILL_OPTION_TYPE",
    "LOCK_OPTION_TYPE",
    "OPT_OPEN_SSL_TYPE",
    "OPT_CHAIN_TYPE",
    "OPT_RELEASE_TYPE",
    "RESOURCE_GROUP_TYPE",
    "SIGNAL_CONDITION_TYPE",
    "FLUSH_OPTION_TYPE_LIST",
    "FLUSH_OPTION_TYPE",
    "FLUSH_LOCK_TYPE",
    "OPT_ACL_TYPE",
    "OPT_JOIN_OR_RESUME",
    "OPT_SUSPEND",
    "OPT_ENABLE_DISABLE",
    "OPT_VIEW_CHECK_OPTION",
    "OPT_EVENT_STATUS_TYPE",
    "HANDLER_TYPE",
    "OPT_EVENT_COMPLETION_TYPE",
    "EVENT_COMPLETION_TYPE",
    "WHICH_AREA",
    "STATEMENT_INFORMATION_TYPE",
    "CONDITION_INFORMATION_TYPE",
    "ROW_FORMAT_TYPE",
    "MERGE_INSERT_TYPE",
    "UNDO_TABLESPACE_STATE",
    "OPT_VIEW_ALGORITHM_TYPE",
    "VIEW_ALGORITHM_TYPE",
    "VIEW_SUID_TYPE",
    "OPT_REPLICA_THREAD_TYPE_LIST",
    "REPLICA_THREAD_TYPE_LIST",
    "REPLICA_THREAD_TYPE",
    "DATA_OR_XML",
    "LOAD_DATA_LOCK",
    "LOAD_SOURCE_TYPE",
    "TABLE_PRIMARY_KEY_CHECK_TYPE",
    "HANDLER_SCAN_FUNCTION",
    "HANDLER_RKEY_FUNCTION",
    "HANDLER_RKEY_MODE",
    "TRANSACTION_ACCESS_MODE_TYPE",
    "ISOLATION_TYPE",
    "OPT_SET_OPTION_TYPE",
    "SET_OPTION_TYPE",
    "TRIGGER_ACTION_TIME_TYPE",
    "TRIGGER_EVENT_TYPE",
    "TRIGGER_ACTION_ORDER_TYPE",
    "PROCEDURE_PARAM_MODE",
    "UDF_RETURN_TYPE",
    "OPT_SET_VARIABLE_TYPE",
]

# 可选的 `DROP` 语句中 `RESTRICT` 选项的枚举值
OPT_DROP_RESTRICT = ms_parser.create_group(
    name="opt_drop_restrict",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.EnumDropRestrict.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RESTRICT],
            action=lambda x: ast.EnumDropRestrict.RESTRICT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CASCADE],
            action=lambda x: ast.EnumDropRestrict.CASCADE
        )
    ]
)

# 可选的 `SHOW` 语句命令类型的枚举值
OPT_SHOW_COMMAND_TYPE = ms_parser.create_group(
    name="opt_show_command_type",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.EnumShowCommandType.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FULL],
            action=lambda x: ast.EnumShowCommandType.FULL
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXTENDED],
            action=lambda x: ast.EnumShowCommandType.EXTENDED
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXTENDED, TType.KEYWORD_FULL],
            action=lambda x: ast.EnumShowCommandType.EXTENDED_FULL
        )
    ]
)

# 可选的 `REPAIR` 语句命令类型的枚举值的列表
OPT_REPAIR_TYPE_LIST = ms_parser.create_group(
    name="opt_repair_type_list",
    rules=[
        ms_parser.create_rule(
            symbols=["repair_type_list"]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.EnumRepairType.DEFAULT
        )
    ]
)

# `REPAIR` 语句命令类型的枚举值的列表
REPAIR_TYPE_LIST = ms_parser.create_group(
    name="repair_type_list",
    rules=[
        ms_parser.create_rule(
            symbols=["repair_type_list", "repair_type"],
            action=lambda x: x[0] | x[1]
        ),
        ms_parser.create_rule(
            symbols=["repair_type"],
            action=lambda x: x[0]
        )
    ]
)

# `REPAIR` 语句命令类型的枚举值
REPAIR_TYPE = ms_parser.create_group(
    name="repair_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_QUICK],
            action=lambda x: ast.EnumRepairType.QUICK
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXTENDED],
            action=lambda x: ast.EnumRepairType.EXTENDED
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_USE],
            action=lambda x: ast.EnumRepairType.USE
        )
    ]
)

# 可选的 `CHECK` 语句命令类型的枚举值的列表
OPT_CHECK_TYPE_LIST = ms_parser.create_group(
    name="opt_check_type_list",
    rules=[
        ms_parser.create_rule(
            symbols=["check_type_list"]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.EnumCheckType.DEFAULT
        )
    ]
)

# `CHECK` 语句命令类型的枚举值的列表
CHECK_TYPE_LIST = ms_parser.create_group(
    name="check_type_list",
    rules=[
        ms_parser.create_rule(
            symbols=["check_type_list", "check_type"],
            action=lambda x: x[0] | x[1]
        ),
        ms_parser.create_rule(
            symbols=["check_type"],
            action=lambda x: x[0]
        )
    ]
)

# `CHECK` 语句命令类型的枚举值
CHECK_TYPE = ms_parser.create_group(
    name="check_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_QUICK],
            action=lambda x: ast.EnumCheckType.QUICK
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FAST],
            action=lambda x: ast.EnumCheckType.FAST
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MEDIUM],
            action=lambda x: ast.EnumCheckType.MEDIUM
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXTENDED],
            action=lambda x: ast.EnumCheckType.EXTENDED
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHANGED],
            action=lambda x: ast.EnumCheckType.CHANGED
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FOR, TType.KEYWORD_UPGRADE],
            action=lambda x: ast.EnumCheckType.FOR_UPGRADE
        )
    ]
)

# 可选的 `CHECKSUM` 语句命令类型的枚举值
OPT_CHECKSUM_TYPE = ms_parser.create_group(
    name="opt_checksum_type",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.EnumChecksumType.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_QUICK],
            action=lambda x: ast.EnumChecksumType.QUICK
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXTENDED],
            action=lambda x: ast.EnumChecksumType.EXTENDED
        )
    ]
)

# 可选的 `SHOW PROFILE` 语句中性能分析指标的枚举值的列表
OPT_PROFILE_TYPE_LIST = ms_parser.create_group(
    name="opt_profile_type_list",
    rules=[
        ms_parser.create_rule(
            symbols=["profile_type_list"]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.EnumProfileType.DEFAULT
        )
    ]
)

# `SHOW PROFILE` 语句中性能分析指标的枚举值的列表
PROFILE_TYPE_LIST = ms_parser.create_group(
    name="profile_type_list",
    rules=[
        ms_parser.create_rule(
            symbols=["profile_type_list", TType.OPERATOR_COMMA, "profile_type"],
            action=lambda x: x[0] | x[1]
        ),
        ms_parser.create_rule(
            symbols=["profile_type"],
            action=lambda x: x[0]
        )
    ]
)

# `SHOW PROFILE` 语句中性能分析指标的枚举值
PROFILE_TYPE = ms_parser.create_group(
    name="profile_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CPU],
            action=lambda x: ast.EnumProfileType.CPU
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MEMORY],
            action=lambda x: ast.EnumProfileType.MEMORY
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BLOCK, TType.KEYWORD_IO],
            action=lambda x: ast.EnumProfileType.BLOCK_IO
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CONTEXT, TType.KEYWORD_SWITCHES],
            action=lambda x: ast.EnumProfileType.CONTEXT_SWITCHES
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PAGE, TType.KEYWORD_FAULTS],
            action=lambda x: ast.EnumProfileType.PAGE_FAULTS
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IPC],
            action=lambda x: ast.EnumProfileType.IPC
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SWAPS],
            action=lambda x: ast.EnumProfileType.SWAPS
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE],
            action=lambda x: ast.EnumProfileType.SOURCE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALL],
            action=lambda x: ast.EnumProfileType.ALL
        )
    ]
)

# 可选的变量类型的枚举值
OPT_VARIABLE_TYPE = ms_parser.create_group(
    name="opt_variable_type",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.EnumVariableType.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GLOBAL],
            action=lambda x: ast.EnumVariableType.GLOBAL
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOCAL],
            action=lambda x: ast.EnumVariableType.LOCAL
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SESSION],
            action=lambda x: ast.EnumVariableType.SESSION
        )
    ]
)

# `INSTALL` 语句的安装选项的枚举值
INSTALL_OPTION_TYPE = ms_parser.create_group(
    name="install_option_type",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumInstallOptionType.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GLOBAL],
            action=lambda _: ast.EnumInstallOptionType.GLOBAL
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PERSIST],
            action=lambda _: ast.EnumInstallOptionType.PERSIST
        )
    ]
)

# `KILL` 语句的选项的枚举值
KILL_OPTION_TYPE = ms_parser.create_group(
    name="kill_option_type",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumKillOptionType.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CONNECTION],
            action=lambda _: ast.EnumKillOptionType.CONNECTION
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_QUERY],
            action=lambda _: ast.EnumKillOptionType.QUERY
        )
    ]
)

# `LOCK` 语句的锁定选项的枚举值
LOCK_OPTION_TYPE = ms_parser.create_group(
    name="lock_option_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_READ],
            action=lambda _: ast.EnumLockOptionType.READ
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WRITE],
            action=lambda _: ast.EnumLockOptionType.WRITE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOW_PRIORITY, TType.KEYWORD_WRITE],
            action=lambda _: ast.EnumLockOptionType.LOW_PRIORITY_WRITE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_READ, TType.KEYWORD_LOCAL],
            action=lambda _: ast.EnumLockOptionType.READ_LOCAL
        )
    ]
)

# SSL 选项的枚举值
OPT_OPEN_SSL_TYPE = ms_parser.create_group(
    name="opt_open_ssl_type",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumOpenSslType.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REQUIRE, TType.KEYWORD_SSL],
            action=lambda _: ast.EnumOpenSslType.REQUIRED
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REQUIRE, TType.KEYWORD_NO, TType.KEYWORD_SSL],
            action=lambda _: ast.EnumOpenSslType.REQUIRED_NO_SSL
        )
    ]
)

# `CHAIN` 选项的枚举值
OPT_CHAIN_TYPE = ms_parser.create_group(
    name="opt_chain_type",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumChainType.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AND, TType.KEYWORD_NO, TType.KEYWORD_CHAIN],
            action=lambda _: ast.EnumChainType.NO
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AND, TType.KEYWORD_CHAIN],
            action=lambda _: ast.EnumChainType.YES
        )
    ]
)

# `RELEASE` 选项的枚举值
OPT_RELEASE_TYPE = ms_parser.create_group(
    name="opt_release_type",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumReleaseType.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RELEASE],
            action=lambda _: ast.EnumReleaseType.YES
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NO, TType.KEYWORD_RELEASE],
            action=lambda _: ast.EnumReleaseType.NO
        )
    ]
)

# 资源组类型的枚举值
RESOURCE_GROUP_TYPE = ms_parser.create_group(
    name="resource_group_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_USER],
            action=lambda _: ast.EnumResourceGroupType.USER
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SYSTEM],
            action=lambda _: ast.EnumResourceGroupType.SYSTEM
        )
    ]
)

# `SIGNAL` 和 `RESIGNAL` 语句中条件信息项名称的枚举值
SIGNAL_CONDITION_TYPE = ms_parser.create_group(
    name="signal_condition_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CLASS_ORIGIN],
            action=lambda _: ast.EnumSignalConditionType.CLASS_ORIGIN
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SUBCLASS_ORIGIN],
            action=lambda _: ast.EnumSignalConditionType.SUBCLASS_ORIGIN
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CONSTRAINT_CATALOG],
            action=lambda _: ast.EnumSignalConditionType.CONSTRAINT_CATALOG
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CONSTRAINT_SCHEMA],
            action=lambda _: ast.EnumSignalConditionType.CONSTRAINT_SCHEMA
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CONSTRAINT_NAME],
            action=lambda _: ast.EnumSignalConditionType.CONSTRAINT_NAME
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CATALOG_NAME],
            action=lambda _: ast.EnumSignalConditionType.CATALOG_NAME
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SCHEMA_NAME],
            action=lambda _: ast.EnumSignalConditionType.SCHEMA_NAME
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TABLE_NAME],
            action=lambda _: ast.EnumSignalConditionType.TABLE_NAME
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COLUMN_NAME],
            action=lambda _: ast.EnumSignalConditionType.COLUMN_NAME
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CURSOR_NAME],
            action=lambda _: ast.EnumSignalConditionType.CURSOR_NAME
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MESSAGE_TEXT],
            action=lambda _: ast.EnumSignalConditionType.MESSAGE_TEXT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MYSQL_ERRNO],
            action=lambda _: ast.EnumSignalConditionType.MYSQL_ERRNO
        )
    ]
)

# `FLUSH` 语句选项的枚举值的列表
FLUSH_OPTION_TYPE_LIST = ms_parser.create_group(
    name="flush_option_type_list",
    rules=[
        ms_parser.create_rule(
            symbols=["flush_option_type_list", TType.OPERATOR_COMMA, "flush_option_type"],
            action=lambda x: x[0] | x[2]
        ),
        ms_parser.create_rule(
            symbols=["flush_option_type"],
            action=lambda x: x[0]
        )
    ]
)

# `FLUSH` 语句选项的枚举值
FLUSH_OPTION_TYPE = ms_parser.create_group(
    name="flush_option_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ERROR, TType.KEYWORD_LOGS],
            action=lambda _: ast.EnumFlushOptionType.ERROR_LOGS
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ENGINE, TType.KEYWORD_LOGS],
            action=lambda _: ast.EnumFlushOptionType.ENGINE_LOGS
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GENERAL, TType.KEYWORD_LOGS],
            action=lambda _: ast.EnumFlushOptionType.GENERAL_LOGS
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SLOW, TType.KEYWORD_LOGS],
            action=lambda _: ast.EnumFlushOptionType.SLOW_LOGS
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BINARY, TType.KEYWORD_LOGS],
            action=lambda _: ast.EnumFlushOptionType.BINARY_LOGS
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RELAY, TType.KEYWORD_LOGS],
            action=lambda _: ast.EnumFlushOptionType.RELAY_LOGS
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PRIVILEGES],
            action=lambda _: ast.EnumFlushOptionType.PRIVILEGES
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOGS],
            action=lambda _: ast.EnumFlushOptionType.LOGS
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STATUS],
            action=lambda _: ast.EnumFlushOptionType.STATUS
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_USER_RESOURCES],
            action=lambda _: ast.EnumFlushOptionType.RESOURCES
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_OPTIMIZER_COSTS],
            action=lambda _: ast.EnumFlushOptionType.OPTIMIZER_COSTS
        )
    ]
)

# `FLUSH` 语句锁定选项的枚举值
FLUSH_LOCK_TYPE = ms_parser.create_group(
    name="flush_lock_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITH, TType.KEYWORD_READ, TType.KEYWORD_LOCK],
            action=lambda _: ast.EnumFlushLockType.WITH_READ_LOCK
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FOR, TType.KEYWORD_EXPORT],
            action=lambda _: ast.EnumFlushLockType.FOR_EXPORT
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumFlushLockType.DEFAULT
        )
    ]
)

# 可选的 ACL 类型枚举值
OPT_ACL_TYPE = ms_parser.create_group(
    name="opt_acl_type",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumAclType.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TABLE],
            action=lambda _: ast.EnumAclType.TABLE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FUNCTION],
            action=lambda _: ast.EnumAclType.FUNCTION
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PROCEDURE],
            action=lambda _: ast.EnumAclType.PROCEDURE
        )
    ]
)

# 可选的 JOIN/RESUME 类型枚举值
OPT_JOIN_OR_RESUME = ms_parser.create_group(
    name="opt_xa_join_or_resume",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumXaJoinOrResume.NONE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_JOIN],
            action=lambda _: ast.EnumXaJoinOrResume.JOIN
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RESUME],
            action=lambda _: ast.EnumXaJoinOrResume.RESUME
        )
    ]
)

# 可选的 SUSPEND 类型枚举值
OPT_SUSPEND = ms_parser.create_group(
    name="opt_xa_suspend",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumXaSuspend.NONE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SUSPEND],
            action=lambda _: ast.EnumXaSuspend.SUSPEND
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SUSPEND, TType.KEYWORD_FOR, TType.KEYWORD_MIGRATE],
            action=lambda _: ast.EnumXaSuspend.FOR_MIGRATE
        )
    ]
)

# 可选的资源组启用/禁用状态枚举值
OPT_ENABLE_DISABLE = ms_parser.create_group(
    name="opt_enable_disable",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumEnableDisable.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ENABLE],
            action=lambda _: ast.EnumEnableDisable.ENABLE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DISABLE],
            action=lambda _: ast.EnumEnableDisable.DISABLE
        )
    ]
)

# 可选的视图检查选项的枚举值
OPT_VIEW_CHECK_OPTION = ms_parser.create_group(
    name="opt_view_check_option",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumViewCheckOption.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITH, TType.KEYWORD_CHECK, TType.KEYWORD_OPTION],
            action=lambda _: ast.EnumViewCheckOption.WITH_CHECK_OPTION
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITH, TType.KEYWORD_CASCADED, TType.KEYWORD_CHECK, TType.KEYWORD_OPTION],
            action=lambda _: ast.EnumViewCheckOption.WITH_CASCADED_CHECK_OPTION
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITH, TType.KEYWORD_LOCAL, TType.KEYWORD_CHECK, TType.KEYWORD_OPTION],
            action=lambda _: ast.EnumViewCheckOption.WITH_LOCAL_CHECK_OPTION
        )
    ]
)

# 可选的事件状态类型的枚举值
OPT_EVENT_STATUS_TYPE = ms_parser.create_group(
    name="opt_event_status_type",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumEventStatusType.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ENABLE],
            action=lambda _: ast.EnumEventStatusType.ENABLE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DISABLE, TType.KEYWORD_ON, TType.KEYWORD_SLAVE],
            action=lambda _: ast.EnumEventStatusType.DISABLE_ON_SLAVE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DISABLE, TType.KEYWORD_ON, TType.KEYWORD_REPLICA],
            action=lambda _: ast.EnumEventStatusType.DISABLE_ON_REPLICA
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DISABLE],
            action=lambda _: ast.EnumEventStatusType.DISABLE
        )
    ]
)

# 处理器类型的枚举值
HANDLER_TYPE = ms_parser.create_group(
    name="handler_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXIT],
            action=lambda _: ast.EnumHandlerType.EXIT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CONTINUE],
            action=lambda _: ast.EnumHandlerType.CONTINUE
        )
    ]
)

# 可选的事件完成类型的枚举值
OPT_EVENT_COMPLETION_TYPE = ms_parser.create_group(
    name="opt_event_completion_type",
    rules=[
        ms_parser.create_rule(
            symbols=["event_completion_type"]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.EnumEventCompletionType.DEFAULT
        )
    ]
)

# 事件完成类型的枚举值
EVENT_COMPLETION_TYPE = ms_parser.create_group(
    name="event_completion_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ON, TType.KEYWORD_COMPLETION, TType.KEYWORD_PRESERVE],
            action=lambda _: ast.EnumEventCompletionType.ON_COMPLETION_PRESERVE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ON, TType.KEYWORD_COMPLETION, TType.KEYWORD_NOT, TType.KEYWORD_PRESERVE],
            action=lambda _: ast.EnumEventCompletionType.ON_COMPLETION_NOT_PRESERVE
        )
    ]
)

# 诊断区域的枚举值
WHICH_AREA = ms_parser.create_group(
    name="which_area",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumDiagnosticsAreaType.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CURRENT],
            action=lambda _: ast.EnumDiagnosticsAreaType.CURRENT_AREA
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STACKED],
            action=lambda _: ast.EnumDiagnosticsAreaType.STACKED_AREA
        )
    ]
)

# 语句诊断信息项名称的枚举值
STATEMENT_INFORMATION_TYPE = ms_parser.create_group(
    name="statement_information_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NUMBER],
            action=lambda _: ast.EnumStatementInformationType.NUMBER
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ROW_COUNT],
            action=lambda _: ast.EnumStatementInformationType.ROW_COUNT
        )
    ]
)

# 条件诊断信息项名称的枚举值
CONDITION_INFORMATION_TYPE = ms_parser.create_group(
    name="condition_information_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CLASS_ORIGIN],
            action=lambda _: ast.EnumConditionInformationType.CLASS_ORIGIN
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SUBCLASS_ORIGIN],
            action=lambda _: ast.EnumConditionInformationType.SUBCLASS_ORIGIN
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CONSTRAINT_CATALOG],
            action=lambda _: ast.EnumConditionInformationType.CONSTRAINT_CATALOG
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CONSTRAINT_SCHEMA],
            action=lambda _: ast.EnumConditionInformationType.CONSTRAINT_SCHEMA
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CONSTRAINT_NAME],
            action=lambda _: ast.EnumConditionInformationType.CONSTRAINT_NAME
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CATALOG_NAME],
            action=lambda _: ast.EnumConditionInformationType.CATALOG_NAME
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SCHEMA_NAME],
            action=lambda _: ast.EnumConditionInformationType.SCHEMA_NAME
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TABLE_NAME],
            action=lambda _: ast.EnumConditionInformationType.TABLE_NAME
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COLUMN_NAME],
            action=lambda _: ast.EnumConditionInformationType.COLUMN_NAME
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CURSOR_NAME],
            action=lambda _: ast.EnumConditionInformationType.CURSOR_NAME
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MESSAGE_TEXT],
            action=lambda _: ast.EnumConditionInformationType.MESSAGE_TEXT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MYSQL_ERRNO],
            action=lambda _: ast.EnumConditionInformationType.MYSQL_ERRNO
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RETURNED_SQLSTATE],
            action=lambda _: ast.EnumConditionInformationType.RETURNED_SQLSTATE
        )
    ]
)

# 行格式类型的枚举值
ROW_FORMAT_TYPE = ms_parser.create_group(
    name="row_format_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DEFAULT],
            action=lambda _: ast.EnumRowFormatType.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FIXED],
            action=lambda _: ast.EnumRowFormatType.FIXED
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DYNAMIC],
            action=lambda _: ast.EnumRowFormatType.DYNAMIC
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COMPRESSED],
            action=lambda _: ast.EnumRowFormatType.COMPRESSED
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REDUNDANT],
            action=lambda _: ast.EnumRowFormatType.REDUNDANT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COMPACT],
            action=lambda _: ast.EnumRowFormatType.COMPACT
        )
    ]
)

# 向 MERGE 表插入数据的类型的枚举值
MERGE_INSERT_TYPE = ms_parser.create_group(
    name="merge_insert_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NO],
            action=lambda _: ast.EnumMergeInsertType.NO
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FIRST],
            action=lambda _: ast.EnumMergeInsertType.FIRST
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LAST],
            action=lambda _: ast.EnumMergeInsertType.LAST
        )
    ]
)

# `UNDO TABLESPACE` 状态的枚举值
UNDO_TABLESPACE_STATE = ms_parser.create_group(
    name="undo_tablespace_state",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ACTIVE],
            action=lambda x: ast.EnumUndoTablespaceState.ACTIVE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INACTIVE],
            action=lambda x: ast.EnumUndoTablespaceState.INACTIVE
        )
    ]
)

# 可选的视图算法类型的枚举值
OPT_VIEW_ALGORITHM_TYPE = ms_parser.create_group(
    name="opt_view_algorithm_type",
    rules=[
        ms_parser.create_rule(
            symbols=["view_algorithm_type"]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.EnumViewAlgorithmType.DEFAULT
        )
    ]
)

# 视图算法类型的枚举值
VIEW_ALGORITHM_TYPE = ms_parser.create_group(
    name="view_algorithm_type",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.EnumViewAlgorithmType.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALGORITHM, TType.OPERATOR_EQ, TType.KEYWORD_UNDEFINED],
            action=lambda x: ast.EnumViewAlgorithmType.UNDEFINED
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALGORITHM, TType.OPERATOR_EQ, TType.KEYWORD_MERGE],
            action=lambda x: ast.EnumViewAlgorithmType.MERGE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALGORITHM, TType.OPERATOR_EQ, TType.KEYWORD_TEMPTABLE],
            action=lambda x: ast.EnumViewAlgorithmType.TEMPTABLE
        )
    ]
)

# 视图 SUID 类型的枚举值
VIEW_SUID_TYPE = ms_parser.create_group(
    name="view_suid_type",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.EnumViewSuidType.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SQL, TType.KEYWORD_SECURITY, TType.KEYWORD_DEFINER],
            action=lambda x: ast.EnumViewSuidType.DEFINER
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SQL, TType.KEYWORD_SECURITY, TType.KEYWORD_INVOKER],
            action=lambda x: ast.EnumViewSuidType.INVOKER
        )
    ]
)

# 可选的副本线程选项的枚举值的列表
OPT_REPLICA_THREAD_TYPE_LIST = ms_parser.create_group(
    name="opt_replica_thread_type_list",
    rules=[
        ms_parser.create_rule(
            symbols=["replica_thread_type_list"],
            action=lambda x: x[0]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.EnumReplicaThreadType.DEFAULT
        )
    ]
)

# 副本线程选项的枚举值的列表
REPLICA_THREAD_TYPE_LIST = ms_parser.create_group(
    name="replica_thread_type_list",
    rules=[
        ms_parser.create_rule(
            symbols=["replica_thread_type_list", TType.OPERATOR_COMMA, "replica_thread_type"],
            action=lambda x: x[0] | x[2]
        ),
        ms_parser.create_rule(
            symbols=["replica_thread_type"],
            action=lambda x: x[0]
        )
    ]
)

# 副本线程选项的枚举值
REPLICA_THREAD_TYPE = ms_parser.create_group(
    name="replica_thread_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SQL_THREAD],
            action=lambda x: ast.EnumReplicaThreadType.SQL_THREAD
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RELAY_THREAD],
            action=lambda x: ast.EnumReplicaThreadType.RELAY_THREAD
        )
    ]
)

# `LOAD` 语句中数据类型的枚举值
DATA_OR_XML = ms_parser.create_group(
    name="data_or_xml",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DATA],
            action=lambda _: ast.EnumDataType.CSV
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_XML],
            action=lambda _: ast.EnumDataType.XML
        )
    ]
)

# `LOAD` 语句中锁定类型的枚举值
LOAD_DATA_LOCK = ms_parser.create_group(
    name="load_data_lock",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumLoadDataLock.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CONCURRENT],
            action=lambda _: ast.EnumLoadDataLock.CONCURRENT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOW_PRIORITY],
            action=lambda _: ast.EnumLoadDataLock.LOW_PRIORITY
        )
    ]
)

# `LOAD` 语句中数据源类型的枚举值
LOAD_SOURCE_TYPE = ms_parser.create_group(
    name="load_source_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INFILE],
            action=lambda _: ast.EnumLoadSourceType.FILE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_URL],
            action=lambda _: ast.EnumLoadSourceType.URL
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_S3],
            action=lambda _: ast.EnumLoadSourceType.S3
        )
    ]
)

# 表主键检查类型的枚举值
TABLE_PRIMARY_KEY_CHECK_TYPE = ms_parser.create_group(
    name="table_primary_key_check_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STREAM],
            action=lambda _: ast.EnumTablePrimaryKeyCheckType.STREAM
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ON],
            action=lambda _: ast.EnumTablePrimaryKeyCheckType.ON
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_OFF],
            action=lambda _: ast.EnumTablePrimaryKeyCheckType.OFF
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GENERATE],
            action=lambda _: ast.EnumTablePrimaryKeyCheckType.GENERATE
        )
    ]
)

# `HANDLER` 语句扫描函数的枚举值
HANDLER_SCAN_FUNCTION = ms_parser.create_group(
    name="handler_scan_function",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FIRST],
            action=lambda _: ast.EnumHandlerScanFunction.FIRST
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NEXT],
            action=lambda _: ast.EnumHandlerScanFunction.NEXT
        )
    ]
)

# `HANDLER` 语句索引键函数的枚举值
HANDLER_RKEY_FUNCTION = ms_parser.create_group(
    name="handler_rkey_function",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FIRST],
            action=lambda _: ast.EnumHandlerRkeyFunction.FIRST
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NEXT],
            action=lambda _: ast.EnumHandlerRkeyFunction.NEXT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PREV],
            action=lambda _: ast.EnumHandlerRkeyFunction.PREV
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LAST],
            action=lambda _: ast.EnumHandlerRkeyFunction.LAST
        )
    ]
)

# `HANDLER` 语句索引键模式的枚举值
HANDLER_RKEY_MODE = ms_parser.create_group(
    name="handler_rkey_mode",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_EQ],
            action=lambda _: ast.EnumHandlerRkeyMode.EQ
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_GT_EQ],
            action=lambda _: ast.EnumHandlerRkeyMode.GE
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LT_EQ],
            action=lambda _: ast.EnumHandlerRkeyMode.LE
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_GT],
            action=lambda _: ast.EnumHandlerRkeyMode.GT
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LT],
            action=lambda _: ast.EnumHandlerRkeyMode.LT
        )
    ]
)

# 事务访问模式类型的枚举值
TRANSACTION_ACCESS_MODE_TYPE = ms_parser.create_group(
    name="transaction_access_mode_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_READ, TType.KEYWORD_ONLY],
            action=lambda _: ast.EnumTransactionAccessModeType.READ_ONLY
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_READ, TType.KEYWORD_WRITE],
            action=lambda _: ast.EnumTransactionAccessModeType.READ_WRITE
        )
    ]
)

# 事务隔离级别类型的枚举值
ISOLATION_TYPE = ms_parser.create_group(
    name="isolation_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_READ, TType.KEYWORD_UNCOMMITTED],
            action=lambda _: ast.EnumIsolationType.READ_UNCOMMITTED
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_READ, TType.KEYWORD_COMMITTED],
            action=lambda _: ast.EnumIsolationType.READ_COMMITTED
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REPEATABLE, TType.KEYWORD_READ],
            action=lambda _: ast.EnumIsolationType.REPEATABLE_READ
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SERIALIZABLE],
            action=lambda _: ast.EnumIsolationType.SERIALIZABLE
        )
    ]
)

# 可选的 SET 语句选项类型的枚举值
OPT_SET_OPTION_TYPE = ms_parser.create_group(
    name="opt_set_option_type",
    rules=[
        ms_parser.create_rule(
            symbols=["set_option_type"]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumSetOptionType.DEFAULT
        )
    ]
)

# SET 语句选项类型的枚举值
SET_OPTION_TYPE = ms_parser.create_group(
    name="set_option_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GLOBAL],
            action=lambda _: ast.EnumSetOptionType.GLOBAL
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PERSIST],
            action=lambda _: ast.EnumSetOptionType.PERSIST
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PERSIST_ONLY],
            action=lambda _: ast.EnumSetOptionType.PERSIST_ONLY
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOCAL],
            action=lambda _: ast.EnumSetOptionType.LOCAL
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SESSION],
            action=lambda _: ast.EnumSetOptionType.SESSION
        )
    ]
)

# 触发器动作时间类型的枚举值
TRIGGER_ACTION_TIME_TYPE = ms_parser.create_group(
    name="trigger_action_time_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BEFORE],
            action=lambda _: ast.EnumTriggerActionTimeType.BEFORE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AFTER],
            action=lambda _: ast.EnumTriggerActionTimeType.AFTER
        )
    ]
)

# 触发器事件类型的枚举值
TRIGGER_EVENT_TYPE = ms_parser.create_group(
    name="trigger_event_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INSERT],
            action=lambda _: ast.EnumTriggerEventType.INSERT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UPDATE],
            action=lambda _: ast.EnumTriggerEventType.UPDATE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DELETE],
            action=lambda _: ast.EnumTriggerEventType.DELETE
        )
    ]
)

# 触发器动作顺序类型的枚举值
TRIGGER_ACTION_ORDER_TYPE = ms_parser.create_group(
    name="trigger_action_order_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FOLLOWS],
            action=lambda _: ast.EnumTriggerActionOrderType.FOLLOWS
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PRECEDES],
            action=lambda _: ast.EnumTriggerActionOrderType.PRECEDES
        )
    ]
)

# 存储过程参数模式的枚举值
PROCEDURE_PARAM_MODE = ms_parser.create_group(
    name="procedure_param_mode",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumProcedureParamMode.IN
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IN],
            action=lambda _: ast.EnumProcedureParamMode.IN
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_OUT],
            action=lambda _: ast.EnumProcedureParamMode.OUT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INOUT],
            action=lambda _: ast.EnumProcedureParamMode.INOUT
        )
    ]
)

# UDF 函数返回值类型的枚举值
UDF_RETURN_TYPE = ms_parser.create_group(
    name="udf_return_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STRING],
            action=lambda _: ast.EnumUdfReturnType.STRING
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REAL],
            action=lambda _: ast.EnumUdfReturnType.REAL
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DECIMAL],
            action=lambda _: ast.EnumUdfReturnType.DECIMAL
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INT],
            action=lambda _: ast.EnumUdfReturnType.INT
        )
    ]
)

# 可选的 `SET` 语句中变量类型的枚举值
OPT_SET_VARIABLE_TYPE = ms_parser.create_group(
    name="opt_set_variable_type",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumSetVariableType.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PERSIST],
            action=lambda _: ast.EnumSetVariableType.PERSIST
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PERSIST_ONLY],
            action=lambda _: ast.EnumSetVariableType.PERSIST_ONLY
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GLOBAL],
            action=lambda _: ast.EnumSetVariableType.GLOBAL
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOCAL],
            action=lambda _: ast.EnumSetVariableType.LOCAL
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SESSION],
            action=lambda _: ast.EnumSetVariableType.SESSION
        )
    ]
)
