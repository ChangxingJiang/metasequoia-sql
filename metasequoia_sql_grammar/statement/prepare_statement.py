"""
PREPARE 语句（prepare statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "PREPARE_STATEMENT",
    "PREPARE_SOURCE"
]

# `PREPARE` 语句
PREPARE_STATEMENT = ms_parser.create_group(
    name="prepare_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PREPARE, "ident", TType.KEYWORD_FROM, "prepare_source"],
            action=lambda x: ast.PrepareStatement(statement_name=x[1].get_str_value(), prepare_source=x[3])
        )
    ]
)

# `PREPARE` 语句的 `FROM` 子句中的值
PREPARE_SOURCE = ms_parser.create_group(
    name="prepare_source",
    rules=[
        ms_parser.create_rule(
            symbols=["text_literal_sys"],
            action=lambda x: x[0]
        ),
        ms_parser.create_rule(
            symbols=["user_variable"],
            action=lambda x: x[0]
        )
    ]
)
