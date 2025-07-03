"""
IMPORT TABLE 语句（import table statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "IMPORT_TABLE_STATEMENT",
]

# `IMPORT TABLE` 语句
IMPORT_TABLE_STATEMENT = ms_parser.create_group(
    name="import_table_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_IMPORT,  # 0
                TType.KEYWORD_TABLE,  # 1
                TType.KEYWORD_FROM,  # 2
                "text_literal_sys_list"  # 3
            ],
            action=lambda x: ast.ImportTableStatement(file_list=x[3])
        )
    ]
)
