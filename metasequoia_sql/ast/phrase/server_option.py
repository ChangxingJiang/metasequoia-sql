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
        self._username = username

    @property
    def username(self) -> str:
        return self._username


class ServerHostOption(ServerOption):
    """HOST 服务器选项"""

    __slots__ = ["_host"]

    def __init__(self, host: str):
        self._host = host

    @property
    def host(self) -> str:
        return self._host


class ServerDatabaseOption(ServerOption):
    """DATABASE 服务器选项"""

    __slots__ = ["_database"]

    def __init__(self, database: str):
        self._database = database

    @property
    def database(self) -> str:
        return self._database


class ServerOwnerOption(ServerOption):
    """OWNER 服务器选项"""

    __slots__ = ["_owner"]

    def __init__(self, owner: str):
        self._owner = owner

    @property
    def owner(self) -> str:
        return self._owner


class ServerPasswordOption(ServerOption):
    """PASSWORD 服务器选项"""

    __slots__ = ["_password"]

    def __init__(self, password: str):
        self._password = password

    @property
    def password(self) -> str:
        return self._password


class ServerSocketOption(ServerOption):
    """SOCKET 服务器选项"""

    __slots__ = ["_socket"]

    def __init__(self, socket: str):
        self._socket = socket

    @property
    def socket(self) -> str:
        return self._socket


class ServerPortOption(ServerOption):
    """PORT 服务器选项"""

    __slots__ = ["_port"]

    def __init__(self, port: int):
        self._port = port

    @property
    def port(self) -> int:
        return self._port
