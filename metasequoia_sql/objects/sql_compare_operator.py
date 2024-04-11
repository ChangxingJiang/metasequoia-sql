"""
比较运算符
"""

import enum
from typing import List

from metasequoia_sql.objects.data_source import DataSource
from metasequoia_sql.objects.sql_base import SQLBase

__all__ = ["SQLCompareOperator", "EnumCompareOperator"]


# ---------------------------------------- 比较运算符 ----------------------------------------


class EnumCompareOperator(enum.Enum):
    """比较运算符的枚举类"""
    EQ = "="
    EQUAL_TO = "="
    NEQ = "!="
    NOT_EQUAL_TO = "!="
    LT = "<"
    LESS_THAN = "<"
    LTE = "<="
    LESS_THAN_OR_EQUAL = "<="
    GT = ">"
    GREATER_THAN = ">"
    GTE = ">="
    GREATER_THAN_OR_EQUAL = ">="


class SQLCompareOperator(SQLBase):
    """比较运算符"""

    def __init__(self, compare_operator: EnumCompareOperator):
        self._compare_operator = compare_operator

    @property
    def compare_operator(self) -> EnumCompareOperator:
        return self._compare_operator

    def source(self, data_source: DataSource) -> str:
        return self.compare_operator.value

    @staticmethod
    def get_used_column_list() -> List[str]:
        """获取使用的字段列表"""
        return []
