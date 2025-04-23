"""
标识符的语义组

ident_sys:
        IDENT
      | IDENT_QUOTED;

ident_2:
        ident '.' ident;

ident_3:
        ident '.' ident '.' ident;

simple_ident:
        ident
      | ident_2
      | ident_3;

simple_ident_list:
        simple_ident_list ',' simple_ident
      | simple_ident;
"""

import metasequoia_parser as ms_parser

from metasequoia_sql_new import ast
from metasequoia_sql_new.terminal import SqlTerminalType as TType

__all__ = [
    "GENERAL_IDENT_SYS",
    "GENERAL_IDENT_2",
    "GENERAL_IDENT_3",
    "GENERAL_SIMPLE_IDENT",
    "GENERAL_SIMPLE_IDENT_LIST"
]

# 不是保留字或非保留关键字的标识符
# 对应 MySQL 语义组：IDENT_sys
GENERAL_IDENT_SYS = ms_parser.create_group(
    name="ident_sys",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.IDENT],
            action=lambda x: ast.Ident(x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.IDENT_QUOTED],
            action=lambda x: ast.Ident(x[0])
        ),
    ]
)

# 点分隔的两个标识符（ident.ident）
# 对应 MySQL 语义组：simple_ident_q（部分）、table_ident（部分）
GENERAL_IDENT_2 = ms_parser.create_group(
    name="ident_2",
    rules=[
        ms_parser.create_rule(
            symbols=["ident", TType.OPERATOR_DOT, "ident"],
            action=lambda x: ast.Ident2D(value1=x[0], value2=x[2])
        ),
    ]
)

# 点分隔的三个标识符（ident.ident.ident）
# 对应 MySQL 语义组：simple_ident_q（部分）
GENERAL_IDENT_3 = ms_parser.create_group(
    name="ident_3",
    rules=[
        ms_parser.create_rule(
            symbols=["ident", TType.OPERATOR_DOT, "ident", TType.OPERATOR_DOT, "ident"],
            action=lambda x: ast.Ident3D(value1=x[0], value2=x[2], value3=x[4])
        ),
    ]
)

# 通用通配符（ident 或 ident.ident 或 ident.ident.ident）
# 对应 MySQL 语义组：simple_ident
GENERAL_SIMPLE_IDENT = ms_parser.create_group(
    name="simple_ident",
    rules=[
        ms_parser.create_rule(
            symbols=["ident"]
        ),
        ms_parser.create_rule(
            symbols=["ident_2"]
        ),
        ms_parser.create_rule(
            symbols=["ident_3"]
        )
    ]
)

# 逗号分隔的通用通配符的列表
# 对应 MySQL 语义组：
GENERAL_SIMPLE_IDENT_LIST = ms_parser.create_group(
    name="simple_ident_list",
    rules=[
        ms_parser.create_rule(
            symbols=["simple_ident_list", TType.OPERATOR_COMMA, "simple_ident"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["simple_ident"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)
