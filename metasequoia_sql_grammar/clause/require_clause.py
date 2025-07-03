"""
REQUIRE 子句（require clause）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "REQUIRE_CLAUSE",
    "REQUIRE_LIST",
    "REQUIRE_LIST_ELEMENT",
]

# `REQUIRE` 子句
REQUIRE_CLAUSE = ms_parser.create_group(
    name="require_clause",
    rules=[
        ms_parser.template.rule.EMPTY_RETURN_NULL,
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REQUIRE, "require_list"],
            action=lambda x: ast.RequireList(x[1])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REQUIRE, TType.KEYWORD_SSL],
            action=lambda _: ast.RequireSsl()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REQUIRE, TType.KEYWORD_X509],
            action=lambda _: ast.RequireX509()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REQUIRE, TType.KEYWORD_NONE],
            action=lambda _: ast.RequireNone()
        )
    ]
)

# REQUIRE 列表
REQUIRE_LIST = ms_parser.create_group(
    name="require_list",
    rules=[
        ms_parser.create_rule(
            symbols=["require_list", "opt_keyword_and", "require_list_element"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["require_list_element"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# REQUIRE 列表元素
REQUIRE_LIST_ELEMENT = ms_parser.create_group(
    name="require_list_element",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SUBJECT, TType.LITERAL_TEXT_STRING],
            action=lambda x: ast.RequireSubject(x[1])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ISSUER, TType.LITERAL_TEXT_STRING],
            action=lambda x: ast.RequireIssuer(x[1])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CIPHER, TType.LITERAL_TEXT_STRING],
            action=lambda x: ast.RequireCipher(x[1])
        )
    ]
)
