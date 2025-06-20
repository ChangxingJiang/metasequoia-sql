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
        self._thread_type = thread_type
        self._channel_name = channel_name

    @property
    def thread_type(self) -> "EnumReplicaThreadType":
        return self._thread_type

    @property
    def channel_name(self) -> Optional[str]:
        return self._channel_name
