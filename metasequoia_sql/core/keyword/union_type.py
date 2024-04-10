"""
组合类型
"""

import enum

from metasequoia_sql.common import TokenScanner
from metasequoia_sql.core import DataSource
from metasequoia_sql.core.base import SQLBase
from metasequoia_sql.errors import SqlParseError

__all__ = ["SQLUnionType"]


class EnumUnionType(enum.Enum):
    """关联类型"""
    UNION_ALL = ["UNION", "ALL"]
    UNION = ["UNION"]
    EXCEPT = ["EXCEPT"]
    INTERSECT = ["INTERSECT"]
    MINUS = ["MINUS"]


class SQLUnionType(SQLBase):
    """关联类型"""

    def __init__(self, union_type: EnumUnionType):
        self._union_type = union_type

    @property
    def union_type(self) -> EnumUnionType:
        return self._union_type

    def source(self, data_source: DataSource) -> str:
        return " ".join(self.union_type.value)

    @staticmethod
    def check(scanner: TokenScanner) -> bool:
        for union_type in EnumUnionType:
            if scanner.search(*union_type.value):
                return True
        return False

    @staticmethod
    def parse(scanner: TokenScanner) -> "SQLUnionType":
        for union_type in EnumUnionType:
            if scanner.search_and_move(*union_type.value):
                return SQLUnionType(union_type=union_type)
        raise SqlParseError(f"无法解析的组合类型: {scanner}")
