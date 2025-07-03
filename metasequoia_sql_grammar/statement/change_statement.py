"""
CHANGE 语句（change statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CHANGE_STATEMENT",
    "CHANGE_REPLICATION_SOURCE",
]

# `CHANGE` 语句
CHANGE_STATEMENT = ms_parser.create_group(
    name="change_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHANGE, "change_replication_source", TType.KEYWORD_TO,
                     "source_def_list", "opt_for_channel"],
            action=lambda x: ast.ChangeReplicationSourceStatement(
                source_def_list=x[3],
                channel_list=x[4]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHANGE, TType.KEYWORD_REPLICATION, TType.KEYWORD_FILTER,
                     "filter_def_list", "opt_for_channel"],
            action=lambda x: ast.ChangeReplicationFilterStatement(
                filter_def_list=x[3],
                channel_list=x[4]
            )
        )
    ]
)

# `CHANGE` 复制源类型
CHANGE_REPLICATION_SOURCE = ms_parser.create_group(
    name="change_replication_source",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER],
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REPLICATION, TType.KEYWORD_SOURCE],
        )
    ]
)
