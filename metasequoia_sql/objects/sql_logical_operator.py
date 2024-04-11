"""
逻辑运算符
"""

import enum
from typing import List

from metasequoia_sql.objects.data_source import DataSource
from metasequoia_sql.objects.sql_base import SQLBase

__all__ = ["SQLLogicalOperator", "EnumLogicalOperator"]


class EnumLogicalOperator(enum.Enum):
    """逻辑运算符的枚举类"""
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


class SQLLogicalOperator(SQLBase):
    """逻辑运算符"""

    def __init__(self, logical_operator: EnumLogicalOperator):
        self._logical_operator = logical_operator

    @property
    def logical_operator(self) -> EnumLogicalOperator:
        return self._logical_operator

    def source(self, data_source: DataSource) -> str:
        return self.logical_operator.value

    @staticmethod
    def get_used_column_list() -> List[str]:
        """获取使用的字段列表"""
        return []
