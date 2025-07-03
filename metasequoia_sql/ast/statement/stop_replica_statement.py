"""
STOP REPLICA 语句（stop replica statement）
"""

from typing import Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.fixed_enum import EnumReplicaThreadType

__all__ = [
    "StopReplicaStatement",
]


class StopReplicaStatement(Statement):
    """STOP REPLICA 语句"""

    __slots__ = ["_thread_type", "_channel_name"]

    def __init__(self, thread_type: "EnumReplicaThreadType", channel_name: Optional[str]):
        """
        初始化 STOP REPLICA 语句

        Parameters
        ----------
        thread_type : EnumReplicaThreadType
            复制线程类型
        channel_name : Optional[str]
            通道名称
        """
        self._thread_type = thread_type
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
    def channel_name(self) -> Optional[str]:
        """
        通道名称

        Returns
        -------
        Optional[str]
            通道名称
        """
        return self._channel_name
