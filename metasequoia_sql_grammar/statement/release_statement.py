"""
RELEASE 语句（release statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "RELEASE_STATEMENT"
]

# `RELEASE` 语句
RELEASE_STATEMENT = ms_parser.create_group(
    name="release_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RELEASE, TType.KEYWORD_SAVEPOINT, "ident"],
            action=lambda x: ast.ReleaseStatement(savepoint_name=x[2].get_str_vale())
        )
    ]
)
