"""
BEGIN 语句（begin statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "BEGIN_STATEMENT"
]

# `BEGIN` 语句
BEGIN_STATEMENT = ms_parser.create_group(
    name="begin_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BEGIN, "opt_keyword_work"],
            action=lambda x: ast.BeginStatement()
        )
    ]
)
