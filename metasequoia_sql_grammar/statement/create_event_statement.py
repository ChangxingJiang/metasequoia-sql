"""
CREATE EVENT 语句（create event statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CREATE_EVENT_STATEMENT",
]

# `CREATE EVENT` 语句
CREATE_EVENT_STATEMENT = ms_parser.create_group(
    name="create_event_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CREATE,  # 0
                "opt_definer_clause",  # 1
                TType.KEYWORD_EVENT,  # 2
                "opt_keyword_if_not_exists",  # 3
                "identifier",  # 4
                "on_schedule_time",  # 5
                "opt_event_completion_type",  # 6
                "opt_event_status_type",  # 7
                "opt_event_comment",  # 8
                TType.KEYWORD_DO,  # 9
                "process_command"  # 10
            ],
            action=lambda x: ast.CreateEventStatement(
                definer=x[1],
                if_not_exists=x[3],
                event_name=x[4],
                schedule_time=x[5],
                completion_type=x[6],
                event_status=x[7],
                event_comment=x[8],
                event_body=x[10]
            )
        )
    ]
)
