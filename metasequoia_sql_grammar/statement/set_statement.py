"""
SET 语句（set statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "SET_EXPR_OR_DEFAULT"
]

# `SET` 语句中的值表达式或 `DEFAULT` 关键字
SET_EXPR_OR_DEFAULT = ms_parser.create_group(
    name="set_expr_or_default",
    rules=[
        ms_parser.create_rule(
            symbols=["expr"]
        ),
        ms_parser.create_rule(
            symbols=["default"],
            action=lambda _: ast.DefaultValue()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ON],
            action=lambda _: ast.StringLiteral("ON")
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALL],
            action=lambda _: ast.StringLiteral("ALL")
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BINARY],
            action=lambda _: ast.StringLiteral("BINARY")
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ROW],
            action=lambda _: ast.StringLiteral("ROW")
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SYSTEM],
            action=lambda _: ast.StringLiteral("SYSTEM")
        )
    ]
)
