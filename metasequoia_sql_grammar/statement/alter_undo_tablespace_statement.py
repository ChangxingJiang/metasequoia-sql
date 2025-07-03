"""
ALTER UNDO TABLESPACE 语句（alter undo tablespace statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ALTER_UNDO_TABLESPACE_STATEMENT",
]

# `ALTER UNDO TABLESPACE` 语句
ALTER_UNDO_TABLESPACE_STATEMENT = ms_parser.create_group(
    name="alter_undo_tablespace_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_ALTER,
                TType.KEYWORD_UNDO,
                TType.KEYWORD_TABLESPACE,
                "ident",
                TType.KEYWORD_SET,
                "undo_tablespace_state",
                "opt_drop_undo_tablespace_option_list"
            ],
            action=lambda x: ast.AlterUndoTablespaceStatement(
                tablespace_name=x[3].get_str_value(),
                state=x[5],
                option_list=x[6]
            )
        )
    ]
)
