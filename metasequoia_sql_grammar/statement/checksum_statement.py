"""
CHECKSUM 语句（checksum statement）
"""

import metasequoia_parser as ms_parser
from metasequoia_sql import ast

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CHECKSUM_STATEMENT"
]

# `CHECKSUM` 语句
CHECKSUM_STATEMENT = ms_parser.create_group(
    name="checksum_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHECKSUM, "keyword_table_or_tables", "identifier_list", "opt_checksum_type"],
            action=lambda x: ast.ChecksumStatement(table_list=x[2], checksum_type=x[3])
        )
    ]
)
