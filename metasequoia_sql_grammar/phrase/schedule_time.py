"""
事件调度时间（schedule time）语法定义
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ON_SCHEDULE_TIME",
    "SCHEDULE_TIME",
    "OPT_SCHEDULE_STARTS",
    "OPT_SCHEDULE_ENDS",
]

# `ON SCHEDULE` 引导的事件调度时间
ON_SCHEDULE_TIME = ms_parser.create_group(
    name="on_schedule_time",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ON, TType.KEYWORD_SCHEDULE, "schedule_time"],
            action=lambda x: x[2]
        )
    ]
)

# 事件调度时间
SCHEDULE_TIME = ms_parser.create_group(
    name="schedule_time",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_EVERY,
                "expr",
                "interval_time_unit",
                "opt_schedule_starts",
                "opt_schedule_ends"
            ],
            action=lambda x: ast.ScheduleTimeEvery(
                interval_expression=x[1],
                interval_type=x[2],
                starts_expression=x[3],
                ends_expression=x[4]
            )
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_AT,
                "expr"
            ],
            action=lambda x: ast.ScheduleTimeAt(
                execute_at_expression=x[1]
            )
        )
    ]
)

# 可选的事件开始时间
OPT_SCHEDULE_STARTS = ms_parser.create_group(
    name="opt_schedule_starts",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STARTS, "expr"],
            action=lambda x: x[1]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的事件结束时间
OPT_SCHEDULE_ENDS = ms_parser.create_group(
    name="opt_schedule_ends",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ENDS, "expr"],
            action=lambda x: x[1]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)
