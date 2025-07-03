"""
KILL 语句（kill statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "KILL_STATEMENT",
]

# `KILL` 语句
KILL_STATEMENT = ms_parser.create_group(
    name="kill_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_KILL,  # 0
                "kill_option_type",  # 1
                "expr"  # 2
            ],
            action=lambda x: ast.KillStatement(option_type=x[1], target_id=x[2])
        )
    ]
)
