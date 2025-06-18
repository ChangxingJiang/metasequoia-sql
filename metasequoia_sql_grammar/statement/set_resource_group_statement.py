"""
SET RESOURCE GROUP 语句（set resource group statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "SET_RESOURCE_GROUP_STATEMENT",
    "THREAD_ID_LIST",
]

# `SET RESOURCE GROUP` 语句
SET_RESOURCE_GROUP_STATEMENT = ms_parser.create_group(
    name="set_resource_group_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SET, TType.KEYWORD_RESOURCE, TType.KEYWORD_GROUP, "ident"],
            action=lambda x: ast.SetResourceGroupStatement(
                resource_group_name=x[3].get_str_value(),
                thread_id_list=None
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SET, TType.KEYWORD_RESOURCE, TType.KEYWORD_GROUP, "ident",
                     TType.KEYWORD_FOR, "thread_id_list"],
            action=lambda x: ast.SetResourceGroupStatement(
                resource_group_name=x[3].get_str_value(),
                thread_id_list=x[5]
            )
        )
    ]
)

# 线程 ID 列表
THREAD_ID_LIST = ms_parser.create_group(
    name="thread_id_list",
    rules=[
        ms_parser.create_rule(
            symbols=["int_literal_or_hex"],
            action=lambda x: [x[0].value]
        ),
        ms_parser.create_rule(
            symbols=["thread_id_list", "opt_comma", "int_literal_or_hex"],
            action=lambda x: x[0] + [x[2].value]
        )
    ]
)
