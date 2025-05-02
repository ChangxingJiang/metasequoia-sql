"""
字段类型的语义组
"""

import metasequoia_parser as ms_parser

from metasequoia_sql_new import ast
from metasequoia_sql_new.terminal import SqlTerminalType as TType

__all__ = [
    "FIELD_TYPE_PARAM_1",
    "OPT_FIELD_TYPE_PARAM_1",
    "FIELD_TYPE_PARAM_2",
    "OPT_FIELD_TYPE_PARAM_2",
    "OPT_FIELD_TYPE_PARAM_0_1",
    "OPT_FIELD_TYPE_PARAM_1_2",
    "CAST_TYPE",
    "FIELD_OPTION",
    "FIELD_OPTION_LIST",
    "OPT_FIELD_OPTION_LIST",
    "FIELD_TYPE",
]

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
            symbols=[TType.OPERATOR_LPAREN, TType.OPERATOR_RPAREN],
            action=lambda x: ast.FieldTypeParams(option_1=None, option_2=None)
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.FieldTypeParams(option_1=None, option_2=None)
        )
    ]
)

# 可选的括号中的 1 个或 2 个字段类型参数
# 对应 MySQL 语义组：func_datetime_precision
OPT_FIELD_TYPE_PARAM_1_2 = ms_parser.create_group(
    name="opt_field_type_param_1_2",
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

# `CAST` 函数、`CONVERT` 函数以及 `JSON_VALUE` 函数中指定的返回值类型
CAST_TYPE = ms_parser.create_group(
    name="cast_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BINARY, "opt_field_type_param_1"],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.BINARY,
                params=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHAR, "opt_field_type_param_1", "opt_charset"],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.CHAR,
                params=x[1],
                charset=x[2]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NCHAR, "opt_field_type_param_1"],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.NCHAR,
                params=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SIGNED],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.SIGNED
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SIGNED, TType.KEYWORD_INT],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.SIGNED_INT
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UNSIGNED],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.UNSIGNED
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UNSIGNED, TType.KEYWORD_INT],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.UNSIGNED_INT
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DATE],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.DATE
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_YEAR],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.YEAR
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TIME, "field_type_param_1"],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.TIME,
                params=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DATETIME, "field_type_param_1"],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.DATETIME,
                params=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DECIMAL, "opt_field_type_param_1_2"],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.DECIMAL,
                params=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_JSON],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.JSON
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REAL],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.REAL
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DOUBLE],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.DOUBLE
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DOUBLE, TType.KEYWORD_PRECISION],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.DOUBLE_PRECISION
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FLOAT, "opt_field_type_param_1"],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.FLOAT,
                params=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_POINT],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.POINT
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LINESTRING],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.LINESTRING
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_POLYGON],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.POLYGON
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MULTIPOINT],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.MULTIPOINT
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MULTILINESTRING],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.MULTILINESTRING
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MULTIPOLYGON],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.MULTIPOLYGON
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GEOMETRYCOLLECTION],
            action=lambda x: ast.CastType(
                field_type=ast.CastTypeEnum.GEOMETRYCOLLECTION
            )
        )
    ]
)

# `JSON_VALUE` 函数中可选的返回值类型
OPT_RETURNING_TYPE = ms_parser.create_group(
    name="opt_returning_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RETURNING, "cast_type"],
            action=lambda x: x[1]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.CastType.default()
        )
    ]
)

# 单个字段选项（`SIGNED`、`UNSIGNED` 或 `ZEROFILL`）
FIELD_OPTION = ms_parser.create_group(
    name="field_option",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SIGNED],
            action=lambda x: ast.FieldOption.SIGNED
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UNSIGNED],
            action=lambda x: ast.FieldOption.UNSIGNED
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ZEROFILL],
            action=lambda x: ast.FieldOption.ZEROFILL
        )
    ]
)

# 多个字段选项（`SIGNED`、`UNSIGNED` 或 `ZEROFILL`）
FIELD_OPTION_LIST = ms_parser.create_group(
    name="field_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["field_option_list", "field_option"],
            action=lambda x: x[0] | x[1]
        ),
        ms_parser.create_rule(
            symbols=["field_option"]
        )
    ]
)

# 可选的多个字段选项（`SIGNED`、`UNSIGNED` 或 `ZEROFILL`）
OPT_FIELD_OPTION_LIST = ms_parser.create_group(
    name="opt_field_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["field_option_list"]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.FieldOption.NONE
        )
    ]
)

# DDL 语句中的字段类型
FIELD_TYPE = ms_parser.create_group(
    name="field_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INT, "opt_field_type_param_1", "opt_field_option_list"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.INT,
                params=x[1],
                options=x[2]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TINYINT, "opt_field_type_param_1", "opt_field_option_list"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.TINYINT,
                params=x[1],
                options=x[2]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SMALLINT, "opt_field_type_param_1", "opt_field_option_list"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.SMALLINT,
                params=x[1],
                options=x[2]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MEDIUMINT, "opt_field_type_param_1", "opt_field_option_list"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.MEDIUMINT,
                params=x[1],
                options=x[2]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BIGINT, "opt_field_type_param_1", "opt_field_option_list"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.BIGINT,
                params=x[1],
                options=x[2]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REAL, "opt_field_type_param_2", "opt_field_option_list"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.REAL,
                params=x[1],
                options=x[2]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DOUBLE, "opt_field_type_param_2", "opt_field_option_list"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.DOUBLE,
                params=x[1],
                options=x[2]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DOUBLE, TType.KEYWORD_PRECISION, "opt_field_type_param_2", "opt_field_option_list"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.DOUBLE_PRECISION,
                params=x[2],
                options=x[3]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FLOAT, "opt_field_type_param_1_2", "opt_field_option_list"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.FLOAT,
                params=x[1],
                options=x[2]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DECIMAL, "opt_field_type_param_1_2", "opt_field_option_list"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.DECIMAL,
                params=x[1],
                options=x[2]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NUMERIC, "opt_field_type_param_1_2", "opt_field_option_list"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.NUMERIC,
                params=x[1],
                options=x[2]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FIXED, "opt_field_type_param_1_2", "opt_field_option_list"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.FIXED,
                params=x[1],
                options=x[2]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BIT],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.BIT
            ),
            sr_priority_as=TType.KEYWORD_USED_AS_KEYWORD
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BIT, "field_type_param_1"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.BIT,
                params=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BOOL],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.BOOL
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BOOLEAN],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.BOOLEAN
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHAR, "field_type_param_1", "opt_charset"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.CHAR,
                params=x[1],
                charset=x[2]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHAR, "opt_charset"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.CHAR,
                charset=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=["keyword_nchar", "field_type_param_1", TType.KEYWORD_BINARY],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.NCHAR_BINARY,
                params=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=["keyword_nchar", "field_type_param_1"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.NCHAR,
                params=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=["keyword_nchar", TType.KEYWORD_BINARY],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.NCHAR_BINARY
            )
        ),
        ms_parser.create_rule(
            symbols=["keyword_nchar"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.NCHAR
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BINARY, "field_type_param_1"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.BINARY,
                params=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BINARY],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.BINARY
            )
        ),
        ms_parser.create_rule(
            symbols=["keyword_varchar", "field_type_param_1", "opt_charset"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.VARCHAR,
                params=x[1],
                charset=x[2]
            )
        ),
        ms_parser.create_rule(
            symbols=["keyword_nvarchar", "field_type_param_1", TType.KEYWORD_BINARY],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.NVARCHAR_BINARY,
                params=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=["keyword_nvarchar", "field_type_param_1"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.NVARCHAR,
                params=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_VARBINARY, "field_type_param_1"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.VARBINARY,
                params=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_YEAR, "opt_field_type_param_1", "opt_field_option_list"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.YEAR,
                params=x[1],
                options=x[2]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DATE],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.DATE
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TIME, "field_type_param_1"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.TIME,
                params=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TIMESTAMP, "field_type_param_1"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.TIMESTAMP,
                params=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DATETIME, "field_type_param_1"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.DATETIME,
                params=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TINYBLOB],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.TINYBLOB,
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BLOB, "opt_field_type_param_1"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.BLOB,
                params=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MEDIUMBLOB],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.MEDIUMBLOB,
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LONGBLOB],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.LONGBLOB,
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GEOMETRY],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.GEOMETRY,
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GEOMETRYCOLLECTION],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.GEOMETRYCOLLECTION,
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_POINT],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.POINT,
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MULTIPOINT],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.MULTIPOINT,
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LINESTRING],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.LINESTRING,
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MULTILINESTRING],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.MULTILINESTRING,
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_POLYGON],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.POLYGON,
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MULTIPOLYGON],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.MULTIPOLYGON,
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LONG, TType.KEYWORD_VARBINARY],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.LONG_VARBINARY,
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LONG, "keyword_varchar", "opt_charset"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.LONG_VARCHAR,
                charset=x[2]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TINYTEXT, "opt_charset"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.TINYTEXT,
                charset=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TEXT, "opt_field_type_param_1", "opt_charset"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.TEXT,
                params=x[1],
                charset=x[2]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MEDIUMTEXT, "opt_charset"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.MEDIUMTEXT,
                charset=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LONGTEXT, "opt_charset"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.LONGTEXT,
                charset=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ENUM, TType.OPERATOR_LPAREN, "text_string_list", TType.OPERATOR_RPAREN,
                     "opt_charset"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.ENUM,
                enum_value_list=[text_string.get_str_value() for text_string in x[2]],
                charset=x[4]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SET, TType.OPERATOR_LPAREN, "text_string_list", TType.OPERATOR_RPAREN,
                     "opt_charset"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.SET,
                enum_value_list=[text_string.get_str_value() for text_string in x[2]],
                charset=x[4]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LONG, "opt_charset"],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.LONG,
                charset=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SERIAL],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.SERIAL,
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_JSON],
            action=lambda x: ast.FieldType(
                field_type=ast.FieldTypeEnum.JSON,
            )
        )
    ]
)
