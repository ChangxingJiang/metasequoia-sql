"""
DDL 索引属性（ddl index attribute）
"""

from enum import IntEnum
from typing import TYPE_CHECKING

from metasequoia_sql.ast.base import Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.literal import NumberLiteral

__all__ = [
    "IndexAttribute",
    "IndexAttrKeyBlockSize",
    "IndexAttrComment",
    "IndexAttrVisible",
    "IndexAttrInvisible",
    "IndexAttrEngineAttribute",
    "IndexAttrSecondaryEngineAttribute",
    "IndexAttrWithParser",
    "IndexAttrUsingIndexType",
    "EnumIndexStructureType"
]


class IndexAttribute(Node):
    """DDL 索引属性"""


class IndexAttrKeyBlockSize(IndexAttribute):
    """KEY_BLOCK_SIZE"""

    __slots__ = (
        "_block_size"
    )

    def __init__(self, block_size: "NumberLiteral"):
        self._block_size = block_size

    @property
    def block_size(self) -> "NumberLiteral":
        return self._block_size


class IndexAttrComment(IndexAttribute):
    """COMMENT"""

    __slots__ = (
        "_comment"
    )

    def __init__(self, comment: str):
        self._comment = comment

    @property
    def comment(self) -> str:
        return self._comment


class IndexAttrVisible(IndexAttribute):
    """VISIBLE"""


class IndexAttrInvisible(IndexAttribute):
    """INVISIBLE"""


class IndexAttrEngineAttribute(IndexAttribute):
    """ENGINE_ATTRIBUTE"""

    __slots__ = (
        "_attribute"
    )

    def __init__(self, attribute: str):
        self._attribute = attribute

    @property
    def attribute(self) -> str:
        return self._attribute


class IndexAttrSecondaryEngineAttribute(IndexAttribute):
    """SECONDARY_ENGINE_ATTRIBUTE"""

    __slots__ = (
        "_attribute"
    )

    def __init__(self, attribute: str):
        self._attribute = attribute

    @property
    def attribute(self) -> str:
        return self._attribute


class IndexAttrWithParser(IndexAttribute):
    """WITH PARSER"""

    __slots__ = (
        "_parser_name"
    )

    def __init__(self, parser_name: str):
        self._parser_name = parser_name

    @property
    def parser_name(self) -> str:
        return self._parser_name


class EnumIndexStructureType(IntEnum):
    """索引数据结构类型"""

    DEFAULT = 0  # %empty
    BTREE = 1  # BTREE
    RTREE = 2  # RTREE
    HASH = 3  # HASH


class IndexAttrUsingIndexType(IndexAttribute):
    """指定索引数据结构类型的子句

    USING index_type
    TYPE index_type
    """

    __slots__ = (
        "_index_structure_type"
    )

    def __init__(self, index_structure_type: EnumIndexStructureType):
        self._index_structure_type = index_structure_type

    @property
    def index_structure_type(self) -> EnumIndexStructureType:
        return self._index_structure_type
