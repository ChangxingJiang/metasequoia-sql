"""
START REPLICA 语句（start replica statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "START_REPLICA_STATEMENT",
    "OPT_REPLICA_UNTIL",
    "REPLICA_UNTIL",
    "REPLICA_UNTIL_ITEM",
    "OPT_USER_OPTION",
    "OPT_PASSWORD_OPTION",
    "OPT_DEFAULT_AUTH_OPTION",
    "OPT_PLUGIN_DIR_OPTION",
]

# `START REPLICA` 语句
START_REPLICA_STATEMENT = ms_parser.create_group(
    name="start_replica_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_START,  # 0
                "keyword_replica_or_slave",  # 1
                "opt_replica_thread_type_list",  # 2
                "opt_replica_until",  # 3
                "opt_user_option",  # 4
                "opt_password_option",  # 5
                "opt_default_auth_option",  # 6
                "opt_plugin_dir_option",  # 7
                "opt_for_channel",  # 8
            ],
            action=lambda x: ast.StartReplicaStatement(
                thread_type=x[2],
                until_conditions=x[3],
                user_name=x[4],
                password=x[5],
                default_auth=x[6],
                plugin_dir=x[7],
                channel_name=x[8]
            )
        )
    ]
)

# 可选的 `UNTIL` 关键字引导的数据源信息的列表
OPT_REPLICA_UNTIL = ms_parser.create_group(
    name="opt_replica_until",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UNTIL, "replica_until"],
            action=lambda x: x[1]
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)

# 复制源信息的列表
REPLICA_UNTIL = ms_parser.create_group(
    name="replica_until",
    rules=[
        ms_parser.create_rule(
            symbols=["replica_until", TType.OPERATOR_COMMA, "replica_until_item"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["replica_until_item"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 复制源信息
REPLICA_UNTIL_ITEM = ms_parser.create_group(
    name="replica_until_item",
    rules=[
        ms_parser.create_rule(
            symbols=["source_file_def"]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SQL_BEFORE_GTIDS, TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.SqlBeforeGtids(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SQL_AFTER_GTIDS, TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.SqlAfterGtids(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SQL_AFTER_MTS_GAPS],
            action=lambda x: ast.SqlAfterMtsGaps()
        )
    ]
)

# 可选的用户选项
OPT_USER_OPTION = ms_parser.create_group(
    name="opt_user_option",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_USER, TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: x[2].get_str_value()
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: None
        )
    ]
)

# 可选的密码选项
OPT_PASSWORD_OPTION = ms_parser.create_group(
    name="opt_password_option",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PASSWORD, TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: x[2].get_str_value()
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: None
        )
    ]
)

# 可选的默认认证选项
OPT_DEFAULT_AUTH_OPTION = ms_parser.create_group(
    name="opt_default_auth_option",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DEFAULT_AUTH, TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: x[2].get_str_value()
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: None
        )
    ]
)

# 可选的插件目录选项
OPT_PLUGIN_DIR_OPTION = ms_parser.create_group(
    name="opt_plugin_dir_option",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PLUGIN_DIR, TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: x[2].get_str_value()
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: None
        )
    ]
)
