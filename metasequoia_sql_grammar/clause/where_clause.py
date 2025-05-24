"""
WHERE 子句（where clause）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_WHERE_CLAUSE",
    "WHERE_CLAUSE"
]

# 可选的 WHERE 子句
OPT_WHERE_CLAUSE = ms_parser.create_group(
    name="opt_where_clause",
    rules=[
        ms_parser.create_rule(
            symbols=["where_clause"]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)

# WHERE 子句
WHERE_CLAUSE = ms_parser.create_group(
    name="where_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WHERE, "expr"],
            action=lambda x: x[1]
        )
    ]
)
