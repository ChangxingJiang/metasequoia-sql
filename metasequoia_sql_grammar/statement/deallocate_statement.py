"""
DEALLOCATE 语句（deallocate statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "DEALLOCATE_STATEMENT"
]

# `DEALLOCATE` 语句
DEALLOCATE_STATEMENT = ms_parser.create_group(
    name="deallocate_statement",
    rules=[
        ms_parser.create_rule(
            symbols=["keyword_deallocate_or_drop", TType.KEYWORD_PREPARE, "ident"],
            action=lambda x: ast.DeallocateStatement(statement_name=x[2].get_str_value())
        )
    ]
)
