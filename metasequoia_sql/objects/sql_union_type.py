"""
组合类型
"""

import enum

from metasequoia_sql.objects.sql_base import SQLBase
from metasequoia_sql.objects.data_source import DataSource

__all__ = ["SQLUnionType", "EnumUnionType"]


# ---------------------------------------- 组合类型 ----------------------------------------


class EnumUnionType(enum.Enum):
    """组合类型的枚举类"""
    UNION_ALL = ["UNION", "ALL"]
    UNION = ["UNION"]
    EXCEPT = ["EXCEPT"]
    INTERSECT = ["INTERSECT"]
    MINUS = ["MINUS"]


class SQLUnionType(SQLBase):
    """组合类型"""

    def __init__(self, union_type: EnumUnionType):
        self._union_type = union_type

    @property
    def union_type(self) -> EnumUnionType:
        return self._union_type

    def source(self, data_source: DataSource) -> str:
        return " ".join(self.union_type.value)
