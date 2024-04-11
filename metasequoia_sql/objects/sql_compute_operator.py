"""
计算运算符
"""

import enum
from typing import List

from metasequoia_sql.errors import UnSupportDataSourceError
from metasequoia_sql.objects.data_source import DataSource
from metasequoia_sql.objects.sql_base import SQLBase

__all__ = ["SQLComputeOperator", "EnumComputeOperator"]


# ---------------------------------------- 计算运算符 ----------------------------------------


class EnumComputeOperator(enum.Enum):
    """计算运算符的枚举类"""
    PLUS = "+"  # 加法运算符
    SUBTRACT = "-"  # 减法运算符
    MULTIPLE = "*"  # 乘法运算符
    DIVIDE = "/"  # 除法运算符
    MOD = "%"  # 取模运算符
    CONCAT = "||"  # 字符串拼接运算符（仅 Oracle、DB2、PostgreSQL 中适用）


class SQLComputeOperator(SQLBase):
    """计算运算符"""

    def __init__(self, compute_operator: EnumComputeOperator):
        self._compute_operator = compute_operator

    @property
    def compute_operator(self) -> EnumComputeOperator:
        return self._compute_operator

    def source(self, data_source: DataSource) -> str:
        if self.compute_operator == EnumComputeOperator.MOD and data_source != DataSource.SQL_SERVER:
            raise UnSupportDataSourceError(f"{data_source} 不支持使用 % 运算符")
        if (self.compute_operator == EnumComputeOperator.CONCAT
                and data_source not in {DataSource.ORACLE, DataSource.DB2, DataSource.POSTGRE_SQL}):
            raise UnSupportDataSourceError(f"{data_source} 不支持使用 || 运算符")
        return self.compute_operator.value

    @staticmethod
    def get_used_column_list() -> List[str]:
        """获取使用的字段列表"""
        return []
