"""
CHECK TABLE 语句（check table statement）
"""

import metasequoia_parser as ms_parser
from metasequoia_sql import ast

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CHECK_TABLE_STATEMENT"
]

# `CHECK TABLE` 语句
CHECK_TABLE_STATEMENT = ms_parser.create_group(
    name="check_table_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHECK, "keyword_table_or_tables", "identifier_list", "opt_check_type_list"],
            action=lambda x: ast.CheckTableStatement(table_list=x[2], check_type=x[3])
        )
    ]
)
