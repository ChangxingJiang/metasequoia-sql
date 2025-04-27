"""
DQL 语句的语义组
"""

import metasequoia_parser as ms_parser

from metasequoia_sql_new import ast
from metasequoia_sql_new.terminal.terminal_type import SqlTerminalType as TType

__all__ = [
    "GENERAL_GROUP_BY_LIST",
    "GENERAL_ORDER_DIRECTION",
    "GENERAL_OPT_ORDER_DIRECTION",
    "GENERAL_ORDER_EXPR",
    "GENERAL_ORDER_BY_LIST",
]

# 分组字段的列表
# 对应 MySQL 语义组：group_list
GENERAL_GROUP_BY_LIST = ms_parser.create_group(
    name="group_by_list",
    rules=[
        ms_parser.create_rule(
            symbols=["group_by_list", TType.OPERATOR_COMMA, "expr"],
            action=lambda x: x[0].append(x[2])
        ),
        ms_parser.create_rule(
            symbols=["expr"],
            action=lambda x: ast.GroupByList(column_list=[x[0]])
        )
    ]
)

# 排序方向的 ASC 或 DESC 关键字
# 对应 MySQL 语义组：ordering_direction
GENERAL_ORDER_DIRECTION = ms_parser.create_group(
    name="order_direction",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ASC],
            action=lambda x: ast.EnumOrderDirection.ASC
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DESC],
            action=lambda x: ast.EnumOrderDirection.DESC
        )
    ]
)

# 可选的排序方向的 ASC 或 DESC 关键字
# 对应 MySQL 语义组：opt_ordering_direction
GENERAL_OPT_ORDER_DIRECTION = ms_parser.create_group(
    name="opt_order_direction",
    rules=[
        ms_parser.create_rule(
            symbols=["order_direction"]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.EnumOrderDirection.DEFAULT
        )
    ]
)

# 排序表达式
# 对应 MySQL 语义组：order_expr
GENERAL_ORDER_EXPR = ms_parser.create_group(
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
GENERAL_ORDER_BY_LIST = ms_parser.create_group(
    name="order_by_list",
    rules=[
        ms_parser.create_rule(
            symbols=["order_by_list", TType.OPERATOR_COMMA, "order_expr"],
            action=lambda x: x[0].append(x[2])
        ),
        ms_parser.create_rule(
            symbols=["order_expr"],
            action=lambda x: ast.OrderByList(column_list=[x[0]])
        )
    ]
)
