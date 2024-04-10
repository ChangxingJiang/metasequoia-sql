"""
排序类型
"""

import enum

from metasequoia_sql.common import TokenScanner
from metasequoia_sql.core import DataSource
from metasequoia_sql.core.base import SQLBaseTemp

__all__ = ["SQLOrderType"]


class EnumOrderType(enum.Enum):
    """排序类型"""
    ASC = "ASC"  # 升序
    DESC = "DESC"  # 降序


class SQLOrderType(SQLBaseTemp):
    def __init__(self, order_type: EnumOrderType):
        self._order_type = order_type

    @property
    def order_type(self) -> EnumOrderType:
        return self._order_type

    def source(self, data_source: DataSource) -> str:
        return self.order_type.value

    @staticmethod
    def check(scanner: TokenScanner) -> bool:
        """任何元素都可以是排序类型（省略升序），所以均返回 True"""
        return True

    @staticmethod
    def parse(scanner: TokenScanner) -> "SQLOrderType":
        if scanner.search_and_move("DESC"):
            return SQLOrderType(order_type=EnumOrderType.DESC)
        return SQLOrderType(order_type=EnumOrderType.ASC)
