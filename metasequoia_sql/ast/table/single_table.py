"""
单表（single table）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Table

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.clause.index_hint_clause import IndexHint

__all__ = [
    "SingleTable"
]


class SingleTable(Table):
    """单表（single table）"""

    __slots__ = ["_table_ident", "_use_partition", "_table_alias", "_index_hints_list"]

    def __init__(self, table_ident: "Identifier",
                 use_partition: Optional[List[Expression]],
                 table_alias: Optional[str],
                 index_hints_list: List["IndexHint"]):
        """
        初始化单表

        Parameters
        ----------
        table_ident : Identifier
            表标识符
        use_partition : Optional[List[Expression]]
            使用的分区列表
        table_alias : Optional[str]
            表别名
        index_hints_list : List[IndexHint]
            索引提示列表
        """
        self._table_ident = table_ident
        self._use_partition = use_partition
        self._table_alias = table_alias
        self._index_hints_list = index_hints_list

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
    def use_partition(self) -> Optional[List[Expression]]:
        """
        使用的分区列表

        Returns
        -------
        Optional[List[Expression]]
            使用的分区列表
        """
        return self._use_partition

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
    def index_hints_list(self) -> List["IndexHint"]:
        """
        索引提示列表

        Returns
        -------
        List[IndexHint]
            索引提示列表
        """
        return self._index_hints_list
