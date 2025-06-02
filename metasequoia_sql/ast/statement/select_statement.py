"""
SELECT 语句（select statement）
"""

from enum import IntEnum, IntFlag
from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node, QueryBody, Statement, Table

if TYPE_CHECKING:
    from metasequoia_sql.ast.clause.into_clause import IntoClause
    from metasequoia_sql.ast.clause.group_by_clause import GroupByClause
    from metasequoia_sql.ast.clause.over_clause import Window
    from metasequoia_sql.ast.basic.ident import TableIdent
    from metasequoia_sql.ast.expression.general_expression import Row
    from metasequoia_sql.ast.clause.order_by_clause import OrderByClause
    from metasequoia_sql.ast.clause.limit_clause import LimitClause
    from metasequoia_sql.ast.clause.locking_clause import LockingClause
    from metasequoia_sql.ast.clause.with_clause import WithClause

__all__ = [
    "SelectOption",
    "SimpleQuery",
    "TableValueConstructor",
    "ExplicitTable",
    "UnionOption",
    "UnionBase",
    "Union",
    "Except",
    "Intersect",
    "QueryExpression",
    "SelectStatement",
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


class SimpleQuery(QueryBody):
    """简单查询（包括查询选项、查询字段表达式、INTO 子句、FROM 子句、WHERE 子句、GROUP BY 子句、HAVING 子句、WINDOW 子句和 QUALIFY 子句）"""

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


class TableValueConstructor(QueryBody):
    """通过值列表构造的表"""

    __slots__ = ["_row_list"]

    def __init__(self, row_list: List["Row"]):
        self._row_list = row_list

    @property
    def row_list(self) -> List["Row"]:
        return self._row_list


class ExplicitTable(QueryBody):
    """明确指定表的查询"""

    __slots__ = ["_table_ident"]

    def __init__(self, table_ident: "TableIdent"):
        self._table_ident = table_ident

    @property
    def table_ident(self) -> "TableIdent":
        return self._table_ident


class UnionOption(IntEnum):
    """联合类型"""

    DEFAULT = 0  # %empty
    DISTINCT = 1  # DISTINCT
    ALL = 2  # ALL


class UnionBase(QueryBody):
    """联合的抽象类"""

    __slots__ = ["_left_operand", "_union_option", "_right_operand"]

    def __init__(self, left_operand: QueryBody, union_option: UnionOption, right_operand: QueryBody):
        self._left_operand = left_operand
        self._union_option = union_option
        self._right_operand = right_operand

    @property
    def left_operand(self) -> QueryBody:
        return self._left_operand

    @property
    def union_option(self) -> UnionOption:
        return self._union_option

    @property
    def right_operand(self) -> QueryBody:
        return self._right_operand


class Union(UnionBase):
    """UNION 联合"""


class Except(UnionBase):
    """EXCEPT 联合"""


class Intersect(UnionBase):
    """INTERSECT 联合"""


class QueryExpression(Node):
    """查询表达式"""

    __slots__ = ["_with_clause", "_query_body", "_order_clause", "_limit_clause", "_locking_clause_list"]

    def __init__(self,
                 with_clause: Optional["WithClause"],
                 query_body: QueryBody,
                 order_by_clause: Optional["OrderByClause"],
                 limit_clause: Optional["LimitClause"],
                 locking_clause_list: Optional[List["LockingClause"]] = None):
        if locking_clause_list is None:
            locking_clause_list = []

        self._with_clause = with_clause
        self._query_body = query_body
        self._order_clause = order_by_clause
        self._limit_clause = limit_clause
        self._locking_clause_list: List["LockingClause"] = locking_clause_list

    @property
    def with_clause(self) -> Optional["WithClause"]:
        return self._with_clause

    @property
    def query_body(self) -> QueryBody:
        return self._query_body

    @property
    def order_clause(self) -> Optional["OrderByClause"]:
        return self._order_clause

    @property
    def limit_clause(self) -> Optional["LimitClause"]:
        return self._limit_clause

    @property
    def locking_clause_list(self) -> List["LockingClause"]:
        return self._locking_clause_list

    def set_locking_clause(self, locking_clause_list: List["LockingClause"]) -> "QueryExpression":
        self._locking_clause_list = locking_clause_list
        return self


class SelectStatement(Statement):
    """SELECT 语句

    【不兼容】不允许在 `SELECT` 语句的最外层添加 `INTO` 子句，仅允许在`FROM` 子句前添加 `INTO` 子句。
    """

    __slots__ = ["_query_expression"]

    def __init__(self, query_expression: QueryExpression):
        self._query_expression = query_expression

    @property
    def query_expression(self) -> QueryExpression:
        return self._query_expression
