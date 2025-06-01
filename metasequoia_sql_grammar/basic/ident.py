"""
标识符（ident）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "IDENT_SYS",
    "IDENT_2",
    "IDENT_3",
    "SIMPLE_IDENT",
    "SIMPLE_IDENT_LIST",
    "IDENT_LIST",
    "OPT_IDENT",
]

# 不是保留字或非保留关键字的标识符
IDENT_SYS = ms_parser.create_group(
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

# 点分隔的两个标识符（`ident.ident`）
IDENT_2 = ms_parser.create_group(
    name="ident_2",
    rules=[
        ms_parser.create_rule(
            symbols=["ident", TType.OPERATOR_DOT, "ident"],
            action=lambda x: ast.Ident2D(value1=x[0].get_str_value(), value2=x[2].get_str_value())
        ),
    ]
)

# 点分隔的三个标识符（`ident.ident.ident`）
IDENT_3 = ms_parser.create_group(
    name="ident_3",
    rules=[
        ms_parser.create_rule(
            symbols=["ident", TType.OPERATOR_DOT, "ident", TType.OPERATOR_DOT, "ident"],
            action=lambda x: ast.Ident3D(value1=x[0].get_str_value(), value2=x[2].get_str_value(),
                                         value3=x[4].get_str_value())
        ),
    ]
)

# 表标识符（`ident` 或 `ident.ident`）
TABLE_IDENT = ms_parser.create_group(
    name="table_ident",
    rules=[
        ms_parser.create_rule(
            symbols=["ident"],
            action=lambda x: ast.TableIdent(schema_name=None, table_name=x[0].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=["ident_2"],
            action=lambda x: ast.TableIdent(schema_name=x[0].value1, table_name=x[0].value2)
        )
    ]
)

# 通用标识符（`ident` 或 `ident.ident` 或 `ident.ident.ident`）
SIMPLE_IDENT = ms_parser.create_group(
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
SIMPLE_IDENT_LIST = ms_parser.create_group(
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

# 一般场景标识符的列表
IDENT_LIST = ms_parser.create_group(
    name="ident_list",
    rules=[
        ms_parser.create_rule(
            symbols=["ident_list", TType.OPERATOR_COMMA, "ident"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["ident"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 可选的单个标识符
OPT_IDENT = ms_parser.create_group(
    name="opt_ident",
    rules=[
        ms_parser.create_rule(
            symbols=["ident"]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)
