"""
DQL 语句中的枚举类型
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    # 比较运算符
    "COMPARE_OPERATOR",

    # 全文索引的选项
    "FULLTEXT_OPTIONS",
    "OPT_IN_NATURAL_LANGUAGE_MODE",
    "OPT_WITH_QUERY_EXPANSION",
]

# 比较运算符
COMPARE_OPERATOR = ms_parser.create_group(
    name="compare_operator",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_EQ],
            action=lambda _: ast.EnumCompareOperator.EQ
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LT_EQ_GT],
            action=lambda _: ast.EnumCompareOperator.EQUAL
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_GT_EQ],
            action=lambda _: ast.EnumCompareOperator.GE
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_GT],
            action=lambda _: ast.EnumCompareOperator.GT
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LT_EQ],
            action=lambda _: ast.EnumCompareOperator.LE
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LT],
            action=lambda _: ast.EnumCompareOperator.LT
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_BANG_EQ],
            action=lambda _: ast.EnumCompareOperator.NE
        ),
    ]
)

# 全文索引的选项
FULLTEXT_OPTIONS = ms_parser.create_group(
    name="fulltext_options",
    rules=[
        ms_parser.create_rule(
            symbols=["opt_in_natural_language_mode", "opt_with_query_expansion"],
            action=lambda x: x[0] | x[1]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IN, TType.KEYWORD_BOOLEAN, TType.KEYWORD_MODE],
            action=lambda _: ast.EnumFulltextOption.IN_BOOLEAN_MODE
        )
    ]
)

# 全文索引可选的 `IN NATURAL LANGUAGE MODE` 选项
OPT_IN_NATURAL_LANGUAGE_MODE = ms_parser.create_group(
    name="opt_in_natural_language_mode",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IN, TType.KEYWORD_NATURAL, TType.KEYWORD_LANGUAGE, TType.KEYWORD_MODE],
            action=lambda _: ast.EnumFulltextOption.IN_NATURAL_LANGUAGE_MODE
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumFulltextOption.DEFAULT
        )
    ]
)

# 全文索引可选的 `WITH QUERY EXPANSION` 选项
OPT_WITH_QUERY_EXPANSION = ms_parser.create_group(
    name="opt_with_query_expansion",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITH, TType.KEYWORD_QUERY, TType.KEYWORD_EXPANSION],
            action=lambda _: ast.EnumFulltextOption.WITH_QUERY_EXPANSION
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumFulltextOption.DEFAULT
        )
    ]
)
