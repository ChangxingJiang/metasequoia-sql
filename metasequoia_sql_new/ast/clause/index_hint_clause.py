"""
索引指定子句（index hint clause）
"""

from enum import IntEnum, IntFlag
from typing import List

from metasequoia_sql_new.ast.base import Node

__all__ = [
    "EnumIndexHintFor",
    "EnumIndexHintType",
    "IndexHint"
]


class EnumIndexHintFor(IntFlag):
    """索引指定子句中的索引用途"""

    DEFAULT = 0
    FOR_JOIN = 1  # FOR JOIN
    FOR_ORDER_BY = 2  # FOR ORDER BY
    FOR_GROUP_BY = 4  # FOR GROUP BY


class EnumIndexHintType(IntEnum):
    """索引指定子句中指定类型"""

    USE = 1  # USE
    FORCE = 2  # FORCE
    IGNORE = 3  # IGNORE


class IndexHint(Node):
    """索引指定子句"""

    def __init__(self,
                 index_hint_type: EnumIndexHintType,
                 index_hint_for: EnumIndexHintFor,
                 index_name_list: List[str]):
        self._index_hint_type = index_hint_type
        self._index_hint_for = index_hint_for
        self._index_name_list = index_name_list

    def attr_list(self) -> List[str]:
        return ["index_hint_type", "index_hint_for", "index_name_list"]

    @property
    def index_hint_type(self) -> EnumIndexHintType:
        return self._index_hint_type

    @property
    def index_hint_for(self) -> EnumIndexHintFor:
        return self._index_hint_for

    @property
    def index_name_list(self) -> List[str]:
        return self._index_name_list
