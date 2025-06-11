"""
ALTER TABLE 语句（alter table statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_KEYWORD_NO_WRITE_TO_BINLOG"
]

# 可选的 `NO_WRITE_TO_BINLOG` 关键字或 `LOCAL` 关键字
OPT_KEYWORD_NO_WRITE_TO_BINLOG = ms_parser.create_group(
    name="opt_keyword_no_write_to_binlog",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NO_WRITE_TO_BINLOG],
            action=ms_parser.template.action.RETURN_TRUE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOCAL],
            action=ms_parser.template.action.RETURN_TRUE
        ),
        ms_parser.create_rule(
            symbols=[],
            action=ms_parser.template.action.RETURN_FALSE
        )
    ]
)
