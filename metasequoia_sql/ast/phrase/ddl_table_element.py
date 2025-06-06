"""
DDL 表元素（ddl table element）
"""

from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.phrase.field_type import FieldType
    from metasequoia_sql.ast.phrase.column_attribute import ColumnAttribute
    from metasequoia_sql.ast.basic.charset_name import Charset
    from metasequoia_sql.ast.basic.ident import TableIdent
    from metasequoia_sql.ast.phrase.ddl_index_attribute import EnumIndexStructureType

__all__ = [
    "FieldDefinition",
    "GeneratedFieldDefinition",
    "ReferencesDefinition",
    "ColumnDefinition",
    "TempOnUpdateOnDelete",
    "TempIndexNameAndType",
    "EnumStoredAttribute",
    "EnumReferenceMatch",
    "EnumReferenceActionOption",
]


class EnumStoredAttribute(IntEnum):
    """DDL 生成字段存储方法"""

    DEFAULT = 1  # DEFAULT
    VIRTUAL = 2  # VIRTUAL
    STORED = 3  # STORED


class FieldDefinition(Node):
    """DDL 字段定义信息"""

    __slots__ = (
        "_field_type",
        "_attribute_list"
    )

    def __init__(self, field_type: "FieldType", attribute_list: List["ColumnAttribute"]):
        self._field_type = field_type
        self._attribute_list = attribute_list

    @property
    def field_type(self) -> "FieldType":
        return self._field_type

    @property
    def attribute_list(self) -> List["ColumnAttribute"]:
        return self._attribute_list


class GeneratedFieldDefinition(FieldDefinition):
    """DDL 生成字段信息"""

    __slots__ = (
        "_collate_charset",
        "_generated_always",
        "_generated_expression",
        "_stored_attribute"
    )

    def __init__(self, field_type: "FieldType",
                 collate_charset: Optional["Charset"],
                 generated_always: bool,
                 generated_expression: Expression,
                 stored_attribute: EnumStoredAttribute,
                 attribute_list: List["ColumnAttribute"]):
        super().__init__(field_type, attribute_list)
        self._collate_charset = collate_charset
        self._generated_always = generated_always
        self._generated_expression = generated_expression
        self._stored_attribute = stored_attribute

    @property
    def collate_charset(self) -> Optional["Charset"]:
        return self._collate_charset

    @property
    def generated_always(self) -> bool:
        return self._generated_always

    @property
    def generated_expression(self) -> Expression:
        return self._generated_expression

    @property
    def stored_attribute(self) -> EnumStoredAttribute:
        return self._stored_attribute


class EnumReferenceMatch(IntEnum):
    """REFERENCES 子句中的 MATCH 子句的枚举值"""

    DEFAULT = 0  # %empty
    MATCH_FULL = 1  # MATCH FULL
    MATCH_PARTIAL = 2  # MATCH PARTIAL
    MATCH_SIMPLE = 3  # MATCH SIMPLE


class EnumReferenceActionOption(IntEnum):
    """REFERENCE 子句中指定外键变化时行为的选项枚举值"""

    DEFAULT = 0  # %empty
    RESTRICT = 1  # RESTRICT
    CASCADE = 2  # CASCADE
    SET_NULL = 3  # SET NULL
    NO_ACTION = 4  # NO ACTION
    SET_DEFAULT = 5  # SET DEFAULT


class TempOnUpdateOnDelete(Node):
    """【临时】REFERENCES 指定外键约束子句中的 ON UPDATE 和 ON DELETE 子句"""

    __slots__ = (
        "_on_update",
        "_on_delete"
    )

    def __init__(self,
                 on_update: EnumReferenceActionOption,
                 on_delete: EnumReferenceActionOption):
        self._on_update = on_update
        self._on_delete = on_delete

    @property
    def on_update(self) -> EnumReferenceActionOption:
        return self._on_update

    @property
    def on_delete(self) -> EnumReferenceActionOption:
        return self._on_delete


class ReferencesDefinition(Node):
    """`REFERENCES` 关键字引导的指定外键约束子句"""

    __slots__ = (
        "_table_ident",
        "_column_list",
        "_match_clause",
        "_on_update",
        "_on_delete"
    )

    def __init__(self,
                 table_ident: "TableIdent",
                 column_list: List[str],
                 match_clause: EnumReferenceMatch,
                 on_update: EnumReferenceActionOption,
                 on_delete: EnumReferenceActionOption):
        self._table_ident = table_ident
        self._column_list = column_list
        self._match_clause = match_clause
        self._on_update = on_update
        self._on_delete = on_delete

    @property
    def table_ident(self) -> "TableIdent":
        return self._table_ident

    @property
    def column_list(self) -> List[str]:
        return self._column_list

    @property
    def match_clause(self) -> EnumReferenceMatch:
        return self._match_clause

    @property
    def on_update(self) -> EnumReferenceActionOption:
        return self._on_update

    @property
    def on_delete(self) -> EnumReferenceActionOption:
        return self._on_delete


class ColumnDefinition(Node):
    """DDL 字段定义信息"""

    __slots__ = (
        "_column_name",
        "_field_definition",
        "_references_definition"
    )

    def __init__(self,
                 column_name: str,
                 field_definition: FieldDefinition,
                 references_definition: Optional[ReferencesDefinition]):
        self._column_name = column_name
        self._field_definition = field_definition
        self._references_definition = references_definition

    @property
    def column_name(self) -> str:
        return self._column_name

    @property
    def field_definition(self) -> FieldDefinition:
        return self._field_definition

    @property
    def references_definition(self) -> Optional[ReferencesDefinition]:
        return self._references_definition


class TempIndexNameAndType(Node):
    """【临时】索引名称和数据结构类型"""

    __slots__ = (
        "_index_name",
        "_index_structure_type"
    )

    def __init__(self,
                 index_name: Optional[str],
                 index_structure_type: "EnumIndexStructureType"):
        self._index_name = index_name
        self._index_structure_type = index_structure_type

    @property
    def index_name(self) -> Optional[str]:
        return self._index_name

    @property
    def index_structure_type(self) -> "EnumIndexStructureType":
        return self._index_structure_type
