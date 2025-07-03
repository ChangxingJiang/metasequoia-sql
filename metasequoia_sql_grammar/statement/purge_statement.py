"""
PURGE 语句（purge statement）
"""

import metasequoia_parser as ms_parser
from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "PURGE_STATEMENT",
    "PURGE_OPTION",
]

# `PURGE` 语句
PURGE_STATEMENT = ms_parser.create_group(
    name="purge_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_PURGE,
                "keyword_master_or_binary",
                TType.KEYWORD_LOGS,
                "purge_option"
            ],
            action=lambda x: ast.PurgeStatement(purge_option=x[3])
        )
    ]
)

# `PURGE` 选项
PURGE_OPTION = ms_parser.create_group(
    name="purge_option",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TO, "text_literal_sys"],
            action=lambda x: ast.PurgeToOption(log_file=x[1].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BEFORE, "expr"],
            action=lambda x: ast.PurgeBeforeOption(before_expression=x[1])
        )
    ]
)
