"""
窗口函数表达式（window function expression）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "STABLE_INTEGER",
    "OPT_FROM_FIRST_OR_LAST",
    "OPT_NULL_TREATMENT",
    "OPT_LEAD_OR_LAG_INFO",
    "WINDOW_FUNCTION_EXPRESSION",
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

# NTH_VALUE 窗口函数中的 FROM FIRST 子句或 FROM LAST 子句
OPT_FROM_FIRST_OR_LAST = ms_parser.create_group(
    name="opt_from_first_or_last",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.FromFirstOrLast.NONE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FROM, TType.KEYWORD_FIRST],
            action=lambda _: ast.FromFirstOrLast.FROM_FIRST
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FROM, TType.KEYWORD_LAST],
            action=lambda _: ast.FromFirstOrLast.FROM_LAST
        )
    ]
)

# 窗口函数中指定 NULL 值处理策略的 RESPECT NULLS 或 IGNORE NULLS 子句
OPT_NULL_TREATMENT = ms_parser.create_group(
    name="opt_null_treatment",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.NullTreatment.NONE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RESPECT, TType.KEYWORD_NULLS],
            action=lambda _: ast.NullTreatment.RESPECT_NULLS
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IGNORE, TType.KEYWORD_NULLS],
            action=lambda _: ast.NullTreatment.IGNORE_NULLS
        )
    ]
)

# LEAD 和 LAG 窗口函数中偏移量及默认值信息
OPT_LEAD_OR_LAG_INFO = ms_parser.create_group(
    name="opt_lead_or_lag_info",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.LeadOrLagInfo(offset=None, default_value=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_COMMA, "stable_integer"],
            action=lambda x: ast.LeadOrLagInfo(offset=x[1], default_value=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_COMMA, "stable_integer", TType.OPERATOR_COMMA, "expr"],
            action=lambda x: ast.LeadOrLagInfo(offset=x[1], default_value=x[3])
        )
    ]
)

# 窗口函数表达式
WINDOW_FUNCTION_EXPRESSION = ms_parser.create_group(
    name="window_function_expression",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ROW_NUMBER, TType.OPERATOR_LPAREN, TType.OPERATOR_RPAREN, "windowing_clause"],
            action=lambda x: ast.FuncWindowRowNumber(window_clause=x[3])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RANK, TType.OPERATOR_LPAREN, TType.OPERATOR_RPAREN, "windowing_clause"],
            action=lambda x: ast.FuncWindowRank(window_clause=x[3])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DENSE_RANK, TType.OPERATOR_LPAREN, TType.OPERATOR_RPAREN, "windowing_clause"],
            action=lambda x: ast.FuncWindowDenseRank(window_clause=x[3])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CUME_DIST, TType.OPERATOR_LPAREN, TType.OPERATOR_RPAREN, "windowing_clause"],
            action=lambda x: ast.FuncWindowCumeDist(window_clause=x[3])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PERCENT_RANK, TType.OPERATOR_LPAREN, TType.OPERATOR_RPAREN, "windowing_clause"],
            action=lambda x: ast.FuncWindowPercentRank(window_clause=x[3])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NTILE, TType.OPERATOR_LPAREN, "stable_integer", TType.OPERATOR_RPAREN,
                     "windowing_clause"],
            action=lambda x: ast.FuncWindowNtile(param=x[2], window_clause=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LEAD, TType.OPERATOR_LPAREN, "expr", "opt_lead_or_lag_info", TType.OPERATOR_RPAREN,
                     "opt_null_treatment", "windowing_clause"],
            action=lambda x: ast.FuncWindowLead(param=x[2], offset=x[3].offset, default_value=x[3].default_value,
                                                null_treatment=x[5], window_clause=x[6])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LAG, TType.OPERATOR_LPAREN, "expr", "opt_lead_or_lag_info", TType.OPERATOR_RPAREN,
                     "opt_null_treatment", "windowing_clause"],
            action=lambda x: ast.FuncWindowLag(param=x[2], offset=x[3].offset, default_value=x[3].default_value,
                                               null_treatment=x[5], window_clause=x[6])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FIRST_VALUE, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN,
                     "opt_null_treatment", "windowing_clause"],
            action=lambda x: ast.FuncWindowFirstValue(param=x[2], null_treatment=x[4], window_clause=x[5])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LAST_VALUE, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN,
                     "opt_null_treatment", "windowing_clause"],
            action=lambda x: ast.FuncWindowLastValue(param=x[2], null_treatment=x[4], window_clause=x[5])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NTH_VALUE, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "simple_expr",
                     TType.OPERATOR_RPAREN, "opt_from_first_or_last", "opt_null_treatment", "windowing_clause"],
            action=lambda x: ast.FuncWindowNthValue(param_1=x[2], param_2=x[4], from_first_or_last=x[6],
                                                    null_treatment=x[7], window_clause=x[8])
        )
    ]
)
