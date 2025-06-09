"""
聚集函数表达式（sum function expression）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "SUM_FUNCTION_EXPRESSION",
    "IN_SUM_EXPR",
    "OPT_SEPARATOR",
    "OPT_DISTINCT",
]

# 聚集函数的表达式
SUM_FUNCTION_EXPRESSION = ms_parser.create_group(
    name="sum_function_expression",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AVG, TType.OPERATOR_LPAREN, "opt_distinct", "in_sum_expr", TType.OPERATOR_RPAREN,
                     "opt_windowing_clause"],
            action=lambda x: ast.FuncSumAvg(distinct=x[2], param=x[3], window_clause=x[5])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_BIT_AND, TType.OPERATOR_LPAREN, "in_sum_expr", TType.OPERATOR_RPAREN,
                     "opt_windowing_clause"],
            action=lambda x: ast.FuncSumBitAnd(param=x[2], window_clause=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_BIT_OR, TType.OPERATOR_LPAREN, "in_sum_expr", TType.OPERATOR_RPAREN,
                     "opt_windowing_clause"],
            action=lambda x: ast.FuncSumBitOr(param=x[2], window_clause=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_JSON_ARRAYAGG, TType.OPERATOR_LPAREN, "in_sum_expr", TType.OPERATOR_RPAREN,
                     "opt_windowing_clause"],
            action=lambda x: ast.FuncSumJsonArrayAgg(param=x[2], window_clause=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_JSON_OBJECTAGG, TType.OPERATOR_LPAREN, "in_sum_expr", TType.OPERATOR_COMMA,
                     "in_sum_expr", TType.OPERATOR_RPAREN, "opt_windowing_clause"],
            action=lambda x: ast.FuncSumJsonObjectAgg(param1=x[2], param2=x[4], window_clause=x[6])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ST_COLLECT, TType.OPERATOR_LPAREN, "opt_distinct", "in_sum_expr",
                     TType.OPERATOR_RPAREN, "opt_windowing_clause"],
            action=lambda x: ast.FuncSumStCollect(distinct=x[2], param=x[3], window_clause=x[5])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_BIT_XOR, TType.OPERATOR_LPAREN, "in_sum_expr", TType.OPERATOR_RPAREN,
                     "opt_windowing_clause"],
            action=lambda x: ast.FuncSumBitXor(param=x[2], window_clause=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_COUNT, TType.OPERATOR_LPAREN, "opt_keyword_all", TType.OPERATOR_STAR,
                     TType.OPERATOR_RPAREN, "opt_windowing_clause"],
            action=lambda x: ast.FuncSumCountStar(window_clause=x[5])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_COUNT, TType.OPERATOR_LPAREN, "opt_distinct", "in_sum_expr", TType.OPERATOR_RPAREN,
                     "opt_windowing_clause"],
            action=lambda x: ast.FuncSumCount(distinct=x[2], param=x[3], window_clause=x[5])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_MIN, TType.OPERATOR_LPAREN, "opt_distinct", "in_sum_expr", TType.OPERATOR_RPAREN,
                     "opt_windowing_clause"],
            action=lambda x: ast.FuncSumMin(distinct=x[2], param=x[3], window_clause=x[5])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_MAX, TType.OPERATOR_LPAREN, "opt_distinct", "in_sum_expr", TType.OPERATOR_RPAREN,
                     "opt_windowing_clause"],
            action=lambda x: ast.FuncSumMax(param=x[3], distinct=x[2], window_clause=x[5])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_STD, TType.OPERATOR_LPAREN, "in_sum_expr", TType.OPERATOR_RPAREN,
                     "opt_windowing_clause"],
            action=lambda x: ast.FuncSumStd(param=x[2], window_clause=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_VARIANCE, TType.OPERATOR_LPAREN, "in_sum_expr", TType.OPERATOR_RPAREN,
                     "opt_windowing_clause"],
            action=lambda x: ast.FuncSumVariance(param=x[2], window_clause=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_STDDEV_SAMP, TType.OPERATOR_LPAREN, "in_sum_expr", TType.OPERATOR_RPAREN,
                     "opt_windowing_clause"],
            action=lambda x: ast.FuncSumStddevSamp(param=x[2], window_clause=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_VAR_SAMP, TType.OPERATOR_LPAREN, "in_sum_expr", TType.OPERATOR_RPAREN,
                     "opt_windowing_clause"],
            action=lambda x: ast.FuncSumVarSamp(param=x[2], window_clause=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_SUM, TType.OPERATOR_LPAREN, "opt_distinct", "in_sum_expr", TType.OPERATOR_RPAREN,
                     "opt_windowing_clause"],
            action=lambda x: ast.FuncSumSum(distinct=x[2], param=x[3], window_clause=x[5])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_GROUP_CONCAT, TType.OPERATOR_LPAREN, "opt_distinct", "expr_list", "opt_order_by_clause",
                     "opt_separator", TType.OPERATOR_RPAREN, "opt_windowing_clause"],
            action=lambda x: ast.FuncSumGroupConcat(distinct=x[2], param_list=x[3], order_by_clause=x[4],
                                                    separator=x[5], window_clause=x[7])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GROUPING, TType.OPERATOR_LPAREN, "expr_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionSumGrouping(param_list=x[2])
        )
    ]
)

# 聚集函数的参数
IN_SUM_EXPR = ms_parser.create_group(
    name="in_sum_expr",
    rules=[
        ms_parser.create_rule(
            symbols=["opt_keyword_all", "expr"],
            action=lambda x: x[1]
        ),
    ]
)

# 可选的 `DISTINCT` 关键字
OPT_DISTINCT = ms_parser.create_group(
    name="opt_distinct",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DISTINCT],
            action=lambda _: True
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: False
        )
    ]
)

# 可选的 `SEPARATOR` 关键字引导的分隔符
OPT_SEPARATOR = ms_parser.create_group(
    name="opt_separator",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SEPARATOR, "text_string"],
            action=lambda x: x[1]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)
