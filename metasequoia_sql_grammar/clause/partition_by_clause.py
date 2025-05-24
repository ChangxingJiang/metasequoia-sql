"""
PARTITION BY 子句
"""

import metasequoia_parser as ms_parser

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_PARTITION_CLAUSE"
]

# 可选的 PARTITION BY 子句
# 对应 MySQL 语义组：opt_partition_clause
OPT_PARTITION_CLAUSE = ms_parser.create_group(
    name="opt_partition_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PARTITION, TType.KEYWORD_BY, "expr_list"],
            action=lambda x: x[2]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)
