"""
ALTER EVENT 语句（alter event statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ALTER_EVENT_STATEMENT",
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
                "opt_on_schedule_time",
                "opt_event_completion_type",
                "opt_event_rename",
                "opt_event_status_type",
                "opt_event_comment",
                "opt_do_process_command"
            ],
            action=lambda x: ast.AlterEventStatement(
                definer=x[1],
                event_name=x[3],
                schedule_time=x[4],
                completion_type=x[5],
                event_rename=x[6],
                event_status=x[7],
                event_comment=x[8],
                process_command=x[9]
            )
        )
    ]
)
