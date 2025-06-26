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
        """初始化 WITH 表
        
        Parameters
        ----------
        table_name : str
            表名
        column_list : List[str]
            列名列表
        query_expression : QueryExpression
            查询表达式
        """
        self._table_name = table_name
        self._column_list = column_list
        self._query_expression = query_expression

    @property
    def table_name(self) -> str:
        """获取表名
        
        Returns
        -------
        str
            表名
        """
        return self._table_name

    @property
    def column_list(self) -> List[str]:
        """获取列名列表
        
        Returns
        -------
        List[str]
            列名列表
        """
        return self._column_list

    @property
    def query_expression(self) -> "QueryExpression":
        """获取查询表达式
        
        Returns
        -------
        QueryExpression
            查询表达式
        """
        return self._query_expression


class WithClause(Node):
    """WITH 子句"""

    __slots__ = ["_table_list", "_recursive"]

    def __init__(self, table_list: List[WithTable], recursive: bool):
        """初始化 WITH 子句
        
        Parameters
        ----------
        table_list : List[WithTable]
            WITH 表列表
        recursive : bool
            是否为递归 WITH
        """
        self._table_list = table_list
        self._recursive = recursive

    @property
    def table_list(self) -> List[WithTable]:
        """获取 WITH 表列表
        
        Returns
        -------
        List[WithTable]
            WITH 表列表
        """
        return self._table_list

    @property
    def recursive(self) -> bool:
        """获取是否递归标志
        
        Returns
        -------
        bool
            是否为递归 WITH
        """
        return self._recursive
