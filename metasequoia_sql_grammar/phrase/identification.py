"""
身份认证（identification）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "IDENTIFICATION",
    "IDENTIFIED_BY_PASSWORD",
    "IDENTIFIED_BY_RANDOM_PASSWORD",
    "IDENTIFIED_WITH_PLUGIN",
    "IDENTIFIED_WITH_PLUGIN_AS_AUTH",
    "IDENTIFIED_WITH_PLUGIN_BY_PASSWORD",
    "IDENTIFIED_WITH_PLUGIN_BY_RANDOM_PASSWORD",
]

# 身份认证（选择具体的认证方式）
IDENTIFICATION = ms_parser.create_group(
    name="identification",
    rules=[
        ms_parser.create_rule(
            symbols=["identified_by_password"]
        ),
        ms_parser.create_rule(
            symbols=["identified_by_random_password"]
        ),
        ms_parser.create_rule(
            symbols=["identified_with_plugin"]
        ),
        ms_parser.create_rule(
            symbols=["identified_with_plugin_as_auth"]
        ),
        ms_parser.create_rule(
            symbols=["identified_with_plugin_by_password"]
        ),
        ms_parser.create_rule(
            symbols=["identified_with_plugin_by_random_password"]
        )
    ]
)

# 使用密码进行身份认证
IDENTIFIED_BY_PASSWORD = ms_parser.create_group(
    name="identified_by_password",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IDENTIFIED, TType.KEYWORD_BY, "text_literal_sys"],
            action=lambda x: ast.IdentifiedByPassword(password=x[2].get_str_value())
        )
    ]
)

# 使用随机密码进行身份认证
IDENTIFIED_BY_RANDOM_PASSWORD = ms_parser.create_group(
    name="identified_by_random_password",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IDENTIFIED, TType.KEYWORD_BY, TType.KEYWORD_RANDOM, TType.KEYWORD_PASSWORD],
            action=lambda x: ast.IdentifiedByRandomPassword()
        )
    ]
)

# 使用插件进行身份认证
IDENTIFIED_WITH_PLUGIN = ms_parser.create_group(
    name="identified_with_plugin",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IDENTIFIED, TType.KEYWORD_WITH, "ident_or_text"],
            action=lambda x: ast.IdentifiedWithPlugin(plugin=x[2].get_str_value())
        )
    ]
)

# 使用插件和认证字符串进行身份认证
IDENTIFIED_WITH_PLUGIN_AS_AUTH = ms_parser.create_group(
    name="identified_with_plugin_as_auth",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IDENTIFIED, TType.KEYWORD_WITH, "ident_or_text", TType.KEYWORD_AS,
                     "text_literal_or_hex"],
            action=lambda x: ast.IdentifiedWithPluginAsAuth(plugin=x[2].get_str_value(), auth_string=x[4])
        )
    ]
)

# 使用插件和密码进行身份认证
IDENTIFIED_WITH_PLUGIN_BY_PASSWORD = ms_parser.create_group(
    name="identified_with_plugin_by_password",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IDENTIFIED, TType.KEYWORD_WITH, "ident_or_text", TType.KEYWORD_BY,
                     "text_literal_sys"],
            action=lambda x: ast.IdentifiedWithPluginByPassword(plugin=x[2].get_str_value(),
                                                                password=x[4].get_str_value())
        )
    ]
)

# 使用插件和随机密码进行身份认证
IDENTIFIED_WITH_PLUGIN_BY_RANDOM_PASSWORD = ms_parser.create_group(
    name="identified_with_plugin_by_random_password",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IDENTIFIED, TType.KEYWORD_WITH, "ident_or_text", TType.KEYWORD_BY,
                     TType.KEYWORD_RANDOM, TType.KEYWORD_PASSWORD],
            action=lambda x: ast.IdentifiedWithPluginByRandomPassword(plugin=x[2].get_str_value())
        )
    ]
)
