"""
INTO 子句（into clause）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.charset_name import Charset
    from metasequoia_sql.ast.basic.variable import Variable

__all__ = [
    "FileFieldOption",
    "FileLineOption",
    "IntoClause",
    "IntoClauseOutfile",
    "IntoClauseDumpfile",
    "IntoClauseVariable",
]


class FileFieldOption(Node):
    """外部文件字段格式选项"""

    __slots__ = ["_terminated_by", "_optionally_enclosed_by", "_enclosed_by", "_escaped_by"]

    def __init__(self,
                 terminated_by: Optional[str] = None,
                 optionally_enclosed_by: Optional[str] = None,
                 enclosed_by: Optional[str] = None,
                 escaped_by: Optional[str] = None):
        self._terminated_by = terminated_by
        self._optionally_enclosed_by = optionally_enclosed_by
        self._enclosed_by = enclosed_by
        self._escaped_by = escaped_by

    @property
    def terminated_by(self) -> str:
        return self._terminated_by

    @property
    def optionally_enclosed_by(self) -> str:
        return self._optionally_enclosed_by

    @property
    def enclosed_by(self) -> str:
        return self._enclosed_by

    @property
    def escaped_by(self) -> str:
        return self._escaped_by

    def merge(self, other: "FileFieldOption") -> "FileFieldOption":
        if other._terminated_by is not None:
            self._terminated_by = other._terminated_by
        if other._optionally_enclosed_by is not None:
            self._optionally_enclosed_by = other._optionally_enclosed_by
        if other._enclosed_by is not None:
            self._enclosed_by = other._enclosed_by
        if other._escaped_by is not None:
            self._escaped_by = other._escaped_by
        return self


class FileLineOption(Node):
    """外部文件行字段格式选项"""

    __slots__ = ["_terminated_by", "_starting_by"]

    def __init__(self,
                 terminated_by: Optional[str] = None,
                 starting_by: Optional[str] = None):
        self._terminated_by = terminated_by
        self._starting_by = starting_by

    @property
    def terminated_by(self) -> Optional[str]:
        return self._terminated_by

    @property
    def starting_by(self) -> Optional[str]:
        return self._starting_by

    def merge(self, other: "FileLineOption") -> "FileLineOption":
        if other._terminated_by is not None:
            self._terminated_by = other._terminated_by
        if other._starting_by is not None:
            self._starting_by = other._starting_by
        return self


class IntoClause(Node):
    """INTO 子句的抽象类"""


class IntoClauseOutfile(IntoClause):
    """INTO 子句（导出结果集到外部格式化文件）"""

    __slots__ = ["_file_path", "_charset", "_field_option", "_line_option"]

    def __init__(self, file_path: str, charset: Optional["Charset"], field_option: FileFieldOption,
                 line_option: FileLineOption):
        self._file_path = file_path
        self._charset = charset
        self._field_option = field_option
        self._line_option = line_option

    @property
    def file_path(self) -> str:
        return self._file_path

    @property
    def charset(self) -> "Charset":
        return self._charset

    @property
    def field_option(self) -> FileFieldOption:
        return self._field_option

    @property
    def line_option(self) -> FileLineOption:
        return self._line_option


class IntoClauseDumpfile(IntoClause):
    """INTO 子句（导出结果集到外部文件）"""

    __slots__ = ["_file_path"]

    def __init__(self, file_path: str):
        self._file_path = file_path

    @property
    def file_path(self) -> str:
        return self._file_path


class IntoClauseVariable(IntoClause):
    """INTO 子句（导出结果集到变量）"""

    __slots__ = ["_variable_list"]

    def __init__(self, variable_list: List["Variable"]):
        self._variable_list = variable_list

    @property
    def variable_list(self) -> List["Variable"]:
        return self._variable_list
