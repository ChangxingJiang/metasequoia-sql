"""
时间单位类型抽象语法树节点
"""

from enum import IntEnum, auto

__all__ = [
    "TimeUnitEnum"
]


class TimeUnitEnum(IntEnum):
    """时间单位类型枚举值"""

    YEAR = auto()  # 年
    QUARTER = auto()  # 季度
    MONTH = auto()  # 月
    WEEK = auto()  # 周
    DAY = auto()  # 日
    HOUR = auto()  # 小时
    MINUTE = auto()  # 分钟
    SECOND = auto()  # 秒
    MICROSECOND = auto()  # 微秒

    YEAR_MONTH = auto()  # 年 + 月
    DAY_HOUR = auto()  # 天 + 小时
    DAY_MINUTE = auto()  # 天 + 分钟
    DAY_SECOND = auto()  # 天 + 秒
    HOUR_MINUTE = auto()  # 小时 + 分钟
    HOUR_SECOND = auto()  # 小时 + 秒
    MINUTE_SECOND = auto()  # 分钟 + 秒
    DAY_MICROSECOND = auto()  # 天 + 微秒
    HOUR_MICROSECOND = auto()  # 小时 + 微秒
    MINUTE_MICROSECOND = auto()  # 分钟 + 微秒
    SECOND_MICROSECOND = auto()  # 秒 + 微秒
