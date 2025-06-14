"""
TRUNCATE 语句（truncate statement）
"""

from typing import TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier

__all__ = [
    "TruncateStatement"
]


class TruncateStatement(Statement):
    """
    TRUNCATE 语句的抽象语法树节点。

    语法规则：
        TRUNCATE [TABLE] table_name
    """

    __slots__ = (
        "_table_ident"
    )

    def __init__(self, table_ident: "Identifier") -> None:
        """
        初始化 TRUNCATE 语句节点。

        Parameters
        ----------
        table_ident : Identifier
            要清空的表的标识符
        """
        self._table_ident = table_ident

    @property
    def table_ident(self) -> "Identifier":
        """
        获取要清空的表的标识符。

        Returns
        -------
        Identifier
            要清空的表的标识符
        """
        return self._table_ident 