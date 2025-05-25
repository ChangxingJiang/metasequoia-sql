"""
PARTITION 子句（partition clause）

用于 DQL 语句中的表子句、`INSERT` 语句、`REPLACE` 语句、`DELETE` 语句和 `LOAD` 语句，指定使用的分区列表。
"""

import metasequoia_parser as ms_parser

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_PARTITION_CLAUSE",
    "PARTITION_CLAUSE",
]

# 可选的 PARTITION 子句
OPT_PARTITION_CLAUSE = ms_parser.create_group(
    name="opt_partition_clause",
    rules=[
        ms_parser.create_rule(
            symbols=["partition_clause"]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)

# PARTITION 子句
PARTITION_CLAUSE = ms_parser.create_group(
    name="partition_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PARTITION, TType.OPERATOR_LPAREN, "ident_list", TType.OPERATOR_RPAREN],
            action=lambda x: x[2]
        )
    ]
)
