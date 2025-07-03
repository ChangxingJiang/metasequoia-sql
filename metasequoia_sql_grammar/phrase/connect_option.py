"""
连接选项（connect option）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_CONNECT_OPTION_LIST",
    "CONNECT_OPTION_LIST",
    "CONNECT_OPTION",
]

# 可选的连接选项列表
OPT_CONNECT_OPTION_LIST = ms_parser.create_group(
    name="opt_connect_option_list",
    rules=[
        ms_parser.template.rule.EMPTY_RETURN_LIST,
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITH, "connect_option_list"],
            action=lambda x: x[1]
        )
    ]
)

# 连接选项列表
CONNECT_OPTION_LIST = ms_parser.create_group(
    name="connect_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["connect_option_list", "connect_option"],
            action=ms_parser.template.action.LIST_APPEND_1
        ),
        ms_parser.create_rule(
            symbols=["connect_option"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 连接选项
CONNECT_OPTION = ms_parser.create_group(
    name="connect_option",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MAX_QUERIES_PER_HOUR, "num_literal_or_hex"],
            action=lambda x: ast.MaxQueriesPerHour(x[1].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MAX_UPDATES_PER_HOUR, "num_literal_or_hex"],
            action=lambda x: ast.MaxUpdatesPerHour(x[1].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MAX_CONNECTIONS_PER_HOUR, "num_literal_or_hex"],
            action=lambda x: ast.MaxConnectionsPerHour(x[1].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MAX_USER_CONNECTIONS, "num_literal_or_hex"],
            action=lambda x: ast.MaxUserConnections(x[1].value)
        )
    ]
)
