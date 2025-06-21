"""
START REPLICA 语句（start replica statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "REPLICA_UNTIL",
    "REPLICA_UNTIL_ITEM",
]

# 可选的 `UNTIL` 关键字引导的数据源信息的列表
OPT_REPLICA_UNTIL = ms_parser.create_group(
    name="opt_replica_until",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UNTIL, "replica_until"],
            action=lambda x: x[1]
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)

# 复制源信息的列表
REPLICA_UNTIL = ms_parser.create_group(
    name="replica_until",
    rules=[
        ms_parser.create_rule(
            symbols=["replica_until", TType.OPERATOR_COMMA, "replica_until_item"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["replica_until_item"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 复制源信息
REPLICA_UNTIL_ITEM = ms_parser.create_group(
    name="replica_until_item",
    rules=[
        ms_parser.create_rule(
            symbols=["source_file_def"]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SQL_BEFORE_GTIDS, TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.SqlBeforeGtids(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SQL_AFTER_GTIDS, TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.SqlAfterGtids(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SQL_AFTER_MTS_GAPS],
            action=lambda x: ast.SqlAfterMtsGaps()
        )
    ]
)
