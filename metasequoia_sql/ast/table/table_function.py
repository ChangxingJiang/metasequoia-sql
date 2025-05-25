"""
生成表函数（table function）
"""

from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node, Table

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Ident
    from metasequoia_sql.ast.basic.charset_name import Charset
    from metasequoia_sql.ast.phrase.field_type import FieldType
    from metasequoia_sql.ast.phrase.json_table_option import JsonOnEmptyOnError

__all__ = [
    "JsonTableColumnType",
    "JsonTableColumnBase",
    "JsonTableColumnForOrdinality",
    "JsonTableColumnForPath",
    "JsonTableColumnForNestedColumns",
    "TableFunctionJsonTable",
]


class JsonTableColumnType(IntEnum):
    """JSON_TABLE 函数中的字段类型"""

    DEFAULT = 0
    EXISTS = 1  # EXISTS（如果 Json 路径存在则为 1，否则为 0）


class JsonTableColumnBase(Node):
    """JSON_TABLE 函数中字段的抽象类"""


class JsonTableColumnForOrdinality(JsonTableColumnBase):
    """JSON_TABLE 函数中的自增字段"""

    __slots__ = ["_column_name"]

    def __init__(self, column_name: "Ident"):
        self._column_name = column_name

    @property
    def column_name(self) -> "Ident":
        return self._column_name


class JsonTableColumnForPath(Node):
    """JSON_TABLE 函数中的通过 Json 路径提取的字段"""

    __slots__ = ["_column_name", "_field_type", "_collate", "_column_type", "_json_path", "_json_on_empty_on_error"]

    def __init__(self,
                 column_name: "Ident",
                 field_type: "FieldType",
                 collate: "Charset",
                 column_type: JsonTableColumnType,
                 json_path: str,
                 json_on_empty_on_error: "JsonOnEmptyOnError"):
        self._column_name = column_name
        self._field_type = field_type
        self._collate = collate
        self._column_type = column_type
        self._json_path = json_path
        self._json_on_empty_on_error = json_on_empty_on_error

    @property
    def column_name(self) -> "Ident":
        return self._column_name

    @property
    def field_type(self) -> "FieldType":
        return self._field_type

    @property
    def collate(self) -> "Charset":
        return self._collate

    @property
    def column_type(self) -> JsonTableColumnType:
        return self._column_type

    @property
    def json_path(self) -> str:
        return self._json_path

    @property
    def json_on_empty_on_error(self) -> "JsonOnEmptyOnError":
        return self._json_on_empty_on_error


class JsonTableColumnForNestedColumns(JsonTableColumnBase):
    """JSON_TABLE 函数中通过 Json 路径炸开的字段列表"""

    __slots__ = ["_json_path", "_column_list"]

    def __init__(self, json_path: str, column_list: List[JsonTableColumnBase]):
        self._json_path = json_path
        self._column_list = column_list

    @property
    def json_path(self) -> str:
        return self._json_path

    @property
    def column_list(self) -> List[JsonTableColumnBase]:
        return self._column_list


class TableFunctionJsonTable(Table):
    """窗口生成函数：JSON_TABLE 函数"""

    __slots__ = ["_json_doc", "_json_path", "_column_list", "_table_alias"]

    def __init__(self, json_doc: Expression, json_path: str, column_list: List[JsonTableColumnBase],
                 table_alias: Optional[str]):
        self._json_doc = json_doc
        self._json_path = json_path
        self._column_list = column_list
        self._table_alias = table_alias

    @property
    def json_doc(self) -> Expression:
        return self._json_doc

    @property
    def json_path(self) -> str:
        return self._json_path

    @property
    def column_list(self) -> List[JsonTableColumnBase]:
        return self._column_list

    @property
    def table_alias(self) -> Optional[str]:
        return self._table_alias
