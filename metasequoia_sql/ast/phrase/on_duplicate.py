"""
重复值处理规则（on duplicate）
"""

from enum import IntEnum

__all__ = [
    "OnDuplicate"
]


class OnDuplicate(IntEnum):
    """
    重复值处理规则
    """

    DEFAULT = 0  # 默认值（ERROR）
    IGNORE = 1  # 忽略
    REPLACE = 2  # 替换
