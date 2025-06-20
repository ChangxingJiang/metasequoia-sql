"""
连接选项（connect option）
"""

from typing import TYPE_CHECKING

from metasequoia_sql.ast.base import Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.base import Expression

__all__ = [
    "ConnectOption",
    "MaxQueriesPerHour",
    "MaxUpdatesPerHour",
    "MaxConnectionsPerHour",
    "MaxUserConnections",
]


class ConnectOption(Node):
    """连接选项的抽象基类"""

    __slots__ = ["_value"]

    def __init__(self, value: int):
        self._value = value

    @property
    def value(self) -> int:
        return self._value


class MaxQueriesPerHour(ConnectOption):
    """每小时最大查询数限制"""


class MaxUpdatesPerHour(ConnectOption):
    """每小时最大更新数限制"""


class MaxConnectionsPerHour(ConnectOption):
    """每小时最大连接数限制"""


class MaxUserConnections(ConnectOption):
    """最大用户连接数限制""" 