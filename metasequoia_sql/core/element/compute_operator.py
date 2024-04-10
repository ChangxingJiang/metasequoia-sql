"""
计算运算符
"""

import enum
from typing import List

from metasequoia_sql.common import TokenScanner
from metasequoia_sql.core.base import SQLBase
from metasequoia_sql.core.data_source import DataSource
from metasequoia_sql.errors import UnSupportDataSourceError, SqlParseError


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

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"

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
    def check(scanner: TokenScanner) -> bool:
        for compute_operator in EnumComputeOperator:
            if scanner.search(compute_operator.value):
                return True
        return False

    @staticmethod
    def parse(scanner: TokenScanner) -> "SQLComputeOperator":
        for compute_operator in EnumComputeOperator:
            if scanner.search_and_move(compute_operator.value):
                return SQLComputeOperator(compute_operator=compute_operator)
        raise SqlParseError(f"无法解析的计算运算符: {scanner}")

    @staticmethod
    def get_used_column_list() -> List[str]:
        """获取使用的字段列表"""
        return []


if __name__ == "__main__":
    from metasequoia_sql.common import build_token_scanner

    assert SQLComputeOperator.check(build_token_scanner("+ 3")) is True
    assert SQLComputeOperator.check(build_token_scanner("- 3")) is True
    assert SQLComputeOperator.check(build_token_scanner("* 3")) is True
    assert SQLComputeOperator.check(build_token_scanner("/ 3")) is True
    assert SQLComputeOperator.check(build_token_scanner("% 3")) is True
    assert SQLComputeOperator.check(build_token_scanner("|| 'A'")) is True
    assert SQLComputeOperator.check(build_token_scanner("3 + 3")) is False

    assert SQLComputeOperator.parse(build_token_scanner("+ 3")).source(DataSource.MYSQL) == "+"
    assert SQLComputeOperator.parse(build_token_scanner("- 3")).source(DataSource.MYSQL) == "-"
    assert SQLComputeOperator.parse(build_token_scanner("* 3")).source(DataSource.MYSQL) == "*"
    assert SQLComputeOperator.parse(build_token_scanner("/ 3")).source(DataSource.MYSQL) == "/"
    assert SQLComputeOperator.parse(build_token_scanner("% 3")).source(DataSource.SQL_SERVER) == "%"
    assert SQLComputeOperator.parse(build_token_scanner("|| 'A'")).source(DataSource.ORACLE) == "||"
