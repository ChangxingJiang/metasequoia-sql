"""
RESET 语句（reset statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "RESET_STATEMENT",
    "RESET_OPTIONS",
    "RESET_OPTION",
    "SOURCE_RESET_OPTIONS",
]

# `RESET` 语句
RESET_STATEMENT = ms_parser.create_group(
    name="reset_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RESET, "reset_options"],
            action=lambda x: ast.ResetOptionsStatement(options=x[1])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RESET, TType.KEYWORD_PERSIST],
            action=lambda x: ast.ResetPersistStatement(if_exists=False, identifier=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RESET, TType.KEYWORD_PERSIST, "opt_keyword_if_exists", "identifier_allow_default"],
            action=lambda x: ast.ResetPersistStatement(if_exists=x[2], identifier=x[3])
        )
    ]
)

# `RESET` 选项列表
RESET_OPTIONS = ms_parser.create_group(
    name="reset_options",
    rules=[
        ms_parser.create_rule(
            symbols=["reset_options", TType.OPERATOR_COMMA, "reset_option"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["reset_option"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# `RESET` 单个选项
RESET_OPTION = ms_parser.create_group(
    name="reset_option",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SLAVE, "opt_keyword_all", "opt_for_channel"],
            action=lambda x: ast.ResetSlaveOption(all_flag=x[1], channel_name=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REPLICA, "opt_keyword_all", "opt_for_channel"],
            action=lambda x: ast.ResetReplicaOption(all_flag=x[1], channel_name=x[2])
        ),
        ms_parser.create_rule(
            symbols=["keyword_master_or_binary_logs_and_gtids", "source_reset_options"],
            action=lambda x: ast.ResetMasterOption(binlog_file_number=x[1])
        )
    ]
)

# `SOURCE RESET` 选项
SOURCE_RESET_OPTIONS = ms_parser.create_group(
    name="source_reset_options",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: None
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TO, "int_literal_or_hex"],
            action=lambda x: x[1].value
        )
    ]
)
