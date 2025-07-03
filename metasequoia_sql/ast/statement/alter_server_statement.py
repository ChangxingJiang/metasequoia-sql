"""
ALTER SERVER 语句（alter server statement）
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.phrase.server_option import ServerOption

__all__ = [
    "AlterServerStatement",
]


class AlterServerStatement(Statement):
    """ALTER SERVER 语句

    Parameters
    ----------
    server_name : str
        服务器名称
    server_options : List["ServerOption"]
        服务器选项列表
    """

    __slots__ = ["_server_name", "_server_options"]

    def __init__(self, server_name: str, server_options: List["ServerOption"]):
        self._server_name = server_name
        self._server_options = server_options

    @property
    def server_name(self) -> str:
        """
        服务器名称

        Returns
        -------
        str
            服务器名称
        """
        return self._server_name

    @property
    def server_options(self) -> List["ServerOption"]:
        """
        服务器选项列表

        Returns
        -------
        List["ServerOption"]
            服务器选项列表
        """
        return self._server_options
