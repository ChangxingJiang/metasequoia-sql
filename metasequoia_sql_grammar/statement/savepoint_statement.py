"""
SAVEPOINT 语句（savepoint statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "SAVEPOINT_STATEMENT"
]

# `SAVEPOINT` 语句
SAVEPOINT_STATEMENT = ms_parser.create_group(
    name="savepoint_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SAVEPOINT, "ident"],
            action=lambda x: ast.SavepointStatement(savepoint_name=x[1].get_str_value())
        )
    ]
)
