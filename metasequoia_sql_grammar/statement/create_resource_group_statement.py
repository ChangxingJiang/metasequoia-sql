"""
CREATE RESOURCE GROUP 语句（create resource group statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CREATE_RESOURCE_GROUP_STATEMENT",
]

# `CREATE RESOURCE GROUP` 语句
CREATE_RESOURCE_GROUP_STATEMENT = ms_parser.create_group(
    name="create_resource_group_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CREATE,  # 0
                TType.KEYWORD_RESOURCE,  # 1
                TType.KEYWORD_GROUP,  # 2
                "ident",  # 3
                TType.KEYWORD_TYPE,  # 4
                "opt_equal",  # 5
                "resource_group_type",  # 6
                "opt_resource_group_vcpu_list",  # 7
                "opt_thread_priority",  # 8
                "opt_enable_disable"  # 9
            ],
            action=lambda x: ast.CreateResourceGroupStatement(
                group_name=x[3].get_str_value(),
                resource_group_type=x[6],
                vcpu_list=x[7],
                priority=x[8],
                enable_disable=x[9]
            )
        )
    ]
)
