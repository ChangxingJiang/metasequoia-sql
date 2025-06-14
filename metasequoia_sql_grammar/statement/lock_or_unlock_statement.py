"""
LOCK/UNLOCK 语句（lock/unlock statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "LOCK_STATEMENT",
    "UNLOCK_STATEMENT",
    "TABLE_LOCK_LIST",
    "TABLE_LOCK",
]

# `LOCK` 语句
LOCK_STATEMENT = ms_parser.create_group(
    name="lock_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_LOCK,  # 0
                "keyword_table_or_tables",  # 1
                "table_lock_list"  # 2
            ],
            action=lambda x: ast.LockTablesStatement(table_lock_list=x[2])
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_LOCK,  # 0
                TType.KEYWORD_INSTANCE,  # 1
                TType.KEYWORD_FOR,  # 2
                TType.KEYWORD_BACKUP  # 3
            ],
            action=lambda _: ast.LockInstanceStatement()
        )
    ]
)

# `UNLOCK` 语句
UNLOCK_STATEMENT = ms_parser.create_group(
    name="unlock_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_UNLOCK,  # 0
                "keyword_table_or_tables"  # 1
            ],
            action=lambda _: ast.UnlockTablesStatement()
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_UNLOCK,  # 0
                TType.KEYWORD_INSTANCE  # 1
            ],
            action=lambda _: ast.UnlockInstanceStatement()
        )
    ]
)

# 单个表的锁定信息的列表
TABLE_LOCK_LIST = ms_parser.create_group(
    name="table_lock_list",
    rules=[
        ms_parser.create_rule(
            symbols=["table_lock"],
            action=lambda x: [x[0]]
        ),
        ms_parser.create_rule(
            symbols=["table_lock_list", TType.OPERATOR_COMMA, "table_lock"],
            action=lambda x: x[0] + [x[2]]
        )
    ]
)

# 单个表的锁定信息
TABLE_LOCK = ms_parser.create_group(
    name="table_lock",
    rules=[
        ms_parser.create_rule(
            symbols=[
                "identifier",  # 0
                "opt_table_alias",  # 1
                "lock_option_type"  # 2
            ],
            action=lambda x: ast.TableLock(table_name=x[0], alias=x[1], lock_option=x[2])
        )
    ]
)
