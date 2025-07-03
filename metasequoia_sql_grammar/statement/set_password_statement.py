"""
SET PASSWORD 语句（set password statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "SET_PASSWORD_STATEMENT",
]

# `SET PASSWORD` 语句
SET_PASSWORD_STATEMENT = ms_parser.create_group(
    name="set_password_statement",
    rules=[
        # SET PASSWORD = 'password' [REPLACE 'current_password'] [RETAIN CURRENT PASSWORD]
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_SET,
                TType.KEYWORD_PASSWORD,
                "equal",
                "text_literal_sys",
                "opt_replace_password",
                "opt_keyword_retain_current_password"
            ],
            action=lambda x: ast.SetPasswordCurrentUserStatement(
                password=x[3].get_str_value(),
                replace_password=x[4],
                retain_current_password=x[5]
            )
        ),
        # SET PASSWORD TO RANDOM [REPLACE 'current_password'] [RETAIN CURRENT PASSWORD]
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_SET,
                TType.KEYWORD_PASSWORD,
                TType.KEYWORD_TO,
                TType.KEYWORD_RANDOM,
                "opt_replace_password",
                "opt_keyword_retain_current_password"
            ],
            action=lambda x: ast.SetPasswordCurrentUserRandomStatement(
                replace_password=x[4],
                retain_current_password=x[5]
            )
        ),
        # SET PASSWORD FOR user = 'password' [REPLACE 'current_password'] [RETAIN CURRENT PASSWORD]
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_SET,
                TType.KEYWORD_PASSWORD,
                TType.KEYWORD_FOR,
                "user_name",
                "equal",
                "text_literal_sys",
                "opt_replace_password",
                "opt_keyword_retain_current_password"
            ],
            action=lambda x: ast.SetPasswordForUserStatement(
                user=x[3],
                password=x[5].get_str_value(),
                replace_password=x[6],
                retain_current_password=x[7]
            )
        ),
        # SET PASSWORD FOR user TO RANDOM [REPLACE 'current_password'] [RETAIN CURRENT PASSWORD]
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_SET,
                TType.KEYWORD_PASSWORD,
                TType.KEYWORD_FOR,
                "user_name",
                TType.KEYWORD_TO,
                TType.KEYWORD_RANDOM,
                "opt_replace_password",
                "opt_keyword_retain_current_password"
            ],
            action=lambda x: ast.SetPasswordForUserRandomStatement(
                user=x[3],
                replace_password=x[6],
                retain_current_password=x[7]
            )
        )
    ]
)
