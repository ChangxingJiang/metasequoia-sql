"""
SQL状态（sqlstate）
"""

from metasequoia_sql.ast.base import Node

__all__ = [
    "SqlState"
]


class SqlState(Node):
    """
    SQL状态的抽象语法树节点。

    语法规则：
        SQLSTATE [VALUE] 'string_literal'
    """

    __slots__ = (
        "_sqlstate_value"
    )

    def __init__(self, sqlstate_value: str) -> None:
        """
        初始化 SQL状态节点。

        Parameters
        ----------
        sqlstate_value : str
            SQL状态值
        """
        self._sqlstate_value = sqlstate_value

    @property
    def sqlstate_value(self) -> str:
        """
        获取SQL状态值。

        Returns
        -------
        str
            SQL状态值
        """
        return self._sqlstate_value 