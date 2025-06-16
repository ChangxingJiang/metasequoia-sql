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
