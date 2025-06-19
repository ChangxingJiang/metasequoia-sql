"""
LOAD 语句（load statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node, Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.fixed_enum import EnumDataType, EnumLoadDataLock, EnumLoadSourceType
    from metasequoia_sql.ast.phrase.on_duplicate import OnDuplicate
    from metasequoia_sql.ast.basic.charset_name import Charset
    from metasequoia_sql.ast.clause.into_clause import FileFieldOption, FileLineOption

__all__ = [
    "LoadStatement",
    "LoadDataSetElement",
]


class LoadStatement(Statement):
    """LOAD 语句"""

    __slots__ = (
        "_data_type", "_load_data_lock", "_is_local", "_source_type", "_source_file", "_source_count",
        "_in_primary_key_order", "_on_duplicate",
        "_table_ident",
        "_use_partition",
        "_load_data_charset",
        "_xml_rows_identified_by",
        "_field_option",
        "_line_option",
        "_ignore_lines",
        "_field_or_var_list",
        "_load_data_set_list", "_parallel_count", "_memory_size", "_use_bulk_algorithm"
    )

    def __init__(self,
                 data_type: "EnumDataType",
                 load_data_lock: "EnumLoadDataLock",
                 is_local: bool,
                 source_type: "EnumLoadSourceType",
                 source_file: str,
                 source_count: int,
                 in_primary_key_order: bool,
                 on_duplicate: "OnDuplicate",
                 table_ident: "Identifier",
                 use_partition: Optional[List[Expression]],
                 load_data_charset: "Charset",
                 xml_rows_identified_by: Optional[str],
                 field_option: "FileFieldOption",
                 line_option: "FileLineOption",
                 ignore_lines: int,
                 field_or_var_list: List[Expression],
                 load_data_set_list: List["LoadDataSetElement"],
                 parallel_count: int,
                 memory_size: int,
                 use_bulk_algorithm: bool):
        self._data_type = data_type
        self._load_data_lock = load_data_lock
        self._is_local = is_local
        self._source_type = source_type
        self._source_file = source_file
        self._source_count = source_count
        self._in_primary_key_order = in_primary_key_order
        self._on_duplicate = on_duplicate
        self._table_ident = table_ident
        self._use_partition = use_partition
        self._load_data_charset = load_data_charset
        self._xml_rows_identified_by = xml_rows_identified_by
        self._field_option = field_option
        self._line_option = line_option
        self._ignore_lines = ignore_lines
        self._field_or_var_list = field_or_var_list
        self._load_data_set_list = load_data_set_list
        self._parallel_count = parallel_count
        self._memory_size = memory_size
        self._use_bulk_algorithm = use_bulk_algorithm

    @property
    def data_type(self) -> "EnumDataType":
        return self._data_type

    @property
    def load_data_lock(self) -> "EnumLoadDataLock":
        return self._load_data_lock

    @property
    def is_local(self) -> bool:
        return self._is_local

    @property
    def source_type(self) -> "EnumLoadSourceType":
        return self._source_type

    @property
    def source_file(self) -> str:
        return self._source_file

    @property
    def source_count(self) -> int:
        return self._source_count

    @property
    def in_primary_key_order(self) -> bool:
        return self._in_primary_key_order

    @property
    def on_duplicate(self) -> "OnDuplicate":
        return self._on_duplicate

    @property
    def table_ident(self) -> "Identifier":
        return self._table_ident

    @property
    def use_partition(self) -> Optional[List[Expression]]:
        return self._use_partition

    @property
    def load_data_charset(self) -> "Charset":
        return self._load_data_charset

    @property
    def xml_rows_identified_by(self) -> Optional[str]:
        return self._xml_rows_identified_by

    @property
    def field_option(self) -> "FileFieldOption":
        return self._field_option

    @property
    def line_option(self) -> "FileLineOption":
        return self._line_option

    @property
    def ignore_lines(self) -> int:
        return self._ignore_lines

    @property
    def field_or_var_list(self) -> List[Expression]:
        return self._field_or_var_list

    @property
    def load_data_set_list(self) -> List["LoadDataSetElement"]:
        return self._load_data_set_list

    @property
    def parallel_count(self) -> int:
        return self._parallel_count

    @property
    def memory_size(self) -> int:
        return self._memory_size

    @property
    def use_bulk_algorithm(self) -> bool:
        return self._use_bulk_algorithm


class LoadDataSetElement(Node):
    """LOAD 语句中的 SET 子句元素"""

    __slots__ = ["_variable", "_expression"]

    def __init__(self, variable: Expression, expression: Expression):
        self._variable = variable
        self._expression = expression

    @property
    def variable(self) -> Expression:
        return self._variable

    @property
    def expression(self) -> Expression:
        return self._expression
