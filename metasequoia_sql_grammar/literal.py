"""
字面值的语义组

text_literal_sys:
        LITERAL_TEXT_STRING;

int_literal:
        LITERAL_INT_NUM;

num_literal:
        int_literal
      | LITERAL_FLOAT_NUM
      | LITERAL_DECIMAL_NUM;

temporal_literal:
        KEYWORD_DATE LITERAL_TEXT_STRING
      | KEYWORD_TIME LITERAL_TEXT_STRING
      | KEYWORD_DATETIME LITERAL_TEXT_STRING;

literal:
        text_literal
      | num_literal
      | temporal_literal
      | KEYWORD_FALSE
      | KEYWORD_TRUE
      | LITERAL_HEX_NUM
      | LITERAL_BIN_NUM
      | LITERAL_UNDERSCORE_CHARSET LITERAL_HEX_NUM
      | LITERAL_UNDERSCORE_CHARSET LITERAL_BIN_NUM;

null_literal:
        KEYWORD_NULL;

literal_or_null:
        literal
      | null_literal;
"""

import metasequoia_parser as ms_parser

from metasequoia_sql_new import ast
from metasequoia_sql_new.terminal import SqlTerminalType as TType

__all__ = [
    "TEXT_LITERAL_SYS",
    "INT_LITERAL",
    "INT_LITERAL_OR_HEX",
    "PAREN_INT_LITERAL_OR_HEX",
    "NUM_LITERAL",
    "NUM_LITERAL_OR_HEX",
    "TEMPORAL_LITERAL",
    "LITERAL",
    "NULL_LITERAL",
    "LITERAL_OR_NULL",
    "TEXT_LITERAL",
    "TEXT_STRING",
    "TEXT_STRING_LIST",
    "SIGNED_LITERAL",
    "SIGNED_LITERAL_OR_NULL",
    "PARAM_MARKER",
    "IDENT_OR_TEXT",
]

# 字符串字面值（不包括 Unicode 字符串）
TEXT_LITERAL_SYS = ms_parser.create_group(
    name="text_literal_sys",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.LITERAL_TEXT_STRING],
            action=lambda x: ast.StringLiteral(value=x[0])
        )
    ]
)

# 整数字面值
INT_LITERAL = ms_parser.create_group(
    name="int_literal",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.LITERAL_INT_NUM],
            action=lambda x: ast.IntLiteral.from_oct_string(x[0])
        )
    ]
)

# 整数字面值或十六进制字面值
INT_LITERAL_OR_HEX = ms_parser.create_group(
    name="int_literal_or_hex",
    rules=[
        ms_parser.create_rule(
            symbols=["int_literal"]
        ),
        ms_parser.create_rule(
            symbols=[TType.LITERAL_HEX_NUM],
            action=lambda x: ast.IntLiteral.from_hex_string(x[0])
        ),
    ]
)

# 包含外层括号的整数字面值或十六进制字面值
PAREN_INT_LITERAL_OR_HEX = ms_parser.create_group(
    name="paren_int_literal_or_hex",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "int_literal_or_hex", TType.OPERATOR_RPAREN],
            action=lambda x: x[1]
        ),
    ]
)

# 数值字面值
NUM_LITERAL = ms_parser.create_group(
    name="num_literal",
    rules=[
        ms_parser.create_rule(
            symbols=["int_literal"],
        ),
        ms_parser.create_rule(
            symbols=[TType.LITERAL_FLOAT_NUM],
            action=lambda x: ast.FloatLiteral(value=x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.LITERAL_DECIMAL_NUM],
            action=lambda x: ast.DecimalLiteral(value=x[0])
        )
    ]
)

# 数值字面值或十六进制字面值
NUM_LITERAL_OR_HEX = ms_parser.create_group(
    name="num_literal_or_hex",
    rules=[
        ms_parser.create_rule(
            symbols=["num_literal"]
        ),
        ms_parser.create_rule(
            symbols=[TType.LITERAL_HEX_NUM],
            action=lambda x: ast.IntLiteral.from_hex_string(x[0])
        ),
    ]
)

# 时间字面值
# 对应 MySQL 语义组：temporal_literal
TEMPORAL_LITERAL = ms_parser.create_group(
    name="temporal_literal",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DATE, TType.LITERAL_TEXT_STRING],
            action=lambda x: ast.TemporalLiteral.create_date_literal(value=x[1])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TIME, TType.LITERAL_TEXT_STRING],
            action=lambda x: ast.TemporalLiteral.create_time_literal(value=x[1])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DATETIME, TType.LITERAL_TEXT_STRING],
            action=lambda x: ast.TemporalLiteral.create_datetime_literal(value=x[1])
        )
    ]
)

# 非空字面值
LITERAL = ms_parser.create_group(
    name="literal",
    rules=[
        ms_parser.create_rule(
            symbols=["text_literal_sys"]
        ),
        ms_parser.create_rule(
            symbols=["num_literal"]
        ),
        ms_parser.create_rule(
            symbols=["temporal_literal"]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FALSE],
            action=lambda x: ast.FalseLiteral()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TRUE],
            action=lambda x: ast.TrueLiteral()
        ),
        ms_parser.create_rule(
            symbols=[TType.LITERAL_HEX_NUM],
            action=lambda x: ast.HexStringLiteral(value=x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.LITERAL_BIN_NUM],
            action=lambda x: ast.BinStringLiteral(value=x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.LITERAL_UNDERSCORE_CHARSET, TType.LITERAL_HEX_NUM],
            action=lambda x: ast.HexStringLiteral(value=x[1], charset=x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.LITERAL_UNDERSCORE_CHARSET, TType.LITERAL_BIN_NUM],
            action=lambda x: ast.BinStringLiteral(value=x[1], charset=x[0])
        ),
    ]
)

# 空值字面值
NULL_LITERAL = ms_parser.create_group(
    name="null_literal",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NULL],
            action=lambda x: ast.NullLiteral()
        )
    ]
)

# 可为空字面值
LITERAL_OR_NULL = ms_parser.create_group(
    name="literal_or_null",
    rules=[
        ms_parser.create_rule(
            symbols=["literal"]
        ),
        ms_parser.create_rule(
            symbols=["null_literal"]
        )
    ]
)

# 字符串字面值
# 对应 MySQL 语义组：text_literal
TEXT_LITERAL = ms_parser.create_group(
    name="text_literal",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.LITERAL_TEXT_STRING],
            action=lambda x: ast.StringLiteral(value=x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.LITERAL_NCHAR_STRING],
            action=lambda x: ast.StringLiteral(value=x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.LITERAL_UNDERSCORE_CHARSET, TType.LITERAL_TEXT_STRING],
            action=lambda x: ast.StringLiteral(value=x[1], charset=x[0])
        ),
        ms_parser.create_rule(
            symbols=["text_literal", TType.LITERAL_TEXT_STRING],
            action=lambda x: ast.StringLiteral(value=x[0].value + x[1])
        )
    ]
)

# 字符串、二进制、十六进制字面值
TEXT_STRING = ms_parser.create_group(
    name="text_string",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.LITERAL_TEXT_STRING],
            action=lambda x: ast.StringLiteral(value=x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.LITERAL_HEX_NUM],
            action=lambda x: ast.HexStringLiteral(value=x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.LITERAL_BIN_NUM],
            action=lambda x: ast.BinStringLiteral(value=x[0])
        )
    ]
)

# 逗号分隔的字符串、二进制、十六进制字面值的列表
TEXT_STRING_LIST = ms_parser.create_group(
    name="text_string_list",
    rules=[
        ms_parser.create_rule(
            symbols=["text_string_list", TType.OPERATOR_COMMA, "text_string"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["text_string"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 非空字面值或有符号的数值字面值
# 对应 MySQL 语义组：signed_literal
SIGNED_LITERAL = ms_parser.create_group(
    name="signed_literal",
    rules=[
        ms_parser.create_rule(
            symbols=["literal"]
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_PLUS, "num_literal"],
            action=lambda x: x[1]
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_SUB, "num_literal"],
            action=lambda x: x[1].neg()
        )
    ]
)

# 非空字面值、有符号的数值字面值或空值字面值
# 对应 MySQL 语义组：signed_literal_or_null
SIGNED_LITERAL_OR_NULL = ms_parser.create_group(
    name="signed_literal_or_null",
    rules=[
        ms_parser.create_rule(
            symbols=["signed_literal"]
        ),
        ms_parser.create_rule(
            symbols=["null_literal"]
        )
    ]
)

# 参数占位符
# 对应 MySQL 语义组：param_marker
PARAM_MARKER = ms_parser.create_group(
    name="param_marker",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.PARAM_MARKER],
            action=lambda _: ast.Param()
        )
    ]
)

# 标识符或字符串字面值表示的名称
# 对应 MySQL 语义组：ident_or_text
IDENT_OR_TEXT = ms_parser.create_group(
    name="ident_or_text",
    rules=[
        ms_parser.create_rule(
            symbols=["ident"]
        ),
        ms_parser.create_rule(
            symbols=["text_literal_sys"]
        ),
        ms_parser.create_rule(
            symbols=[TType.LEX_HOSTNAME],
            action=lambda x: ast.Hostname(value=x[0])
        )
    ]
)
