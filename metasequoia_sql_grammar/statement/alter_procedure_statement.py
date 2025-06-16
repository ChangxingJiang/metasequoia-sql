"""
ALTER PROCEDURE 语句（alter procedure statement）
"""

import metasequoia_parser as ms_parser
from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ALTER_PROCEDURE_STATEMENT",
]

# `ALTER PROCEDURE` 语句
ALTER_PROCEDURE_STATEMENT = ms_parser.create_group(
    name="alter_procedure_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_ALTER,
                TType.KEYWORD_PROCEDURE,
                "identifier",
                "alter_function_option_list"
            ],
            action=lambda x: ast.AlterProcedureStatement(
                procedure_name=x[2],
                option_list=x[3]
            )
        )
    ]
)
