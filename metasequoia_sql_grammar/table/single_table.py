"""
单表（single table）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "SINGLE_TABLE_PARENS",
    "SINGLE_TABLE",
]

# 包含任意层嵌套括号的、通过表明标识符定义的单个表
SINGLE_TABLE_PARENS = ms_parser.create_group(
    name="single_table_parens",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "single_table_parens", TType.OPERATOR_RPAREN],
            action=lambda x: x[1]
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "single_table", TType.OPERATOR_RPAREN],
            action=lambda x: x[1]
        )
    ]
)

# 通过表名标识符定义的单个表
SINGLE_TABLE = ms_parser.create_group(
    name="single_table",
    rules=[
        ms_parser.create_rule(
            symbols=["identifier", "opt_partition_clause", "opt_table_alias", "opt_index_hint_list"],
            action=lambda x: ast.SingleTable(table_ident=x[0], use_partition=x[1], table_alias=x[2],
                                             index_hints_list=x[3])
        )
    ]
)
