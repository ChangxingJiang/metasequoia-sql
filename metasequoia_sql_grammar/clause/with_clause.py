"""
WITH 子句（with clause）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_WITH_CLAUSE",
    "WITH_CLAUSE",
    "WITH_TABLE_LIST",
    "WITH_TABLE",
]

# 可选的 `WITH` 子句
OPT_WITH_CLAUSE = ms_parser.create_group(
    name="opt_with_clause",
    rules=[
        ms_parser.create_rule(
            symbols=["with_clause"],
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# `WITH` 子句
WITH_CLAUSE = ms_parser.create_group(
    name="with_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITH, "with_table_list"],
            action=lambda x: ast.WithClause(table_list=x[1], recursive=False)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITH, TType.KEYWORD_RECURSIVE, "with_table_list"],
            action=lambda x: ast.WithClause(table_list=x[2], recursive=True)
        )
    ]
)

# `WITH` 子句中的表的列表
WITH_TABLE_LIST = ms_parser.create_group(
    name="with_table_list",
    rules=[
        ms_parser.create_rule(
            symbols=["with_table_list", TType.OPERATOR_COMMA, "with_table"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["with_table"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# `WITH` 子句中的表
WITH_TABLE = ms_parser.create_group(
    name="with_table",
    rules=[
        ms_parser.create_rule(
            symbols=["ident", "opt_ident_list_parens", TType.KEYWORD_AS, "subquery"],
            action=lambda x: ast.WithTable(table_name=x[0].get_str_value(), column_list=x[1], query_expression=x[3])
        )
    ]
)
