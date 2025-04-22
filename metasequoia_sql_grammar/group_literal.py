"""
字面值的语义组

text_literal:
        LITERAL_TEXT_STRING
      | LITERAL_NCHAR_STRING;

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
    "GROUP_TEXT_LITERAL",
    "GROUP_INT_LITERAL",
    "GROUP_NUM_LITERAL",
    "GROUP_TEMPORAL_LITERAL",
    "GROUP_LITERAL",
    "GROUP_NULL_LITERAL",
    "GROUP_LITERAL_OR_NULL",
]

# 字符串字面值
# 对应 MySQL 语义组：TEXT_STRING_sys
GROUP_TEXT_LITERAL = ms_parser.create_group(
    name="text_literal",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.LITERAL_TEXT_STRING],
            action=lambda x: ast.StringLiteral(value=x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.LITERAL_NCHAR_STRING],
            action=lambda x: ast.StringLiteral(value=x[0])
        )
    ]
)

# 整数字面值
# 对应 MySQL 语义组：int64_literal
GROUP_INT_LITERAL = ms_parser.create_group(
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
GROUP_NUM_LITERAL = ms_parser.create_group(
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
GROUP_TEMPORAL_LITERAL = ms_parser.create_group(
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
GROUP_LITERAL = ms_parser.create_group(
    name="literal",
    rules=[
        ms_parser.create_rule(
            symbols=["text_literal"]
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
GROUP_NULL_LITERAL = ms_parser.create_group(
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
GROUP_LITERAL_OR_NULL = ms_parser.create_group(
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
