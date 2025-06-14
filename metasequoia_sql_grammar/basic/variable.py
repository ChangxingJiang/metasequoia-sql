"""
变量（variable）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "VARIABLE_NAME",
    "USER_VARIABLE_LIST",
    "USER_VARIABLE",
    "USER_OR_LOCAL_VARIABLE_LIST",
    "USER_OR_LOCAL_VARIABLE",
    "SYSTEM_VARIABLE_TYPE",
    "SYSTEM_VARIABLE",
    "SYSTEM_OR_USER_VARIABLE",
    "USER_VARIABLE_ASSIGNMENT",
]

# 用户变量或系统变量的变量名
VARIABLE_NAME = ms_parser.create_group(
    name="variable_name",
    rules=[
        ms_parser.create_rule(
            symbols=["ident"],
            action=lambda x: x[0].get_str_value()
        ),
        ms_parser.create_rule(
            symbols=["text_literal_sys"],
            action=lambda x: x[0].get_str_value()
        ),
        ms_parser.create_rule(
            symbols=[TType.LEX_HOSTNAME],
            action=lambda x: x[0]
        )
    ]
)

# 用户变量的列表
USER_VARIABLE_LIST = ms_parser.create_group(
    name="user_variable_list",
    rules=[
        ms_parser.create_rule(
            symbols=["user_variable_list", TType.OPERATOR_COMMA, "user_variable"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["user_variable"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 用户变量
USER_VARIABLE = ms_parser.create_group(
    name="user_variable",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_AT, "variable_name"],
            action=lambda x: ast.UserVariable(variable_name=x[1])
        )
    ]
)

# 用户变量或本地变量的列表
USER_OR_LOCAL_VARIABLE_LIST = ms_parser.create_group(
    name="user_or_local_variable_list",
    rules=[
        ms_parser.create_rule(
            symbols=["user_or_local_variable_list", TType.OPERATOR_COMMA, "user_or_local_variable"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["user_or_local_variable"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 用户变量或本地变量
USER_OR_LOCAL_VARIABLE = ms_parser.create_group(
    name="user_or_local_variable",
    rules=[
        ms_parser.create_rule(
            symbols=["user_variable"]
        ),
        ms_parser.create_rule(
            symbols=["ident_or_text"],
            action=lambda x: ast.LocalVariable(variable_name=x[0].get_str_value())
        )
    ]
)

# 系统变量类型
SYSTEM_VARIABLE_TYPE = ms_parser.create_group(
    name="system_variable_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GLOBAL, TType.OPERATOR_DOT],
            action=lambda _: ast.EnumSystemVariableType.GLOBAL
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOCAL, TType.OPERATOR_DOT],
            action=lambda _: ast.EnumSystemVariableType.LOCAL
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SESSION, TType.OPERATOR_DOT],
            action=lambda _: ast.EnumSystemVariableType.SESSION
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumSystemVariableType.DEFAULT
        )
    ]
)

# 系统变量
SYSTEM_VARIABLE = ms_parser.create_group(
    name="system_variable",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_AT, TType.OPERATOR_AT, "system_variable_type", "variable_name"],
            action=lambda x: ast.SystemVariable(variable_type=x[2], variable_namespace=None,
                                                variable_name=x[3])
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_AT, TType.OPERATOR_AT, "system_variable_type", "variable_name", TType.OPERATOR_DOT,
                     "ident"],
            action=lambda x: ast.SystemVariable(variable_type=x[2], variable_namespace=x[3],
                                                variable_name=x[5].get_str_value())
        )
    ]
)

# 系统变量或用户变量
SYSTEM_OR_USER_VARIABLE = ms_parser.create_group(
    name="system_or_user_variable",
    rules=[
        ms_parser.create_rule(
            symbols=["user_variable"]
        ),
        ms_parser.create_rule(
            symbols=["system_variable"]
        )
    ]
)

# 用户变量赋值语句
USER_VARIABLE_ASSIGNMENT = ms_parser.create_group(
    name="user_variable_assignment",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_AT, "variable_name", TType.OPERATOR_COLON_EQ, "expr"],
            action=lambda x: ast.UserVariableAssignment(variable_name=x[1], variable_value=x[3])
        )
    ]
)
