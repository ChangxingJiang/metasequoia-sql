"""
CREATE LOGFILE GROUP 语句（create logfile statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CREATE_LOGFILE_STATEMENT"
]

# `CREATE LOGFILE` 语句
CREATE_LOGFILE_STATEMENT = ms_parser.create_group(
    name="create_logfile_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CREATE, TType.KEYWORD_LOGFILE, TType.KEYWORD_GROUP, "ident", TType.KEYWORD_ADD,
                     "undofile", "opt_create_logfile_option_list"],
            action=lambda x: ast.CreateLogfileStatement(
                logfile_group_name=x[3].get_str_value(),
                undofile=x[5],
                options=x[6]
            )
        )
    ]
)
