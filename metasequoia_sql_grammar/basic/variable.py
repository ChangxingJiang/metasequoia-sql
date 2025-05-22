"""
变量（variable）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql_new import ast
from metasequoia_sql_new.terminal import SqlTerminalType as TType

__all__ = [
    "USER_VARIABLE"
]

USER_VARIABLE = ms_parser.create_group(
    name="user_variable",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_AT, "ident"],
            action=lambda x: ast.UserVariable(variable_name=x[1].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_AT, "text_literal_sys"],
            action=lambda x: ast.UserVariable(variable_name=x[1].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_AT, TType.LEX_HOSTNAME],
            action=lambda x: ast.UserVariable(variable_name=x[1])
        )
    ]
)
