"""
窗口函数表达式（window function expression）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql_new import ast
from metasequoia_sql_new.terminal import SqlTerminalType as TType

__all__ = [
    "PARAM_OR_VAR"
]

PARAM_OR_VAR = ms_parser.create_group(
    name="param_or_var",
    rules=[
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
