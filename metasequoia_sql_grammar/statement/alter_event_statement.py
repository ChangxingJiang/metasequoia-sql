"""
ALTER EVENT 语句（alter event statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ALTER_EVENT_STATEMENT",
    "EVENT_ON_SCHEDULE_ON_COMPLETE",
]

# `ALTER EVENT` 语句
ALTER_EVENT_STATEMENT = ms_parser.create_group(
    name="alter_event_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_ALTER,
                "opt_definer_clause",
                TType.KEYWORD_EVENT,
                "identifier",
                "event_on_schedule_on_complete",
                "opt_event_rename",
                "opt_event_status_type",
                "opt_event_comment",
                "opt_do_process_command"
            ],
            action=lambda x: ast.AlterEventStatement(
                definer=x[1],
                event_name=x[3],
                schedule_time=x[4][0],
                completion_type=x[4][1],
                event_rename=x[5],
                event_status=x[6],
                event_comment=x[7],
                process_command=x[8]
            )
        )
    ]
)

# `ALTER EVENT` 语句中可选的事件调度时间子句和事件完成类型子句
EVENT_ON_SCHEDULE_ON_COMPLETE = ms_parser.create_group(
    name="event_on_schedule_on_complete",
    rules=[
        ms_parser.create_rule(
            symbols=["on_schedule_time", "opt_event_completion_type"],
            action=lambda x: (x[0], x[1])
        ),
        ms_parser.create_rule(
            symbols=["on_schedule_time"],
            action=lambda x: (x[0], None)
        ),
        ms_parser.create_rule(
            symbols=["opt_event_completion_type"],
            action=lambda x: (None, x[0])
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: (None, None)
        )
    ]
)
