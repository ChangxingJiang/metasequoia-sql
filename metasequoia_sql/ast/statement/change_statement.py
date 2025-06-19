"""
CHANGE 语句（change statement）
"""

from abc import ABC
from enum import IntEnum
from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.phrase.source_definition import SourceDefinition
    from metasequoia_sql.ast.phrase.filter_definition import FilterDefinition

__all__ = [
    "ChangeType",
    "ChangeStatement",
    "ChangeReplicationSourceStatement",
    "ChangeReplicationFilterStatement",
]


class ChangeType(IntEnum):
    """CHANGE 语句类型枚举"""

    REPLICATION_SOURCE = 1
    REPLICATION_FILTER = 2


class ChangeStatement(Statement, ABC):
    """CHANGE 语句的抽象基类"""

    __slots__ = ["_change_type", "_channel_list"]

    def __init__(self, change_type: ChangeType, channel_list: List[str]):
        self._change_type = change_type
        self._channel_list = channel_list

    @property
    def change_type(self) -> ChangeType:
        return self._change_type

    @property
    def channel_list(self) -> List[str]:
        return self._channel_list


class ChangeReplicationSourceStatement(ChangeStatement):
    """CHANGE REPLICATION SOURCE 语句"""

    __slots__ = ["_source_def_list"]

    def __init__(self,
                 source_def_list: List["SourceDefinition"],
                 channel_list: List[str]):
        super().__init__(ChangeType.REPLICATION_SOURCE, channel_list)
        self._source_def_list = source_def_list

    @property
    def source_def_list(self) -> List["SourceDefinition"]:
        return self._source_def_list


class ChangeReplicationFilterStatement(ChangeStatement):
    """CHANGE REPLICATION FILTER 语句"""

    __slots__ = ["_filter_def_list"]

    def __init__(self,
                 filter_def_list: List["FilterDefinition"],
                 channel_list: List[str]):
        super().__init__(ChangeType.REPLICATION_FILTER, channel_list)
        self._filter_def_list = filter_def_list

    @property
    def filter_def_list(self) -> List["FilterDefinition"]:
        return self._filter_def_list
