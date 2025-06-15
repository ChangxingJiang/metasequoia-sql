"""
HELP 语句（help statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "HELP_STATEMENT"
]

# `HELP` 语句
HELP_STATEMENT = ms_parser.create_group(
    name="help_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_HELP, "ident_or_text"],
            action=lambda x: ast.HelpStatement(search_string=x[1].get_str_value())
        )
    ]
)
