"""
DEFINER 子句（definer clause）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql.terminal.terminal_type import SqlTerminalType as TType

__all__ = [
    "OPT_DEFINDER_CLAUSE"
]

# 可选的指定定义者的 `DEFINER` 子句
OPT_DEFINDER_CLAUSE = ms_parser.create_group(
    name="opt_definer_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DEFINER, TType.OPERATOR_EQ, "user_name"],
            action=lambda x: x[2]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)
