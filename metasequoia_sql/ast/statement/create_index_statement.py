"""
CREATE INDEX 语句（create index statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.phrase.ddl_table_element import EnumIndexType, IndexKeyDefinition
    from metasequoia_sql.ast.phrase.ddl_index_attribute import IndexAttrUsingIndexType, IndexAttribute
    from metasequoia_sql.ast.basic.ident import TableIdent
    from metasequoia_sql.ast.phrase.ddl_alter_option import AlterOptionLock, AlterOptionAlgorithm

__all__ = [
    "CreateIndexStmt"
]


class CreateIndexStmt(Statement):
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
                 table_name: "TableIdent",
                 index_key_list: List[IndexKeyDefinition],
                 index_options: List[IndexAttribute],
                 alter_lock: Optional["AlterOptionLock"],
                 alter_algorithm: Optional["AlterOptionAlgorithm"]
                 ):
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
        return self._index_type

    @property
    def index_name(self) -> str:
        return self._index_name

    @property
    def index_structure_type(self) -> Optional["IndexAttrUsingIndexType"]:
        return self._index_structure_type

    @property
    def table_name(self) -> "TableIdent":
        return self._table_name

    @property
    def index_key_list(self) -> List["IndexKeyDefinition"]:
        return self._index_key_list

    @property
    def index_options(self) -> List["IndexAttribute"]:
        return self._index_options

    @property
    def alter_lock(self) -> Optional["AlterOptionLock"]:
        return self._alter_lock

    @property
    def alter_algorithm(self) -> Optional["AlterOptionAlgorithm"]:
        return self._alter_algorithm
