"""
FLUSH 语句（flush statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "FLUSH_STATEMENT",
]

# `FLUSH` 语句
FLUSH_STATEMENT = ms_parser.create_group(
    name="flush_statement",
    rules=[
        # FLUSH [NO_WRITE_TO_BINLOG] TABLES [table_list] [WITH READ LOCK | FOR EXPORT]
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_FLUSH,
                "opt_keyword_no_write_to_binlog",
                "keyword_table_or_tables",
                "opt_identifier_list",
                "flush_lock_type"
            ],
            action=lambda x: ast.FlushTablesStatement(
                no_write_to_binlog=x[1],
                table_list=x[3],
                flush_lock_type=x[4]
            )
        ),
        # FLUSH [NO_WRITE_TO_BINLOG] flush_option_list
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_FLUSH,
                "opt_keyword_no_write_to_binlog",
                "flush_option_type_list"
            ],
            action=lambda x: ast.FlushOptionsStatement(
                no_write_to_binlog=x[1],
                flush_options=x[2]
            )
        )
    ]
)
