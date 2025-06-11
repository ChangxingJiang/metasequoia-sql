"""
DDL 表元素（ddl table element）
"""

from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.phrase.field_type import FieldType
    from metasequoia_sql.ast.phrase.ddl_column_attribute import ColumnAttribute
    from metasequoia_sql.ast.basic.charset_name import Charset
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.phrase.ddl_index_attribute import EnumIndexStructureType
    from metasequoia_sql.ast.clause.order_by_clause import EnumOrderDirection
    from metasequoia_sql.ast.phrase.ddl_index_attribute import IndexAttribute

__all__ = [
    "TableElement",

    # 字段定义
    "FieldDefinition",
    "GeneratedFieldDefinition",
    "ReferencesDefinition",
    "ColumnDefinition",

    # 索引定义
    "IndexDefinition",
    "IndexKeyDefinition",
    "ForeignKeyDefinition",
    "CheckConstraintDefinition",

    # 临时对象
    "TempOnUpdateOnDelete",
    "TempIndexNameAndType",

    # 枚举类
    "EnumStoredAttribute",
    "EnumReferenceMatch",
    "EnumReferenceActionOption",
    "EnumIndexType",
]


class EnumStoredAttribute(IntEnum):
    """DDL 生成字段存储方法"""

    DEFAULT = 1  # DEFAULT
    VIRTUAL = 2  # VIRTUAL
    STORED = 3  # STORED


class TableElement(Node):
    """DDL 表元素"""


class FieldDefinition(TableElement):
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
                 table_ident: "Identifier",
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
    def table_ident(self) -> "Identifier":
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


class IndexKeyDefinition(Node):
    """索引字段定义"""

    __slots__ = (
        "_column_name",
        "_index_length",
        "_expression",
        "_order_direction"
    )

    def __init__(self,
                 column_name: Optional[str],
                 index_length: Optional[int],
                 expression: Optional[Expression],
                 order_direction: "EnumOrderDirection"):
        self._column_name = column_name
        self._index_length = index_length
        self._expression = expression
        self._order_direction = order_direction

    @staticmethod
    def create_by_column(column_name: str, index_length: Optional[int],
                         order_direction: "EnumOrderDirection") -> "IndexKeyDefinition":
        return IndexKeyDefinition(column_name, index_length, None, order_direction)

    @staticmethod
    def create_by_expression(expression: Expression,
                             order_direction: "EnumOrderDirection") -> "IndexKeyDefinition":
        return IndexKeyDefinition(None, None, expression, order_direction)

    @property
    def column_name(self) -> str:
        return self._column_name

    @property
    def index_length(self) -> Optional[int]:
        return self._index_length

    @property
    def expression(self) -> Optional[Expression]:
        return self._expression

    @property
    def order_direction(self) -> "EnumOrderDirection":
        return self._order_direction


class EnumIndexType(IntEnum):
    """索引类型"""

    KEY = 1  # KEY、INDEX、INDEXES
    FULLTEXT = 2  # FULLTEXT、FULLTEXT KEY、FULLTEXT INDEX、FULLTEXT INDEXES
    SPATIAL = 3  # SPATIAL、SPATIAL KEY、SPATIAL INDEX、SPATIAL INDEXES
    PRIMARY = 4  # PRIMARY KEY
    UNIQUE = 5  # UNIQUE KEY、UNIQUE INDEX、UNIQUE INDEXES


class IndexDefinition(TableElement):
    """索引定义信息"""

    __slots__ = (
        "_index_type",
        "_index_name",
        "_index_structure_type",
        "_index_key_list",
        "_index_options"
    )

    def __init__(self,
                 index_type: EnumIndexType,
                 index_name: Optional[str],
                 index_structure_type: Optional["EnumIndexStructureType"],
                 index_key_list: List["IndexKeyDefinition"],
                 index_options: List["IndexAttribute"]
                 ):
        self._index_type = index_type
        self._index_name = index_name
        self._index_structure_type = index_structure_type
        self._index_key_list = index_key_list
        self._index_options = index_options

    @property
    def index_type(self) -> EnumIndexType:
        return self._index_type

    @property
    def index_name(self) -> Optional[str]:
        return self._index_name

    @property
    def index_structure_type(self) -> "EnumIndexStructureType":
        return self._index_structure_type

    @property
    def index_key_list(self) -> List["IndexKeyDefinition"]:
        return self._index_key_list

    @property
    def index_options(self) -> List["IndexAttribute"]:
        return self._index_options


class ForeignKeyDefinition(TableElement):
    """外键定义信息"""

    __slots__ = (
        "_constraint_name",
        "_index_name",
        "_column_list",
        "_references"
    )

    def __init__(self,
                 constraint_name: Optional[str],
                 index_name: Optional[str],
                 column_list: Optional[IndexKeyDefinition],
                 references: ReferencesDefinition
                 ):
        self._constraint_name = constraint_name
        self._index_name = index_name
        self._column_list = column_list
        self._references = references

    @property
    def constraint_name(self) -> Optional[str]:
        return self._constraint_name

    @property
    def index_name(self) -> Optional[str]:
        return self._index_name

    @property
    def column_list(self) -> Optional[IndexKeyDefinition]:
        return self._column_list

    @property
    def references(self) -> ReferencesDefinition:
        return self._references


class CheckConstraintDefinition(TableElement):
    """CHECK 约束"""

    __slots__ = (
        "_constraint_name",
        "_check_expression",
        "_enforced"
    )

    def __init__(self,
                 constraint_name: Optional[str],
                 check_expression: Expression,
                 enforced: Optional[bool]
                 ):
        self._constraint_name = constraint_name
        self._check_expression = check_expression
        self._enforced = enforced

    @property
    def constraint_name(self) -> Optional[str]:
        return self._constraint_name

    @property
    def check_expression(self) -> Expression:
        return self._check_expression

    @property
    def enforced(self) -> Optional[bool]:
        return self._enforced
