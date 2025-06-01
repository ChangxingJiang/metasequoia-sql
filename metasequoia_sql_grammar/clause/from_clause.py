"""
FROM 子句（from clause）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal.terminal_type import SqlTerminalType as TType

__all__ = [
    "OPT_FROM_CLAUSE",
    "FROM_CLAUSE",
]

# 可选的 FROM 子句
OPT_FROM_CLAUSE = ms_parser.create_group(
    name="opt_from_clause",
    rules=[
        ms_parser.create_rule(
            symbols=["from_clause"]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: [],
            sr_priority_as=TType.EMPTY_FROM_CLAUSE
        )
    ]
)

# FROM 子句
FROM_CLAUSE = ms_parser.create_group(
    name="from_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FROM, TType.KEYWORD_DUAL],
            action=lambda _: [ast.DualTable()]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FROM, "table_reference_list"],
            action=lambda x: x[1]
        )
    ]
)
