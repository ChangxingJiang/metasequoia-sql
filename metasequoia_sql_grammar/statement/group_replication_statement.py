"""
GROUP REPLICATION 语句（group replication statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "GROUP_REPLICATION_STATEMENT",
    "OPT_GROUP_REPLICATION_START_OPTION_LIST",
    "GROUP_REPLICATION_START_OPTION_LIST",
    "GROUP_REPLICATION_START_OPTION",
    "GROUP_REPLICATION_USER",
    "GROUP_REPLICATION_PASSWORD",
    "GROUP_REPLICATION_PLUGIN_AUTH",
]

# `GROUP REPLICATION` 语句
GROUP_REPLICATION_STATEMENT = ms_parser.create_group(
    name="group_replication_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_START, TType.KEYWORD_GROUP_REPLICATION, "opt_group_replication_start_option_list"],
            action=lambda x: ast.GroupReplicationStartStatement(options=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STOP, TType.KEYWORD_GROUP_REPLICATION],
            action=lambda x: ast.GroupReplicationStopStatement()
        )
    ]
)

# 可选的 `GROUP REPLICATION START` 选项的列表
OPT_GROUP_REPLICATION_START_OPTION_LIST = ms_parser.create_group(
    name="opt_group_replication_start_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["group_replication_start_option_list"]
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)

# `GROUP REPLICATION START` 选项的列表
GROUP_REPLICATION_START_OPTION_LIST = ms_parser.create_group(
    name="group_replication_start_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["group_replication_start_option"],
            action=ms_parser.template.action.LIST_INIT_0
        ),
        ms_parser.create_rule(
            symbols=["group_replication_start_option_list", TType.OPERATOR_COMMA, "group_replication_start_option"],
            action=ms_parser.template.action.LIST_APPEND_2
        )
    ]
)

# `GROUP REPLICATION START` 的选项
GROUP_REPLICATION_START_OPTION = ms_parser.create_group(
    name="group_replication_start_option",
    rules=[
        ms_parser.create_rule(
            symbols=["group_replication_user"]
        ),
        ms_parser.create_rule(
            symbols=["group_replication_password"]
        ),
        ms_parser.create_rule(
            symbols=["group_replication_plugin_auth"]
        )
    ]
)

# `GROUP REPLICATION` 的 `USER` 选项
GROUP_REPLICATION_USER = ms_parser.create_group(
    name="group_replication_user",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_USER, TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.GroupReplicationUser(user=x[2].get_str_value())
        )
    ]
)

# `GROUP REPLICATION` 的 `PASSWORD` 选项
GROUP_REPLICATION_PASSWORD = ms_parser.create_group(
    name="group_replication_password",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PASSWORD, TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.GroupReplicationPassword(password=x[2].get_str_value())
        )
    ]
)

# `GROUP REPLICATION` 的插件认证选项
GROUP_REPLICATION_PLUGIN_AUTH = ms_parser.create_group(
    name="group_replication_plugin_auth",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DEFAULT_AUTH, TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.GroupReplicationPluginAuth(plugin_auth=x[2].get_str_value())
        )
    ]
)
