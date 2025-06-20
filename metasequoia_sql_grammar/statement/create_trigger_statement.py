"""
CREATE TRIGGER 语句（create trigger statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CREATE_TRIGGER_STATEMENT",
    "TRIGGER_FOLLOWS_PRECEDES_CLAUSE",
]

# `CREATE TRIGGER` 语句
CREATE_TRIGGER_STATEMENT = ms_parser.create_group(
    name="create_trigger_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CREATE,  # 0
                "opt_definer_clause",  # 1
                TType.KEYWORD_TRIGGER,  # 2
                "opt_keyword_if_not_exists",  # 3
                "identifier",  # 4
                "trigger_action_time_type",  # 5
                "trigger_event_type",  # 6
                TType.KEYWORD_ON,  # 7
                "identifier",  # 8
                TType.KEYWORD_FOR,  # 9
                TType.KEYWORD_EACH,  # 10
                TType.KEYWORD_ROW,  # 11
                "trigger_follows_precedes_clause",  # 12
                "process_command"  # 13
            ],
            action=lambda x: ast.CreateTriggerStatement(
                definer=x[1],
                if_not_exists=x[3],
                trigger_name=x[4],
                action_time=x[5],
                trigger_event=x[6],
                table_ident=x[8],
                follows_precedes_clause=x[12],
                trigger_body=x[13]
            )
        )
    ]
)

# 触发器的 `FOLLOWS` 或 `PRECEDES` 子句
TRIGGER_FOLLOWS_PRECEDES_CLAUSE = ms_parser.create_group(
    name="trigger_follows_precedes_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.TriggerFollowsPrecedesClause(
                ordering_clause=None,
                anchor_trigger_name=None
            )
        ),
        ms_parser.create_rule(
            symbols=["trigger_action_order_type", "ident_or_text"],
            action=lambda x: ast.TriggerFollowsPrecedesClause(
                ordering_clause=x[0],
                anchor_trigger_name=x[1].get_str_value()
            )
        )
    ]
)
