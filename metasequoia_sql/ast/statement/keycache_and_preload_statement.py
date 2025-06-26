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
        """
        初始化管理分区节点

        Parameters
        ----------
        partition_list : Optional[List[str]]
            分区列表
        """
        self._partition_list = partition_list

    @property
    def partition_list(self) -> Optional[List[str]]:
        """
        分区列表

        Returns
        -------
        Optional[List[str]]
            分区列表
        """
        return self._partition_list


class AssignToKeycache(Node):
    """分配到键缓存节点: table_name [cache_key_list]"""

    __slots__ = ["_table_name", "_cache_key_list"]

    def __init__(self, table_name: "Identifier", cache_key_list: List[str]):
        """
        初始化分配到键缓存节点

        Parameters
        ----------
        table_name : Identifier
            表名称
        cache_key_list : List[str]
            缓存键列表
        """
        self._table_name = table_name
        self._cache_key_list = cache_key_list

    @property
    def table_name(self) -> "Identifier":
        """
        表名称

        Returns
        -------
        Identifier
            表名称
        """
        return self._table_name

    @property
    def cache_key_list(self) -> List[str]:
        """
        缓存键列表

        Returns
        -------
        List[str]
            缓存键列表
        """
        return self._cache_key_list


class KeycacheStatement(Statement):
    """KEYCACHE 语句"""


class CacheIndexStatement(KeycacheStatement):
    """CACHE INDEX 语句: CACHE INDEX keycache_list IN key_cache_name"""

    __slots__ = ["_keycache_list", "_key_cache_name"]

    def __init__(self, keycache_list: List[AssignToKeycache], key_cache_name: Expression):
        """
        初始化 CACHE INDEX 语句

        Parameters
        ----------
        keycache_list : List[AssignToKeycache]
            键缓存列表
        key_cache_name : Expression
            键缓存名称
        """
        self._keycache_list = keycache_list
        self._key_cache_name = key_cache_name

    @property
    def keycache_list(self) -> List[AssignToKeycache]:
        """
        键缓存列表

        Returns
        -------
        List[AssignToKeycache]
            键缓存列表
        """
        return self._keycache_list

    @property
    def key_cache_name(self) -> Expression:
        """
        键缓存名称

        Returns
        -------
        Expression
            键缓存名称
        """
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
        """
        初始化 CACHE INDEX 分区语句

        Parameters
        ----------
        table_name : Identifier
            表名称
        partition : AdmPartition
            分区
        cache_key_list : List[str]
            缓存键列表
        key_cache_name : Expression
            键缓存名称
        """
        self._table_name = table_name
        self._partition = partition
        self._cache_key_list = cache_key_list
        self._key_cache_name = key_cache_name

    @property
    def table_name(self) -> "Identifier":
        """
        表名称

        Returns
        -------
        Identifier
            表名称
        """
        return self._table_name

    @property
    def partition(self) -> AdmPartition:
        """
        分区

        Returns
        -------
        AdmPartition
            分区
        """
        return self._partition

    @property
    def cache_key_list(self) -> List[str]:
        """
        缓存键列表

        Returns
        -------
        List[str]
            缓存键列表
        """
        return self._cache_key_list

    @property
    def key_cache_name(self) -> Expression:
        """
        键缓存名称

        Returns
        -------
        Expression
            键缓存名称
        """
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
        """
        初始化预加载键节点

        Parameters
        ----------
        table_name : Identifier
            表名称
        cache_key_list : List[str]
            缓存键列表
        ignore_leaves : bool
            是否忽略叶子节点
        """
        self._table_name = table_name
        self._cache_key_list = cache_key_list
        self._ignore_leaves = ignore_leaves

    @property
    def table_name(self) -> "Identifier":
        """
        表名称

        Returns
        -------
        Identifier
            表名称
        """
        return self._table_name

    @property
    def cache_key_list(self) -> List[str]:
        """
        缓存键列表

        Returns
        -------
        List[str]
            缓存键列表
        """
        return self._cache_key_list

    @property
    def ignore_leaves(self) -> bool:
        """
        是否忽略叶子节点

        Returns
        -------
        bool
            是否忽略叶子节点
        """
        return self._ignore_leaves


class PreloadStatement(Statement):
    """PRELOAD 语句"""


class LoadIndexStatement(PreloadStatement):
    """LOAD INDEX 语句: LOAD INDEX INTO CACHE preload_list"""

    __slots__ = ["_preload_list"]

    def __init__(self, preload_list: List[PreloadKeys]):
        """
        初始化 LOAD INDEX 语句

        Parameters
        ----------
        preload_list : List[PreloadKeys]
            预加载列表
        """
        self._preload_list = preload_list

    @property
    def preload_list(self) -> List[PreloadKeys]:
        """
        预加载列表

        Returns
        -------
        List[PreloadKeys]
            预加载列表
        """
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
        """
        初始化 LOAD INDEX 分区语句

        Parameters
        ----------
        table_name : Identifier
            表名称
        partition : AdmPartition
            分区
        cache_key_list : List[str]
            缓存键列表
        ignore_leaves : bool
            是否忽略叶子节点
        """
        self._table_name = table_name
        self._partition = partition
        self._cache_key_list = cache_key_list
        self._ignore_leaves = ignore_leaves

    @property
    def table_name(self) -> "Identifier":
        """
        表名称

        Returns
        -------
        Identifier
            表名称
        """
        return self._table_name

    @property
    def partition(self) -> AdmPartition:
        """
        分区

        Returns
        -------
        AdmPartition
            分区
        """
        return self._partition

    @property
    def cache_key_list(self) -> List[str]:
        """
        缓存键列表

        Returns
        -------
        List[str]
            缓存键列表
        """
        return self._cache_key_list

    @property
    def ignore_leaves(self) -> bool:
        """
        是否忽略叶子节点

        Returns
        -------
        bool
            是否忽略叶子节点
        """
        return self._ignore_leaves
