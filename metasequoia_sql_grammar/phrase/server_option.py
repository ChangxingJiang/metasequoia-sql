"""
服务器选项（server option）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "SERVER_OPTIONS_LIST",
    "SERVER_OPTION",
]

# 服务器选项的列表
SERVER_OPTIONS_LIST = ms_parser.create_group(
    name="server_options_list",
    rules=[
        ms_parser.create_rule(
            symbols=["server_options_list", TType.OPERATOR_COMMA, "server_option"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["server_option"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 服务器选项
SERVER_OPTION = ms_parser.create_group(
    name="server_option",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_USER, "text_literal_sys"],
            action=lambda x: ast.ServerUserOption(username=x[1].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_HOST, "text_literal_sys"],
            action=lambda x: ast.ServerHostOption(host=x[1].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DATABASE, "text_literal_sys"],
            action=lambda x: ast.ServerDatabaseOption(database=x[1].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_OWNER, "text_literal_sys"],
            action=lambda x: ast.ServerOwnerOption(owner=x[1].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PASSWORD, "text_literal_sys"],
            action=lambda x: ast.ServerPasswordOption(password=x[1].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOCKET, "text_literal_sys"],
            action=lambda x: ast.ServerSocketOption(socket=x[1].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PORT, "num_literal_or_hex"],
            action=lambda x: ast.ServerPortOption(port=int(x[1].value))
        )
    ]
)
