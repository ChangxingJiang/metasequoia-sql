"""
ALTER FUNCTION 语句（alter function statement）
"""

import metasequoia_parser as ms_parser
from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ALTER_FUNCTION_STATEMENT",
]

# `ALTER FUNCTION` 语句
ALTER_FUNCTION_STATEMENT = ms_parser.create_group(
    name="alter_function_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_ALTER,
                TType.KEYWORD_FUNCTION,
                "identifier",
                "alter_function_option_list"
            ],
            action=lambda x: ast.AlterFunctionStatement(
                function_name=x[2],
                option_list=x[3]
            )
        )
    ]
)
