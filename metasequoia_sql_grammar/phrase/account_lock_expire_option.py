"""
账户锁定和密码过期选项（account lock expire option）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_ACCOUNT_LOCK_EXPIRE_OPTION_LIST",
    "ACCOUNT_LOCK_EXPIRE_OPTION_LIST",
    "ACCOUNT_LOCK_EXPIRE_OPTION",
]

# 可选的账户锁定和密码过期选项列表
OPT_ACCOUNT_LOCK_EXPIRE_OPTION_LIST = ms_parser.create_group(
    name="opt_account_lock_expire_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: []
        ),
        ms_parser.create_rule(
            symbols=["account_lock_expire_option_list"],
            action=lambda x: x[0]
        )
    ]
)

# 账户锁定和密码过期选项列表
ACCOUNT_LOCK_EXPIRE_OPTION_LIST = ms_parser.create_group(
    name="account_lock_expire_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["account_lock_expire_option_list", "account_lock_expire_option"],
            action=ms_parser.template.action.LIST_APPEND_1
        ),
        ms_parser.create_rule(
            symbols=["account_lock_expire_option"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 账户锁定和密码过期选项
ACCOUNT_LOCK_EXPIRE_OPTION = ms_parser.create_group(
    name="account_lock_expire_option",
    rules=[
        # 账户解锁
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ACCOUNT, TType.KEYWORD_UNLOCK],
            action=lambda _: ast.AccountUnlock()
        ),
        # 账户锁定
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ACCOUNT, TType.KEYWORD_LOCK],
            action=lambda _: ast.AccountLock()
        ),
        # 密码立即过期
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PASSWORD, TType.KEYWORD_EXPIRE],
            action=lambda _: ast.PasswordExpire()
        ),
        # 密码间隔过期
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PASSWORD, TType.KEYWORD_EXPIRE, TType.KEYWORD_INTERVAL, "num_literal_or_hex",
                     TType.KEYWORD_DAY],
            action=lambda x: ast.PasswordExpireInterval(x[3].value)
        ),
        # 密码永不过期
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PASSWORD, TType.KEYWORD_EXPIRE, TType.KEYWORD_NEVER],
            action=lambda _: ast.PasswordExpireNever()
        ),
        # 密码过期使用默认设置
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PASSWORD, TType.KEYWORD_EXPIRE, TType.KEYWORD_DEFAULT],
            action=lambda _: ast.PasswordExpireDefault()
        ),
        # 密码历史长度
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PASSWORD, TType.KEYWORD_HISTORY, "num_literal_or_hex"],
            action=lambda x: ast.PasswordHistory(x[2].value)
        ),
        # 密码历史使用默认设置
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PASSWORD, TType.KEYWORD_HISTORY, TType.KEYWORD_DEFAULT],
            action=lambda _: ast.PasswordHistoryDefault()
        ),
        # 密码重用间隔
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PASSWORD, TType.KEYWORD_REUSE, TType.KEYWORD_INTERVAL, "num_literal_or_hex",
                     TType.KEYWORD_DAY],
            action=lambda x: ast.PasswordReuseInterval(x[3].value)
        ),
        # 密码重用间隔使用默认设置
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PASSWORD, TType.KEYWORD_REUSE, TType.KEYWORD_INTERVAL, TType.KEYWORD_DEFAULT],
            action=lambda _: ast.PasswordReuseIntervalDefault()
        ),
        # 需要当前密码
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PASSWORD, TType.KEYWORD_REQUIRE, TType.KEYWORD_CURRENT],
            action=lambda _: ast.PasswordRequireCurrent()
        ),
        # 当前密码要求使用默认设置
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PASSWORD, TType.KEYWORD_REQUIRE, TType.KEYWORD_CURRENT, TType.KEYWORD_DEFAULT],
            action=lambda _: ast.PasswordRequireCurrentDefault()
        ),
        # 当前密码可选
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PASSWORD, TType.KEYWORD_REQUIRE, TType.KEYWORD_CURRENT, TType.KEYWORD_OPTIONAL],
            action=lambda _: ast.PasswordRequireCurrentOptional()
        ),
        # 失败登录尝试次数
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FAILED_LOGIN_ATTEMPTS, "num_literal_or_hex"],
            action=lambda x: ast.FailedLoginAttempts(x[1].value)
        ),
        # 密码锁定时间
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PASSWORD_LOCK_TIME, "num_literal_or_hex"],
            action=lambda x: ast.PasswordLockTime(x[1].value)
        ),
        # 密码无限制锁定
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PASSWORD_LOCK_TIME, TType.KEYWORD_UNBOUNDED],
            action=lambda _: ast.PasswordLockTimeUnbounded()
        )
    ]
)
