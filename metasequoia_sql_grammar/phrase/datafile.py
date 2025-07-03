"""
表空间数据文件（datafile）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "DATAFILE",
]

# 表空间数据文件名称
DATAFILE = ms_parser.create_group(
    name="datafile",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DATAFILE, "text_literal_sys"],
            action=lambda x: x[1].get_str_value()
        )
    ]
)
