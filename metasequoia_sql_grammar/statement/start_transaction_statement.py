"""
START TRANSACTION 语句（start transaction statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "START_TRANSACTION_STATEMENT",
    "OPT_START_TRANSACTION_OPTIONS_LIST",
    "START_TRANSACTION_OPTIONS_LIST",
    "START_TRANSACTION_OPTIONS"
]

# `START TRANSACTION` 语句
START_TRANSACTION_STATEMENT = ms_parser.create_group(
    name="start_transaction_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_START, TType.KEYWORD_TRANSACTION, "opt_start_transaction_options_list"],
            action=lambda x: ast.StartTransactionStatement(options=x[2])
        )
    ]
)

# 可选的事务选项的列表
OPT_START_TRANSACTION_OPTIONS_LIST = ms_parser.create_group(
    name="opt_start_transaction_options_list",
    rules=[
        ms_parser.create_rule(
            symbols=["start_transaction_options_list"],
            action=lambda x: x[0]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.StartTransactionOption.DEFAULT
        )
    ]
)

# 事务选项的列表
START_TRANSACTION_OPTIONS_LIST = ms_parser.create_group(
    name="start_transaction_options_list",
    rules=[
        ms_parser.create_rule(
            symbols=["start_transaction_options_list", TType.OPERATOR_COMMA, "start_transaction_options"],
            action=lambda x: x[0] | x[2]
        ),
        ms_parser.create_rule(
            symbols=["start_transaction_options"],
            action=lambda x: x[0]
        )
    ]
)

# 事务选项
START_TRANSACTION_OPTIONS = ms_parser.create_group(
    name="start_transaction_options",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITH, TType.KEYWORD_CONSISTENT, TType.KEYWORD_SNAPSHOT],
            action=lambda _: ast.StartTransactionOption.WITH_CONSISTENT_SNAPSHOT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_READ, TType.KEYWORD_ONLY],
            action=lambda _: ast.StartTransactionOption.READ_ONLY
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_READ, TType.KEYWORD_WRITE],
            action=lambda _: ast.StartTransactionOption.READ_WRITE
        )
    ]
)
