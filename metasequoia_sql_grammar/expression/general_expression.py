"""
通用表达式的语义组
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPERATOR_COMPARE",
    "SIMPLE_EXPR",
    "BINARY_EXPR",
    "PREDICATE_EXPR",
    "BOOL_EXPR",
    "EXPR",
    "OPT_EXPR",
    "EXPR_LIST",
    "OPT_EXPR_LIST",
    "UDF_EXPRESSION",
    "UDF_EXPR_LIST",
    "OPT_UDF_EXPR_LIST",
    "MATCH_COLUMN_LIST",
    "OPT_IN_NATURAL_LANGUAGE_MODE",
    "OPT_WITH_QUERY_EXPANSION",
    "FULLTEXT_OPTIONS",
    "OPT_KEYWORD_ARRAY",
    "OPT_KEYWORD_INTERVAL",
    "WHEN_LIST",
]

# 比较运算符
OPERATOR_COMPARE = ms_parser.create_group(
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
            action=lambda x: ast.OperatorCollate(collation_operand=x[0], collation_name=x[2]),
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
        # TODO : row_subquery
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
        # TODO : EXISTS table_subquery
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
            symbols=[TType.WORD_CAST, TType.OPERATOR_LPAREN, "expr", TType.KEYWORD_AT, TType.KEYWORD_TIME,
                     TType.KEYWORD_ZONE, "opt_keyword_interval", "text_literal_sys", TType.KEYWORD_AS,
                     TType.KEYWORD_DATETIME, "field_type_param_1", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionCastAtTimeZone(expression=x[2], is_interval=x[6], time_zone=x[7],
                                                        precision=x[10].option_1)
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
            action=lambda x: ast.OperatorJsonSeparator(expression=x[0], path=x[2], is_unquoted=False)
        ),
        ms_parser.create_rule(
            symbols=["simple_ident", TType.KEYWORD_JSON_UNQUOTED_SEPARATOR, "text_literal_sys"],
            action=lambda x: ast.OperatorJsonSeparator(expression=x[0], path=x[2], is_unquoted=True)
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
            action=lambda x: ast.OperatorBitOr(left_operand=x[0], right_operand=x[2]),
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
        # TODO : bit_expr IN_SYM table_subquery
        # TODO : bit_expr not IN_SYM table_subquery
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
            action=lambda x: ast.OperatorNotInValues(operand=x[0], value_list=[x[3]])
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.KEYWORD_NOT, TType.KEYWORD_IN, TType.OPERATOR_LPAREN, "expr",
                     TType.OPERATOR_COMMA, "expr_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.OperatorNotInValues(operand=x[0], value_list=[x[3]] + x[5])
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
            action=lambda x: ast.OperatorRegexp(left_operand=x[0], right_operand=x[1])
        ),
        ms_parser.create_rule(
            symbols=["binary_expr", TType.KEYWORD_NOT, TType.KEYWORD_REGEXP, "binary_expr"],
            action=lambda x: ast.OperatorNotRegexp(left_operand=x[0], right_operand=x[2])
        ),
        ms_parser.create_rule(
            symbols=["binary_expr"],
            sr_priority_as=TType.OPERATOR_COLON_EQ
        )
    ]
)

# 布尔表达式 TODO 待完成
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
            symbols=["bool_expr", "operator_compare", "predicate_expr"],
            action=lambda x: ast.OperatorCompare(left_operand=x[0], right_operand=x[2], operator=x[1])
        ),
        ms_parser.create_rule(
            symbols=["predicate_expr"],
            sr_priority_as=TType.OPERATOR_COLON_EQ
        )
    ]
)

# 一般表达式 TODO 待完成
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
        ms_parser.template.group.EMPTY_NULL
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
            action=lambda x: ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["udf_expr"],
            action=lambda x: ms_parser.template.action.LIST_INIT_0
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

# 全文本索引可选的 IN NATURAL LANGUAGE MODE 选项
OPT_IN_NATURAL_LANGUAGE_MODE = ms_parser.create_group(
    name="opt_in_natural_language_mode",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IN, TType.KEYWORD_NATURAL, TType.KEYWORD_LANGUAGE, TType.KEYWORD_MODE],
            action=lambda _: ast.FulltextOption.IN_NATURAL_LANGUAGE_MODE
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.FulltextOption.DEFAULT
        )
    ]
)

# 全文本索引可选的 WITH QUERY EXPANSION 选项
OPT_WITH_QUERY_EXPANSION = ms_parser.create_group(
    name="opt_with_query_expansion",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITH, TType.KEYWORD_QUERY, TType.KEYWORD_EXPANSION],
            action=lambda _: ast.FulltextOption.WITH_QUERY_EXPANSION
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.FulltextOption.DEFAULT
        )
    ]
)

# 全文本索引的选项
FULLTEXT_OPTIONS = ms_parser.create_group(
    name="fulltext_options",
    rules=[
        ms_parser.create_rule(
            symbols=["opt_in_natural_language_mode", "opt_with_query_expansion"],
            action=lambda x: x[0] | x[1]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IN, TType.KEYWORD_BOOLEAN, TType.KEYWORD_MODE],
            action=lambda _: ast.FulltextOption.IN_BOOLEAN_MODE
        )
    ]
)

# 可选的 ARRAY 关键字
OPT_KEYWORD_ARRAY = ms_parser.create_group(
    name="opt_keyword_array",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ARRAY],
            action=lambda _: True
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: False
        )
    ]
)

# 可选的 INTERVAL 关键字
OPT_KEYWORD_INTERVAL = ms_parser.create_group(
    name="opt_keyword_interval",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INTERVAL],
            action=lambda _: True
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: False
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
        ms_parser.template.group.EMPTY_NULL
    ]
)
