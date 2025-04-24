"""
基础元素节点
"""

import enum

__all__ = [
    "EnumOperatorCompare"
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
