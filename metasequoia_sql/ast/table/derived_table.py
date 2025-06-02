"""
派生表（derived table）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Table

if TYPE_CHECKING:
    from metasequoia_sql.ast.statement.select_statement import QueryExpression

__all__ = [
    "DerivedTable"
]


class DerivedTable(Table):
    """派生表"""

    __slots__ = ["_lateral", "_query_expression", "_table_alias", "_column_list"]

    def __init__(self,
                 lateral: bool,
                 query_expression: "QueryExpression",
                 table_alias: Optional[str],
                 column_list: List[str]):
        self._lateral = lateral
        self._query_expression = query_expression
        self._table_alias = table_alias
        self._column_list = column_list

    @property
    def lateral(self) -> bool:
        return self._lateral

    @property
    def query_expression(self) -> "QueryExpression":
        return self._query_expression

    @property
    def table_alias(self) -> Optional[str]:
        return self._table_alias

    @property
    def column_list(self) -> List[str]:
        return self._column_list
