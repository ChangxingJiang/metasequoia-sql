"""
REPAIR TABLE 语句（repair table statement）
"""

import metasequoia_parser as ms_parser
from metasequoia_sql import ast

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "REPAIR_TABLE_STATEMENT"
]

# `REPAIR TABLE` 语句
REPAIR_TABLE_STATEMENT = ms_parser.create_group(
    name="repair_table_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REPAIR, "opt_keyword_no_write_to_binlog", "keyword_table_or_tables",
                     "identifier_list", "opt_repair_type_list"],
            action=lambda x: ast.RepairTableStatement(no_write_to_binlog=x[1], table_list=x[3], repair_type=x[4])
        )
    ]
)
