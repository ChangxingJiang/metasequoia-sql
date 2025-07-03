"""
窗口函数的节点
"""

import enum
from typing import List, Optional

from metasequoia_sql.ast.base import Expression
from metasequoia_sql.ast.base import Node
from metasequoia_sql.ast.basic.time_unit import TimeUnitEnum
from metasequoia_sql.ast.clause.order_by_clause import OrderByClause

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

    __slots__ = ["_boundary_type", "_value", "_time_unit"]

    def __init__(self, boundary_type: WindowBoundaryTypeEnum,
                 value: Optional[Expression] = None,
                 time_unit: Optional[TimeUnitEnum] = None):
        """初始化窗口边界
        
        Parameters
        ----------
        boundary_type : WindowBoundaryTypeEnum
            边界类型
        value : Optional[Expression], optional
            边界值表达式, by default None
        time_unit : Optional[TimeUnitEnum], optional
            时间单位, by default None
        """
        self._boundary_type = boundary_type
        self._value = value
        self._time_unit = time_unit

    @staticmethod
    def create_unbounded_preceding() -> "WindowBorder":
        """创建 UNBOUNDED PRECEDING 边界
        
        Returns
        -------
        WindowBorder
            窗口边界实例
        """
        return WindowBorder(
            boundary_type=WindowBoundaryTypeEnum.UNBOUNDED_PRECEDING
        )

    @staticmethod
    def create_value_preceding(value: Expression) -> "WindowBorder":
        """创建 VALUE PRECEDING 边界
        
        Parameters
        ----------
        value : Expression
            边界值表达式
            
        Returns
        -------
        WindowBorder
            窗口边界实例
        """
        return WindowBorder(
            boundary_type=WindowBoundaryTypeEnum.VALUE_PRECEDING,
            value=value
        )

    @staticmethod
    def create_interval_preceding(value: Expression, time_unit: TimeUnitEnum) -> "WindowBorder":
        """创建 INTERVAL PRECEDING 边界
        
        Parameters
        ----------
        value : Expression
            间隔值表达式
        time_unit : TimeUnitEnum
            时间单位
            
        Returns
        -------
        WindowBorder
            窗口边界实例
        """
        return WindowBorder(
            boundary_type=WindowBoundaryTypeEnum.INTERVAL_PRECEDING,
            value=value,
            time_unit=time_unit
        )

    @staticmethod
    def create_current_row() -> "WindowBorder":
        """创建 CURRENT ROW 边界
        
        Returns
        -------
        WindowBorder
            窗口边界实例
        """
        return WindowBorder(
            boundary_type=WindowBoundaryTypeEnum.CURRENT_ROW
        )

    @staticmethod
    def create_unbounded_following() -> "WindowBorder":
        """创建 UNBOUNDED FOLLOWING 边界
        
        Returns
        -------
        WindowBorder
            窗口边界实例
        """
        return WindowBorder(
            boundary_type=WindowBoundaryTypeEnum.UNBOUNDED_FOLLOWING
        )

    @staticmethod
    def create_value_following(value: Expression) -> "WindowBorder":
        """创建 VALUE FOLLOWING 边界
        
        Parameters
        ----------
        value : Expression
            边界值表达式
            
        Returns
        -------
        WindowBorder
            窗口边界实例
        """
        return WindowBorder(
            boundary_type=WindowBoundaryTypeEnum.VALUE_FOLLOWING,
            value=value
        )

    @staticmethod
    def create_interval_following(value: Expression, time_unit: TimeUnitEnum) -> "WindowBorder":
        """创建 INTERVAL FOLLOWING 边界
        
        Parameters
        ----------
        value : Expression
            间隔值表达式
        time_unit : TimeUnitEnum
            时间单位
            
        Returns
        -------
        WindowBorder
            窗口边界实例
        """
        return WindowBorder(
            boundary_type=WindowBoundaryTypeEnum.INTERVAL_FOLLOWING,
            value=value,
            time_unit=time_unit
        )

    @property
    def boundary_type(self) -> WindowBoundaryTypeEnum:
        """获取边界类型
        
        Returns
        -------
        WindowBoundaryTypeEnum
            边界类型
        """
        return self._boundary_type

    @property
    def value(self) -> Optional[Expression]:
        """获取边界值表达式
        
        Returns
        -------
        Optional[Expression]
            边界值表达式
        """
        return self._value

    @property
    def time_unit(self) -> Optional[TimeUnitEnum]:
        """获取时间单位
        
        Returns
        -------
        Optional[TimeUnitEnum]
            时间单位
        """
        return self._time_unit


class WindowBorders(Node):
    """窗口的两侧边界值

    {start_border}
    BETWEEN {start_border} AND {end_border}
    """

    __slots__ = ["_start_border", "_end_border"]

    def __init__(self, start_border: WindowBorder, end_border: WindowBorder):
        """初始化窗口两侧边界
        
        Parameters
        ----------
        start_border : WindowBorder
            开始边界
        end_border : WindowBorder
            结束边界
        """
        self._start_border = start_border
        self._end_border = end_border

    @staticmethod
    def create_by_start_border(start_border: WindowBorder) -> "WindowBorders":
        """通过开始边界创建窗口边界，结束边界默认为 CURRENT ROW
        
        Parameters
        ----------
        start_border : WindowBorder
            开始边界
            
        Returns
        -------
        WindowBorders
            窗口边界实例
        """
        return WindowBorders(
            start_border=start_border,
            end_border=WindowBorder.create_current_row()
        )

    @property
    def start_border(self) -> WindowBorder:
        """获取开始边界
        
        Returns
        -------
        WindowBorder
            开始边界
        """
        return self._start_border

    @property
    def end_border(self) -> WindowBorder:
        """获取结束边界
        
        Returns
        -------
        WindowBorder
            结束边界
        """
        return self._end_border


class WindowFrame(Node):
    """窗口框架子句（包括边界类型、边界值、排除值）"""

    __slots__ = ["_border_type", "_borders", "_exclusion"]

    def __init__(self,
                 border_type: WindowBorderTypeEnum,
                 borders: WindowBorders,
                 exclusion: WindowExclusionTypeEnum):
        """初始化窗口框架子句
        
        Parameters
        ----------
        border_type : WindowBorderTypeEnum
            边界类型
        borders : WindowBorders
            窗口边界
        exclusion : WindowExclusionTypeEnum
            排除类型
        """
        self._border_type = border_type
        self._borders = borders
        self._exclusion = exclusion

    @property
    def border_type(self) -> WindowBorderTypeEnum:
        """获取边界类型
        
        Returns
        -------
        WindowBorderTypeEnum
            边界类型
        """
        return self._border_type

    @property
    def borders(self) -> WindowBorders:
        """获取窗口边界
        
        Returns
        -------
        WindowBorders
            窗口边界
        """
        return self._borders

    @property
    def exclusion(self) -> WindowExclusionTypeEnum:
        """获取排除类型
        
        Returns
        -------
        WindowExclusionTypeEnum
            排除类型
        """
        return self._exclusion


class Window(Node):
    """窗口（包括可选的窗口名称、可选的 PARTITION BY 子句、可选的 ORDER BY 子句和可选的窗口框架子句"""

    __slots__ = ["_name", "_partition_clause", "_order_clause", "_frame_clause"]

    def __init__(self,
                 name: Optional[str],
                 partition_clause: Optional[List[Expression]],
                 order_clause: Optional[OrderByClause],
                 frame_clause: Optional[WindowFrame]):
        """初始化窗口
        
        Parameters
        ----------
        name : Optional[str]
            窗口名称
        partition_clause : Optional[List[Expression]]
            分区子句表达式列表
        order_clause : Optional[OrderByClause]
            排序子句
        frame_clause : Optional[WindowFrame]
            窗口框架子句
        """
        self._name = name
        self._partition_clause = partition_clause
        self._order_clause = order_clause
        self._frame_clause = frame_clause

    @staticmethod
    def create_by_name(name: str) -> "Window":
        """通过名称创建窗口
        
        Parameters
        ----------
        name : str
            窗口名称
            
        Returns
        -------
        Window
            窗口实例
        """
        return Window(
            name=name,
            partition_clause=None,
            order_clause=None,
            frame_clause=None
        )

    @property
    def name(self) -> Optional[str]:
        """获取窗口名称
        
        Returns
        -------
        Optional[str]
            窗口名称
        """
        return self._name

    @property
    def partition_clause(self) -> Optional[List[Expression]]:
        """获取分区子句表达式列表
        
        Returns
        -------
        Optional[List[Expression]]
            分区子句表达式列表
        """
        return self._partition_clause

    @property
    def order_clause(self) -> Optional[OrderByClause]:
        """获取排序子句
        
        Returns
        -------
        Optional[OrderByClause]
            排序子句
        """
        return self._order_clause

    @property
    def frame_clause(self) -> Optional[WindowFrame]:
        """获取窗口框架子句
        
        Returns
        -------
        Optional[WindowFrame]
            窗口框架子句
        """
        return self._frame_clause
