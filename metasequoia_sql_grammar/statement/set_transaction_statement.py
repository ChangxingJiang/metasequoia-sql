"""
SET TRANSACTION 语句
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "SET_TRANSACTION_STATEMENT",
    "ISOLATION_LEVEL"
]

# `SET TRANSACTION` 语句
SET_TRANSACTION_STATEMENT = ms_parser.create_group(
    name="set_transaction_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_SET,  # 0
                "opt_set_option_type",  # 1
                TType.KEYWORD_TRANSACTION,  # 2
                "transaction_access_mode_type",  # 3
            ],
            action=lambda x: ast.SetTransactionStatement(
                set_option=x[1],
                transaction_access_mode=x[3],
                isolation_level=None
            )
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_SET,  # 0
                "opt_set_option_type",  # 1
                TType.KEYWORD_TRANSACTION,  # 2
                "transaction_access_mode_type",  # 3
                TType.OPERATOR_COMMA,  # 4
                "isolation_level"  # 5
            ],
            action=lambda x: ast.SetTransactionStatement(
                set_option=x[1],
                transaction_access_mode=x[3],
                isolation_level=x[5]
            )
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_SET,  # 0
                "opt_set_option_type",  # 1
                TType.KEYWORD_TRANSACTION,  # 2
                "isolation_level"  # 3
            ],
            action=lambda x: ast.SetTransactionStatement(
                set_option=x[1],
                transaction_access_mode=None,
                isolation_level=x[3]
            )
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_SET,  # 0
                "opt_set_option_type",  # 1
                TType.KEYWORD_TRANSACTION,  # 2
                "isolation_level",  # 3
                TType.OPERATOR_COMMA,  # 4
                "transaction_access_mode_type"  # 5
            ],
            action=lambda x: ast.SetTransactionStatement(
                set_option=x[1],
                transaction_access_mode=x[5],
                isolation_level=x[3]
            )
        )
    ]
)

# 指定隔离级别子句
ISOLATION_LEVEL = ms_parser.create_group(
    name="isolation_level",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ISOLATION, TType.KEYWORD_LEVEL, "isolation_type"],
            action=lambda x: x[2]
        )
    ]
)
