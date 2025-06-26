"""
CREATE SERVER 语句（create server statement）
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.phrase.server_option import ServerOption

__all__ = [
    "CreateServerStatement"
]


class CreateServerStatement(Statement):
    """
    CREATE SERVER 语句
    
    Parameters
    ----------
    server_name : str
        服务器名称
    wrapper_name : str
        外部数据包装器名称
    options : List[ServerOption]
        服务器选项列表
    """

    __slots__ = ("_server_name", "_wrapper_name", "_options")

    def __init__(self,
                 server_name: str,
                 wrapper_name: str,
                 options: List["ServerOption"]):
        self._server_name = server_name
        self._wrapper_name = wrapper_name
        self._options = options

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
    def wrapper_name(self) -> str:
        """
        外部数据包装器名称

        Returns
        -------
        str
            外部数据包装器名称
        """
        return self._wrapper_name

    @property
    def options(self) -> List["ServerOption"]:
        """
        服务器选项列表

        Returns
        -------
        List["ServerOption"]
            服务器选项列表
        """
        return self._options
