"""
DO 语句（do statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "DO_STATEMENT"
]

# `DO` 语句
DO_STATEMENT = ms_parser.create_group(
    name="do_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DO, "select_item_list"],
            action=lambda x: ast.DoStatement(expressions=x[1])
        )
    ]
)
