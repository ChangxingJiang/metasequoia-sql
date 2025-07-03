"""
LOCKING 子句（locking clause）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal.terminal_type import SqlTerminalType as TType

__all__ = [
    "LOCKING_CLAUSE_LIST",
    "LOCKING_CLAUSE",
    "LOCK_STRENGTH",
    "OPT_LOCKED_ROW_ACTION",
]

# 锁指定子句的列表
LOCKING_CLAUSE_LIST = ms_parser.create_group(
    name="locking_clause_list",
    rules=[
        ms_parser.create_rule(
            symbols=["locking_clause_list", "locking_clause"],
            action=ms_parser.template.action.LIST_APPEND_1
        ),
        ms_parser.create_rule(
            symbols=["locking_clause"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 锁指定子句
LOCKING_CLAUSE = ms_parser.create_group(
    name="locking_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FOR, "lock_strength", "opt_locked_row_action"],
            action=lambda x: ast.LockingClause(lock_strength=x[1], table_list=[], locked_row_action=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FOR, "lock_strength", TType.KEYWORD_ON, "table_ident_opt_wild_list",
                     "opt_locked_row_action"],
            action=lambda x: ast.LockingClause(lock_strength=x[1], table_list=x[3], locked_row_action=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOCK, TType.KEYWORD_IN, TType.KEYWORD_SHARE, TType.KEYWORD_MODE],
            action=lambda _: ast.LockingClause(lock_strength=ast.LockStrength.SHARE, table_list=[],
                                               locked_row_action=ast.LockedRowAction.WAIT)
        )
    ]
)

# 指定锁类型的关键字（`UPDATE` 或 `SHARE`）
LOCK_STRENGTH = ms_parser.create_group(
    name="lock_strength",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UPDATE],
            action=lambda _: ast.LockStrength.UPDATE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHARE],
            action=lambda _: ast.LockStrength.SHARE
        )
    ]
)

# 可选的指定锁行为的关键字（`SKIP LOCKED` 或 `NOWAIT`）
OPT_LOCKED_ROW_ACTION = ms_parser.create_group(
    name="opt_locked_row_action",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SKIP, TType.KEYWORD_LOCKED],
            action=lambda _: ast.LockedRowAction.SKIP_LOCKED
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NOWAIT],
            action=lambda _: ast.LockedRowAction.NOWAIT
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.LockedRowAction.WAIT
        )
    ]
)
