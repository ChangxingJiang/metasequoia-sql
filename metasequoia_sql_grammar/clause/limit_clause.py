"""
LIMIT 子句（limit clause）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal.terminal_type import SqlTerminalType as TType

__all__ = [
    "OPT_LIMIT_CLAUSE",
    "LIMIT_CLAUSE",
    "LIMIT_OPTION"
]

# 可选的 LIMIT 子句
OPT_LIMIT_CLAUSE = ms_parser.create_group(
    name="opt_limit_clause",
    rules=[
        ms_parser.create_rule(
            symbols=["limit_clause"]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)

# LIMIT 子句
LIMIT_CLAUSE = ms_parser.create_group(
    name="limit_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LIMIT, "limit_option"],
            action=lambda x: ast.LimitClause(offset=None, limit=x[1])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LIMIT, "limit_option", TType.OPERATOR_COMMA, "limit_option"],
            action=lambda x: ast.LimitClause(offset=x[1], limit=x[3])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LIMIT, "limit_option", TType.KEYWORD_OFFSET, "limit_option"],
            action=lambda x: ast.LimitClause(offset=x[3], limit=x[1])
        )
    ]
)

# LIMIT 子句中的数量
LIMIT_OPTION = ms_parser.create_group(
    name="limit_option",
    rules=[
        ms_parser.create_rule(
            symbols=["ident"]
        ),
        ms_parser.create_rule(
            symbols=["param_marker"]
        ),
        ms_parser.create_rule(
            symbols=["int_literal"]
        )
    ]
)
