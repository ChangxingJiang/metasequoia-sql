"""
参数（param）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "PARAM_MARKER",
]

# 参数占位符
# 对应 MySQL 语义组：param_marker
PARAM_MARKER = ms_parser.create_group(
    name="param_marker",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.PARAM_MARKER],
            action=lambda _: ast.Param()
        )
    ]
)
