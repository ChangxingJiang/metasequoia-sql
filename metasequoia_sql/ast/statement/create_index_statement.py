"""
CREATE INDEX 语句（create index statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.phrase.ddl_table_element import EnumIndexType, IndexKeyDefinition
    from metasequoia_sql.ast.phrase.ddl_index_attribute import IndexAttrUsingIndexType, IndexAttribute
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.phrase.ddl_alter_option import AlterOptionLock, AlterOptionAlgorithm

__all__ = [
    "CreateIndexStmt"
]


class CreateIndexStmt(Statement):
    # pylint: disable=R0902
    """CREATE INDEX 语句"""

    __slots__ = (
        "_index_type",
        "_index_name",
        "_index_structure_type",
        "_table_name",
        "_index_key_list",
        "_index_options",
        "_alter_lock",
        "_alter_algorithm"
    )

    def __init__(self,
                 index_type: "EnumIndexType",
                 index_name: str,
                 index_structure_type: Optional["IndexAttrUsingIndexType"],
                 table_name: "Identifier",
                 index_key_list: List["IndexKeyDefinition"],
                 index_options: List["IndexAttribute"],
                 alter_lock: Optional["AlterOptionLock"],
                 alter_algorithm: Optional["AlterOptionAlgorithm"]
                 ):
        # pylint: disable=R0913
        self._index_type = index_type
        self._index_name = index_name
        self._index_structure_type = index_structure_type
        self._table_name = table_name
        self._index_key_list = index_key_list
        self._index_options = index_options
        self._alter_lock = alter_lock
        self._alter_algorithm = alter_algorithm

    @property
    def index_type(self) -> "EnumIndexType":
        """
        索引类型

        Returns
        -------
        EnumIndexType
            索引类型
        """
        return self._index_type

    @property
    def index_name(self) -> str:
        """
        索引名称

        Returns
        -------
        str
            索引名称
        """
        return self._index_name

    @property
    def index_structure_type(self) -> Optional["IndexAttrUsingIndexType"]:
        """
        索引结构类型

        Returns
        -------
        Optional["IndexAttrUsingIndexType"]
            索引结构类型
        """
        return self._index_structure_type

    @property
    def table_name(self) -> "Identifier":
        """
        表名标识符

        Returns
        -------
        Identifier
            表名标识符
        """
        return self._table_name

    @property
    def index_key_list(self) -> List["IndexKeyDefinition"]:
        """
        索引键定义列表

        Returns
        -------
        List["IndexKeyDefinition"]
            索引键定义列表
        """
        return self._index_key_list

    @property
    def index_options(self) -> List["IndexAttribute"]:
        """
        索引属性列表

        Returns
        -------
        List["IndexAttribute"]
            索引属性列表
        """
        return self._index_options

    @property
    def alter_lock(self) -> Optional["AlterOptionLock"]:
        """
        ALTER 锁选项

        Returns
        -------
        Optional["AlterOptionLock"]
            ALTER 锁选项
        """
        return self._alter_lock

    @property
    def alter_algorithm(self) -> Optional["AlterOptionAlgorithm"]:
        """
        ALTER 算法选项

        Returns
        -------
        Optional["AlterOptionAlgorithm"]
            ALTER 算法选项
        """
        return self._alter_algorithm
