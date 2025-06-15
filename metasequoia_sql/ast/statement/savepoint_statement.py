"""
SAVEPOINT 语句（savepoint statement）
"""

from typing import TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier

__all__ = [
    "SavepointStatement"
]


class SavepointStatement(Statement):
    """
    SAVEPOINT 语句的抽象语法树节点。

    语法规则：
        SAVEPOINT savepoint_name
    """

    __slots__ = (
        "_savepoint_name"
    )

    def __init__(self, savepoint_name: str) -> None:
        """
        初始化 SAVEPOINT 语句节点。

        Parameters
        ----------
        savepoint_name : Identifier
            保存点的名称
        """
        self._savepoint_name = savepoint_name

    @property
    def savepoint_name(self) -> str:
        """
        获取保存点的名称。

        Returns
        -------
        Identifier
            保存点的名称
        """
        return self._savepoint_name 