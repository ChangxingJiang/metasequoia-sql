"""
GROUP REPLICATION 语句相关的 AST 节点
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Node, Statement

if TYPE_CHECKING:
    pass

__all__ = [
    "GroupReplicationStartOption",
    "GroupReplicationUser",
    "GroupReplicationPassword",
    "GroupReplicationPluginAuth",
    "GroupReplicationStartStatement",
    "GroupReplicationStopStatement",
]


class GroupReplicationStartOption(Node):
    """GROUP REPLICATION START 选项的抽象基类"""


class GroupReplicationUser(GroupReplicationStartOption):
    """GROUP REPLICATION 用户选项"""

    __slots__ = ["_user"]

    def __init__(self, user: str):
        self._user = user

    @property
    def user(self) -> str:
        return self._user


class GroupReplicationPassword(GroupReplicationStartOption):
    """GROUP REPLICATION 密码选项"""

    __slots__ = ["_password"]

    def __init__(self, password: str):
        self._password = password

    @property
    def password(self) -> str:
        return self._password


class GroupReplicationPluginAuth(GroupReplicationStartOption):
    """GROUP REPLICATION 插件认证选项"""

    __slots__ = ["_plugin_auth"]

    def __init__(self, plugin_auth: str):
        self._plugin_auth = plugin_auth

    @property
    def plugin_auth(self) -> str:
        return self._plugin_auth


class GroupReplicationStatement(Statement):
    """`GROUP REPLICATION` 语句"""


class GroupReplicationStartStatement(GroupReplicationStatement):
    """START GROUP_REPLICATION 语句"""

    __slots__ = ["_options"]

    def __init__(self, options: List[GroupReplicationStartOption]):
        self._options = options

    @property
    def options(self) -> List[GroupReplicationStartOption]:
        return self._options


class GroupReplicationStopStatement(GroupReplicationStatement):
    """STOP GROUP_REPLICATION 语句"""

    __slots__ = []
