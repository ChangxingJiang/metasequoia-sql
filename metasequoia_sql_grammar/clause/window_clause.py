"""
WINDOW 子句（window clause）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_WINDOW_CLAUSE",
    "WINDOW_DEFINITION_LIST",
    "WINDOW_DEFINITION",
]

# 窗口子句
OPT_WINDOW_CLAUSE = ms_parser.create_group(
    name="opt_window_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WINDOW, "window_definition_list"],
            action=lambda x: x[2]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 窗口定义子句的列表
WINDOW_DEFINITION_LIST = ms_parser.create_group(
    name="window_definition_list",
    rules=[
        ms_parser.create_rule(
            symbols=["window_definition_list", TType.OPERATOR_COMMA, "window_definition"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["window_definition"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 窗口定义子句
WINDOW_DEFINITION = ms_parser.create_group(
    name="window_definition",
    rules=[
        ms_parser.create_rule(
            symbols=["ident", TType.KEYWORD_AS, TType.OPERATOR_LPAREN, "opt_ident", "opt_partition_by_clause",
                     "opt_order_by_clause", "opt_window_frame_clause", TType.OPERATOR_RPAREN],
            action=lambda x: ast.Window(name=x[0].get_str_value(), partition_clause=x[4], order_clause=x[5],
                                        frame_clause=x[6])
        ),
    ]
)
