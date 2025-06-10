"""
DDL 修改表选项（ddl alter option）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_ALTER_OPTION_LOCK_AND_ALGORITHM",
    "ALTER_OPTION_ALGORITHM",
    "ALTER_OPTION_LOCK"
]

# 可选的任意顺序的 `ALGORITHM` 和 `LOCK` 修改表选项子句
OPT_ALTER_OPTION_LOCK_AND_ALGORITHM = ms_parser.create_group(
    name="opt_alter_option_lock_and_algorithm",
    rules=[
        ms_parser.create_rule(
            symbols=["alter_option_algorithm", "alter_option_lock"],
            action=lambda x: ast.TempAlterOptionList(
                algorithm=x[0],
                lock=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=["alter_option_lock", "alter_option_algorithm"],
            action=lambda x: ast.TempAlterOptionList(
                algorithm=x[1],
                lock=x[0]
            )
        ),
        ms_parser.create_rule(
            symbols=["alter_option_algorithm"],
            action=lambda x: ast.TempAlterOptionList(
                algorithm=x[0],
                lock=None
            )
        ),
        ms_parser.create_rule(
            symbols=["alter_option_lock"],
            action=lambda x: ast.TempAlterOptionList(
                algorithm=None,
                lock=x[0]
            )
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.TempAlterOptionList(
                algorithm=None,
                lock=None
            )
        )
    ]
)

# DDL 修改表选项：`ALGORITHM`（创建索引时使用的算法或机制）
ALTER_OPTION_ALGORITHM = ms_parser.create_group(
    name="alter_option_algorithm",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALGORITHM, "opt_equal", TType.KEYWORD_DEFAULT],
            action=lambda _: ast.AlterAlgorithmOption(value="DEFAULT")
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALGORITHM, "opt_equal", "ident"],
            action=lambda x: ast.AlterAlgorithmOption(value=x[2].get_str_value().upper())
        )
    ]
)

# DDL 修改表选项：`LOCK`（指定创建索引时对表施加的锁类型）
ALTER_OPTION_LOCK = ms_parser.create_group(
    name="alter_option_lock",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOCK, "opt_equal", TType.KEYWORD_DEFAULT],
            action=lambda _: ast.AlterLockOption(value="DEFAULT")
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOCK, "opt_equal", "ident"],
            action=lambda x: ast.AlterLockOption(value=x[2].get_str_value().upper())
        )
    ]
)
