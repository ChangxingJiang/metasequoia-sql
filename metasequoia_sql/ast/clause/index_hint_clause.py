"""
索引指定子句（index hint clause）
"""

from enum import IntEnum, IntFlag
from typing import List

from metasequoia_sql.ast.base import Node

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

    __slots__ = ["_index_hint_type", "_index_hint_for", "_index_name_list"]

    def __init__(self,
                 index_hint_type: EnumIndexHintType,
                 index_hint_for: EnumIndexHintFor,
                 index_name_list: List[str]):
        """初始化索引指定子句
        
        Parameters
        ----------
        index_hint_type : EnumIndexHintType
            索引指定类型
        index_hint_for : EnumIndexHintFor
            索引用途
        index_name_list : List[str]
            索引名称列表
        """
        self._index_hint_type = index_hint_type
        self._index_hint_for = index_hint_for
        self._index_name_list = index_name_list

    @property
    def index_hint_type(self) -> EnumIndexHintType:
        """获取索引指定类型
        
        Returns
        -------
        EnumIndexHintType
            索引指定类型
        """
        return self._index_hint_type

    @property
    def index_hint_for(self) -> EnumIndexHintFor:
        """获取索引用途
        
        Returns
        -------
        EnumIndexHintFor
            索引用途
        """
        return self._index_hint_for

    @property
    def index_name_list(self) -> List[str]:
        """获取索引名称列表
        
        Returns
        -------
        List[str]
            索引名称列表
        """
        return self._index_name_list
