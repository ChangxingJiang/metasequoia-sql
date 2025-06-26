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
        """初始化排序字段
        
        Parameters
        ----------
        column : Expression
            排序列表达式
        direction : EnumOrderDirection
            排序方向
        """
        self._column = column
        self._direction = direction

    @property
    def column(self) -> Expression:
        """获取排序列表达式
        
        Returns
        -------
        Expression
            排序列表达式
        """
        return self._column

    @property
    def direction(self) -> EnumOrderDirection:
        """获取排序方向
        
        Returns
        -------
        EnumOrderDirection
            排序方向
        """
        return self._direction


class OrderByClause(Node):
    """ORDER BY 子句"""

    __slots__ = ["_column_list"]

    def __init__(self, column_list: List[OrderExpression]):
        """初始化 ORDER BY 子句
        
        Parameters
        ----------
        column_list : List[OrderExpression]
            排序字段列表
        """
        self._column_list = column_list

    @property
    def column_list(self) -> List[OrderExpression]:
        """获取排序字段列表
        
        Returns
        -------
        List[OrderExpression]
            排序字段列表
        """
        return self._column_list

    def append(self, column: OrderExpression) -> "OrderByClause":
        """添加排序字段
        
        Parameters
        ----------
        column : OrderExpression
            要添加的排序字段
            
        Returns
        -------
        OrderByClause
            当前 ORDER BY 子句实例
        """
        self._column_list.append(column)
        return self
