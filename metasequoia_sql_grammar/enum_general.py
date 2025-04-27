"""
枚举类型的语义组
"""

import metasequoia_parser as ms_parser

from metasequoia_sql_new import ast
from metasequoia_sql_new.terminal.terminal_type import SqlTerminalType as TType

__all__ = [
    "GENERAL_OPERATOR_COMPARE",
    "GENERAL_ORDER_DIRECTION",
    "GENERAL_OPT_ORDER_DIRECTION",
    "GENERAL_WINDOW_BORDER_TYPE",
]

# 比较运算符
# 对应 MySQL 语义组：comp_op
GENERAL_OPERATOR_COMPARE = ms_parser.create_group(
    name="operator_compare",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_EQ],
            action=lambda _: ast.EnumOperatorCompare.EQ
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LT_EQ_GT],
            action=lambda _: ast.EnumOperatorCompare.EQUAL
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_GT_EQ],
            action=lambda _: ast.EnumOperatorCompare.GE
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_GT],
            action=lambda _: ast.EnumOperatorCompare.GT
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LT_EQ],
            action=lambda _: ast.EnumOperatorCompare.LE
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LT],
            action=lambda _: ast.EnumOperatorCompare.LT
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_BANG_EQ],
            action=lambda _: ast.EnumOperatorCompare.NE
        ),
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

# 窗口的边界类型
# 对应 MySQL 语义组：window_frame_units
GENERAL_WINDOW_BORDER_TYPE = ms_parser.create_group(
    name="window_border_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ROWS],
            action=lambda x: ast.EnumWindowBorderType.ROWS
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RANGE],
            action=lambda x: ast.EnumWindowBorderType.RANGE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GROUPS],
            action=lambda x: ast.EnumWindowBorderType.GROUPS
        )
    ]
)

