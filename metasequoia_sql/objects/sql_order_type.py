"""
排序类型
"""

import enum

from metasequoia_sql.objects.sql_base import SQLBase
from metasequoia_sql.objects.data_source import DataSource

__all__ = ["SQLOrderType", "EnumOrderType"]


# ---------------------------------------- 排序类型 ----------------------------------------


class EnumOrderType(enum.Enum):
    """排序类型"""
    ASC = "ASC"  # 升序
    DESC = "DESC"  # 降序


class SQLOrderType(SQLBase):
    def __init__(self, order_type: EnumOrderType):
        self._order_type = order_type

    @property
    def order_type(self) -> EnumOrderType:
        return self._order_type

    def source(self, data_source: DataSource) -> str:
        return self.order_type.value
