"""
窗口函数的节点
"""

import enum
import typing

from metasequoia_sql_new.ast.base import Expression
from metasequoia_sql_new.ast.base import Node
from metasequoia_sql_new.ast.order_clause import OrderClause
from metasequoia_sql_new.ast.time_unit import TimeUnitEnum

__all__ = [
    "WindowBorderTypeEnum",
    "WindowExclusionTypeEnum",
    "WindowBoundaryTypeEnum",
    "WindowBorder",
    "WindowBorders",
    "WindowFrame",
    "Window",
]


class WindowBorderTypeEnum(enum.IntEnum):
    """窗口边界类型"""

    ROWS = enum.auto()  # 基于物理行来定义窗口的边界
    RANGE = enum.auto()  # 基于值的范围来定义窗口的边界
    GROUPS = enum.auto()  # 基于分组键的值来定义窗口的边界


class WindowExclusionTypeEnum(enum.IntEnum):
    """窗口排除的类型"""

    CURRENT_ROW = enum.auto()  # 排除当前行
    GROUP = enum.auto()  # 排除当前行及与当前行具有相同排序值的行
    TIES = enum.auto()  # 排除与当前行具有相同排序值的行，但会保留当前行
    NO_OTHERS = enum.auto()  # 默认行为，不排除任何行
    NULL = enum.auto()


class WindowBoundaryTypeEnum(enum.IntEnum):
    """窗口边界值类型的枚举类型"""

    UNBOUNDED_PRECEDING = enum.auto()  # 以分区内的第一行作为窗口开始位置
    VALUE_PRECEDING = enum.auto()  # 如果边界类型为 ROWS 则为行数，如果边界类型为 RANGE 则为边界值
    INTERVAL_PRECEDING = enum.auto()  # 时间间隔的边界

    CURRENT_ROW = enum.auto()  # 当前行

    INTERVAL_FOLLOWING = enum.auto()  # 时间间隔的边界
    VALUE_FOLLOWING = enum.auto()  # 如果边界类型为 ROWS 则为行数，如果边界类型为 RANGE 则为边界值
    UNBOUNDED_FOLLOWING = enum.auto()  # 以分区内的最后一行作为窗口结束位置


class WindowBorder(Node):
    """窗口的单侧边界值

    UNBOUNDED [PRECEDING|FOLLOWING]
    {value} [PRECEDING|FOLLOWING]
    INTERVAL {value} {time_unit} [PRECEDING|FOLLOWING]
    CURRENT ROW
    """

    def __init__(self, boundary_type: WindowBoundaryTypeEnum,
                 value: typing.Optional[Expression] = None,
                 time_unit: typing.Optional[TimeUnitEnum] = None):
        self._boundary_type = boundary_type
        self._value = value
        self._time_unit = time_unit

    @staticmethod
    def create_unbounded_preceding() -> "WindowBorder":
        return WindowBorder(
            boundary_type=WindowBoundaryTypeEnum.UNBOUNDED_PRECEDING
        )

    @staticmethod
    def create_value_preceding(value: Expression) -> "WindowBorder":
        return WindowBorder(
            boundary_type=WindowBoundaryTypeEnum.VALUE_PRECEDING,
            value=value
        )

    @staticmethod
    def create_interval_preceding(value: Expression, time_unit: TimeUnitEnum) -> "WindowBorder":
        return WindowBorder(
            boundary_type=WindowBoundaryTypeEnum.INTERVAL_PRECEDING,
            value=value,
            time_unit=time_unit
        )

    @staticmethod
    def create_current_row() -> "WindowBorder":
        return WindowBorder(
            boundary_type=WindowBoundaryTypeEnum.CURRENT_ROW
        )

    @staticmethod
    def create_unbounded_following() -> "WindowBorder":
        return WindowBorder(
            boundary_type=WindowBoundaryTypeEnum.UNBOUNDED_FOLLOWING
        )

    @staticmethod
    def create_value_following(value: Expression) -> "WindowBorder":
        return WindowBorder(
            boundary_type=WindowBoundaryTypeEnum.VALUE_FOLLOWING,
            value=value
        )

    @staticmethod
    def create_interval_following(value: Expression, time_unit: TimeUnitEnum) -> "WindowBorder":
        return WindowBorder(
            boundary_type=WindowBoundaryTypeEnum.INTERVAL_FOLLOWING,
            value=value,
            time_unit=time_unit
        )

    def attr_list(self) -> typing.List[str]:
        return ["boundary_type", "value", "time_unit"]

    @property
    def boundary_type(self) -> WindowBoundaryTypeEnum:
        return self._boundary_type

    @property
    def value(self) -> typing.Optional[Expression]:
        return self._value

    @property
    def time_unit(self) -> typing.Optional[TimeUnitEnum]:
        return self._time_unit


class WindowBorders(Node):
    """窗口的两侧边界值

    {start_border}
    BETWEEN {start_border} AND {end_border}
    """

    def __init__(self, start_border: WindowBorder, end_border: WindowBorder):
        self._start_border = start_border
        self._end_border = end_border

    @staticmethod
    def create_by_start_border(start_border: WindowBorder) -> "WindowBorders":
        return WindowBorders(
            start_border=start_border,
            end_border=WindowBorder.create_current_row()
        )

    def attr_list(self) -> typing.List[str]:
        return ["start_border", "end_border"]

    @property
    def start_border(self) -> WindowBorder:
        return self._start_border

    @property
    def end_border(self) -> WindowBorder:
        return self._end_border


class WindowFrame(Node):
    """窗口框架子句（包括边界类型、边界值、排除值）"""

    def __init__(self,
                 border_type: WindowBorderTypeEnum,
                 borders: WindowBorders,
                 exclusion: WindowExclusionTypeEnum):
        self._border_type = border_type
        self._borders = borders
        self._exclusion = exclusion

    def attr_list(self) -> typing.List[str]:
        return ["border_type", "borders", "exclusion"]

    @property
    def border_type(self) -> WindowBorderTypeEnum:
        return self._border_type

    @property
    def borders(self) -> WindowBorders:
        return self._borders

    @property
    def exclusion(self) -> WindowExclusionTypeEnum:
        return self._exclusion


class Window(Node):
    """窗口（包括可选的窗口名称、可选的 PARTITION BY 子句、可选的 ORDER BY 子句和可选的窗口框架子句"""

    def __init__(self,
                 name: typing.Optional[Expression],
                 partition_clause: typing.Optional[typing.List[Expression]],
                 order_clause: typing.Optional[OrderClause],
                 frame_clause: typing.Optional[WindowFrame]):
        self._name = name
        self._partition_clause = partition_clause
        self._order_clause = order_clause
        self._frame_clause = frame_clause

    @staticmethod
    def create_by_name(name: Expression) -> "Window":
        return Window(
            name=name,
            partition_clause=None,
            order_clause=None,
            frame_clause=None
        )

    def attr_list(self) -> typing.List[str]:
        return ["name", "partition_clause", "order_clause", "frame_clause"]

    @property
    def name(self) -> typing.Optional[Expression]:
        return self._name

    @property
    def partition_clause(self) -> typing.Optional[typing.List[Expression]]:
        return self._partition_clause

    @property
    def order_clause(self) -> typing.Optional[OrderClause]:
        return self._order_clause

    @property
    def frame_clause(self) -> typing.Optional[WindowFrame]:
        return self._frame_clause
