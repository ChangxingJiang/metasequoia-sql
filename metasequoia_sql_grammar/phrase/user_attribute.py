"""
用户属性（user attribute）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_USER_ATTRIBUTE",
]

# 可选的用户属性
OPT_USER_ATTRIBUTE = ms_parser.create_group(
    name="opt_user_attribute",
    rules=[
        # 空选项 - 不使用用户属性注释
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: None
        ),
        # 用户属性
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ATTRIBUTE, "text_literal_sys"],
            action=lambda x: ast.UserAttributeText(x[1].get_str_value())
        ),
        # 用户注释
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COMMENT, "text_literal_sys"],
            action=lambda x: ast.UserComment(x[1].get_str_value())
        )
    ]
)
