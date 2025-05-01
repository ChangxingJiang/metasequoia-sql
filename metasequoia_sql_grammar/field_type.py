"""
字段类型的语义组
"""

import metasequoia_parser as ms_parser
from metasequoia_sql_new import ast
from metasequoia_sql_new.terminal import SqlTerminalType as TType

__all__ = [
    "CHARSET_ASCII",  # ASCII 相关字符集名称关键字
    "CHARSET_UNICODE",  # UNICODE 相关字符集名称关键字
    "OPT_CHARSET",  # 可选的指定字符集信息
    "FIELD_LENGTH",
]

# ASCII 相关字符集名称关键字
# 对应 MySQL 语义组：ascii
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
# 对应 MySQL 语义组：unicode
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

# 可选的指定字符集信息
# 对应 MySQL 语义组：opt_charset_with_opt_binary
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
        # TODO 获取 CHARSET_NAME 待改为获取字符串值方法
        ms_parser.create_rule(
            symbols=["keyword_charset", "charset_name"],
            action=lambda x: ast.Charset(charset_type=ast.CharsetTypeEnum.CHARSET_NAME, charset_name=x[1].value)
        ),
        ms_parser.create_rule(
            symbols=["keyword_charset", "charset_name", TType.KEYWORD_BINARY],
            action=lambda x: ast.Charset(charset_type=ast.CharsetTypeEnum.CHARSET_NAME_BINARY, charset_name=x[1].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BINARY, "keyword_charset", "charset_name"],
            action=lambda x: ast.Charset(charset_type=ast.CharsetTypeEnum.BINARY_CHARSET_NAME, charset_name=x[2].value)
        )
    ]
)

# 指定字段类型长度的括号
# 对应 MySQL 语义组：field_length、type_datetime_precision
FIELD_LENGTH = ms_parser.create_group(
    name="field_length",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, TType.LITERAL_INT_NUM, TType.OPERATOR_RPAREN],
            action=lambda x: x[1]
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, TType.LITERAL_DECIMAL_NUM, TType.OPERATOR_RPAREN],
            action=lambda x: x[1]
        )
    ]
)

# 可选的指定字段类型长度的括号
# 对应 MySQL 语义组：opt_field_length
OPT_FIELD_LENGTH = ms_parser.create_group(
    name="opt_field_length",
    rules=[
        ms_parser.create_rule(
            symbols=["field_length"]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)

# 标准的浮点数精度信息的括号
# 对应 MySQL 语义组：standard_float_options
STANDARD_FLOAT_OPTIONS = ms_parser.create_group(
    name="standard_float_options",
    rules=[
        ms_parser.create_rule(
            symbols=["field_length"],
            action=lambda x: ast.FloatOptions(length=x[0], decimal=None)
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.FloatOptions(length=None, decimal=None)
        )
    ]
)

# 可选的字符集名称及可选的 BINARY 关键字
# 对应 MySQL 语义组：opt_charset_with_opt_binary
# OPT_CHARSET_WITH_OPT_BINARY = ms_parser.create_group(
#     name="opt_charset_with_opt_binary",
#     rules=[
#         ms_parser.create_rule(
#             symbols=[]
#         )
#     ]
# )
