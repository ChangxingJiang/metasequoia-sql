"""
过滤器定义（filter definition）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "FILTER_DEF_LIST",
    "FILTER_DEF",
    "OPT_FILTER_DB_PAIR_LIST",
    "FILTER_DB_PAIR_LIST",
]

# 过滤器定义的列表
FILTER_DEF_LIST = ms_parser.create_group(
    name="filter_def_list",
    rules=[
        ms_parser.create_rule(
            symbols=["filter_def_list", TType.OPERATOR_COMMA, "filter_def"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["filter_def"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 过滤器定义
FILTER_DEF = ms_parser.create_group(
    name="filter_def",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REPLICATE_DO_DB, TType.OPERATOR_EQ, "parens_opt_ident_list"],
            action=lambda x: ast.ReplicateDoDbFilter(db_list=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REPLICATE_IGNORE_DB, TType.OPERATOR_EQ, "parens_opt_ident_list"],
            action=lambda x: ast.ReplicateIgnoreDbFilter(db_list=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REPLICATE_DO_TABLE, TType.OPERATOR_EQ, "parens_opt_qualified_identifier_list"],
            action=lambda x: ast.ReplicateDoTableFilter(table_list=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REPLICATE_IGNORE_TABLE, TType.OPERATOR_EQ, "parens_opt_qualified_identifier_list"],
            action=lambda x: ast.ReplicateIgnoreTableFilter(table_list=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REPLICATE_WILD_DO_TABLE, TType.OPERATOR_EQ, "parens_opt_text_literal_sys_list"],
            action=lambda x: ast.ReplicateWildDoTableFilter(pattern_list=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REPLICATE_WILD_IGNORE_TABLE, TType.OPERATOR_EQ, "parens_opt_text_literal_sys_list"],
            action=lambda x: ast.ReplicateWildIgnoreTableFilter(pattern_list=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REPLICATE_REWRITE_DB, TType.OPERATOR_EQ, "opt_filter_db_pair_list"],
            action=lambda x: ast.ReplicateRewriteDbFilter(db_pair_list=x[2])
        ),
    ]
)

# 可选的数据库对列表
OPT_FILTER_DB_PAIR_LIST = ms_parser.create_group(
    name="opt_filter_db_pair_list",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, TType.OPERATOR_RPAREN],
            action=lambda _: []
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "filter_db_pair_list", TType.OPERATOR_RPAREN],
            action=lambda x: x[1]
        )
    ]
)

# 数据库对列表
FILTER_DB_PAIR_LIST = ms_parser.create_group(
    name="filter_db_pair_list",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "ident", TType.OPERATOR_COMMA, "ident", TType.OPERATOR_RPAREN],
            action=lambda x: [(x[1].get_str_value(), x[3].get_str_value())]
        ),
        ms_parser.create_rule(
            symbols=["filter_db_pair_list", TType.OPERATOR_COMMA, TType.OPERATOR_LPAREN, "ident", TType.OPERATOR_COMMA,
                     "ident", TType.OPERATOR_RPAREN],
            action=lambda x: x[0] + [(x[3].get_str_value(), x[5].get_str_value())]
        )
    ]
)
