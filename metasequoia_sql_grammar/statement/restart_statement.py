"""
RESTART 语句（restart statement）
"""

import metasequoia_parser as ms_parser
from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "RESTART_STATEMENT",
]

# `RESTART` 语句
RESTART_STATEMENT = ms_parser.create_group(
    name="restart_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RESTART],
            action=lambda x: ast.RestartStatement()
        )
    ]
)
