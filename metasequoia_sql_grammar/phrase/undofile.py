"""
日志文件撤销文件（undofile）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "UNDOFILE",
]

# 日志文件组的撤销文件
UNDOFILE = ms_parser.create_group(
    name="undofile",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UNDOFILE, "text_literal_sys"],
            action=lambda x: x[1].get_str_value()
        )
    ]
)
