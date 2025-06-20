"""
ALTER USER 语句相关的语义组
"""

import metasequoia_parser as ms_parser
from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ALTER_USER_STATEMENT",
    "OPT_REPLACE_PASSWORD",
]

# `ALTER USER` 语句
ALTER_USER_STATEMENT = ms_parser.create_group(
    name="alter_user_statement",
    rules=[
        # alter_user_command alter_user_list require_clause connect_options opt_account_lock_password_expire_options opt_user_attribute
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_ALTER,
                TType.KEYWORD_USER,
                "opt_keyword_if_exists",
                "alter_user_list",
                "require_clause",
                "opt_connect_option_list",
                "opt_account_lock_expire_option_list",
                "opt_user_attribute"
            ],
            action=lambda x: ast.AlterUserStandardStatement(
                if_exists=x[2],
                user_list=x[3],
                require_clause=x[4],
                connect_options=x[5],
                account_lock_expire_options=x[6],
                user_attribute=x[7]
            )
        ),
        # alter_user_command user_func identified_by_random_password opt_replace_password opt_retain_current_password
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_ALTER,
                TType.KEYWORD_USER,
                "opt_keyword_if_exists",
                TType.KEYWORD_USER,
                TType.OPERATOR_LPAREN,
                TType.OPERATOR_RPAREN,
                "identified_by_random_password",
                "opt_replace_password",
                "opt_keyword_retain_current_password"
            ],
            action=lambda x: ast.AlterUserCurrentUserRandomPasswordStatement(
                if_exists=x[2],
                identification=x[6],
                replace_password=x[7],
                retain_current_password=x[8]
            )
        ),
        # alter_user_command user_func identified_by_password opt_replace_password opt_retain_current_password
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_ALTER,
                TType.KEYWORD_USER,
                "opt_keyword_if_exists",
                TType.KEYWORD_USER,
                TType.OPERATOR_LPAREN,
                TType.OPERATOR_RPAREN,
                "identified_by_password",
                "opt_replace_password",
                "opt_keyword_retain_current_password"
            ],
            action=lambda x: ast.AlterUserCurrentUserPasswordStatement(
                if_exists=x[2],
                identification=x[6],
                replace_password=x[7],
                retain_current_password=x[8]
            )
        ),
        # alter_user_command user_func DISCARD OLD PASSWORD
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_ALTER,
                TType.KEYWORD_USER,
                "opt_keyword_if_exists",
                TType.KEYWORD_USER,
                TType.OPERATOR_LPAREN,
                TType.OPERATOR_RPAREN,
                TType.KEYWORD_DISCARD,
                TType.KEYWORD_OLD,
                TType.KEYWORD_PASSWORD
            ],
            action=lambda x: ast.AlterUserCurrentUserDiscardPasswordStatement(
                if_exists=x[2]
            )
        ),
        # alter_user_command user DEFAULT ROLE ALL
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_ALTER,
                TType.KEYWORD_USER,
                "opt_keyword_if_exists",
                "user_name",
                TType.KEYWORD_DEFAULT,
                TType.KEYWORD_ROLE,
                TType.KEYWORD_ALL
            ],
            action=lambda x: ast.AlterUserDefaultRoleAllStatement(
                if_exists=x[2],
                user=x[3]
            )
        ),
        # alter_user_command user DEFAULT ROLE NONE
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_ALTER,
                TType.KEYWORD_USER,
                "opt_keyword_if_exists",
                "user_name",
                TType.KEYWORD_DEFAULT,
                TType.KEYWORD_ROLE,
                TType.KEYWORD_NONE
            ],
            action=lambda x: ast.AlterUserDefaultRoleNoneStatement(
                if_exists=x[2],
                user=x[3]
            )
        ),
        # alter_user_command user DEFAULT ROLE role_list
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_ALTER,
                TType.KEYWORD_USER,
                "opt_keyword_if_exists",
                "user_name",
                TType.KEYWORD_DEFAULT,
                TType.KEYWORD_ROLE,
                "role_name_list"
            ],
            action=lambda x: ast.AlterUserDefaultRoleListStatement(
                if_exists=x[2],
                user=x[3],
                role_list=x[6]
            )
        ),
        # alter_user_command user opt_user_registration
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_ALTER,
                TType.KEYWORD_USER,
                "opt_keyword_if_exists",
                "user_name",
                "user_registration"
            ],
            action=lambda x: ast.AlterUserRegistrationStatement(
                if_exists=x[2],
                user=x[3],
                user_registration=x[4]
            )
        ),
        # alter_user_command user_func opt_user_registration
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_ALTER,
                TType.KEYWORD_USER,
                "opt_keyword_if_exists",
                TType.KEYWORD_USER,
                TType.OPERATOR_LPAREN,
                TType.OPERATOR_RPAREN,
                "user_registration"
            ],
            action=lambda x: ast.AlterUserCurrentUserRegistrationStatement(
                if_exists=x[2],
                user_registration=x[6]
            )
        )
    ]
)

# 可选的替换密码
OPT_REPLACE_PASSWORD = ms_parser.create_group(
    name="opt_replace_password",
    rules=[
        # 空选项
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: None
        ),
        # REPLACE TEXT_STRING_password
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REPLACE, "text_literal_sys"],
            action=lambda x: x[1].get_str_value()
        )
    ]
) 