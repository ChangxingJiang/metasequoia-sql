"""
时间单位类型语义组
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "TIME_UNIT",
    "INTERVAL_TIME_UNIT",
]

# 时间单位关键字
# 对应 MySQL 语义组：interval_time_stamp
TIME_UNIT = ms_parser.create_group(
    name="time_unit",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_YEAR],
            action=lambda x: ast.TimeUnitEnum.YEAR
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_QUARTER],
            action=lambda x: ast.TimeUnitEnum.QUARTER
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MONTH],
            action=lambda x: ast.TimeUnitEnum.MONTH
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WEEK],
            action=lambda x: ast.TimeUnitEnum.WEEK
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DAY],
            action=lambda x: ast.TimeUnitEnum.DAY
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_HOUR],
            action=lambda x: ast.TimeUnitEnum.HOUR
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MINUTE],
            action=lambda x: ast.TimeUnitEnum.MINUTE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SECOND],
            action=lambda x: ast.TimeUnitEnum.SECOND
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MICROSECOND],
            action=lambda x: ast.TimeUnitEnum.MICROSECOND
        )
    ]
)

# 时间单位关键字（INTERVAL 中的关键字）
# 对应 MySQL 语义组：interval
INTERVAL_TIME_UNIT = ms_parser.create_group(
    name="interval_time_unit",
    rules=[
        ms_parser.create_rule(
            symbols=["time_unit"]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_YEAR_MONTH],
            action=lambda x: ast.TimeUnitEnum.YEAR_MONTH
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DAY_HOUR],
            action=lambda x: ast.TimeUnitEnum.DAY_HOUR
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DAY_MINUTE],
            action=lambda x: ast.TimeUnitEnum.DAY_MINUTE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DAY_SECOND],
            action=lambda x: ast.TimeUnitEnum.DAY_SECOND
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DAY_MICROSECOND],
            action=lambda x: ast.TimeUnitEnum.DAY_MICROSECOND
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_HOUR_MINUTE],
            action=lambda x: ast.TimeUnitEnum.HOUR_MINUTE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_HOUR_SECOND],
            action=lambda x: ast.TimeUnitEnum.HOUR_SECOND
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_HOUR_MICROSECOND],
            action=lambda x: ast.TimeUnitEnum.HOUR_MICROSECOND
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MINUTE_SECOND],
            action=lambda x: ast.TimeUnitEnum.MINUTE_SECOND
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MINUTE_MICROSECOND],
            action=lambda x: ast.TimeUnitEnum.MINUTE_MICROSECOND
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SECOND_MICROSECOND],
            action=lambda x: ast.TimeUnitEnum.SECOND_MICROSECOND
        ),
    ]
)
