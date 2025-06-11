"""
DESCRIBE 语句（describe statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast

__all__ = [
    "DESCRIBE_STATEMENT",
    "OPT_DESCRIBE_COLUMN"
]

# DESCRIBE 语句
DESCRIBE_STATEMENT = ms_parser.create_group(
    name="describe_statement",
    rules=[
        ms_parser.create_rule(
            symbols=["keyword_describe_or_explain", "table_ident", "opt_describe_column"],
            action=lambda x: ast.DescribeStatement(table_name=x[1], describe_column=x[2])
        )
    ]
)

# 可选的 DESCRIBE 描述字段
OPT_DESCRIBE_COLUMN = ms_parser.create_group(
    name="opt_describe_column",
    rules=[
        ms_parser.create_rule(
            symbols=["text_string"],
            action=lambda x: x[0].get_str_value()
        ),
        ms_parser.create_rule(
            symbols=["ident"],
            action=lambda x: x[0].get_str_value()
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)
