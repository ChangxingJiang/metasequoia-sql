"""
ALTER RESOURCE GROUP 语句（alter resource group statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ALTER_RESOURCE_GROUP_STATEMENT",
]

# `ALTER RESOURCE GROUP` 语句
ALTER_RESOURCE_GROUP_STATEMENT = ms_parser.create_group(
    name="alter_resource_group_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_ALTER,  # 0
                TType.KEYWORD_RESOURCE,  # 1
                TType.KEYWORD_GROUP,  # 2
                "ident",  # 3
                "opt_resource_group_vcpu_list",  # 4
                "opt_thread_priority",  # 5
                "opt_enable_disable",  # 6
                "opt_keyword_force"  # 7
            ],
            action=lambda x: ast.AlterResourceGroupStatement(
                group_name=x[3].get_str_value(),
                vcpu_list=x[4],
                priority=x[5],
                enable_disable=x[6],
                force=x[7]
            )
        )
    ]
)
