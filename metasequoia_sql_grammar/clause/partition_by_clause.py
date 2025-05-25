"""
PARTITION BY 子句（partition by clause）

用于窗口函数中的 `OVER` 子句，指定窗口分区规则。
"""

import metasequoia_parser as ms_parser

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_PARTITION_BY_CLAUSE"
]

# 可选的 PARTITION BY 子句
OPT_PARTITION_BY_CLAUSE = ms_parser.create_group(
    name="opt_partition_by_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PARTITION, TType.KEYWORD_BY, "expr_list"],
            action=lambda x: x[2]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)
