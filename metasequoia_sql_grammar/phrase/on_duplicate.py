"""
重复值处理规则（on duplicate）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_ON_DUPLICATE",
    "ON_DUPLICATE",
]

# 可选的指定重复值处理规则的 `REPLACE` 或 `IGNORE` 关键字
OPT_ON_DUPLICATE = ms_parser.create_group(
    name="opt_on_duplicate",
    rules=[
        ms_parser.create_rule(
            symbols=["on_duplicate"]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.OnDuplicate.DEFAULT
        )
    ]
)

# 指定重复值处理规则的 `REPLACE` 或 `IGNORE` 关键字
ON_DUPLICATE = ms_parser.create_group(
    name="on_duplicate",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IGNORE],
            action=lambda _: ast.OnDuplicate.IGNORE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REPLACE],
            action=lambda _: ast.OnDuplicate.REPLACE
        )
    ]
)
