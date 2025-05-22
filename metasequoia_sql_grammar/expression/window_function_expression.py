"""
窗口函数表达式（window function expression）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql_new import ast
from metasequoia_sql_new.terminal import SqlTerminalType as TType

__all__ = [
    "STABLE_INTEGER"
]

# 在执行过程中为常量的整数（字面值、参数占位符或用户变量）
STABLE_INTEGER = ms_parser.create_group(
    name="stable_integer",
    rules=[
        ms_parser.create_rule(
            symbols=["int_literal"]
        ),
        ms_parser.create_rule(
            symbols=["param_marker"]
        ),
        ms_parser.create_rule(
            symbols=["ident"]
        ),
        ms_parser.create_rule(
            symbols=["user_variable"]
        )
    ]
)
