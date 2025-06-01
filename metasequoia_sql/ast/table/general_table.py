"""
通用表逻辑（general table）
"""

from metasequoia_sql.ast.base import Table

__all__ = [
    "DualTable"
]


class DualTable(Table):
    """虚拟表"""
