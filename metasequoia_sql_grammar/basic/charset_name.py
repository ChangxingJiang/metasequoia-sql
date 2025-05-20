"""
字符集相关语义组
"""

import metasequoia_parser as ms_parser

from metasequoia_sql_new import ast
from metasequoia_sql_new.terminal import SqlTerminalType as TType

__all__ = [
    "CHARSET_ASCII",
    "CHARSET_UNICODE",
    "CHARSET_NAME",
    "OPT_CHARSET",
]

# ASCII 相关字符集名称关键字
CHARSET_ASCII = ms_parser.create_group(
    name="charset_ascii",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ASCII],
            action=lambda x: ast.CharsetTypeEnum.ASCII
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BINARY, TType.KEYWORD_ASCII],
            action=lambda x: ast.CharsetTypeEnum.BINARY_ASCII
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ASCII, TType.KEYWORD_BINARY],
            action=lambda x: ast.CharsetTypeEnum.ASCII_BINARY
        )
    ]
)

# UNICODE 相关字符集名称关键字
CHARSET_UNICODE = ms_parser.create_group(
    name="charset_unicode",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UNICODE],
            action=lambda x: ast.CharsetTypeEnum.UNICODE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BINARY, TType.KEYWORD_UNICODE],
            action=lambda x: ast.CharsetTypeEnum.BINARY_UNICODE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UNICODE, TType.KEYWORD_BINARY],
            action=lambda x: ast.CharsetTypeEnum.UNICODE_BINARY
        )
    ]
)

# 字符集名称
CHARSET_NAME = ms_parser.create_group(
    name="charset_name",
    rules=[
        ms_parser.create_rule(
            symbols=["ident_or_text"],
            action=lambda x: ast.Charset(
                charset_type=ast.CharsetTypeEnum.CHARSET_NAME,
                charset_name=x[0].get_str_value()
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BINARY],
            action=lambda x: ast.Charset(charset_type=ast.CharsetTypeEnum.BINARY, charset_name=None)
        )
    ]
)

# 可选的指定字符集信息
OPT_CHARSET = ms_parser.create_group(
    name="opt_charset",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.Charset(charset_type=ast.CharsetTypeEnum.DEFAULT, charset_name=None)
        ),
        ms_parser.create_rule(
            symbols=["charset_ascii"],
            action=lambda x: ast.Charset(charset_type=x[0], charset_name=None)
        ),
        ms_parser.create_rule(
            symbols=["charset_unicode"],
            action=lambda x: ast.Charset(charset_type=x[0], charset_name=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BYTE],
            action=lambda x: ast.Charset(charset_type=ast.CharsetTypeEnum.BYTE, charset_name=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BINARY],
            action=lambda x: ast.Charset(charset_type=ast.CharsetTypeEnum.BINARY, charset_name=None)
        ),
        ms_parser.create_rule(
            symbols=["keyword_charset", "charset_name"],
            action=lambda x: x[1]
        ),
        ms_parser.create_rule(
            symbols=["keyword_charset", "charset_name", TType.KEYWORD_BINARY],
            action=lambda x: x[1].add_back_binary()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BINARY, "keyword_charset", "charset_name"],
            action=lambda x: x[2].add_front_binary()
        )
    ]
)
