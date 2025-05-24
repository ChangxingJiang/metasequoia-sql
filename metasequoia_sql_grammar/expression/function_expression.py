"""
普通函数表达式（function expression）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "FUNCTION_EXPRESSION",
    "NOW_EXPRESSION",
    "DATE_TIME_TYPE",
]

# 函数表达式
FUNCTION_EXPRESSION = ms_parser.create_group(
    name="function_expression",
    rules=[
        # 关键字函数：函数名称为官方 SQL 2003 关键字，因为函数名是一个官方标记（token），所以解析器中需要有专门的语法规则，不会产生任何潜在的冲突
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHAR, TType.OPERATOR_LPAREN, "expr_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionChar.create(param_list=x[2], charset_name=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHAR, TType.OPERATOR_LPAREN, "expr_list", TType.KEYWORD_USING, "charset_name",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionChar.create(param_list=x[2], charset_name=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CURRENT_USER, "opt_braces"],
            action=lambda _: ast.FunctionExpression(function_name="current_user", param_list=[])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DATE, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="date", param_list=[x[2]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DAY, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="day", param_list=[x[2]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_HOUR, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="hour", param_list=[x[2]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INSERT, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_COMMA, "expr", TType.OPERATOR_COMMA, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="insert", param_list=[x[2], x[4], x[6], x[8]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INTERVAL, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_LPAREN],
            action=lambda x: ast.FunctionExpression(function_name="interval", param_list=[x[2], x[4]]),
            sr_priority_as=TType.KEYWORD_INTERVAL
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INTERVAL, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_COMMA, "expr_list", TType.OPERATOR_LPAREN],
            action=lambda x: ast.FunctionExpression(function_name="interval", param_list=[x[2]] + [x[4]] + x[6]),
            sr_priority_as=TType.KEYWORD_INTERVAL
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_JSON_VALUE, TType.OPERATOR_LPAREN, "simple_expr", TType.OPERATOR_COMMA,
                     "text_literal", "opt_returning_type", "json_on_empty_on_error", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionJsonValue.create(param_list=[x[2], x[4]], returning_type=x[5],
                                                          json_on_empty_on_error=x[6])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LEFT, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="left", param_list=[x[2], x[4]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MINUTE, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="minute", param_list=[x[2]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MONTH, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="month", param_list=[x[2]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RIGHT, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="right", param_list=[x[2], x[4]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SECOND, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="second", param_list=[x[2]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TIME, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="time", param_list=[x[2]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TIMESTAMP, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="timestamp", param_list=[x[2]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TIMESTAMP, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="timestamp", param_list=[x[2], x[4]])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_TRIM, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionTrim.create_as_default(chars_to_remove=None, source_string=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_TRIM, TType.OPERATOR_LPAREN, "expr", TType.KEYWORD_FROM, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionTrim.create_as_default(chars_to_remove=x[2], source_string=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_TRIM, TType.OPERATOR_LPAREN, TType.KEYWORD_LEADING, TType.KEYWORD_FROM, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionTrim.create_as_leading(chars_to_remove=None, source_string=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_TRIM, TType.OPERATOR_LPAREN, TType.KEYWORD_LEADING, "expr", TType.KEYWORD_FROM, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionTrim.create_as_leading(chars_to_remove=x[3], source_string=x[5])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_TRIM, TType.OPERATOR_LPAREN, TType.KEYWORD_TRAILING, TType.KEYWORD_FROM, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionTrim.create_as_trailing(chars_to_remove=None, source_string=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_TRIM, TType.OPERATOR_LPAREN, TType.KEYWORD_TRAILING, "expr", TType.KEYWORD_FROM, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionTrim.create_as_trailing(chars_to_remove=x[3], source_string=x[5])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_TRIM, TType.OPERATOR_LPAREN, TType.KEYWORD_BOTH, TType.KEYWORD_FROM, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionTrim.create_as_both(chars_to_remove=None, source_string=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_TRIM, TType.OPERATOR_LPAREN, TType.KEYWORD_BOTH, "expr", TType.KEYWORD_FROM, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionTrim.create_as_both(chars_to_remove=x[3], source_string=x[5])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_USER, TType.OPERATOR_LPAREN, TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="user", param_list=[])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_YEAR, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="year", param_list=[x[2]])
        ),

        # 非关键字函数：函数名称为非保留关键字，因为函数名不是官方保留字，所以需要专门的语法规则，以避免与语言的其他部分产生不兼容的问题。
        # 一个函数出现在这里，要不是出于对其他 SQL 语法兼容的考虑，要不是出于类型推导的需要。
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ADDDATE, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="adddate", param_list=[x[2], x[4]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ADDDATE, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "time_interval",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="adddate", param_list=[x[2], x[4]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CURRENT_DATE, "opt_braces"],
            action=lambda x: ast.FunctionExpression(function_name="current_date", param_list=[])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_CURTIME, "opt_field_type_param_0_1"],
            action=lambda x: ast.FunctionExpression(function_name="curtime", param_list=x[1].as_param_list())
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_DATE_ADD_INTERVAL, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "time_interval",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="date_add_interval", param_list=[x[2], x[4]]),
            sr_priority_as=TType.KEYWORD_INTERVAL
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_DATE_SUB_INTERVAL, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "time_interval",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="date_sub_interval", param_list=[x[2], x[4]]),
            sr_priority_as=TType.KEYWORD_INTERVAL
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_EXTRACT, TType.OPERATOR_LPAREN, "interval_time_unit", TType.KEYWORD_FROM, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExtract.create(time_unit=x[2], source_expression=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GET_FORMAT, TType.OPERATOR_LPAREN, "date_time_type", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionGetFormat.create(date_time_type=x[2], format_type=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOG, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="log", param_list=[x[2]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOG, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="log", param_list=[x[2], x[4]])
        ),
        ms_parser.create_rule(
            symbols=["now_expression"],
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_POSITION, TType.OPERATOR_LPAREN, "binary_expr", TType.KEYWORD_IN, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionPosition.create(sub_string=x[2], string=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SUBDATE, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="subdate", param_list=[x[2], x[4]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SUBDATE, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "time_interval",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="subdate", param_list=[x[2], x[4]])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_SUBSTRING, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_COMMA, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionSubstring.create(string=x[2], pos=x[4], length=x[6])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_SUBSTRING, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionSubstring.create(string=x[2], pos=x[4], length=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_SUBSTRING, TType.OPERATOR_LPAREN, "expr", TType.KEYWORD_FROM, "expr",
                     TType.KEYWORD_FOR, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionSubstring.create(string=x[2], pos=x[4], length=x[6])
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_SUBSTRING, TType.OPERATOR_LPAREN, "expr", TType.KEYWORD_FROM, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionSubstring.create(string=x[2], pos=x[4], length=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_SYSDATE, "opt_field_type_param_0_1"],
            action=lambda x: ast.FunctionExpression(function_name="sysdate", param_list=x[1].as_param_list())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TIMESTAMP_ADD, TType.OPERATOR_LPAREN, "time_unit", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_COMMA, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="timestamp_add", param_list=[x[2], x[4], x[6]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TIMESTAMP_DIFF, TType.OPERATOR_LPAREN, "time_unit", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_COMMA, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="timestamp_diff", param_list=[x[2], x[4], x[6]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UTC_DATE, "opt_braces"],
            action=lambda x: ast.FunctionExpression(function_name="utc_date", param_list=[])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UTC_TIME, "opt_field_type_param_0_1"],
            action=lambda x: ast.FunctionExpression(function_name="utc_time", param_list=x[1].as_param_list())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UTC_TIMESTAMP, "opt_field_type_param_0_1"],
            action=lambda x: ast.FunctionExpression(function_name="utc_timestamp", param_list=x[1].as_param_list())
        ),

        # 冲突风险函数：函数名称为非保留关键字，因为使用了常规的语法形式且该非保留关键字在文法的其他部分也有使用，所以需要专门的语法规则来处理
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ASCII, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="ascii", param_list=[x[2]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHARSET, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="charset", param_list=[x[2]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COALESCE, TType.OPERATOR_LPAREN, "expr_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="coalesce", param_list=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COLLATION, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="collation", param_list=[x[2]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DATABASE, TType.OPERATOR_LPAREN, TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="database", param_list=[])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IF, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_COMMA, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="if", param_list=[x[2], x[4], x[6]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FORMAT, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="format", param_list=[x[2], x[4]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FORMAT, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_COMMA, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="format", param_list=[x[2], x[4], x[6]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MICROSECOND, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="microsecond", param_list=[x[2]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MOD, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="mod", param_list=[x[2], x[4]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_QUARTER, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="quarter", param_list=[x[2]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REPEAT, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="repeat", param_list=[x[2], x[4]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REPLACE, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_COMMA, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="replace", param_list=[x[2], x[4], x[6]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REVERSE, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="reverse", param_list=[x[2]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ROW_COUNT, TType.OPERATOR_LPAREN, TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="row_count", param_list=[])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TRUNCATE, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="truncate", param_list=[x[2], x[4]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WEEK, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="week", param_list=[x[2]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WEEK, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="week", param_list=[x[2], x[4]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WEIGHT_STRING, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionWeightString.create(param1=x[2], param2=None, param3=None, param4=None,
                                                             binary_flag=False)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WEIGHT_STRING, TType.OPERATOR_LPAREN, "expr", TType.KEYWORD_AS, TType.KEYWORD_CHAR,
                     "paren_int_literal_or_hex", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionWeightString.create(param1=x[2], param2=None, param3=x[5], param4=None,
                                                             binary_flag=False)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WEIGHT_STRING, TType.OPERATOR_LPAREN, "expr", TType.KEYWORD_AS, TType.KEYWORD_BINARY,
                     "paren_int_literal_or_hex", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionWeightString.create(param1=x[2], param2=None, param3=x[5], param4=None,
                                                             binary_flag=True)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WEIGHT_STRING, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA,
                     "num_literal_or_hex", TType.OPERATOR_COMMA, "num_literal_or_hex", TType.OPERATOR_COMMA,
                     "num_literal_or_hex", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionWeightString.create(param1=x[2], param2=x[4], param3=x[6], param4=x[8],
                                                             binary_flag=False)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GEOMETRYCOLLECTION, TType.OPERATOR_LPAREN, "opt_expr_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="geometrycollection", param_list=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LINESTRING, TType.OPERATOR_LPAREN, "expr_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="linestring", param_list=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MULTILINESTRING, TType.OPERATOR_LPAREN, "expr_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="multilinestring", param_list=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MULTIPOINT, TType.OPERATOR_LPAREN, "expr_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="multipoint", param_list=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MULTIPOLYGON, TType.OPERATOR_LPAREN, "expr_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="multipolygon", param_list=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_POINT, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="point", param_list=[x[2], x[4]])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_POLYGON, TType.OPERATOR_LPAREN, "expr_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name="polygon", param_list=x[2])
        ),

        # 常规函数：函数名称不是关键字，通常不会对语言引入副作用
        ms_parser.create_rule(
            symbols=["ident_sys", TType.OPERATOR_LPAREN, "opt_udf_expr_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(function_name=x[0].get_str_value(), param_list=x[2])
        ),
        ms_parser.create_rule(
            symbols=["ident", TType.OPERATOR_DOT, "ident", TType.OPERATOR_LPAREN, "opt_expr_list",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FunctionExpression(schema_name=x[0].get_str_value(),
                                                    function_name=x[2].get_str_value(),
                                                    param_list=x[4])
        )
    ]
)

# 时间类型（`DATE`、`TIME` 或者 `DATETIME`）
DATE_TIME_TYPE = ms_parser.create_group(
    name="date_time_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DATE],
            action=lambda _: ast.DateTimeTypeEnum.DATE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TIME],
            action=lambda _: ast.DateTimeTypeEnum.TIME
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TIMESTAMP],
            action=lambda _: ast.DateTimeTypeEnum.TIMESTAMP
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DATETIME],
            action=lambda _: ast.DateTimeTypeEnum.DATETIME
        ),
    ]
)

# `NOW` 关键字及精度
NOW_EXPRESSION = ms_parser.create_group(
    name="now_expression",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.WORD_NOW, "opt_field_type_param_0_1"],
            action=lambda x: ast.FunctionExpression(function_name="now", param_list=x[1].as_param_list())
        )
    ]
)
