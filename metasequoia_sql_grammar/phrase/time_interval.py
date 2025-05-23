"""
时间间隔（time interval）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql_new import ast
from metasequoia_sql_new.terminal import SqlTerminalType as TType

__all__ = [
    "TIME_INTERVAL"
]

TIME_INTERVAL = ms_parser.create_group(
    name="time_interval",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INTERVAL, "expr", "interval_time_unit"],
            action=lambda x: ast.TimeInterval(time_value=x[1], time_unit=x[2])
        )
    ]
)
