"""
START REPLICA 语句（start replica statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.fixed_enum import EnumReplicaThreadType
    from metasequoia_sql.ast.phrase.source_definition import SourceDefinition

__all__ = [
    "StartReplicaStatement",
]


class StartReplicaStatement(Statement):
    """START REPLICA 语句"""

    __slots__ = (
        "_thread_type",
        "_until_conditions",
        "_user_name",
        "_password",
        "_default_auth",
        "_plugin_dir",
        "_channel_name",
    )

    def __init__(
            self,
            thread_type: "EnumReplicaThreadType",
            until_conditions: List["SourceDefinition"],
            user_name: Optional[str],
            password: Optional[str],
            default_auth: Optional[str],
            plugin_dir: Optional[str],
            channel_name: Optional[str]
    ):
        # pylint: disable=R0913
        """
        初始化 START REPLICA 语句

        Parameters
        ----------
        thread_type : EnumReplicaThreadType
            复制线程类型
        until_conditions : List[SourceDefinition]
            停止条件列表
        user_name : Optional[str]
            用户名
        password : Optional[str]
            密码
        default_auth : Optional[str]
            默认认证方式
        plugin_dir : Optional[str]
            插件目录
        channel_name : Optional[str]
            通道名称
        """
        self._thread_type = thread_type
        self._until_conditions = until_conditions
        self._user_name = user_name
        self._password = password
        self._default_auth = default_auth
        self._plugin_dir = plugin_dir
        self._channel_name = channel_name

    @property
    def thread_type(self) -> "EnumReplicaThreadType":
        """
        复制线程类型

        Returns
        -------
        EnumReplicaThreadType
            复制线程类型
        """
        return self._thread_type

    @property
    def until_conditions(self) -> List["SourceDefinition"]:
        """
        停止条件列表

        Returns
        -------
        List[SourceDefinition]
            停止条件列表
        """
        return self._until_conditions

    @property
    def user_name(self) -> Optional[str]:
        """
        用户名

        Returns
        -------
        Optional[str]
            用户名
        """
        return self._user_name

    @property
    def password(self) -> Optional[str]:
        """
        密码

        Returns
        -------
        Optional[str]
            密码
        """
        return self._password

    @property
    def default_auth(self) -> Optional[str]:
        """
        默认认证方式

        Returns
        -------
        Optional[str]
            默认认证方式
        """
        return self._default_auth

    @property
    def plugin_dir(self) -> Optional[str]:
        """
        插件目录

        Returns
        -------
        Optional[str]
            插件目录
        """
        return self._plugin_dir

    @property
    def channel_name(self) -> Optional[str]:
        """
        通道名称

        Returns
        -------
        Optional[str]
            通道名称
        """
        return self._channel_name
