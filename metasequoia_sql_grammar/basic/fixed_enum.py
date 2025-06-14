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
