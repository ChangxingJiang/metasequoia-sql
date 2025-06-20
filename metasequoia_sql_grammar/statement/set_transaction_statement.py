"""
SET TRANSACTION 语句
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ISOLATION_LEVEL"
]

# 隔离级别
ISOLATION_LEVEL = ms_parser.create_group(
    name="isolation_level",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ISOLATION, TType.KEYWORD_LEVEL, "isolation_type"],
            action=lambda x: x[2]
        )
    ]
)
