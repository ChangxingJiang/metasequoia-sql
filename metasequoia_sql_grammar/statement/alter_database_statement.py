"""
ALTER DATABASE 语句（alter database statement）
"""

import metasequoia_parser as ms_parser
from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ALTER_DATABASE_STATEMENT",
]

# `ALTER DATABASE` 语句
ALTER_DATABASE_STATEMENT = ms_parser.create_group(
    name="alter_database_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_ALTER,
                TType.KEYWORD_DATABASE,
                "opt_ident",
                "alter_database_option_list"
            ],
            action=lambda x: ast.AlterDatabaseStatement(
                database_name=x[2],
                option_list=x[3]
            )
        )
    ]
)
