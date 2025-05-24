"""
时间间隔表达式（time interval）
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic import TimeUnitEnum

__all__ = [
    "TimeInterval"
]


class TimeInterval(Node):
    """时间间隔"""

    def __init__(self, time_unit: "TimeUnitEnum", time_value: Expression):
        self._time_unit = time_unit
        self._time_value = time_value

    def attr_list(self) -> List[str]:
        return ["time_unit", "time_value"]

    @property
    def time_unit(self) -> "TimeUnitEnum":
        return self._time_unit

    @property
    def time_value(self) -> Expression:
        return self._time_value
