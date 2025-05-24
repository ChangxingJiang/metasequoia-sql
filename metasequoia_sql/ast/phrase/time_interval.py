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
        self._time_unit = time_unit
        self._time_value = time_value

    @property
    def time_unit(self) -> "TimeUnitEnum":
        return self._time_unit

    @property
    def time_value(self) -> Expression:
        return self._time_value
