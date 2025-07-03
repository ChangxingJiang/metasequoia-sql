"""
SQL状态（sqlstate）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "SQLSTATE"
]

# SQL 状态
SQLSTATE = ms_parser.create_group(
    name="sql_state",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SQLSTATE, "opt_keyword_value", "text_literal_sys"],
            action=lambda x: ast.SqlState(sqlstate_value=x[2].get_str_value())
        )
    ]
)
