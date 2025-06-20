"""
STOP REPLICA 语句（stop replica statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "STOP_REPLICA_STATEMENT",
]

# `STOP REPLICA` 语句
STOP_REPLICA_STATEMENT = ms_parser.create_group(
    name="stop_replica_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STOP, "keyword_replica_or_slave", "opt_replica_thread_type_list", "opt_for_channel"],
            action=lambda x: ast.StopReplicaStatement(thread_type=x[2], channel_name=x[3])
        )
    ]
)
