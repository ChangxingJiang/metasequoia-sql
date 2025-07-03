"""
时间间隔表达式（time interval）
"""

from typing import TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic import TimeUnitEnum

__all__ = [
    "TimeInterval"
]


class TimeInterval(Node):
    """时间间隔"""

    __slots__ = ["_time_unit", "_time_value"]

    def __init__(self, time_unit: "TimeUnitEnum", time_value: Expression):
        """
        初始化时间间隔。

        Parameters
        ----------
        time_unit : TimeUnitEnum
            时间单位
        time_value : Expression
            时间值表达式
        """
        self._time_unit = time_unit
        self._time_value = time_value

    @property
    def time_unit(self) -> "TimeUnitEnum":
        """
        获取时间单位。

        Returns
        -------
        TimeUnitEnum
            时间单位
        """
        return self._time_unit

    @property
    def time_value(self) -> Expression:
        """
        获取时间值表达式。

        Returns
        -------
        Expression
            时间值表达式
        """
        return self._time_value
