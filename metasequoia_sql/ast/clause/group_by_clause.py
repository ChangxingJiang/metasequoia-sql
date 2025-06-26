"""
GROUP BY 子句（group by clause）
"""

from enum import IntEnum
from typing import List

from metasequoia_sql.ast.base import Expression, Node

__all__ = [
    "EnumOlapOpt",
    "GroupByClause",
]


class EnumOlapOpt(IntEnum):
    """GROUP BY 子句中的分组统计信息规则"""

    DEFAULT = 0  # %empty
    ROLLUP = 1  # ROLLUP 或 WITH_ROLLUP
    CUBE = 2  # CUBE


class GroupByClause(Node):
    """GROUP BY 子句"""

    __slots__ = ["_columns", "_olap_opt"]

    def __init__(self, columns: List[Expression], olap_opt: EnumOlapOpt) -> None:
        """初始化 GROUP BY 子句
        
        Parameters
        ----------
        columns : List[Expression]
            分组列表达式列表
        olap_opt : EnumOlapOpt
            OLAP 选项
        """
        self._columns = columns
        self._olap_opt = olap_opt

    @property
    def columns(self) -> List[Expression]:
        """获取分组列表达式列表
        
        Returns
        -------
        List[Expression]
            分组列表达式列表
        """
        return self._columns

    @property
    def olap_opt(self) -> EnumOlapOpt:
        """获取 OLAP 选项
        
        Returns
        -------
        EnumOlapOpt
            OLAP 选项
        """
        return self._olap_opt
