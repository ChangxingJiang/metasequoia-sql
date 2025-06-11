"""
固定的枚举类型（fixed enum）
"""

from enum import IntEnum

__all__ = [
    "EnumDropRestrict"
]


class EnumDropRestrict(IntEnum):
    """枚举类型：DROP 语句中的 RESTRICT 选项"""

    DEFAULT = 0
    CASCADE = 1  # 如果尝试删除一个有其他对象依赖的对象，则删除该对象的同时删除依赖该对象的其他对象
    RESTRICT = 2  # 如果尝试删除一个有其他对象依赖的对象，则会报错
