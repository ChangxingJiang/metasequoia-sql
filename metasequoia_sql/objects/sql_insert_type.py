"""
插入类型
"""

import enum

from metasequoia_sql.objects.sql_base import SQLBase
from metasequoia_sql.objects.data_source import DataSource

__all__ = ["SQLInsertType", "EnumInsertType"]


class EnumInsertType(enum.Enum):
    """插入类型"""
    INSERT_INTO = ["INSERT", "INTO"]
    INSERT_OVERWRITE = ["INSERT", "OVERWRITE"]


class SQLInsertType(SQLBase):
    """插入类型"""

    def __init__(self, insert_type: EnumInsertType):
        self._insert_type = insert_type

    @property
    def insert_type(self) -> EnumInsertType:
        return self._insert_type

    def source(self, data_source: DataSource) -> str:
        return " ".join(self.insert_type.value)
