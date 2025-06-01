"""
WITH 子句（with clause）
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.statement.select_statement import QueryExpression

__all__ = [
    "WithTable",
    "WithClause"
]


class WithTable(Node):
    """WITH 子句中的表"""

    __slots__ = ["_table_name", "_column_list", "_query_expression"]

    def __init__(self, table_name: str, column_list: List[str], query_expression: "QueryExpression"):
        self._table_name = table_name
        self._column_list = column_list
        self._query_expression = query_expression

    @property
    def table_name(self) -> str:
        return self._table_name

    @property
    def column_list(self) -> List[str]:
        return self._column_list

    @property
    def query_expression(self) -> "QueryExpression":
        return self._query_expression


class WithClause(Node):
    """WITH 子句"""

    __slots__ = ["_table_list", "_recursive"]

    def __init__(self, table_list: List[WithTable], recursive: bool):
        self._table_list = table_list
        self._recursive = recursive

    @property
    def table_list(self) -> List[WithTable]:
        return self._table_list

    @property
    def recursive(self) -> bool:
        return self._recursive
