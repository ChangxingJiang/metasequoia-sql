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

    # TABLESPACE 选项列表
    "OPT_DROP_TABLESPACE_OPTION_LIST",
    "DROP_TABLESPACE_OPTION_LIST",
    "DROP_TABLESPACE_OPTION",

    # UNDO TABLESPACE 选项列表
    "OPT_DROP_UNDO_TABLESPACE_OPTION_LIST",
    "DROP_UNDO_TABLESPACE_OPTION_LIST",
    "DROP_UNDO_TABLESPACE_OPTION",

    # ALTER TABLESPACE 选项
    "ALTER_OPTION_ENGINE",
    "ALTER_OPTION_WAIT",
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

# 可选的 `DROP TABLESPACE` 和 `DROP LOGFILE` 的选项的列表
OPT_DROP_TABLESPACE_OPTION_LIST = ms_parser.create_group(
    name="opt_drop_tablespace_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["drop_tablespace_option_list"]
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)

# `DROP TABLESPACE` 和 `DROP LOGFILE` 的选项的列表
DROP_TABLESPACE_OPTION_LIST = ms_parser.create_group(
    name="drop_tablespace_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["drop_tablespace_option_list", "opt_comma", "drop_tablespace_option"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["drop_tablespace_option"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# `DROP TABLESPACE` 和 `DROP LOGFILE` 的选项
DROP_TABLESPACE_OPTION = ms_parser.create_group(
    name="drop_tablespace_option",
    rules=[
        ms_parser.create_rule(
            symbols=["alter_option_engine"]
        ),
        ms_parser.create_rule(
            symbols=["alter_option_wait"]
        )
    ]
)

# 可选的 `UNDO TABLESPACE` 的选项的列表
OPT_DROP_UNDO_TABLESPACE_OPTION_LIST = ms_parser.create_group(
    name="opt_drop_undo_tablespace_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["drop_undo_tablespace_option_list"]
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)

# `UNDO TABLESPACE` 的选项的列表
DROP_UNDO_TABLESPACE_OPTION_LIST = ms_parser.create_group(
    name="drop_undo_tablespace_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["drop_undo_tablespace_option_list", "opt_comma", "drop_undo_tablespace_option"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["drop_undo_tablespace_option"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# `UNDO TABLESPACE` 的选项
DROP_UNDO_TABLESPACE_OPTION = ms_parser.create_group(
    name="drop_undo_tablespace_option",
    rules=[
        ms_parser.create_rule(
            symbols=["alter_option_engine"]
        )
    ]
)

# ALTER 选项：ENGINE
ALTER_OPTION_ENGINE = ms_parser.create_group(
    name="alter_option_engine",
    rules=[
        ms_parser.create_rule(
            symbols=["opt_keyword_storage", TType.KEYWORD_ENGINE, "opt_equal", "ident_or_text"],
            action=lambda x: ast.AlterOptionEngine(value=x[3].get_str_value())
        )
    ]
)

# ALTER 选项：`WAIT` 或 `NO_WAIT`
ALTER_OPTION_WAIT = ms_parser.create_group(
    name="alter_option_wait",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WAIT],
            action=lambda _: ast.AlterOptionWait(value=True)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NO_WAIT],
            action=lambda _: ast.AlterOptionWait(value=False)
        )
    ]
)
