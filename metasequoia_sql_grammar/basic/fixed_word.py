"""
固定的词语组合
"""

import metasequoia_parser as ms_parser

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_KEYWORD_OF",
    "OPT_KEYWORD_ALL",
    "OPT_KEYWORD_INTO",
    "OPT_BRACES",
    "KEYWORD_CHARSET",
    "KEYWORD_NCHAR",
    "KEYWORD_VARCHAR",
    "KEYWORD_NVARCHAR",
    "OPT_EQUAL",
    "EQUAL",
]

# 可选的 `OPT` 关键字
OPT_KEYWORD_OF = ms_parser.create_group(
    name="opt_keyword_of",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_OF]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)

# 可选的 `ALL` 关键字
OPT_KEYWORD_ALL = ms_parser.create_group(
    name="opt_keyword_all",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALL]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)

# 可选的 `INTO` 关键字
OPT_KEYWORD_INTO = ms_parser.create_group(
    name="opt_keyword_into",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INTO]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)

# 可选的 `DEFAULT` 关键字
OPT_KEYWORD_DEFAULT = ms_parser.create_group(
    name="opt_keyword_default",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DEFAULT]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)

# 可选的空括号
OPT_BRACES = ms_parser.create_group(
    name="opt_braces",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, TType.OPERATOR_RPAREN]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)

# 可选的逗号
OPT_COMMA = ms_parser.create_group(
    name="opt_comma",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_COMMA]
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

# `NCHAR` 关键字或 `NATIONAL CHAR` 关键字（兼容的 `NCHAR` 类型名称）
KEYWORD_NCHAR = ms_parser.create_group(
    name="keyword_nchar",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NCHAR],
            action=lambda _: None
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NATIONAL, TType.KEYWORD_CHAR],
            action=lambda _: None
        )
    ]
)

# `CHAR VARYING` 关键字或 `VARCHAR` 关键字（兼容的 `VARCHAR` 类型名称）
KEYWORD_VARCHAR = ms_parser.create_group(
    name="keyword_varchar",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_VARCHAR],
            action=lambda _: None
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHAR, TType.KEYWORD_VARYING],
            action=lambda _: None
        )
    ]
)

# `NVARCHAR` 关键字、`NATIONAL VARCHAR` 关键字、`NCHAR VARCHAR` 关键字、`NATIONAL CHAR VARYING` 关键字或 `NCHAR VARYING` 关键字
# （兼容的 `NVARCHAR` 类型名称）
KEYWORD_NVARCHAR = ms_parser.create_group(
    name="keyword_nvarchar",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NVARCHAR],
            action=lambda _: None
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NATIONAL, TType.KEYWORD_VARCHAR],
            action=lambda _: None
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NCHAR, TType.KEYWORD_VARCHAR],
            action=lambda _: None
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NATIONAL, TType.KEYWORD_CHAR, TType.KEYWORD_VARYING],
            action=lambda _: None
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NCHAR, TType.KEYWORD_VARYING],
            action=lambda _: None
        )
    ]
)

# 可选的 `=` 运算符或 `:=` 运算符
OPT_EQUAL = ms_parser.create_group(
    name="opt_equal",
    rules=[
        ms_parser.create_rule(
            symbols=["equal"]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)

# `=` 运算符或 `:=` 运算符
EQUAL = ms_parser.create_group(
    name="equal",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_EQ]
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_COLON_EQ]
        )
    ]
)
