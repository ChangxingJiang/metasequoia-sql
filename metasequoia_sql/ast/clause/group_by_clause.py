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

    def __init__(self, columns: List[Expression], olap_opt: EnumOlapOpt) -> None:
        self._columns = columns
        self._olap_opt = olap_opt

    def attr_list(self) -> List[str]:
        return ["columns", "olap_opt"]

    @property
    def columns(self) -> List[Expression]:
        return self._columns

    @property
    def olap_opt(self) -> EnumOlapOpt:
        return self._olap_opt
