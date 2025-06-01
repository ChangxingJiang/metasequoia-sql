"""
SELECT 语句（select statement）
"""

from enum import IntFlag
from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Query, Table

if TYPE_CHECKING:
    from metasequoia_sql.ast.clause.into_clause import IntoClause
    from metasequoia_sql.ast.clause.group_by_clause import GroupByClause
    from metasequoia_sql.ast.clause.over_clause import Window
    from metasequoia_sql.ast.basic.ident import Ident

__all__ = [
    "SelectOption",
    "SimpleQuery",
    "ExplicitTable",
]


class SelectOption(IntFlag):
    """查询选项"""

    DEFAULT = 0
    STRAIGHT_JOIN = 1 << 0  # STRAIGHT_JOIN
    HIGH_PRIORITY = 1 << 1  # HIGH_PRIORITY
    DISTINCT = 1 << 2  # DISTINCT
    SQL_SMALL_RESULT = 1 << 3  # SQL_SMALL_RESULT
    SQL_BIG_RESULT = 1 << 4  # SQL_BIG_RESULT
    SQL_BUFFER_RESULT = 1 << 5  # SQL_BUFFER_RESULT
    SQL_CALC_FOUND_ROWS = 1 << 6  # SQL_CALC_FOUND_ROWS
    ALL = 1 << 7  # ALL
    SQL_NO_CACHE = 1 << 8  # SQL_NO_CACHE


class SimpleQuery(Query):
    """基础查询（包括查询选项、查询字段表达式、INTO 子句、FROM 子句、WHERE 子句、GROUP BY 子句、HAVING 子句、WINDOW 子句和 QUALIFY 子句）"""

    __slots__ = ["_select_option", "_select_item_list", "_into_clause", "_from_clause", "_where_clause",
                 "_group_by_clause", "_having_clause", "_window_clause", "_qualify_clause"]

    def __init__(self,
                 select_option: SelectOption,
                 select_item_list: List[Expression],
                 into_clause: Optional["IntoClause"],
                 from_clause: Optional[List[Table]],
                 where_clause: Optional[Expression],
                 group_by_clause: Optional["GroupByClause"],
                 having_clause: Optional[Expression],
                 window_clause: Optional[List["Window"]],
                 qualify_clause: Optional[Expression]
                 ):
        self._select_option = select_option
        self._select_item_list = select_item_list
        self._into_clause = into_clause
        self._from_clause = from_clause
        self._where_clause = where_clause
        self._group_by_clause = group_by_clause
        self._having_clause = having_clause
        self._window_clause = window_clause
        self._qualify_clause = qualify_clause

    @property
    def select_option(self) -> SelectOption:
        return self._select_option

    @property
    def select_item_list(self) -> List[Expression]:
        return self._select_item_list

    @property
    def into_clause(self) -> Optional["IntoClause"]:
        return self._into_clause

    @property
    def from_clause(self) -> Optional[List[Table]]:
        return self._from_clause

    @property
    def where_clause(self) -> Optional[Expression]:
        return self._where_clause

    @property
    def group_by_clause(self) -> Optional["GroupByClause"]:
        return self._group_by_clause

    @property
    def having_clause(self) -> Optional[Expression]:
        return self._having_clause

    @property
    def window_clause(self) -> Optional[List["Window"]]:
        return self._window_clause

    @property
    def quality_clause(self) -> Optional[Expression]:
        return self._qualify_clause


class ExplicitTable(Query):
    """明确指定表的查询"""

    __slots__ = ["_table_ident"]

    def __init__(self, table_ident: "Ident"):
        self._table_ident = table_ident

    @property
    def table_ident(self) -> "Ident":
        return self._table_ident
