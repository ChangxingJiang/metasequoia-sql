"""
ALTER TABLE 语句（alter table statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ALTER_TABLE_STATEMENT"
]

ALTER_TABLE_STATEMENT = ms_parser.create_group(
    name="alter_table_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALTER, TType.KEYWORD_TABLE, "identifier", "opt_alter_table_actions"],
            action=lambda x: ast.AlterTableStatement(
                table_ident=x[2],
                command_list=x[3]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALTER, TType.KEYWORD_TABLE, "identifier", "standalone_alter_table_action"],
            action=lambda x: ast.AlterTableStatement(
                table_ident=x[2],
                command_list=x[3]
            )
        )
    ]
)
