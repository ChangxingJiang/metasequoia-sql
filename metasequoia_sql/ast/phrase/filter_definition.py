"""
过滤器定义相关节点
"""

from abc import ABC
from enum import IntEnum
from typing import List, TYPE_CHECKING, Tuple

from metasequoia_sql.ast.base import Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier

__all__ = [
    "FilterType",
    "FilterDefinition",
    "ReplicateDoDbFilter",
    "ReplicateIgnoreDbFilter",
    "ReplicateDoTableFilter",
    "ReplicateIgnoreTableFilter",
    "ReplicateWildDoTableFilter",
    "ReplicateWildIgnoreTableFilter",
    "ReplicateRewriteDbFilter",
]


class FilterType(IntEnum):
    """过滤器类型枚举"""

    REPLICATE_DO_DB = 1
    REPLICATE_IGNORE_DB = 2
    REPLICATE_DO_TABLE = 3
    REPLICATE_IGNORE_TABLE = 4
    REPLICATE_WILD_DO_TABLE = 5
    REPLICATE_WILD_IGNORE_TABLE = 6
    REPLICATE_REWRITE_DB = 7


class FilterDefinition(Node, ABC):
    """过滤器定义的抽象基类"""

    __slots__ = ["_filter_type"]

    def __init__(self, filter_type: FilterType):
        self._filter_type = filter_type

    @property
    def filter_type(self) -> FilterType:
        """获取过滤器类型。
        
        Returns
        -------
        FilterType
            过滤器类型
        """
        return self._filter_type


class ReplicateDoDbFilter(FilterDefinition):
    """REPLICATE_DO_DB 过滤器"""

    __slots__ = ["_db_list"]

    def __init__(self, db_list: List[str]):
        super().__init__(FilterType.REPLICATE_DO_DB)
        self._db_list = db_list

    @property
    def db_list(self) -> List[str]:
        """获取数据库列表。
        
        Returns
        -------
        List[str]
            数据库列表
        """
        return self._db_list


class ReplicateIgnoreDbFilter(FilterDefinition):
    """REPLICATE_IGNORE_DB 过滤器"""

    __slots__ = ["_db_list"]

    def __init__(self, db_list: List[str]):
        super().__init__(FilterType.REPLICATE_IGNORE_DB)
        self._db_list = db_list

    @property
    def db_list(self) -> List[str]:
        """获取数据库列表。
        
        Returns
        -------
        List[str]
            数据库列表
        """
        return self._db_list


class ReplicateDoTableFilter(FilterDefinition):
    """REPLICATE_DO_TABLE 过滤器"""

    __slots__ = ["_table_list"]

    def __init__(self, table_list: List["Identifier"]):
        super().__init__(FilterType.REPLICATE_DO_TABLE)
        self._table_list = table_list

    @property
    def table_list(self) -> List["Identifier"]:
        """获取表列表。
        
        Returns
        -------
        List[Identifier]
            表列表
        """
        return self._table_list


class ReplicateIgnoreTableFilter(FilterDefinition):
    """REPLICATE_IGNORE_TABLE 过滤器"""

    __slots__ = ["_table_list"]

    def __init__(self, table_list: List["Identifier"]):
        super().__init__(FilterType.REPLICATE_IGNORE_TABLE)
        self._table_list = table_list

    @property
    def table_list(self) -> List["Identifier"]:
        """获取表列表。
        
        Returns
        -------
        List[Identifier]
            表列表
        """
        return self._table_list


class ReplicateWildDoTableFilter(FilterDefinition):
    """REPLICATE_WILD_DO_TABLE 过滤器"""

    __slots__ = ["_pattern_list"]

    def __init__(self, pattern_list: List[str]):
        super().__init__(FilterType.REPLICATE_WILD_DO_TABLE)
        self._pattern_list = pattern_list

    @property
    def pattern_list(self) -> List[str]:
        """获取模式列表。
        
        Returns
        -------
        List[str]
            模式列表
        """
        return self._pattern_list


class ReplicateWildIgnoreTableFilter(FilterDefinition):
    """REPLICATE_WILD_IGNORE_TABLE 过滤器"""

    __slots__ = ["_pattern_list"]

    def __init__(self, pattern_list: List[str]):
        super().__init__(FilterType.REPLICATE_WILD_IGNORE_TABLE)
        self._pattern_list = pattern_list

    @property
    def pattern_list(self) -> List[str]:
        """获取模式列表。
        
        Returns
        -------
        List[str]
            模式列表
        """
        return self._pattern_list


class ReplicateRewriteDbFilter(FilterDefinition):
    """REPLICATE_REWRITE_DB 过滤器"""

    __slots__ = ["_db_pair_list"]

    def __init__(self, db_pair_list: List[Tuple[str, str]]):
        super().__init__(FilterType.REPLICATE_REWRITE_DB)
        self._db_pair_list = db_pair_list

    @property
    def db_pair_list(self) -> List[Tuple[str, str]]:
        """获取数据库配对列表。
        
        Returns
        -------
        List[Tuple[str, str]]
            数据库配对列表
        """
        return self._db_pair_list
