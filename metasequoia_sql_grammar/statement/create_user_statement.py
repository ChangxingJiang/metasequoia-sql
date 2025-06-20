"""
CREATE USER 语句
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CREATE_USER_STATEMENT",
    "DEFAULT_ROLE_CLAUSE",
    "CREATE_USER_LIST",
    "CREATE_USER",
    "OPT_CREATE_USER_WITH_MFA",
    "INITIAL_AUTH",
]

# `CREATE USER` 语句
CREATE_USER_STATEMENT = ms_parser.create_group(
    name="create_user_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CREATE,  # 0
                TType.KEYWORD_USER,  # 1
                "opt_keyword_if_not_exists",  # 2
                "create_user_list",  # 3
                "default_role_clause",  # 4
                "require_clause",  # 5
                "opt_connect_option_list",  # 6
                "opt_account_lock_expire_option_list",  # 7
                "opt_user_attribute"  # 8
            ],
            action=lambda x: ast.CreateUserStatement(
                if_not_exists=x[2],
                user_list=x[3],
                default_role_clause=x[4],
                require_clause=x[5],
                connect_options=x[6],
                account_lock_expire_options=x[7],
                user_attribute=x[8]
            )
        )
    ]
)

# 默认角色子句
DEFAULT_ROLE_CLAUSE = ms_parser.create_group(
    name="default_role_clause",
    rules=[
        # 空选项
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: None
        ),
        # DEFAULT ROLE role_list
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DEFAULT, TType.KEYWORD_ROLE, "role_name_list"],
            action=lambda x: ast.DefaultRoleClause(x[2])
        )
    ]
)

# 创建用户的列表
CREATE_USER_LIST = ms_parser.create_group(
    name="create_user_list",
    rules=[
        ms_parser.create_rule(
            symbols=["create_user_list", TType.OPERATOR_COMMA, "create_user"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["create_user"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 创建用户
CREATE_USER = ms_parser.create_group(
    name="create_user",
    rules=[
        # user identification opt_create_user_with_mfa
        ms_parser.create_rule(
            symbols=["user_name", "identification", "opt_create_user_with_mfa"],
            action=lambda x: ast.CreateUser(
                user=x[0],
                first_identification=x[1],
                mfa_identifications=x[2]
            )
        ),
        # user identified_with_plugin opt_initial_auth
        ms_parser.create_rule(
            symbols=["user_name", "identified_with_plugin", "initial_auth"],
            action=lambda x: ast.CreateUser(
                user=x[0],
                initial_auth=x[2]
            )
        ),
        # user opt_create_user_with_mfa
        ms_parser.create_rule(
            symbols=["user_name", "opt_create_user_with_mfa"],
            action=lambda x: ast.CreateUser(
                user=x[0],
                mfa_identifications=x[1]
            )
        )
    ]
)

# 可选的多因子认证
OPT_CREATE_USER_WITH_MFA = ms_parser.create_group(
    name="opt_create_user_with_mfa",
    rules=[
        # 空选项
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: []
        ),
        # AND identification（第二因子）
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AND, "identification"],
            action=lambda x: [x[1]]
        ),
        # AND identification AND identification（第二、第三因子）
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AND, "identification", TType.KEYWORD_AND, "identification"],
            action=lambda x: [x[1], x[3]]
        )
    ]
)

# 初始认证
INITIAL_AUTH = ms_parser.create_group(
    name="initial_auth",
    rules=[
        # INITIAL AUTHENTICATION identified_by_random_password
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INITIAL, TType.KEYWORD_AUTHENTICATION, "identified_by_random_password"],
            action=lambda x: ast.InitialAuthRandom(x[2])
        ),
        # INITIAL AUTHENTICATION identified_with_plugin_as_auth
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INITIAL, TType.KEYWORD_AUTHENTICATION, "identified_with_plugin_as_auth"],
            action=lambda x: ast.InitialAuthPlugin(x[2])
        ),
        # INITIAL AUTHENTICATION identified_by_password
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INITIAL, TType.KEYWORD_AUTHENTICATION, "identified_by_password"],
            action=lambda x: ast.InitialAuthPassword(x[2])
        )
    ]
)
