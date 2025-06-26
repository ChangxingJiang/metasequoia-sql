"""
RELEASE 语句（release statement）
"""

from typing import TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    pass

__all__ = [
    "ReleaseStatement"
]


class ReleaseStatement(Statement):
    """
    RELEASE SAVEPOINT 语句的抽象语法树节点。

    语法规则：
        RELEASE SAVEPOINT savepoint_name
    """

    __slots__ = (
        "_savepoint_name",
    )

    def __init__(self, savepoint_name: str) -> None:
        """
        初始化 RELEASE SAVEPOINT 语句节点。

        Parameters
        ----------
        savepoint_name : str
            要释放的保存点的名称
        """
        self._savepoint_name = savepoint_name

    @property
    def savepoint_name(self) -> str:
        """
        获取要释放的保存点的名称。

        Returns
        -------
        str
            要释放的保存点的名称
        """
        return self._savepoint_name
