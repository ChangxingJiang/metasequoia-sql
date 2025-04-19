"""
标识符的语义组
"""

import metasequoia_parser as ms_parser

from metasequoia_sql_new import ast
from metasequoia_sql_new.terminal import SqlTerminalType as TType

GROUP_IDENT = ms_parser.create_group(
    name="ident",
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

GROUP_IDENT_2D = ms_parser.create_group(
    name="ident_2",
    rules=[
        ms_parser.create_rule(
            symbols=["ident", TType.OPERATOR_DOT, "ident"],
            action=lambda x: ast.Ident2D(value1=x[0], value2=x[2])
        ),
    ]
)

GROUP_IDENT_3D = ms_parser.create_group(
    name="ident_3",
    rules=[
        ms_parser.create_rule(
            symbols=["ident", TType.OPERATOR_DOT, "ident", TType.OPERATOR_DOT, "ident"],
            action=lambda x: ast.Ident3D(value1=x[0], value2=x[2], value3=x[4])
        ),
    ]
)

GROUP_SIMPLE_IDENT = ms_parser.create_group(
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

GROUP_SIMPLE_IDENT_LIST = ms_parser.create_group(
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
