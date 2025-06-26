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
        """
        初始化派生表

        Parameters
        ----------
        lateral : bool
            是否为 LATERAL 派生表
        query_expression : QueryExpression
            查询表达式
        table_alias : Optional[str]
            表别名
        column_list : List[str]
            列名列表
        """
        self._lateral = lateral
        self._query_expression = query_expression
        self._table_alias = table_alias
        self._column_list = column_list

    @property
    def lateral(self) -> bool:
        """
        是否为 LATERAL 派生表

        Returns
        -------
        bool
            是否为 LATERAL 派生表
        """
        return self._lateral

    @property
    def query_expression(self) -> "QueryExpression":
        """
        查询表达式

        Returns
        -------
        QueryExpression
            查询表达式
        """
        return self._query_expression

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

    @property
    def column_list(self) -> List[str]:
        """
        列名列表

        Returns
        -------
        List[str]
            列名列表
        """
        return self._column_list
