"""
USE 语句（use statement）
"""

import metasequoia_parser as ms_parser
from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "USE_STATEMENT",
]

# `USE` 语句
USE_STATEMENT = ms_parser.create_group(
    name="use_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_USE, "ident"],
            action=lambda x: ast.UseStatement(database_name=x[1])
        )
    ]
)
