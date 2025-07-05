# pylint: disable=R0801

"""
通用表达式的语义组
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "SIMPLE_EXPR",
    "BINARY_EXPR",
    "PREDICATE_EXPR",
    "BOOL_EXPR",
    "EXPR",
    "OPT_EXPR",
    "OPT_PAREN_EXPR_LIST",
    "OPT_EXPR_LIST",
    "EXPR_LIST",
    "UDF_EXPRESSION",
    "UDF_EXPR_LIST",
    "OPT_UDF_EXPR_LIST",
    "MATCH_COLUMN_LIST",
    "WHEN_LIST",
    "OPT_CASE_ELSE",
    "OPT_EXPR_OR_DEFAULT_LIST",
    "EXPR_OR_DEFAULT_LIST",
    "EXPR_OR_DEFAULT",
    "SUBQUERY",
    "OPT_DEFAULT_EXPR",
]

# 简单表达式
SIMPLE_EXPR = ms_parser.create_group(
    name="simple_expr",
    rules=[
        ms_parser.create_rule(
            symbols=["simple_ident"],
        ),
        ms_parser.create_rule(
            symbols=["function_expression"],
        ),
        ms_parser.create_rule(
            symbols=["simple_expr", TType.KEYWORD_COLLATE, "ident_or_text"],
            action=lambda x: ast.OperatorCollate(collation_operand=x[0], collation_name=x[2].get_str_value()),
            sr_priority_as=TType.NEG
        ),
        ms_parser.create_rule(
            symbols=["literal_or_null"],
        ),
        ms_parser.create_rule(
            symbols=["param_marker"],
        ),
        ms_parser.create_rule(
            symbols=["system_or_user_variable"]
        ),
        ms_parser.create_rule(
            symbols=["user_variable_assignment"]
        ),
        ms_parser.create_rule(
            symbols=["sum_function_expression"]
        ),
        ms_parser.create_rule(
            symbols=["window_function_expression"]
        ),
        ms_parser.create_rule(
            symbols=["simple_expr", TType.OPERATOR_BAR_BAR, "simple_expr"],
            action=lambda x: ast.OperatorConcat(left_operand=x[0], right_operand=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_PLUS, "simple_expr"],
            action=lambda x: x[1],
            sr_priority_as=TType.NEG
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_SUB, "simple_expr"],
            action=lambda x: ast.OperatorNegative(operand=x[1]),
            sr_priority_as=TType.NEG
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_TILDE, "simple_expr"],
            action=lambda x: ast.OperatorBitNot(operand=x[1]),
            sr_priority_as=TType.NEG
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_BANG, "simple_expr"],
            action=lambda x: ast.OperatorTruthTransform(operand=x[1]),
            sr_priority_as=TType.NEG
        ),
        ms_parser.create_rule(
            symbols=["subquery"],
            action=lambda x: ast.SingleRowSubSelect(query_expression=x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: x[1]
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.Row(value_list=[x[1]] + x[3])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ROW, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr_list",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.Row(value_list=[x[2]] + x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXISTS, "subquery"],
            action=lambda x: ast.ExistsSubSelect(query_expression=x[1])
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LBRACE, "ident", "expr", TType.OPERATOR_RBRACE],
            action=lambda x: ast.OdbcDate(odbc_type=x[1].get_str_value(), odbc_value=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MATCH, "match_column_list", TType.KEYWORD_AGAINST, TType.OPERATOR_LPAREN,
                     "binary_expr", "fulltext_options", TType.OPERATOR_RPAREN],
            action=lambda x: ast.OperatorMatch(column_list=x[1], sub_string=x[4], fulltext_options=x[5])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BINARY, "simple_expr"],
            action=lambda x: ast.OperatorBinary(operand=x[1]),
            sr_priority_as=TType.NEG
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_CAST, TType.OPERATOR_LPAREN, "expr", TType.KEYWORD_AS, "cast_type", "opt_keyword_array",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionCast(expression=x[2], cast_type=x[4], at_local=False, is_array_cast=x[5])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_CAST, TType.OPERATOR_LPAREN, "expr", TType.KEYWORD_AT, TType.KEYWORD_LOCAL,
                     TType.KEYWORD_AS, "cast_type", "opt_keyword_array", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionCast(expression=x[2], cast_type=x[6], at_local=True, is_array_cast=x[7])
        ),
        ms_parser.create_rule(
            symbols=[
                TType.WORD_CAST,  # 0
                TType.OPERATOR_LPAREN,  # 1
                "expr",  # 2
                TType.KEYWORD_AT,  # 3
                TType.KEYWORD_TIME,  # 4
                TType.KEYWORD_ZONE,  # 5
                "opt_keyword_interval",  # 6
                "text_literal_sys",  # 7
                TType.KEYWORD_AS,  # 8
                TType.KEYWORD_DATETIME,  # 9
                "field_type_param_1",  # 10
                TType.OPERATOR_RPAREN  # 11
            ],
            action=lambda x: ast.FunctionCastAtTimeZone(
                expression=x[2],
                is_interval=x[6],
                time_zone=x[7].get_str_value(),
                precision=x[10].option_1
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CASE, "opt_expr", "when_list", "opt_else", TType.KEYWORD_END],
            action=lambda x: ast.Case(case_expression=x[1], when_list=x[2], else_expression=x[3])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CONVERT, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "cast_type",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionConvert(expression=x[2], cast_type=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CONVERT, TType.OPERATOR_LPAREN, "expr", TType.KEYWORD_USING, "charset_name",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionConvertCharset(expression=x[2], charset=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DEFAULT, TType.OPERATOR_LPAREN, "simple_ident", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="default", param_list=[x[2]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_VALUES, TType.OPERATOR_LPAREN, "simple_ident", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="values", param_list=[x[2]])
        ),
        ms_parser.create_rule(
            symbols=["time_interval", TType.OPERATOR_PLUS, "expr"],
            action=lambda x: ast.OperatorDatePlus(left_operand=x[0], right_operand=x[2])
        ),
        ms_parser.create_rule(
            symbols=["simple_ident", TType.KEYWORD_JSON_SEPARATOR, "text_literal_sys"],
            action=lambda x: ast.OperatorJsonSeparator(expression=x[0], path=x[2].get_str_value(), is_unquoted=False)
        ),
        ms_parser.create_rule(
            symbols=["simple_ident", TType.KEYWORD_JSON_UNQUOTED_SEPARATOR, "text_literal_sys"],
            action=lambda x: ast.OperatorJsonSeparator(expression=x[0], path=x[2].get_str_value(), is_unquoted=True)
        )
    ]
)

# 二元表达式
BINARY_EXPR = ms_parser.create_group(
    name="binary_expr",
    rules=[
        ms_parser.create_rule(
            symbols=["binary_expr", TType.OPERATOR_BAR, "binary_expr"],
            action=lambda x: ast.OperatorBitOr(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_BAR
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.OPERATOR_AMP, "binary_expr"],
            action=lambda x: ast.OperatorBitAnd(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_AMP
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.OPERATOR_LT_LT, "binary_expr"],
            action=lambda x: ast.OperatorShiftLeft(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_LT_LT
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.OPERATOR_GT_GT, "binary_expr"],
            action=lambda x: ast.OperatorShiftRight(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_GT_GT
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.OPERATOR_PLUS, "binary_expr"],
            action=lambda x: ast.OperatorPlus(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_PLUS
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.OPERATOR_SUB, "binary_expr"],
            action=lambda x: ast.OperatorMinus(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_SUB
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.OPERATOR_PLUS, "time_interval"],
            action=lambda x: ast.OperatorPlusDate(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_PLUS
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.OPERATOR_SUB, "time_interval"],
            action=lambda x: ast.OperatorMinusDate(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_SUB
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.OPERATOR_STAR, "binary_expr"],
            action=lambda x: ast.OperatorMul(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_STAR
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.OPERATOR_SLASH, "binary_expr"],
            action=lambda x: ast.OperatorDiv(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_SLASH
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.OPERATOR_PERCENT, "binary_expr"],
            action=lambda x: ast.OperatorMod(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_PERCENT
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.KEYWORD_DIV, "binary_expr"],
            action=lambda x: ast.OperatorDivInt(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.KEYWORD_DIV
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.KEYWORD_MOD, "binary_expr"],
            action=lambda x: ast.OperatorMod(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.KEYWORD_MOD
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.OPERATOR_CARET, "binary_expr"],
            action=lambda x: ast.OperatorBitXor(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_CARET
        ),
        ms_parser.create_rule(
            symbols=["simple_expr"],
            sr_priority_as=TType.OPERATOR_COLON_EQ
        )
    ]
)

# 谓语表达式
PREDICATE_EXPR = ms_parser.create_group(
    name="predicate_expr",
    rules=[
        ms_parser.create_rule(
            symbols=["binary_expr", TType.KEYWORD_IN, "subquery"],
            action=lambda x: ast.OperatorInSubSelect(operand=x[0], subquery_expression=x[2])
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.KEYWORD_NOT, TType.KEYWORD_IN, "subquery"],
            action=lambda x: ast.OperatorNotInSubSelect(operand=x[0], subquery_expression=x[3])
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.KEYWORD_IN, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.OperatorInValues(operand=x[0], value_list=[x[3]])
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.KEYWORD_IN, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr_list",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.OperatorInValues(operand=x[0], value_list=[x[3]] + x[5])
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.KEYWORD_NOT, TType.KEYWORD_IN, TType.OPERATOR_LPAREN, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.OperatorNotInValues(operand=x[0], value_list=[x[4]])
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.KEYWORD_NOT, TType.KEYWORD_IN, TType.OPERATOR_LPAREN, "expr",
                     TType.OPERATOR_COMMA, "expr_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.OperatorNotInValues(operand=x[0], value_list=[x[4]] + x[6])
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.KEYWORD_MEMBER, "opt_keyword_of", TType.OPERATOR_LPAREN, "simple_expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.OperatorMemberOf(left_operand=x[0], right_operand=x[4])
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.KEYWORD_BETWEEN, "binary_expr", TType.KEYWORD_AND, "predicate_expr"],
            action=lambda x: ast.OperatorBetween(first_operand=x[0], second_operand=x[2], third_operand=x[4])
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.KEYWORD_NOT, TType.KEYWORD_BETWEEN, "binary_expr", TType.KEYWORD_AND,
                     "predicate_expr"],
            action=lambda x: ast.OperatorNotBetween(first_operand=x[0], second_operand=x[3], third_operand=x[5])
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.KEYWORD_SOUNDS, TType.KEYWORD_LIKE, "binary_expr"],
            action=lambda x: ast.OperatorSoundsLike(left_operand=x[0], right_operand=x[3])
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.KEYWORD_LIKE, "simple_expr"],
            action=lambda x: ast.OperatorLike(first_operand=x[0], second_operand=x[2], third_operand=None)
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.KEYWORD_LIKE, "simple_expr", TType.KEYWORD_ESCAPE, "simple_expr"],
            action=lambda x: ast.OperatorLike(first_operand=x[0], second_operand=x[2], third_operand=x[4]),
            sr_priority_as=TType.KEYWORD_LIKE
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.KEYWORD_NOT, TType.KEYWORD_LIKE, "simple_expr"],
            action=lambda x: ast.OperatorNotLike(first_operand=x[0], second_operand=x[3], third_operand=None)
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.KEYWORD_NOT, TType.KEYWORD_LIKE, "simple_expr", TType.KEYWORD_ESCAPE,
                     "simple_expr"],
            action=lambda x: ast.OperatorNotLike(first_operand=x[0], second_operand=x[3], third_operand=x[5]),
            sr_priority_as=TType.KEYWORD_LIKE
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.KEYWORD_REGEXP, "binary_expr"],
            action=lambda x: ast.OperatorRegexp(left_operand=x[0], right_operand=x[2])
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.KEYWORD_NOT, TType.KEYWORD_REGEXP, "binary_expr"],
            action=lambda x: ast.OperatorNotRegexp(left_operand=x[0], right_operand=x[3])
        ),
        ms_parser.create_rule(
            symbols=["binary_expr"],
            sr_priority_as=TType.OPERATOR_COLON_EQ
        )
    ]
)

# 布尔表达式
BOOL_EXPR = ms_parser.create_group(
    name="bool_expr",
    rules=[
        ms_parser.create_rule(
            symbols=["bool_expr", TType.KEYWORD_IS, TType.KEYWORD_NULL],
            action=lambda x: ast.OperatorIsNull(operand=x[0]),
            sr_priority_as=TType.KEYWORD_IS
        ),
        ms_parser.create_rule(
            symbols=["bool_expr", TType.KEYWORD_IS, TType.KEYWORD_NOT, TType.KEYWORD_NULL],
            action=lambda x: ast.OperatorIsNotNull(operand=x[0]),
            sr_priority_as=TType.KEYWORD_IS
        ),
        ms_parser.create_rule(
            symbols=["bool_expr", "compare_operator", "predicate_expr"],
            action=lambda x: ast.OperatorCompare(left_operand=x[0], right_operand=x[2], operator=x[1])
        ),
        ms_parser.create_rule(
            symbols=["bool_expr", "compare_operator", TType.KEYWORD_ALL, "subquery"],
            action=lambda x: ast.OperatorCompareAll(operand=x[0], operator=x[1], subquery_expression=x[3]),
            sr_priority_as=TType.OPERATOR_EQ
        ),
        ms_parser.create_rule(
            symbols=["bool_expr", "compare_operator", TType.KEYWORD_ANY, "subquery"],
            action=lambda x: ast.OperatorCompareAny(operand=x[0], operator=x[1], subquery_expression=x[3]),
            sr_priority_as=TType.OPERATOR_EQ
        ),
        ms_parser.create_rule(
            symbols=["predicate_expr"],
            sr_priority_as=TType.OPERATOR_COLON_EQ
        )
    ]
)

# 一般表达式
EXPR = ms_parser.create_group(
    name="expr",
    rules=[
        ms_parser.create_rule(
            symbols=["expr", TType.KEYWORD_OR, "expr"],
            action=lambda x: ast.OperatorOr(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.KEYWORD_OR
        ),
        ms_parser.create_rule(
            symbols=["expr", TType.KEYWORD_XOR, "expr"],
            action=lambda x: ast.OperatorXor(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.KEYWORD_XOR
        ),
        ms_parser.create_rule(
            symbols=["expr", TType.KEYWORD_AND, "expr"],
            action=lambda x: ast.OperatorAnd(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.KEYWORD_AND
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NOT, "expr"],
            action=lambda x: ast.OperatorNot(operand=x[1]),
            sr_priority_as=TType.KEYWORD_NOT
        ),
        ms_parser.create_rule(
            symbols=["bool_expr", TType.KEYWORD_IS, TType.KEYWORD_TRUE],
            action=lambda x: ast.OperatorIsTrue(operand=x[0]),
            sr_priority_as=TType.KEYWORD_IS
        ),
        ms_parser.create_rule(
            symbols=["bool_expr", TType.KEYWORD_IS, TType.KEYWORD_NOT, TType.KEYWORD_TRUE],
            action=lambda x: ast.OperatorIsNotTrue(operand=x[0]),
            sr_priority_as=TType.KEYWORD_IS
        ),
        ms_parser.create_rule(
            symbols=["bool_expr", TType.KEYWORD_IS, TType.KEYWORD_FALSE],
            action=lambda x: ast.OperatorIsFalse(operand=x[0]),
            sr_priority_as=TType.KEYWORD_IS
        ),
        ms_parser.create_rule(
            symbols=["bool_expr", TType.KEYWORD_IS, TType.KEYWORD_NOT, TType.KEYWORD_FALSE],
            action=lambda x: ast.OperatorIsNotFalse(operand=x[0]),
            sr_priority_as=TType.KEYWORD_IS
        ),
        ms_parser.create_rule(
            symbols=["bool_expr", TType.KEYWORD_IS, TType.KEYWORD_UNKNOWN],
            action=lambda x: ast.OperatorIsUnknown(operand=x[0]),
            sr_priority_as=TType.KEYWORD_IS
        ),
        ms_parser.create_rule(
            symbols=["bool_expr", TType.KEYWORD_IS, TType.KEYWORD_NOT, TType.KEYWORD_UNKNOWN],
            action=lambda x: ast.OperatorIsNotUnknown(operand=x[0]),
            sr_priority_as=TType.KEYWORD_IS
        ),
        ms_parser.create_rule(
            symbols=["bool_expr"],
            sr_priority_as=TType.OPERATOR_COLON_EQ
        )
    ]
)

# 可选的一般表达式
OPT_EXPR = ms_parser.create_group(
    name="opt_expr",
    rules=[
        ms_parser.create_rule(
            symbols=["expr"]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的嵌套括号内可选的逗号分隔的一般表达式列表
OPT_PAREN_EXPR_LIST = ms_parser.create_group(
    name="opt_paren_expr_list",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "opt_expr_list", TType.OPERATOR_RPAREN],
            action=lambda x: x[1]
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)

# 可选的逗号分隔的一般表达式列表
OPT_EXPR_LIST = ms_parser.create_group(
    name="opt_expr_list",
    rules=[
        ms_parser.create_rule(
            symbols=["expr_list"]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: []
        )
    ]
)

# 逗号分隔的一般表达式列表
EXPR_LIST = ms_parser.create_group(
    name="expr_list",
    rules=[
        ms_parser.create_rule(
            symbols=["expr_list", TType.OPERATOR_COMMA, "expr"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["expr"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# UDF 表达式（自定义函数中的参数）
UDF_EXPRESSION = ms_parser.create_group(
    name="udf_expr",
    rules=[
        ms_parser.create_rule(
            symbols=["expr", "opt_select_alias"],
            action=lambda x: ast.UdfExpression(expression=x[0], alias=x[1])
        )
    ]
)

# 逗号分隔的 UDF 表达式的列表
UDF_EXPR_LIST = ms_parser.create_group(
    name="udf_expr_list",
    rules=[
        ms_parser.create_rule(
            symbols=["udf_expr_list", TType.OPERATOR_COMMA, "udf_expr"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["udf_expr"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 可选的逗号分隔的 UDF 表达式的列表
OPT_UDF_EXPR_LIST = ms_parser.create_group(
    name="opt_udf_expr_list",
    rules=[
        ms_parser.create_rule(
            symbols=["udf_expr_list"]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: []
        )
    ]
)

# MATCH 函数的列名的列表
MATCH_COLUMN_LIST = ms_parser.create_group(
    name="match_column_list",
    rules=[
        ms_parser.create_rule(
            symbols=["simple_ident_list"],
            action=lambda x: x[0]
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "simple_ident_list", TType.OPERATOR_RPAREN],
            action=lambda x: x[1]
        )
    ]
)

# CASE 结构中的 WHEN 条件的列表
WHEN_LIST = ms_parser.create_group(
    name="when_list",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WHEN, "expr", TType.KEYWORD_THEN, "expr"],
            action=lambda x: [ast.WhenItem(condition=x[1], expression=x[3])]
        ),
        ms_parser.create_rule(
            symbols=["when_list", TType.KEYWORD_WHEN, "expr", TType.KEYWORD_THEN, "expr"],
            action=lambda x: x[0] + [ast.WhenItem(condition=x[2], expression=x[4])]
        )
    ]
)

# CASE 结构中可选的 ELSE 子句
OPT_CASE_ELSE = ms_parser.create_group(
    name="opt_else",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ELSE, "expr"],
            action=lambda x: x[1]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的一般表达式或 `DEFAULT` 关键字的列表
OPT_EXPR_OR_DEFAULT_LIST = ms_parser.create_group(
    name="opt_expr_or_default_list",
    rules=[
        ms_parser.create_rule(
            symbols=["expr_or_default_list"]
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)

# 一般表达式或 `DEFAULT` 关键字的列表
EXPR_OR_DEFAULT_LIST = ms_parser.create_group(
    name="expr_or_default_list",
    rules=[
        ms_parser.create_rule(
            symbols=["expr_or_default_list", TType.OPERATOR_COMMA, "expr_or_default"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["expr_or_default"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 一般表达式或 `DEFAULT 关键字
EXPR_OR_DEFAULT = ms_parser.create_group(
    name="expr_or_default",
    rules=[
        ms_parser.create_rule(
            symbols=["expr"]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DEFAULT],
            action=lambda _: ast.DefaultValue()
        )
    ]
)

# 子查询表达式
SUBQUERY = ms_parser.create_group(
    name="subquery",
    rules=[
        ms_parser.create_rule(
            symbols=["query_expression_parens"],
            action=lambda x: x[0],
            sr_priority_as=TType.SUBQUERY_AS_EXPR
        )
    ]
)

# 可选的 `DEFAULT` 关键字引导的表达式
OPT_DEFAULT_EXPR = ms_parser.create_group(
    name="opt_default_expr",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DEFAULT, "expr"],
            action=lambda x: x[1]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)
