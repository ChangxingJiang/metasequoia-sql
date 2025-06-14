"""
CLONE 语句（clone statement）
"""

from typing import Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.fixed_enum import EnumOpenSslType
    from metasequoia_sql.ast.basic.literal import UserName

__all__ = [
    "TempDatadirSsl",
    "CloneStatement",
    "CloneLocalStatement",
    "CloneInstanceStatement",
]


class TempDatadirSsl:
    """临时数据目录和 SSL 选项信息"""

    __slots__ = (
        "_data_directory",
        "_open_ssl",
    )

    def __init__(self, data_directory: Optional[str], open_ssl: "EnumOpenSslType"):
        self._data_directory = data_directory
        self._open_ssl = open_ssl

    @property
    def data_directory(self) -> Optional[str]:
        return self._data_directory

    @property
    def open_ssl(self) -> "EnumOpenSslType":
        return self._open_ssl


class CloneStatement(Statement):
    """CLONE 语句基类"""


class CloneLocalStatement(CloneStatement):
    """CLONE LOCAL DATA DIRECTORY 语句"""

    __slots__ = (
        "_data_directory",
    )

    def __init__(self, data_directory: str):
        self._data_directory = data_directory

    @property
    def data_directory(self) -> str:
        return self._data_directory


class CloneInstanceStatement(CloneStatement):
    """CLONE INSTANCE FROM 语句"""

    __slots__ = (
        "_user",
        "_port",
        "_password",
        "_data_directory",
        "_open_ssl",
    )

    def __init__(self, user: "UserName", port: int, password: str, data_directory: Optional[str],
                 open_ssl: "EnumOpenSslType"):
        self._user = user
        self._port = port
        self._password = password
        self._data_directory = data_directory
        self._open_ssl = open_ssl

    @property
    def user(self) -> "UserName":
        return self._user

    @property
    def port(self) -> int:
        return self._port

    @property
    def password(self) -> str:
        return self._password

    @property
    def data_directory(self) -> Optional[str]:
        return self._data_directory

    @property
    def open_ssl(self) -> "EnumOpenSslType":
        return self._open_ssl
