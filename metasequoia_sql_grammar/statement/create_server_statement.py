"""
CREATE SERVER 语句（create server statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CREATE_SERVER_STATEMENT"
]

# `CREATE SERVER` 语句
CREATE_SERVER_STATEMENT = ms_parser.create_group(
    name="create_server_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CREATE, TType.KEYWORD_SERVER, "ident_or_text", TType.KEYWORD_FOREIGN,
                     TType.KEYWORD_DATA, TType.KEYWORD_WRAPPER, "ident_or_text", TType.KEYWORD_OPTIONS,
                     TType.OPERATOR_LPAREN, "server_options_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.CreateServerStatement(
                server_name=x[2].get_str_value(),
                wrapper_name=x[6].get_str_value(),
                options=x[9]
            )
        )
    ]
)
