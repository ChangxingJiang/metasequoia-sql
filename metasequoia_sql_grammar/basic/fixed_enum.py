"""
固定的枚举类型（fixed enum）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_DROP_RESTRICT",
    "OPT_SHOW_COMMAND_TYPE",
    "OPT_REPAIR_TYPE_LIST",
    "REPAIR_TYPE_LIST",
    "REPAIR_TYPE",
]

# 可选的 `DROP` 语句中 `RESTRICT` 选项的枚举值
OPT_DROP_RESTRICT = ms_parser.create_group(
    name="opt_drop_restrict",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.EnumDropRestrict.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RESTRICT],
            action=lambda x: ast.EnumDropRestrict.RESTRICT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CASCADE],
            action=lambda x: ast.EnumDropRestrict.CASCADE
        )
    ]
)

# 可选的 `SHOW` 语句命令类型的枚举值
OPT_SHOW_COMMAND_TYPE = ms_parser.create_group(
    name="opt_show_command_type",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.EnumShowCommandType.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FULL],
            action=lambda x: ast.EnumShowCommandType.FULL
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXTENDED],
            action=lambda x: ast.EnumShowCommandType.EXTENDED
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXTENDED, TType.KEYWORD_FULL],
            action=lambda x: ast.EnumShowCommandType.EXTENDED_FULL
        )
    ]
)

# 可选的 `REPAIR` 语句命令类型的枚举值的列表
OPT_REPAIR_TYPE_LIST = ms_parser.create_group(
    name="opt_repair_type_list",
    rules=[
        ms_parser.create_rule(
            symbols=["repair_type_list"]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.EnumRepairType.DEFAULT
        )
    ]
)

# `REPAIR` 语句命令类型的枚举值的列表
REPAIR_TYPE_LIST = ms_parser.create_group(
    name="repair_type_list",
    rules=[
        ms_parser.create_rule(
            symbols=["repair_type_list", "repair_type"],
            action=lambda x: x[0] | x[1]
        ),
        ms_parser.create_rule(
            symbols=["repair_type"],
            action=lambda x: x[0]
        )
    ]
)

# `REPAIR` 语句命令类型的枚举值
REPAIR_TYPE = ms_parser.create_group(
    name="repair_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_QUICK],
            action=lambda x: ast.EnumRepairType.QUICK
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXTENDED],
            action=lambda x: ast.EnumRepairType.EXTENDED
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_USE],
            action=lambda x: ast.EnumRepairType.USE
        )
    ]
)
