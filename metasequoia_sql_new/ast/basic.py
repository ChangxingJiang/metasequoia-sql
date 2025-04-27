"""
基础元素节点
"""

import enum

__all__ = [
    "EnumOperatorCompare",
    "EnumOrderDirection",
    "EnumWindowBorderType",
]


class EnumOperatorCompare(enum.IntEnum):
    """比较运算符的枚举类"""

    EQ = enum.auto()  # =
    EQUAL = enum.auto()  # <=>
    GE = enum.auto()  # >=
    GT = enum.auto()  # >
    LE = enum.auto()  # <=
    LT = enum.auto()  # <
    NE = enum.auto()  # <> 或 !=


class EnumOrderDirection(enum.IntEnum):
    """排序方向"""

    ASC = enum.auto()  # 升序
    DESC = enum.auto()  # 降序
    DEFAULT = enum.auto()  # 没有明确指定排序方向


class EnumWindowBorderType(enum.IntEnum):
    """窗口边界类型"""

    ROWS = enum.auto()  # 基于物理行来定义窗口的边界
    RANGE = enum.auto()  # 基于值的范围来定义窗口的边界
    GROUPS = enum.auto()  # 基于分组键的值来定义窗口的边界
