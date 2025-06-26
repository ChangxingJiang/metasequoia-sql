"""
SET 语句（set statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "SET_STATEMENT",
    "OPTION_VALUE_LIST",
    "OPTION_VALUE",
    "OPTION_VALUE_FOLLOWING_OPTION_TYPE",
    "OPTION_VALUE_NO_OPTION_TYPE",
    "OPTION_VALUE_BY_EXPR",
    "SET_EXPR_OR_DEFAULT",
]

# `SET` 语句
SET_STATEMENT = ms_parser.create_group(
    name="set_statement",
    rules=[
        # SET option_value_list
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SET, "option_value_list"],
            action=lambda x: ast.SetStatement(option_values=x[1])
        )
    ]
)

# `SET` 语句中的选项值的列表
OPTION_VALUE_LIST = ms_parser.create_group(
    name="option_value_list",
    rules=[
        ms_parser.create_rule(
            symbols=["option_value_list", TType.OPERATOR_COMMA, "option_value"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["option_value"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# `SET` 语句中的选项值
OPTION_VALUE = ms_parser.create_group(
    name="option_value",
    rules=[
        # option_type option_value_following_option_type
        ms_parser.create_rule(
            symbols=["set_option_type", "option_value_following_option_type"],
            action=lambda x: x[1].set_option_type(x[0])
        ),
        # option_value_no_option_type
        ms_parser.create_rule(
            symbols=["option_value_no_option_type"],
            action=lambda x: x[0]
        )
    ]
)

# `SET` 语句的选项值（有选项类型）
OPTION_VALUE_FOLLOWING_OPTION_TYPE = ms_parser.create_group(
    name="option_value_following_option_type",
    rules=[
        # lvalue_variable equal set_expr_or_default
        ms_parser.create_rule(
            symbols=["option_value_by_expr"]
        )
    ]
)

# `SET` 语句的选项值（无选项类型）
OPTION_VALUE_NO_OPTION_TYPE = ms_parser.create_group(
    name="option_value_no_option_type",
    rules=[
        # lvalue_variable equal set_expr_or_default
        ms_parser.create_rule(
            symbols=["option_value_by_expr"]
        ),
        # @ ident_or_text equal expr
        ms_parser.create_rule(
            symbols=["user_variable", "equal", "expr"],
            action=lambda x: ast.SetUserVariableValue(variable=x[0], value=x[2],
                                                      option_type=ast.EnumSetOptionType.DEFAULT)
        ),
        # @ @ opt_set_var_ident_type lvalue_variable equal set_expr_or_default
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_AT, TType.OPERATOR_AT, "opt_set_variable_type", "variable_identifier", "equal",
                     "set_expr_or_default"],
            action=lambda x: ast.SetSystemVariableValue(variable_type=x[2], variable=x[3], value=x[5],
                                                        option_type=ast.EnumSetOptionType.DEFAULT)
        ),
        # character_set old_or_new_charset_name_or_default
        ms_parser.create_rule(
            symbols=["keyword_charset", "charset_name_or_default"],
            action=lambda x: ast.SetCharsetValue(charset=x[1], option_type=ast.EnumSetOptionType.DEFAULT)
        ),
        # NAMES equal expr (bad syntax, always fails)
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NAMES, "equal", "expr"],
            action=lambda x: ast.SetNamesInvalidValue(value=x[2], option_type=ast.EnumSetOptionType.DEFAULT)
        ),
        # NAMES charset_name opt_collate
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NAMES, "charset_name", "opt_collate"],
            action=lambda x: ast.SetNamesValue(charset=x[1], collation=x[2], option_type=ast.EnumSetOptionType.DEFAULT)
        ),
        # NAMES DEFAULT
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NAMES, TType.KEYWORD_DEFAULT],
            action=lambda x: ast.SetNamesDefaultValue(option_type=ast.EnumSetOptionType.DEFAULT)
        )
    ]
)

# `SET` 语句中通过表达式赋值的值表达式
OPTION_VALUE_BY_EXPR = ms_parser.create_group(
    name="option_value_by_expr",
    rules=[
        # lvalue_variable equal set_expr_or_default
        ms_parser.create_rule(
            symbols=["variable_identifier", "equal", "set_expr_or_default"],
            action=lambda x: ast.SetVariableValue(variable=x[0], value=x[2], option_type=ast.EnumSetOptionType.DEFAULT)
        )
    ]
)

# `SET` 语句中的值表达式或 `DEFAULT` 关键字
SET_EXPR_OR_DEFAULT = ms_parser.create_group(
    name="set_expr_or_default",
    rules=[
        ms_parser.create_rule(
            symbols=["expr"]
        ),
        ms_parser.create_rule(
            symbols=["default"],
            action=lambda _: ast.DefaultValue()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ON],
            action=lambda _: ast.StringLiteral("ON")
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALL],
            action=lambda _: ast.StringLiteral("ALL")
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BINARY],
            action=lambda _: ast.StringLiteral("BINARY")
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ROW],
            action=lambda _: ast.StringLiteral("ROW")
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SYSTEM],
            action=lambda _: ast.StringLiteral("SYSTEM")
        )
    ]
)
