"""
通用的基础元素语义组
"""

import metasequoia_parser as ms_parser
from metasequoia_sql_new.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_OF",
    "OPT_BRACES",
    "KEYWORD_CHARSET",
]

# 可选的 `OPT` 关键字
# 对应 MySQL 语义组：opt_of
OPT_OF = ms_parser.create_group(
    name="opt_of",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_OF]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)

# 可选的空括号
# 对应 MySQL 语义组：optional_braces
OPT_BRACES = ms_parser.create_group(
    name="opt_braces",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, TType.OPERATOR_RPAREN]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)

# `CHARSET` 关键字或 `CHAR SET` 关键字
KEYWORD_CHARSET = ms_parser.create_group(
    name="keyword_charset",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHAR, TType.KEYWORD_SET],
            action=lambda _: None
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHARSET],
            action=lambda _: None
        )
    ]
)
