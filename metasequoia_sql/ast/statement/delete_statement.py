"""
DELETE 语句（delete statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Statement, Table

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import TableIdent
    from metasequoia_sql.ast.clause.order_by_clause import OrderByClause
    from metasequoia_sql.ast.clause.limit_clause import LimitClause
    from metasequoia_sql.ast.clause.with_clause import WithClause
    from metasequoia_sql.ast.phrase.dml_option import DmlOption

__all__ = [
    "DeleteStatement",
    "DeleteFromStatement",
    "DeleteColumnFromStatement",
    "DeleteFromUsingStatement",
]


class DeleteStatement(Statement):
    """DELETE 语句的抽象类"""


class DeleteFromStatement(DeleteStatement):
    """DELETE ... FROM ... 格式的 DELETE 语句"""

    __slots__ = (
        "_with_clause",
        "_options",
        "_table_name",
        "_table_alias",
        "_use_partition",
        "_where_clause",
        "_order_by_clause",
        "_limit_clause"
    )

    def __init__(self,
                 with_clause: Optional["WithClause"],
                 options: "DmlOption",
                 table_name: "TableIdent",
                 table_alias: Optional[str],
                 use_partition: Optional[List[Expression]],
                 where_clause: Optional[Expression],
                 order_by_clause: Optional["OrderByClause"],
                 limit_clause: Optional["LimitClause"]):
        self._with_clause = with_clause
        self._options = options
        self._table_name = table_name
        self._table_alias = table_alias
        self._use_partition = use_partition
        self._where_clause = where_clause
        self._order_by_clause = order_by_clause
        self._limit_clause = limit_clause

    @property
    def with_clause(self) -> Optional["WithClause"]:
        return self._with_clause

    @property
    def options(self) -> "DmlOption":
        return self._options

    @property
    def table_name(self) -> "TableIdent":
        return self._table_name

    @property
    def table_alias(self) -> Optional[str]:
        return self._table_alias

    @property
    def use_partition(self) -> Optional[List[Expression]]:
        return self._use_partition

    @property
    def where_clause(self) -> Optional[Expression]:
        return self._where_clause

    @property
    def order_by_clause(self) -> Optional["OrderByClause"]:
        return self._order_by_clause

    @property
    def limit_clause(self) -> Optional["LimitClause"]:
        return self._limit_clause


class DeleteColumnFromStatement(DeleteStatement):
    """DELETE ... table.*, table.* FROM ... 格式的 DELETE 语句"""

    __slots__ = (
        "_with_clause",
        "_options",
        "_wild_table_list",
        "_from_table_list",
        "_where_clause"
    )

    def __init__(self,
                 with_clause: Optional["WithClause"],
                 options: "DmlOption",
                 wild_table_list: List["TableIdent"],
                 from_table_list: List[Table],
                 where_clause: Optional[Expression]
                 ):
        self._with_clause = with_clause
        self._options = options
        self._wild_table_list = wild_table_list
        self._from_table_list = from_table_list
        self._where_clause = where_clause

    @property
    def with_clause(self) -> Optional["WithClause"]:
        return self._with_clause

    @property
    def options(self) -> "DmlOption":
        return self._options

    @property
    def wild_table_list(self) -> List["TableIdent"]:
        return self._wild_table_list

    @property
    def from_table_list(self) -> List[Table]:
        return self._from_table_list

    @property
    def where_clause(self) -> Optional[Expression]:
        return self._where_clause


class DeleteFromUsingStatement(DeleteStatement):
    """DELETE... FROM... USING... 格式的 DELETE 语句"""

    __slots__ = (
        "_with_clause",
        "_options",
        "_from_table_list",
        "_using_table_list",
        "_where_clause"
    )

    def __init__(self,
                 with_clause: Optional["WithClause"],
                 options: "DmlOption",
                 from_table_list: List["TableIdent"],
                 using_table_list: List[Table],
                 where_clause: Optional[Expression]
                 ):
        self._with_clause = with_clause
        self._options = options
        self._from_table_list = from_table_list
        self._using_table_list = using_table_list
        self._where_clause = where_clause

    @property
    def with_clause(self) -> Optional["WithClause"]:
        return self._with_clause

    @property
    def options(self) -> "DmlOption":
        return self._options

    @property
    def from_table_list(self) -> List["TableIdent"]:
        return self._from_table_list

    @property
    def using_table_list(self) -> List[Table]:
        return self._using_table_list

    @property
    def where_clause(self) -> Optional[Expression]:
        return self._where_clause
