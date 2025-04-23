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
    "GENERAL_TEXT_LITERAL_SYS",
    "GENERAL_INT_LITERAL",
    "GENERAL_NUM_LITERAL",
    "GENERAL_TEMPORAL_LITERAL",
    "GENERAL_LITERAL",
    "GENERAL_NULL_LITERAL",
    "GENERAL_LITERAL_OR_NULL",
    "GENERAL_TEXT_LITERAL",
    "GENERAL_TEXT_STRING",
    "GENERAL_SIGNED_LITERAL",
    "GENERAL_SIGNED_LITERAL_OR_NULL",
]

# 字符串字面值（不包括 Unicode 字符串）
# 对应 MySQL 语义组：TEXT_STRING_sys
# 对应 MySQL 语义组：TEXT_STRING_literal
# 对应 MySQL 语义组：TEXT_STRING_filesystem
# 对应 MySQL 语义组：TEXT_STRING_password
# 对应 MySQL 语义组：TEXT_STRING_validated
# 对应 MySQL 语义组：TEXT_STRING_sys_nonewline
# 对应 MySQL 语义组：filter_wild_db_table_string
GENERAL_TEXT_LITERAL_SYS = ms_parser.create_group(
    name="text_literal_sys",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.LITERAL_TEXT_STRING],
            action=lambda x: ast.StringLiteral(value=x[0])
        )
    ]
)

# 整数字面值
# 对应 MySQL 语义组：int64_literal
GENERAL_INT_LITERAL = ms_parser.create_group(
    name="int_literal",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.LITERAL_INT_NUM],
            action=lambda x: ast.IntLiteral(value=x[0])
        )
    ]
)

# 数值字面值
# 对应 MySQL 语义组：NUM_literal
GENERAL_NUM_LITERAL = ms_parser.create_group(
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

# 时间字面值
# 对应 MySQL 语义组：temporal_literal
GENERAL_TEMPORAL_LITERAL = ms_parser.create_group(
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
# 对应 MySQL 语义组：literal
GENERAL_LITERAL = ms_parser.create_group(
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
# 对应 MySQL 语义组：null_as_literal
GENERAL_NULL_LITERAL = ms_parser.create_group(
    name="null_literal",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NULL],
            action=lambda x: ast.NullLiteral()
        )
    ]
)

# 字面值或空值字面值
# 对应 MySQL 语义组：literal_or_null
GENERAL_LITERAL_OR_NULL = ms_parser.create_group(
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
GENERAL_TEXT_LITERAL = ms_parser.create_group(
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

# 字符串字面值或二进制、十六进制字面值
# 对应 MySQL 语义组：text_string
GENERAL_TEXT_STRING = ms_parser.create_group(
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

# 非空字面值，有符号的数值字面值
# 对应 MySQL 语义组：signed_literal
GENERAL_SIGNED_LITERAL = ms_parser.create_group(
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
GENERAL_SIGNED_LITERAL_OR_NULL = ms_parser.create_group(
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
