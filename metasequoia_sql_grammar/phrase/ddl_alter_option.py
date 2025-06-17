"""
DDL 修改表选项（ddl alter option）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ALTER_COMMAND_MODIFIER_LIST",
    "ALTER_COMMAND_MODIFIER",
    "OPT_ALTER_OPTION_LOCK_AND_ALGORITHM",
    "ALTER_OPTION_ALGORITHM",
    "ALTER_OPTION_LOCK",
    "OPT_ALTER_OPTION_WITH_VALIDATION",
    "ALTER_OPTION_WITH_VALIDATION",
]

# `ALTER` 命令的修饰选项的列表
ALTER_COMMAND_MODIFIER_LIST = ms_parser.create_group(
    name="alter_command_modifier_list",
    rules=[
        ms_parser.create_rule(
            symbols=["alter_command_modifier_list", TType.OPERATOR_COMMA, "alter_command_modifier"],
            action=lambda x: x[0].merge(x[2])
        ),
        ms_parser.create_rule(
            symbols=["alter_command_modifier"],
            action=lambda x: x[0]
        )
    ]
)

# `ALTER` 命令的修饰选项
ALTER_COMMAND_MODIFIER = ms_parser.create_group(
    name="alter_command_modifier",
    rules=[
        ms_parser.create_rule(
            symbols=["alter_option_algorithm"],
            action=lambda x: ast.TempAlterOptionList(
                algorithm=x[0]
            )
        ),
        ms_parser.create_rule(
            symbols=["alter_option_lock"],
            action=lambda x: ast.TempAlterOptionList(
                lock=x[0]
            )
        ),
        ms_parser.create_rule(
            symbols=["alter_option_with_validation"],
            action=lambda x: ast.TempAlterOptionList(
                validation=x[0]
            )
        )
    ]
)

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
                algorithm=x[0]
            )
        ),
        ms_parser.create_rule(
            symbols=["alter_option_lock"],
            action=lambda x: ast.TempAlterOptionList(
                algorithm=None
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
            action=lambda _: ast.AlterOptionAlgorithm(value="DEFAULT")
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALGORITHM, "opt_equal", "ident"],
            action=lambda x: ast.AlterOptionAlgorithm(value=x[2].get_str_value().upper())
        )
    ]
)

# DDL 修改表选项：`LOCK`（指定创建索引时对表施加的锁类型）
ALTER_OPTION_LOCK = ms_parser.create_group(
    name="alter_option_lock",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOCK, "opt_equal", TType.KEYWORD_DEFAULT],
            action=lambda _: ast.AlterOptionLock(value="DEFAULT")
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOCK, "opt_equal", "ident"],
            action=lambda x: ast.AlterOptionLock(value=x[2].get_str_value().upper())
        )
    ]
)

# 可选的 DDL 修改表选项：`WITH VALIDATION` 或 `WITHOUT VALIDATION`
OPT_ALTER_OPTION_WITH_VALIDATION = ms_parser.create_group(
    name="opt_alter_option_with_validation",
    rules=[
        ms_parser.create_rule(
            symbols=["alter_option_with_validation"]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.AlterOptionWithValidation(value=None)
        )
    ]
)

# DDL 修改表选项：`WITH VALIDATION` 或 `WITHOUT VALIDATION`
ALTER_OPTION_WITH_VALIDATION = ms_parser.create_group(
    name="alter_option_with_validation",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITH, TType.KEYWORD_VALIDATION],
            action=lambda _: ast.AlterOptionWithValidation(value=True)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITHOUT, TType.KEYWORD_VALIDATION],
            action=lambda _: ast.AlterOptionWithValidation(value=False)
        )
    ]
)
