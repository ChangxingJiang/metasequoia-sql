"""
UPDATE 语句（update statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node, Statement, Table

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Ident
    from metasequoia_sql.ast.clause.order_by_clause import OrderByClause
    from metasequoia_sql.ast.clause.limit_clause import LimitClause
    from metasequoia_sql.ast.clause.with_clause import WithClause
    from metasequoia_sql.ast.phrase.dml_option import DmlOption

__all__ = [
    "UpdateElement",
    "UpdateStatement",
]


class UpdateElement(Node):
    """UPDATE 语句中的更新项"""

    __slots__ = ("_column_name", "_column_value")

    def __init__(self, column_name: "Ident", column_value: Expression):
        self._column_name = column_name
        self._column_value = column_value

    @property
    def column_name(self) -> "Ident":
        return self._column_name

    @property
    def column_value(self) -> Expression:
        return self._column_value


class UpdateStatement(Statement):
    """UPDATE 语句"""

    __slots__ = (
        "_with_clause",
        "_dml_option",
        "_table_list",
        "_update_list",
        "_where_clause",
        "_order_by_clause",
        "_limit_clause"
    )

    def __init__(self,
                 with_clause: Optional["WithClause"],
                 options: Optional["DmlOption"],
                 table_list: List[Table],
                 update_list: List[UpdateElement],
                 where_clause: Optional[Expression],
                 order_by_clause: Optional["OrderByClause"],
                 limit_clause: Optional["LimitClause"]
                 ):
        self._with_clause = with_clause
        self._dml_option = options
        self._table_list = table_list
        self._update_list = update_list
        self._where_clause = where_clause
        self._order_by_clause = order_by_clause
        self._limit_clause = limit_clause

    @property
    def with_clause(self) -> Optional["WithClause"]:
        return self._with_clause

    @property
    def dml_option(self) -> Optional["DmlOption"]:
        return self._dml_option

    @property
    def table_list(self) -> List[Table]:
        return self._table_list

    @property
    def update_list(self) -> List[UpdateElement]:
        return self._update_list

    @property
    def where_clause(self) -> Optional[Expression]:
        return self._where_clause

    @property
    def order_by_clause(self) -> Optional["OrderByClause"]:
        return self._order_by_clause

    @property
    def limit_clause(self) -> Optional["LimitClause"]:
        return self._limit_clause
