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
        "_block_size",
    )

    def __init__(self, block_size: "NumberLiteral"):
        """
        初始化键块大小属性。

        Parameters
        ----------
        block_size : NumberLiteral
            键块大小
        """
        self._block_size = block_size

    @property
    def block_size(self) -> "NumberLiteral":
        """获取键块大小。
        
        Returns
        -------
        NumberLiteral
            键块大小
        """
        return self._block_size


class IndexAttrComment(IndexAttribute):
    """COMMENT"""

    __slots__ = (
        "_comment",
    )

    def __init__(self, comment: str):
        """
        初始化索引注释属性。

        Parameters
        ----------
        comment : str
            注释内容
        """
        self._comment = comment

    @property
    def comment(self) -> str:
        """获取索引注释内容。
        
        Returns
        -------
        str
            注释内容
        """
        return self._comment


class IndexAttrVisible(IndexAttribute):
    """VISIBLE"""


class IndexAttrInvisible(IndexAttribute):
    """INVISIBLE"""


class IndexAttrEngineAttribute(IndexAttribute):
    """ENGINE_ATTRIBUTE"""

    __slots__ = (
        "_attribute",
    )

    def __init__(self, attribute: str):
        """
        初始化引擎属性。

        Parameters
        ----------
        attribute : str
            引擎属性
        """
        self._attribute = attribute

    @property
    def attribute(self) -> str:
        """获取引擎属性。
        
        Returns
        -------
        str
            引擎属性
        """
        return self._attribute


class IndexAttrSecondaryEngineAttribute(IndexAttribute):
    """SECONDARY_ENGINE_ATTRIBUTE"""

    __slots__ = (
        "_attribute",
    )

    def __init__(self, attribute: str):
        """
        初始化次级引擎属性。

        Parameters
        ----------
        attribute : str
            次级引擎属性
        """
        self._attribute = attribute

    @property
    def attribute(self) -> str:
        """获取次级引擎属性。
        
        Returns
        -------
        str
            次级引擎属性
        """
        return self._attribute


class IndexAttrWithParser(IndexAttribute):
    """WITH PARSER"""

    __slots__ = (
        "_parser_name",
    )

    def __init__(self, parser_name: str):
        """
        初始化解析器名称属性。

        Parameters
        ----------
        parser_name : str
            解析器名称
        """
        self._parser_name = parser_name

    @property
    def parser_name(self) -> str:
        """获取解析器名称。
        
        Returns
        -------
        str
            解析器名称
        """
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
        "_index_structure_type",
    )

    def __init__(self, index_structure_type: EnumIndexStructureType):
        """
        初始化索引结构类型属性。

        Parameters
        ----------
        index_structure_type : EnumIndexStructureType
            索引结构类型
        """
        self._index_structure_type = index_structure_type

    @property
    def index_structure_type(self) -> EnumIndexStructureType:
        """获取索引结构类型。
        
        Returns
        -------
        EnumIndexStructureType
            索引结构类型
        """
        return self._index_structure_type
