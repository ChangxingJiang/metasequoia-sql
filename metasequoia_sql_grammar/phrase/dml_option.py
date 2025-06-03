"""
DML 语句选项（dml option）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_KEYWORD_IGNORE",
    "OPT_KEYWORD_LOW_PRIORITY",
    "OPT_DELETE_OPTION_LIST",
    "DELETE_OPTION_LIST",
    "DELETE_OPTION",
]

# 可选的 `IGNORE` 关键字
OPT_KEYWORD_IGNORE = ms_parser.create_group(
    name="opt_keyword_ignore",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IGNORE],
            action=lambda _: ast.DmlOption.IGNORE
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.DmlOption.DEFAULT
        )
    ]
)

# 可选的 `LOW_PRIORITY` 关键字
OPT_KEYWORD_LOW_PRIORITY = ms_parser.create_group(
    name="opt_keyword_low_priority",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOW_PRIORITY],
            action=lambda _: ast.DmlOption.LOW_PRIORITY
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.DmlOption.DEFAULT
        )
    ]
)

# 可选的 `DELETE` 语句中的选项的列表
OPT_DELETE_OPTION_LIST = ms_parser.create_group(
    name="opt_delete_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["delete_option_list"]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.DmlOption.DEFAULT
        )
    ]
)

# `DELETE` 语句中的选项的列表
DELETE_OPTION_LIST = ms_parser.create_group(
    name="delete_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["delete_option_list", "delete_option"],
            action=lambda x: x[0] | x[1]
        ),
        ms_parser.create_rule(
            symbols=["delete_option"],
            action=lambda x: x[0]
        )
    ]
)

# `DELETE` 语句中的选项（`quick`、`LOW_PRIORITY` 或 `IGNORE` 关键字）
DELETE_OPTION = ms_parser.create_group(
    name="delete_option",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_QUICK],
            action=lambda _: ast.DmlOption.QUICK
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOW_PRIORITY],
            action=lambda _: ast.DmlOption.LOW_PRIORITY
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IGNORE],
            action=lambda _: ast.DmlOption.IGNORE
        ),
    ]
)
