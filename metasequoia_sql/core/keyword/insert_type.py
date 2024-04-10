"""
插入语句类型
"""

import enum

from metasequoia_sql.common import TokenScanner
from metasequoia_sql.core import DataSource
from metasequoia_sql.core.base import SQLBase
from metasequoia_sql.errors import SqlParseError


__all__ = ["SQLInsertType"]


class EnumInsertType(enum.Enum):
    """插入类型"""
    INSERT_INTO = ["INSERT", "INTO"]
    INSERT_OVERWRITE = ["INSERT", "OVERWRITE"]


class SQLInsertType(SQLBase):
    def __init__(self, insert_type: EnumInsertType):
        self._insert_type = insert_type

    @property
    def insert_type(self) -> EnumInsertType:
        return self._insert_type

    def source(self, data_source: DataSource) -> str:
        return " ".join(self.insert_type.value)

    @staticmethod
    def check(scanner: TokenScanner) -> bool:
        """任何元素都可以是排序类型（省略升序），所以均返回 True"""
        return scanner.search_and_move("INSERT", "INTO") or scanner.search_and_move("INSERT", "OVERWRITE")

    @staticmethod
    def parse(scanner: TokenScanner) -> "SQLInsertType":
        # 解析 INSERT 类型
        if scanner.search_and_move("INSERT", "INTO"):
            return SQLInsertType(insert_type=EnumInsertType.INSERT_INTO)
        if scanner.search_and_move("INSERT", "OVERWRITE"):
            return SQLInsertType(insert_type=EnumInsertType.INSERT_OVERWRITE)
        raise SqlParseError(f"未知的 INSERT 类型: {scanner}")
