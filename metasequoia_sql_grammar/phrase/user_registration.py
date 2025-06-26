"""
用户注册（user registration）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "USER_REGISTRATION",
]

# 用户注册
USER_REGISTRATION = ms_parser.create_group(
    name="user_registration",
    rules=[
        # factor INITIATE REGISTRATION
        ms_parser.create_rule(
            symbols=[
                TType.LITERAL_INT_NUM,
                TType.KEYWORD_FACTOR,
                TType.KEYWORD_INITIATE,
                TType.KEYWORD_REGISTRATION
            ],
            action=lambda x: ast.UserRegistrationInitiate(
                factor=int(x[0])
            )
        ),
        # factor UNREGISTER
        ms_parser.create_rule(
            symbols=[
                TType.LITERAL_INT_NUM,
                TType.KEYWORD_FACTOR,
                TType.KEYWORD_UNREGISTER
            ],
            action=lambda x: ast.UserRegistrationUnregister(
                factor=int(x[0])
            )
        ),
        # factor FINISH REGISTRATION SET CHALLENGE_RESPONSE AS TEXT_STRING_hash
        ms_parser.create_rule(
            symbols=[
                TType.LITERAL_INT_NUM,
                TType.KEYWORD_FACTOR,
                TType.KEYWORD_FINISH,
                TType.KEYWORD_REGISTRATION,
                TType.KEYWORD_SET,
                TType.KEYWORD_CHALLENGE_RESPONSE,
                TType.KEYWORD_AS,
                "text_literal_sys"
            ],
            action=lambda x: ast.UserRegistrationFinish(
                factor=int(x[0]),
                challenge_response=x[7].get_str_value()
            )
        )
    ]
)
