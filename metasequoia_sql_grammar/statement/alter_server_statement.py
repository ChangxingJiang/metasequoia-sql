"""
ALTER SERVER 语句（alter server statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ALTER_SERVER_STATEMENT",
]

# `ALTER SERVER` 语句
ALTER_SERVER_STATEMENT = ms_parser.create_group(
    name="alter_server_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALTER, TType.KEYWORD_SERVER, "ident_or_text", TType.KEYWORD_OPTIONS,
                     TType.OPERATOR_LPAREN, "server_options_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.AlterServerStatement(
                server_name=x[2].get_str_value(),
                server_options=x[5]
            )
        )
    ]
)
