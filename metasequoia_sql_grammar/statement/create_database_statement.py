"""
CREATE DATABASE 语句（create database statement）
"""

import metasequoia_parser as ms_parser
from metasequoia_sql.ast import statement as ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CREATE_DATABASE_STATEMENT"
]

# `CREATE DATABASE` 语句
CREATE_DATABASE_STATEMENT = ms_parser.create_group(
    name="create_database_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CREATE, TType.KEYWORD_DATABASE, "opt_keyword_if_not_exists", "ident",
                     "opt_create_database_option_list"],
            action=lambda x: ast.CreateDatabaseStatement(
                if_not_exists=x[2],
                database_name=x[3].get_str_value(),
                options=x[4]
            )
        )
    ]
)
