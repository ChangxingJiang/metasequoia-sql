"""
普通函数表达式（function expression）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql_new import ast
from metasequoia_sql_new.terminal import SqlTerminalType as TType

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
