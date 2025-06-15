"""
CREATE ROLE 语句（create role statement）
"""

import metasequoia_parser as ms_parser
from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CREATE_ROLE_STATEMENT",
]

# `CREATE ROLE` 语句
CREATE_ROLE_STATEMENT = ms_parser.create_group(
    name="create_role_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CREATE,
                TType.KEYWORD_ROLE,
                "opt_keyword_if_not_exists",
                "role_name_list"
            ],
            action=lambda x: ast.CreateRoleStatement(
                if_not_exists=x[2],
                role_list=x[3]
            )
        )
    ]
)
