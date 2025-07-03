"""
CREATE UNDO TABLESPACE 语句（create undo tablespace statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CREATE_UNDO_TABLESPACE_STATEMENT"
]

# `CREATE UNDO TABLESPACE` 语句
CREATE_UNDO_TABLESPACE_STATEMENT = ms_parser.create_group(
    name="create_undo_tablespace_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CREATE, TType.KEYWORD_UNDO, TType.KEYWORD_TABLESPACE, "ident", TType.KEYWORD_ADD,
                     "datafile", "opt_drop_undo_tablespace_option_list"],
            action=lambda x: ast.CreateUndoTablespaceStatement(
                tablespace_name=x[3].get_str_value(),
                datafile=x[5],
                options=x[6]
            )
        )
    ]
)
