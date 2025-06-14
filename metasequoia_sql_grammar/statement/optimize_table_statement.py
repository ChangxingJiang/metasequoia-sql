"""
OPTIMIZE TABLE 语句（optimize table statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPTIMIZE_TABLE_STATEMENT",
]

# `OPTIMIZE TABLE` 语句
OPTIMIZE_TABLE_STATEMENT = ms_parser.create_group(
    name="optimize_table_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_OPTIMIZE,  # 0
                "opt_keyword_no_write_to_binlog",  # 1
                "keyword_table_or_tables",  # 2
                "identifier_list",  # 3
            ],
            action=lambda x: ast.OptimizeTableStatement(
                no_write_to_binlog=x[1],
                table_list=x[3]
            )
        )
    ]
)
