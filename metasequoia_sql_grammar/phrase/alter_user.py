"""
修改用户信息命令（alter user）
"""

import metasequoia_parser as ms_parser
from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ALTER_USER_LIST",
    "ALTER_USER",
]

# `ALTER USER` 语义组的列表
ALTER_USER_LIST = ms_parser.create_group(
    name="alter_user_list",
    rules=[
        ms_parser.create_rule(
            symbols=["alter_user_list", TType.OPERATOR_COMMA, "alter_user"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["alter_user"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# `ALTER USER` 语义组
ALTER_USER = ms_parser.create_group(
    name="alter_user",
    rules=[
        # user identified_by_password REPLACE TEXT_STRING_password opt_retain_current_password
        ms_parser.create_rule(
            symbols=[
                "user_name",
                "identified_by_password",
                TType.KEYWORD_REPLACE,
                "text_literal_sys",
                "opt_keyword_retain_current_password"
            ],
            action=lambda x: ast.AlterUserIdentifiedByPasswordReplace(
                user=x[0],
                identification=x[1],
                current_password=x[3].get_str_value(),
                retain_current_password=x[4]
            )
        ),
        # user identified_with_plugin_by_password REPLACE TEXT_STRING_password opt_retain_current_password
        ms_parser.create_rule(
            symbols=[
                "user_name",
                "identified_with_plugin_by_password",
                TType.KEYWORD_REPLACE,
                "text_literal_sys",
                "opt_keyword_retain_current_password"
            ],
            action=lambda x: ast.AlterUserIdentifiedWithPluginByPasswordReplace(
                user=x[0],
                identification=x[1],
                current_password=x[3].get_str_value(),
                retain_current_password=x[4]
            )
        ),
        # user identified_by_password opt_retain_current_password
        ms_parser.create_rule(
            symbols=[
                "user_name",
                "identified_by_password",
                "opt_keyword_retain_current_password"
            ],
            action=lambda x: ast.AlterUserIdentifiedByPassword(
                user=x[0],
                identification=x[1],
                retain_current_password=x[2]
            )
        ),
        # user identified_by_random_password opt_retain_current_password
        ms_parser.create_rule(
            symbols=[
                "user_name",
                "identified_by_random_password",
                "opt_keyword_retain_current_password"
            ],
            action=lambda x: ast.AlterUserIdentifiedByRandomPassword(
                user=x[0],
                identification=x[1],
                retain_current_password=x[2]
            )
        ),
        # user identified_by_random_password REPLACE TEXT_STRING_password opt_retain_current_password
        ms_parser.create_rule(
            symbols=[
                "user_name",
                "identified_by_random_password",
                TType.KEYWORD_REPLACE,
                "text_literal_sys",
                "opt_keyword_retain_current_password"
            ],
            action=lambda x: ast.AlterUserIdentifiedByRandomPasswordReplace(
                user=x[0],
                identification=x[1],
                current_password=x[3].get_str_value(),
                retain_current_password=x[4]
            )
        ),
        # user identified_with_plugin
        ms_parser.create_rule(
            symbols=[
                "user_name",
                "identified_with_plugin"
            ],
            action=lambda x: ast.AlterUserIdentifiedWithPlugin(
                user=x[0],
                identification=x[1]
            )
        ),
        # user identified_with_plugin_as_auth opt_retain_current_password
        ms_parser.create_rule(
            symbols=[
                "user_name",
                "identified_with_plugin_as_auth",
                "opt_keyword_retain_current_password"
            ],
            action=lambda x: ast.AlterUserIdentifiedWithPluginAsAuth(
                user=x[0],
                identification=x[1],
                retain_current_password=x[2]
            )
        ),
        # user identified_with_plugin_by_password opt_retain_current_password
        ms_parser.create_rule(
            symbols=[
                "user_name",
                "identified_with_plugin_by_password",
                "opt_keyword_retain_current_password"
            ],
            action=lambda x: ast.AlterUserIdentifiedWithPluginByPassword(
                user=x[0],
                identification=x[1],
                retain_current_password=x[2]
            )
        ),
        # user identified_with_plugin_by_random_password opt_retain_current_password
        ms_parser.create_rule(
            symbols=[
                "user_name",
                "identified_with_plugin_by_random_password",
                "opt_keyword_retain_current_password"
            ],
            action=lambda x: ast.AlterUserIdentifiedWithPluginByRandomPassword(
                user=x[0],
                identification=x[1],
                retain_current_password=x[2]
            )
        ),
        # user opt_discard_old_password
        ms_parser.create_rule(
            symbols=[
                "user_name",
                "opt_keyword_discard_old_password"
            ],
            action=lambda x: ast.AlterUserDiscardOldPassword(
                user=x[0],
                discard_old_password=x[1]
            )
        ),
        # user ADD factor identification
        ms_parser.create_rule(
            symbols=[
                "user_name",
                TType.KEYWORD_ADD,
                TType.LITERAL_INT_NUM,
                TType.KEYWORD_FACTOR,
                "identification"
            ],
            action=lambda x: ast.AlterUserAddFactor(
                user=x[0],
                factor=int(x[2]),
                identification=x[4]
            )
        ),
        # user ADD factor identification ADD factor identification
        ms_parser.create_rule(
            symbols=[
                "user_name",
                TType.KEYWORD_ADD,
                TType.LITERAL_INT_NUM,
                TType.KEYWORD_FACTOR,
                "identification",
                TType.KEYWORD_ADD,
                TType.LITERAL_INT_NUM,
                TType.KEYWORD_FACTOR,
                "identification"
            ],
            action=lambda x: ast.AlterUserAddTwoFactors(
                user=x[0],
                first_factor=int(x[2]),
                first_identification=x[4],
                second_factor=int(x[6]),
                second_identification=x[8]
            )
        ),
        # user MODIFY factor identification
        ms_parser.create_rule(
            symbols=[
                "user_name",
                TType.KEYWORD_MODIFY,
                TType.LITERAL_INT_NUM,
                TType.KEYWORD_FACTOR,
                "identification"
            ],
            action=lambda x: ast.AlterUserModifyFactor(
                user=x[0],
                factor=int(x[2]),
                identification=x[4]
            )
        ),
        # user MODIFY factor identification MODIFY factor identification
        ms_parser.create_rule(
            symbols=[
                "user_name",
                TType.KEYWORD_MODIFY,
                TType.LITERAL_INT_NUM,
                TType.KEYWORD_FACTOR,
                "identification",
                TType.KEYWORD_MODIFY,
                TType.LITERAL_INT_NUM,
                TType.KEYWORD_FACTOR,
                "identification"
            ],
            action=lambda x: ast.AlterUserModifyTwoFactors(
                user=x[0],
                first_factor=int(x[2]),
                first_identification=x[4],
                second_factor=int(x[6]),
                second_identification=x[8]
            )
        ),
        # user DROP factor
        ms_parser.create_rule(
            symbols=[
                "user_name",
                TType.KEYWORD_DROP,
                TType.LITERAL_INT_NUM,
                TType.KEYWORD_FACTOR,
            ],
            action=lambda x: ast.AlterUserDropFactor(
                user=x[0],
                factor=int(x[2])
            )
        ),
        # user DROP factor DROP factor
        ms_parser.create_rule(
            symbols=[
                "user_name",
                TType.KEYWORD_DROP,
                TType.LITERAL_INT_NUM,
                TType.KEYWORD_FACTOR,
                TType.KEYWORD_DROP,
                TType.LITERAL_INT_NUM,
                TType.KEYWORD_FACTOR,
            ],
            action=lambda x: ast.AlterUserDropTwoFactors(
                user=x[0],
                first_factor=int(x[2]),
                second_factor=int(x[5])
            )
        )
    ]
)
