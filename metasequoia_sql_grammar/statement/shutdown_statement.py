"""
SHUTDOWN 语句（shutdown statement）
"""

import metasequoia_parser as ms_parser
from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "SHUTDOWN_STATEMENT",
]

# `SHUTDOWN` 语句
SHUTDOWN_STATEMENT = ms_parser.create_group(
    name="shutdown_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHUTDOWN],
            action=lambda x: ast.ShutdownStatement()
        )
    ]
)
