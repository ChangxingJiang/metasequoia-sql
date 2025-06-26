"""
HANDLER 语句（handler statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.fixed_enum import EnumHandlerScanFunction, EnumHandlerRkeyFunction, \
        EnumHandlerRkeyMode
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
        """
        表标识符

        Returns
        -------
        Identifier
            表标识符
        """
        return self._table_ident

    @property
    def table_alias(self) -> Optional[str]:
        """
        表别名

        Returns
        -------
        Optional[str]
            表别名
        """
        return self._table_alias


class HandlerCloseStatement(HandlerStatement):
    """HANDLER ... CLOSE 语句"""

    __slots__ = ["_handler_name"]

    def __init__(self, handler_name: str):
        self._handler_name = handler_name

    @property
    def handler_name(self) -> str:
        """
        处理器名称

        Returns
        -------
        str
            处理器名称
        """
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
        """
        处理器名称

        Returns
        -------
        str
            处理器名称
        """
        return self._handler_name

    @property
    def scan_function(self) -> "EnumHandlerScanFunction":
        """
        扫描函数类型

        Returns
        -------
        EnumHandlerScanFunction
            扫描函数类型
        """
        return self._scan_function

    @property
    def where_clause(self) -> Optional["Expression"]:
        """
        WHERE 子句

        Returns
        -------
        Optional[Expression]
            WHERE 子句
        """
        return self._where_clause

    @property
    def limit_clause(self) -> Optional["LimitClause"]:
        """
        LIMIT 子句

        Returns
        -------
        Optional[LimitClause]
            LIMIT 子句
        """
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
        # pylint: disable=R0913
        self._handler_name = handler_name
        self._index_name = index_name
        self._rkey_function = rkey_function
        self._where_clause = where_clause
        self._limit_clause = limit_clause

    @property
    def handler_name(self) -> str:
        """
        处理器名称

        Returns
        -------
        str
            处理器名称
        """
        return self._handler_name

    @property
    def index_name(self) -> str:
        """
        索引名称

        Returns
        -------
        str
            索引名称
        """
        return self._index_name

    @property
    def rkey_function(self) -> "EnumHandlerRkeyFunction":
        """
        记录键函数类型

        Returns
        -------
        EnumHandlerRkeyFunction
            记录键函数类型
        """
        return self._rkey_function

    @property
    def where_clause(self) -> Optional["Expression"]:
        """
        WHERE 子句

        Returns
        -------
        Optional[Expression]
            WHERE 子句
        """
        return self._where_clause

    @property
    def limit_clause(self) -> Optional["LimitClause"]:
        """
        LIMIT 子句

        Returns
        -------
        Optional[LimitClause]
            LIMIT 子句
        """
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
        # pylint: disable=R0913
        self._handler_name = handler_name
        self._index_name = index_name
        self._rkey_mode = rkey_mode
        self._values = values
        self._where_clause = where_clause
        self._limit_clause = limit_clause

    @property
    def handler_name(self) -> str:
        """
        处理器名称

        Returns
        -------
        str
            处理器名称
        """
        return self._handler_name

    @property
    def index_name(self) -> str:
        """
        索引名称

        Returns
        -------
        str
            索引名称
        """
        return self._index_name

    @property
    def rkey_mode(self) -> "EnumHandlerRkeyMode":
        """
        记录键模式

        Returns
        -------
        EnumHandlerRkeyMode
            记录键模式
        """
        return self._rkey_mode

    @property
    def values(self) -> List["Row"]:
        """
        值列表

        Returns
        -------
        List[Row]
            值列表
        """
        return self._values

    @property
    def where_clause(self) -> Optional["Expression"]:
        """
        WHERE 子句

        Returns
        -------
        Optional[Expression]
            WHERE 子句
        """
        return self._where_clause

    @property
    def limit_clause(self) -> Optional["LimitClause"]:
        """
        LIMIT 子句

        Returns
        -------
        Optional[LimitClause]
            LIMIT 子句
        """
        return self._limit_clause
