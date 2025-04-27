"""
DQL 语句节点
"""

import typing
from typing import List

from metasequoia_sql_new.ast.base import Expression
from metasequoia_sql_new.ast.base import Node
from metasequoia_sql_new.ast.basic import EnumOrderDirection

__all__ = [
    "GroupByList",
    "OrderExpression",
    "OrderByList",
]


class GroupByList(Node):
    """分组字段列表（用于 GROUP BY 子句和 PARTITION BY 子句）"""

    def __init__(self, column_list: List[Expression]):
        self._column_list = column_list

    def attr_list(self) -> typing.List[str]:
        return ["column_list"]

    @property
    def column_list(self) -> List[Expression]:
        return self._column_list

    def append(self, column: Expression) -> "GroupByList":
        self._column_list.append(column)
        return self


class OrderExpression(Node):
    """排序字段（用于 ORDER BY 子句）"""

    def __init__(self, column: Expression, direction: EnumOrderDirection):
        self._column = column
        self._direction = direction

    def attr_list(self) -> typing.List[str]:
        return ["column", "direction"]

    @property
    def column(self) -> Expression:
        return self._column

    @property
    def direction(self) -> EnumOrderDirection:
        return self._direction


class OrderByList(Node):
    """排序字段的列表（用于 ORDER BY 子句）"""

    def __init__(self, column_list: List[OrderExpression]):
        self._column_list = column_list

    def attr_list(self) -> typing.List[str]:
        return ["column_list"]

    @property
    def column_list(self) -> List[OrderExpression]:
        return self._column_list

    def append(self, column: OrderExpression) -> "OrderByList":
        self._column_list.append(column)
        return self
