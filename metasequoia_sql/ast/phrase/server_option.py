"""
服务器选项（server option）
"""

from metasequoia_sql.ast.base import Node

__all__ = [
    "ServerOption",
    "ServerUserOption",
    "ServerHostOption",
    "ServerDatabaseOption",
    "ServerOwnerOption",
    "ServerPasswordOption",
    "ServerSocketOption",
    "ServerPortOption",
]


class ServerOption(Node):
    """服务器选项的基类"""


class ServerUserOption(ServerOption):
    """USER 服务器选项"""

    __slots__ = ["_username"]

    def __init__(self, username: str):
        """
        初始化 USER 服务器选项

        Parameters
        ----------
        username : str
            用户名
        """
        self._username = username

    @property
    def username(self) -> str:
        """
        用户名

        Returns
        -------
        str
            用户名
        """
        return self._username


class ServerHostOption(ServerOption):
    """HOST 服务器选项"""

    __slots__ = ["_host"]

    def __init__(self, host: str):
        """
        初始化 HOST 服务器选项

        Parameters
        ----------
        host : str
            主机地址
        """
        self._host = host

    @property
    def host(self) -> str:
        """
        主机地址

        Returns
        -------
        str
            主机地址
        """
        return self._host


class ServerDatabaseOption(ServerOption):
    """DATABASE 服务器选项"""

    __slots__ = ["_database"]

    def __init__(self, database: str):
        """
        初始化 DATABASE 服务器选项

        Parameters
        ----------
        database : str
            数据库名
        """
        self._database = database

    @property
    def database(self) -> str:
        """
        数据库名

        Returns
        -------
        str
            数据库名
        """
        return self._database


class ServerOwnerOption(ServerOption):
    """OWNER 服务器选项"""

    __slots__ = ["_owner"]

    def __init__(self, owner: str):
        """
        初始化 OWNER 服务器选项

        Parameters
        ----------
        owner : str
            所有者
        """
        self._owner = owner

    @property
    def owner(self) -> str:
        """
        所有者

        Returns
        -------
        str
            所有者
        """
        return self._owner


class ServerPasswordOption(ServerOption):
    """PASSWORD 服务器选项"""

    __slots__ = ["_password"]

    def __init__(self, password: str):
        """
        初始化 PASSWORD 服务器选项

        Parameters
        ----------
        password : str
            密码
        """
        self._password = password

    @property
    def password(self) -> str:
        """
        密码

        Returns
        -------
        str
            密码
        """
        return self._password


class ServerSocketOption(ServerOption):
    """SOCKET 服务器选项"""

    __slots__ = ["_socket"]

    def __init__(self, socket: str):
        """
        初始化 SOCKET 服务器选项

        Parameters
        ----------
        socket : str
            套接字路径
        """
        self._socket = socket

    @property
    def socket(self) -> str:
        """
        套接字路径

        Returns
        -------
        str
            套接字路径
        """
        return self._socket


class ServerPortOption(ServerOption):
    """PORT 服务器选项"""

    __slots__ = ["_port"]

    def __init__(self, port: int):
        """
        初始化 PORT 服务器选项

        Parameters
        ----------
        port : int
            端口号
        """
        self._port = port

    @property
    def port(self) -> int:
        """
        端口号

        Returns
        -------
        int
            端口号
        """
        return self._port
