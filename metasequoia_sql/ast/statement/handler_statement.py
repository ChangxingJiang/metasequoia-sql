"""
HANDLER 语句（handler statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement, Expression

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.fixed_enum import EnumHandlerScanFunction, EnumHandlerRkeyFunction, EnumHandlerRkeyMode
    from metasequoia_sql.ast.expression.general_expression import Row
    from metasequoia_sql.ast.clause.limit_clause import LimitClause

__all__ = [
    "HandlerStatement",
    "HandlerOpenStatement",
    "HandlerCloseStatement", 
    "HandlerTableScanStatement",
    "HandlerIndexScanStatement",
    "HandlerIndexRangeScanStatement",
]


class HandlerStatement(Statement):
    """HANDLER 语句的抽象基类"""


class HandlerOpenStatement(HandlerStatement):
    """HANDLER ... OPEN 语句"""

    __slots__ = ["_table_ident", "_table_alias"]

    def __init__(self, table_ident: "Identifier", table_alias: Optional[str]):
        self._table_ident = table_ident
        self._table_alias = table_alias

    @property
    def table_ident(self) -> "Identifier":
        return self._table_ident

    @property
    def table_alias(self) -> Optional[str]:
        return self._table_alias


class HandlerCloseStatement(HandlerStatement):
    """HANDLER ... CLOSE 语句"""

    __slots__ = ["_handler_name"]

    def __init__(self, handler_name: str):
        self._handler_name = handler_name

    @property
    def handler_name(self) -> str:
        return self._handler_name


class HandlerTableScanStatement(HandlerStatement):
    """HANDLER ... READ 表扫描语句"""

    __slots__ = ["_handler_name", "_scan_function", "_where_clause", "_limit_clause"]

    def __init__(self, 
                 handler_name: str,
                 scan_function: "EnumHandlerScanFunction",
                 where_clause: Optional["Expression"],
                 limit_clause: Optional["LimitClause"]):
        self._handler_name = handler_name
        self._scan_function = scan_function
        self._where_clause = where_clause
        self._limit_clause = limit_clause

    @property
    def handler_name(self) -> str:
        return self._handler_name

    @property
    def scan_function(self) -> "EnumHandlerScanFunction":
        return self._scan_function

    @property
    def where_clause(self) -> Optional["Expression"]:
        return self._where_clause

    @property
    def limit_clause(self) -> Optional["LimitClause"]:
        return self._limit_clause


class HandlerIndexScanStatement(HandlerStatement):
    """HANDLER ... READ 索引扫描语句"""

    __slots__ = ["_handler_name", "_index_name", "_rkey_function", "_where_clause", "_limit_clause"]

    def __init__(self,
                 handler_name: str,
                 index_name: str,
                 rkey_function: "EnumHandlerRkeyFunction",
                 where_clause: Optional["Expression"],
                 limit_clause: Optional["LimitClause"]):
        self._handler_name = handler_name
        self._index_name = index_name
        self._rkey_function = rkey_function
        self._where_clause = where_clause
        self._limit_clause = limit_clause

    @property
    def handler_name(self) -> str:
        return self._handler_name

    @property
    def index_name(self) -> str:
        return self._index_name

    @property
    def rkey_function(self) -> "EnumHandlerRkeyFunction":
        return self._rkey_function

    @property
    def where_clause(self) -> Optional["Expression"]:
        return self._where_clause

    @property
    def limit_clause(self) -> Optional["LimitClause"]:
        return self._limit_clause


class HandlerIndexRangeScanStatement(HandlerStatement):
    """HANDLER ... READ 索引范围扫描语句"""

    __slots__ = ["_handler_name", "_index_name", "_rkey_mode", "_values", "_where_clause", "_limit_clause"]

    def __init__(self,
                 handler_name: str,
                 index_name: str,
                 rkey_mode: "EnumHandlerRkeyMode",
                 values: List["Row"],
                 where_clause: Optional["Expression"],
                 limit_clause: Optional["LimitClause"]):
        self._handler_name = handler_name
        self._index_name = index_name
        self._rkey_mode = rkey_mode
        self._values = values
        self._where_clause = where_clause
        self._limit_clause = limit_clause

    @property
    def handler_name(self) -> str:
        return self._handler_name

    @property
    def index_name(self) -> str:
        return self._index_name

    @property
    def rkey_mode(self) -> "EnumHandlerRkeyMode":
        return self._rkey_mode

    @property
    def values(self) -> List["Row"]:
        return self._values

    @property
    def where_clause(self) -> Optional["Expression"]:
        return self._where_clause

    @property
    def limit_clause(self) -> Optional["LimitClause"]:
        return self._limit_clause 