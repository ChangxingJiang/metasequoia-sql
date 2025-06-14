"""
TRUNCATE 语句（truncate statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "TRUNCATE_STATEMENT"
]

# `TRUNCATE` 语句
TRUNCATE_STATEMENT = ms_parser.create_group(
    name="truncate_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TRUNCATE, "opt_keyword_table", "identifier"],
            action=lambda x: ast.TruncateStatement(table_ident=x[2])
        )
    ]
) 