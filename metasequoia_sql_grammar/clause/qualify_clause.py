"""
QUALIFY 子句（qualify clause）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_QUALIFY_CLAUSE",
]

# 可选的 QUALIFY 子句
OPT_QUALIFY_CLAUSE = ms_parser.create_group(
    name="opt_qualify_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_QUALIFY, "expr"],
            action=lambda x: x[1]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)
