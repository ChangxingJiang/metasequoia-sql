"""
ORDER BY 语句节点
"""

from enum import IntEnum, auto
from typing import List

from metasequoia_sql.ast.base import Expression
from metasequoia_sql.ast.base import Node

__all__ = [
    "EnumOrderDirection",
    "OrderExpression",
    "OrderByClause",
]


class EnumOrderDirection(IntEnum):
    """排序方向"""

    ASC = auto()  # 升序
    DESC = auto()  # 降序
    DEFAULT = auto()  # 没有明确指定排序方向


class OrderExpression(Node):
    """排序字段（用于 ORDER BY 子句）"""

    __slots__ = ["_column", "_direction"]

    def __init__(self, column: Expression, direction: EnumOrderDirection):
        self._column = column
        self._direction = direction

    @property
    def column(self) -> Expression:
        return self._column

    @property
    def direction(self) -> EnumOrderDirection:
        return self._direction


class OrderByClause(Node):
    """ORDER BY 子句"""

    __slots__ = ["_column_list"]

    def __init__(self, column_list: List[OrderExpression]):
        self._column_list = column_list

    @property
    def column_list(self) -> List[OrderExpression]:
        return self._column_list

    def append(self, column: OrderExpression) -> "OrderByClause":
        self._column_list.append(column)
        return self
