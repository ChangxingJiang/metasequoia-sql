"""
HAVING 子句（having clause）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_HAVING_CLAUSE",
]

# 可选的 HAVING 子句
OPT_HAVING_CLAUSE = ms_parser.create_group(
    name="opt_having_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_HAVING, "expr"],
            action=lambda x: x[1]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)
