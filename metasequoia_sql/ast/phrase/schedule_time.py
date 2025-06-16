"""
事件调度时间（schedule time）

用于 `CREATE EVENT` 和 `ALTER EVENT` 语句中的调度时间定义。
"""

from typing import Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.time_unit import TimeUnitEnum

__all__ = [
    "ScheduleTime",
    "ScheduleTimeEvery",
    "ScheduleTimeAt",
]


class ScheduleTime(Node):
    """事件调度时间基类"""


class ScheduleTimeEvery(ScheduleTime):
    """事件调度时间：每隔一定时间执行（EVERY...）"""

    __slots__ = (
        "_interval_expression",
        "_interval_type",
        "_starts_expression",
        "_ends_expression"
    )

    def __init__(self,
                 interval_expression: Expression,
                 interval_type: "TimeUnitEnum",
                 starts_expression: Optional[Expression],
                 ends_expression: Optional[Expression]):
        """
        初始化每隔一定时间执行的调度时间

        Parameters
        ----------
        interval_expression : Expression
            时间间隔表达式
        interval_type : TimeUnitEnum
            时间间隔类型（如 SECOND、MINUTE、HOUR 等）
        starts_expression : Optional[Expression]
            开始时间表达式，如果为 None 则表示立即开始
        ends_expression : Optional[Expression]
            结束时间表达式，如果为 None 则表示永不结束
        """
        self._interval_expression = interval_expression
        self._interval_type = interval_type
        self._starts_expression = starts_expression
        self._ends_expression = ends_expression

    @property
    def interval_expression(self) -> Expression:
        return self._interval_expression

    @property
    def interval_type(self) -> "TimeUnitEnum":
        return self._interval_type

    @property
    def starts_expression(self) -> Optional[Expression]:
        return self._starts_expression

    @property
    def ends_expression(self) -> Optional[Expression]:
        return self._ends_expression


class ScheduleTimeAt(ScheduleTime):
    """事件调度时间：在指定时间执行（AT...）"""

    __slots__ = (
        "_execute_at_expression",
    )

    def __init__(self, execute_at_expression: Expression):
        """
        初始化在指定时间执行的调度时间

        Parameters
        ----------
        execute_at_expression : Expression
            执行时间表达式
        """
        self._execute_at_expression = execute_at_expression

    @property
    def execute_at_expression(self) -> Expression:
        return self._execute_at_expression
