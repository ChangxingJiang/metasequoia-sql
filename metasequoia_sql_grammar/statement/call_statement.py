"""
CALL 语句（call statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CALL_STATEMENT"
]

# `CALL` 语句
CALL_STATEMENT = ms_parser.create_group(
    name="call_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CALL, "identifier", "opt_paren_expr_list"],
            action=lambda x: ast.CallStatement(function_name=x[1], arguments=x[2])
        )
    ]
)
