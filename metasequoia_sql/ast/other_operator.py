"""
基础元素节点
"""

import enum

__all__ = [
    "EnumOrderDirection",
]


class EnumOrderDirection(enum.IntEnum):
    """排序方向"""

    ASC = enum.auto()  # 升序
    DESC = enum.auto()  # 降序
    DEFAULT = enum.auto()  # 没有明确指定排序方向
