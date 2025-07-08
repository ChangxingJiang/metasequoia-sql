"""
ORDER BY 子句语义组
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal.terminal_type import SqlTerminalType as TType

__all__ = [
    "ORDER_EXPR",
    "ORDER_BY_LIST",
    "OPT_ORDER_BY_CLAUSE",
]

# 排序表达式
# 对应 MySQL 语义组：order_expr
ORDER_EXPR = ms_parser.create_group(
    name="order_expr",
    rules=[
        ms_parser.create_rule(
            symbols=["expr", "opt_order_direction"],
            action=lambda x: ast.OrderExpression(column=x[0], direction=x[1])
        )
    ]
)

# 排序字段的列表
# 对应 MySQL 语义组：order_list、gorder_list
ORDER_BY_LIST = ms_parser.create_group(
    name="order_by_list",
    rules=[
        ms_parser.create_rule(
            symbols=["order_by_list", TType.OPERATOR_COMMA, "order_expr"],
            action=lambda x: x[0].append(x[2])
        ),
        ms_parser.create_rule(
            symbols=["order_expr"],
            action=lambda x: ast.OrderByClause(column_list=[x[0]])
        )
    ]
)

# 可选的 ORDER BY 子句
# 对应 MySQL 语义组：opt_order_clause、order_clause（超集）、opt_window_order_by_clause
OPT_ORDER_BY_CLAUSE = ms_parser.create_group(
    name="opt_order_by_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ORDER, TType.KEYWORD_BY, "order_by_list"],
            action=lambda x: x[2]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)
