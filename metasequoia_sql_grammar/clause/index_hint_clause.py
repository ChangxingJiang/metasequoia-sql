"""
索引指定子句（index hint clause）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql_new import ast
from metasequoia_sql_new.terminal.terminal_type import SqlTerminalType as TType

__all__ = [
    "INDEX_HINT_FOR",
    "INDEX_HINT_TYPE",
    "HINT_KEY_NAME",
    "HINT_KEY_NAME_LIST",
    "OPT_HINT_KEY_NAME_LIST",
    "INDEX_HINT",
    "INDEX_HINT_LIST",
    "OPT_INDEX_HINT_LIST",
]

# 索引指定子句中的索引用途
INDEX_HINT_FOR = ms_parser.create_group(
    name="index_hint_for",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FOR, TType.KEYWORD_JOIN],
            action=lambda _: ast.EnumIndexHintFor.FOR_JOIN
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FOR, TType.KEYWORD_ORDER, TType.KEYWORD_BY],
            action=lambda _: ast.EnumIndexHintFor.FOR_ORDER_BY
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FOR, TType.KEYWORD_GROUP, TType.KEYWORD_BY],
            action=lambda _: ast.EnumIndexHintFor.FOR_GROUP_BY
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumIndexHintFor.DEFAULT
        )
    ]
)

# 索引指定子句中指定类型
INDEX_HINT_TYPE = ms_parser.create_group(
    name="index_hint_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FORCE],
            action=lambda _: ast.EnumIndexHintType.FORCE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IGNORE],
            action=lambda _: ast.EnumIndexHintType.IGNORE
        )
    ]
)

# 索引指定子句中的索引名称
HINT_KEY_NAME = ms_parser.create_group(
    name="hint_key_name",
    rules=[
        ms_parser.create_rule(
            symbols=["ident"],
            action=lambda x: x[0].get_str_value()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PRIMARY],
            action=lambda _: "PRIMARY"
        )
    ]
)

# 索引指定子句中的索引名称的列表
HINT_KEY_NAME_LIST = ms_parser.create_group(
    name="hint_key_name_list",
    rules=[
        ms_parser.create_rule(
            symbols=["hint_key_name_list", TType.OPERATOR_COMMA, "hint_key_name"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["hint_key_name"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 索引指定子句中可选的索引名称的列表
OPT_HINT_KEY_NAME_LIST = ms_parser.create_group(
    name="opt_hint_key_name_list",
    rules=[
        ms_parser.create_rule(
            symbols=["hint_key_name_list"]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: []
        )
    ]
)

# 索引指定子句
INDEX_HINT = ms_parser.create_group(
    name="index_hint",
    rules=[
        ms_parser.create_rule(
            symbols=["index_hint_type", "keyword_key_or_index", "index_hint_for", TType.OPERATOR_LPAREN,
                     "hint_key_name_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.IndexHint(index_hint_type=x[0], index_hint_for=x[2], index_name_list=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_USE, "keyword_key_or_index", "index_hint_for", TType.OPERATOR_LPAREN,
                     "opt_hint_key_name_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.IndexHint(index_hint_type=ast.EnumIndexHintType.USE, index_hint_for=x[2],
                                           index_name_list=x[4])
        ),
    ]
)

# 索引指定子句的列表
INDEX_HINT_LIST = ms_parser.create_group(
    name="index_hint_list",
    rules=[
        ms_parser.create_rule(
            symbols=["index_hint_list", "index_hint"],
            action=ms_parser.template.action.LIST_APPEND_1
        ),
        ms_parser.create_rule(
            symbols=["index_hint"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 可选的索引指定子句的列表
OPT_INDEX_HINT_LIST = ms_parser.create_group(
    name="opt_index_hint_list",
    rules=[
        ms_parser.create_rule(
            symbols=["index_hint_list"]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)
