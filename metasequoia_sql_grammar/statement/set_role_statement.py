"""
SET ROLE 语句（set role statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "SET_ROLE_STATEMENT",
]

# `SET ROLE` 语句
SET_ROLE_STATEMENT = ms_parser.create_group(
    name="set_role_statement",
    rules=[
        # SET ROLE role_list
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SET, TType.KEYWORD_ROLE, "role_name_list"],
            action=lambda x: ast.SetRoleListStatement(role_list=x[2])
        ),
        # SET ROLE NONE
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SET, TType.KEYWORD_ROLE, TType.KEYWORD_NONE],
            action=lambda x: ast.SetRoleNoneStatement()
        ),
        # SET ROLE DEFAULT
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SET, TType.KEYWORD_ROLE, TType.KEYWORD_DEFAULT],
            action=lambda x: ast.SetRoleDefaultStatement()
        ),
        # SET DEFAULT ROLE role_list TO role_list
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SET, TType.KEYWORD_DEFAULT, TType.KEYWORD_ROLE, "role_name_list",
                     TType.KEYWORD_TO, "user_name_list"],
            action=lambda x: ast.SetDefaultRoleStatement(role_list=x[3], user_list=x[5])
        ),
        # SET DEFAULT ROLE NONE TO role_list
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SET, TType.KEYWORD_DEFAULT, TType.KEYWORD_ROLE, TType.KEYWORD_NONE,
                     TType.KEYWORD_TO, "user_name_list"],
            action=lambda x: ast.SetDefaultRoleNoneStatement(user_list=x[5])
        ),
        # SET DEFAULT ROLE ALL TO role_list
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SET, TType.KEYWORD_DEFAULT, TType.KEYWORD_ROLE, TType.KEYWORD_ALL,
                     TType.KEYWORD_TO, "user_name_list"],
            action=lambda x: ast.SetDefaultRoleAllStatement(user_list=x[5])
        ),
        # SET ROLE ALL opt_except_role_list (合并 opt_except_role_list 到这里)
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SET, TType.KEYWORD_ROLE, TType.KEYWORD_ALL],
            action=lambda x: ast.SetRoleAllStatement(except_role_list=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SET, TType.KEYWORD_ROLE, TType.KEYWORD_ALL, TType.KEYWORD_EXCEPT, "role_name_list"],
            action=lambda x: ast.SetRoleAllStatement(except_role_list=x[4])
        )
    ]
)
