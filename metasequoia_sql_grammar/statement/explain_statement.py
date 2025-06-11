"""
EXPLAIN 语句（explain statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "EXPLAIN_STATEMENT",
    "OPT_EXPLAIN_OPTIONS",
    "OPT_EXPLAIN_FORMAT",
    "OPT_EXPLAIN_INTO",
    "OPT_EXPLAIN_FOR_SCHEMA"
]

# `EXPLAIN` 语句
EXPLAIN_STATEMENT = ms_parser.create_group(
    name="explain_statement",
    rules=[
        ms_parser.create_rule(
            symbols=["keyword_describe_or_explain", "opt_explain_options", "opt_explain_for_schema",
                     "select_statement"],
            action=lambda x: ast.ExplainStatementForStatement(options=x[1], schema_name=x[2], statement=x[3])
        ),
        ms_parser.create_rule(
            symbols=["keyword_describe_or_explain", "opt_explain_options", "opt_explain_for_schema",
                     "insert_statement"],
            action=lambda x: ast.ExplainStatementForStatement(options=x[1], schema_name=x[2], statement=x[3])
        ),
        ms_parser.create_rule(
            symbols=["keyword_describe_or_explain", "opt_explain_options", "opt_explain_for_schema",
                     "replace_statement"],
            action=lambda x: ast.ExplainStatementForStatement(options=x[1], schema_name=x[2], statement=x[3])
        ),
        ms_parser.create_rule(
            symbols=["keyword_describe_or_explain", "opt_explain_options", "opt_explain_for_schema",
                     "update_statement"],
            action=lambda x: ast.ExplainStatementForStatement(options=x[1], schema_name=x[2], statement=x[3])
        ),
        ms_parser.create_rule(
            symbols=["keyword_describe_or_explain", "opt_explain_options", "opt_explain_for_schema",
                     "delete_statement"],
            action=lambda x: ast.ExplainStatementForStatement(options=x[1], schema_name=x[2], statement=x[3])
        ),
        ms_parser.create_rule(
            symbols=["keyword_describe_or_explain", "opt_explain_options", TType.KEYWORD_FOR, TType.KEYWORD_CONNECTION,
                     "int_literal_or_hex"],
            action=lambda x: ast.ExplainStatementForConnection(options=x[1], thread_id=x[4].value)
        )
    ]
)

# 可选的 `EXPLAIN` 分析选项
OPT_EXPLAIN_OPTIONS = ms_parser.create_group(
    name="opt_explain_options",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ANALYZE, "opt_explain_format"],
            action=lambda x: ast.ExplainOptions(is_analysis=True, explain_format=x[1])
        ),
        ms_parser.create_rule(
            symbols=["opt_explain_format", "opt_explain_into"],
            action=lambda x: ast.ExplainOptions(is_analysis=False, explain_into=x[1])
        )
    ]
)

# 可选的 `FORMAT` 引导的指定分析结果格式子句
OPT_EXPLAIN_FORMAT = ms_parser.create_group(
    name="opt_explain_format",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FORMAT, TType.OPERATOR_EQ, "ident_or_text"],
            action=lambda x: x[2].get_str_value()
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的 `INTO` 引导的指定分析结果写入变量子句
OPT_EXPLAIN_INTO = ms_parser.create_group(
    name="opt_explain_into",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INTO, "user_variable"],
            action=lambda x: x[1]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的 `FOR DATABASE` 引导的指定分析数据库子句
OPT_EXPLAIN_FOR_SCHEMA = ms_parser.create_group(
    name="opt_explain_for_schema",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FOR, TType.KEYWORD_DATABASE, "ident_or_text"],
            action=lambda x: x[2].get_str_value()
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)
