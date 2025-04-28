"""
基础元素节点
"""

import enum

__all__ = [
    "EnumOperatorCompare",
    "EnumOrderDirection",
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
