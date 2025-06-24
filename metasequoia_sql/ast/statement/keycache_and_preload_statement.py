"""
KEYCACHE 和 PRELOAD 语句（keycache and preload statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node, Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier

__all__ = [
    "AdmPartition",
    "AssignToKeycache",
    "KeycacheStatement",
    "CacheIndexStatement",
    "CacheIndexPartitionsStatement",
    "PreloadKeys",
    "PreloadStatement",
    "LoadIndexStatement",
    "LoadIndexPartitionsStatement",
]


class AdmPartition(Node):
    """管理分区节点: PARTITION (partition_list)"""

    __slots__ = ["_partition_list"]

    def __init__(self, partition_list: Optional[List[str]]):
        self._partition_list = partition_list

    @property
    def partition_list(self) -> Optional[List[str]]:
        return self._partition_list


class AssignToKeycache(Node):
    """分配到键缓存节点: table_name [cache_key_list]"""

    __slots__ = ["_table_name", "_cache_key_list"]

    def __init__(self, table_name: "Identifier", cache_key_list: List[str]):
        self._table_name = table_name
        self._cache_key_list = cache_key_list

    @property
    def table_name(self) -> "Identifier":
        return self._table_name

    @property
    def cache_key_list(self) -> List[str]:
        return self._cache_key_list


class KeycacheStatement(Statement):
    """KEYCACHE 语句"""


class CacheIndexStatement(KeycacheStatement):
    """CACHE INDEX 语句: CACHE INDEX keycache_list IN key_cache_name"""

    __slots__ = ["_keycache_list", "_key_cache_name"]

    def __init__(self, keycache_list: List[AssignToKeycache], key_cache_name: Expression):
        self._keycache_list = keycache_list
        self._key_cache_name = key_cache_name

    @property
    def keycache_list(self) -> List[AssignToKeycache]:
        return self._keycache_list

    @property
    def key_cache_name(self) -> Expression:
        return self._key_cache_name


class CacheIndexPartitionsStatement(KeycacheStatement):
    """CACHE INDEX 分区语句: CACHE INDEX table_name partition cache_key_list IN key_cache_name"""

    __slots__ = ["_table_name", "_partition", "_cache_key_list", "_key_cache_name"]

    def __init__(
            self,
            table_name: "Identifier",
            partition: AdmPartition,
            cache_key_list: List[str],
            key_cache_name: Expression
    ):
        self._table_name = table_name
        self._partition = partition
        self._cache_key_list = cache_key_list
        self._key_cache_name = key_cache_name

    @property
    def table_name(self) -> "Identifier":
        return self._table_name

    @property
    def partition(self) -> AdmPartition:
        return self._partition

    @property
    def cache_key_list(self) -> List[str]:
        return self._cache_key_list

    @property
    def key_cache_name(self) -> Expression:
        return self._key_cache_name


class PreloadKeys(Node):
    """预加载键节点: table_name [cache_key_list] [IGNORE LEAVES]"""

    __slots__ = ["_table_name", "_cache_key_list", "_ignore_leaves"]

    def __init__(
            self,
            table_name: "Identifier",
            cache_key_list: List[str],
            ignore_leaves: bool
    ):
        self._table_name = table_name
        self._cache_key_list = cache_key_list
        self._ignore_leaves = ignore_leaves

    @property
    def table_name(self) -> "Identifier":
        return self._table_name

    @property
    def cache_key_list(self) -> List[str]:
        return self._cache_key_list

    @property
    def ignore_leaves(self) -> bool:
        return self._ignore_leaves


class PreloadStatement(Statement):
    """PRELOAD 语句"""


class LoadIndexStatement(PreloadStatement):
    """LOAD INDEX 语句: LOAD INDEX INTO CACHE preload_list"""

    __slots__ = ["_preload_list"]

    def __init__(self, preload_list: List[PreloadKeys]):
        self._preload_list = preload_list

    @property
    def preload_list(self) -> List[PreloadKeys]:
        return self._preload_list


class LoadIndexPartitionsStatement(PreloadStatement):
    """LOAD INDEX 分区语句: LOAD INDEX INTO CACHE table_name partition cache_key_list [IGNORE LEAVES]"""

    __slots__ = ["_table_name", "_partition", "_cache_key_list", "_ignore_leaves"]

    def __init__(
            self,
            table_name: "Identifier",
            partition: AdmPartition,
            cache_key_list: List[str],
            ignore_leaves: bool
    ):
        self._table_name = table_name
        self._partition = partition
        self._cache_key_list = cache_key_list
        self._ignore_leaves = ignore_leaves

    @property
    def table_name(self) -> "Identifier":
        return self._table_name

    @property
    def partition(self) -> AdmPartition:
        return self._partition

    @property
    def cache_key_list(self) -> List[str]:
        return self._cache_key_list

    @property
    def ignore_leaves(self) -> bool:
        return self._ignore_leaves
