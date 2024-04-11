"""
关联类型
"""

import enum

from metasequoia_sql.common import TokenScanner
from metasequoia_sql.objects.sql_base import SQLBase
from metasequoia_sql.objects.data_source import DataSource
from metasequoia_sql.errors import SqlParseError

__all__ = ["SQLJoinType", "EnumJoinType"]


class EnumJoinType(enum.Enum):
    """关联类型的枚举类"""
    JOIN = ["JOIN"]  # 内连接
    INNER_JOIN = ["INNER", "JOIN"]  # 内连接
    LEFT_JOIN = ["LEFT", "JOIN"]  # 左外连接
    LEFT_OUTER_JOIN = ["LEFT", "OUTER", "JOIN"]  # 左外连接
    RIGHT_JOIN = ["RIGHT", "JOIN"]  # 右外连接
    RIGHT_OUTER_JOIN = ["RIGHT", "OUTER", "JOIN"]  # 右外连接
    FULL_JOIN = ["FULL", "JOIN"]  # 全外连接
    FULL_OUTER_JOIN = ["FULL", "OUTER", "JOIN"]  # 全外连接
    CROSS_JOIN = ["CROSS", "JOIN"]  # 交叉连接


class SQLJoinType(SQLBase):
    """关联类型"""

    def __init__(self, join_type: EnumJoinType):
        self._join_type = join_type

    @property
    def join_type(self) -> EnumJoinType:
        return self._join_type

    def source(self, data_source: DataSource) -> str:
        return " ".join(self.join_type.value)

    @staticmethod
    def check(scanner: TokenScanner) -> bool:
        for join_type in EnumJoinType:
            if scanner.search(*join_type.value):
                return True
        return False

    @staticmethod
    def parse(scanner: TokenScanner) -> "SQLJoinType":
        for join_type in EnumJoinType:
            if scanner.search_and_move(*join_type.value):
                return SQLJoinType(join_type=join_type)
        raise SqlParseError(f"无法解析的关联类型: {scanner}")
