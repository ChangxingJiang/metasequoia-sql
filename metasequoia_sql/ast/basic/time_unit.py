"""
时间单位类型抽象语法树节点
"""

import enum

__all__ = [
    "TimeUnitEnum"
]


class TimeUnitEnum(enum.IntEnum):
    """时间单位类型枚举值"""

    YEAR = enum.auto()  # 年
    QUARTER = enum.auto()  # 季度
    MONTH = enum.auto()  # 月
    WEEK = enum.auto()  # 周
    DAY = enum.auto()  # 日
    HOUR = enum.auto()  # 小时
    MINUTE = enum.auto()  # 分钟
    SECOND = enum.auto()  # 秒
    MICROSECOND = enum.auto()  # 微秒

    YEAR_MONTH = enum.auto()  # 年 + 月
    DAY_HOUR = enum.auto()  # 天 + 小时
    DAY_MINUTE = enum.auto()  # 天 + 分钟
    DAY_SECOND = enum.auto()  # 天 + 秒
    HOUR_MINUTE = enum.auto()  # 小时 + 分钟
    HOUR_SECOND = enum.auto()  # 小时 + 秒
    MINUTE_SECOND = enum.auto()  # 分钟 + 秒
    DAY_MICROSECOND = enum.auto()  # 天 + 微秒
    HOUR_MICROSECOND = enum.auto()  # 小时 + 微秒
    MINUTE_MICROSECOND = enum.auto()  # 分钟 + 微秒
    SECOND_MICROSECOND = enum.auto()  # 秒 + 微秒
