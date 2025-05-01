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
    "FIELD_TYPE_PARAM_1",
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
        ms_parser.create_rule(
            symbols=["keyword_charset", "charset_name"],
            action=lambda x: ast.Charset(charset_type=ast.CharsetTypeEnum.CHARSET_NAME,
                                         charset_name=x[1].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=["keyword_charset", "charset_name", TType.KEYWORD_BINARY],
            action=lambda x: ast.Charset(charset_type=ast.CharsetTypeEnum.CHARSET_NAME_BINARY,
                                         charset_name=x[1].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BINARY, "keyword_charset", "charset_name"],
            action=lambda x: ast.Charset(charset_type=ast.CharsetTypeEnum.BINARY_CHARSET_NAME,
                                         charset_name=x[2].get_str_value())
        )
    ]
)

# 括号中的 1 个字段类型参数
# 对应 MySQL 语义组：field_length、type_datetime_precision
FIELD_TYPE_PARAM_1 = ms_parser.create_group(
    name="field_type_param_1",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "num_literal", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FieldTypeParams(option_1=x[1], option_2=None)
        ),
    ]
)

# 可选的括号中的 1 个字段类型参数
# 对应 MySQL 语义组：opt_field_length
OPT_FIELD_TYPE_PARAM_1 = ms_parser.create_group(
    name="opt_field_type_param_1",
    rules=[
        ms_parser.create_rule(
            symbols=["field_type_param_1"]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.FieldTypeParams(option_1=None, option_2=None)
        )
    ]
)

# 括号中的 2 个字段类型参数
# 对应 MySQL 语义组：precision
FIELD_TYPE_PARAM_2 = ms_parser.create_group(
    name="field_type_param_2",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "num_literal", TType.OPERATOR_COMMA, "num_literal", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FieldTypeParams(option_1=x[1], option_2=x[3])
        )
    ]
)

# 可选的括号中的 2 个字段类型参数
# 对应 MySQL 语义组：opt_precision
OPT_FIELD_TYPE_PARAM_2 = ms_parser.create_group(
    name="opt_field_type_param_2",
    rules=[
        ms_parser.create_rule(
            symbols=["field_type_param_2"]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.FieldTypeParams(option_1=None, option_2=None)
        )
    ]
)

# 可选的括号中的 0 个或 1 个字段类型参数
# 对应 MySQL 语义组：func_datetime_precision
OPT_FIELD_TYPE_PARAM_0_1 = ms_parser.create_group(
    name="opt_field_type_param_0_1",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "num_literal", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FieldTypeParams(option_1=x[1], option_2=None)
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.FieldTypeParams(option_1=None, option_2=None)
        )
    ]
)

# 可选的括号中的 0 个、1 个或 2 个字段类型参数
# 对应 MySQL 语义组：func_datetime_precision
OPT_FIELD_TYPE_PARAM_0_1_2 = ms_parser.create_group(
    name="opt_field_type_param_0_1_2",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "num_literal", TType.OPERATOR_COMMA, "num_literal", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FieldTypeParams(option_1=x[1], option_2=x[3])
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "num_literal", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FieldTypeParams(option_1=x[1], option_2=None)
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.FieldTypeParams(option_1=None, option_2=None)
        )
    ]
)
