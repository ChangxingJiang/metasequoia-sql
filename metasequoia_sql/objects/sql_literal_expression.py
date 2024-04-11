"""
字面值表达式
"""

import abc
from typing import List
from typing import Optional

from metasequoia_sql.objects.data_source import DataSource
from metasequoia_sql.objects.sql_general_expression import SQLGeneralExpression

__all__ = ["SQLLiteralExpression", "SQLLiteralIntegerExpression", "SQLLiteralFloatExpression",
           "SQLLiteralStringExpression", "SQLLiteralHexExpression", "SQLLiteralBitExpression",
           "SQLLiteralBoolExpression", "SQLLiteralNullExpression"]


class SQLLiteralExpression(SQLGeneralExpression, abc.ABC):
    """字面值表达式"""

    def as_int(self) -> Optional[int]:
        """将字面值作为整形返回"""
        return None

    def as_string(self) -> str:
        """将字面值作为字符串返回"""
        return self.source()

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return []


class SQLLiteralIntegerExpression(SQLLiteralExpression):
    """整数字面值"""

    def __init__(self, value: int):
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        return f"{self.value}"

    def as_int(self) -> int:
        return self.value

    def as_string(self) -> str:
        return f"{self.value}"


class SQLLiteralFloatExpression(SQLLiteralExpression):
    """浮点数字面值"""

    def __init__(self, value: float):
        self._value = value

    @property
    def value(self) -> float:
        return self._value

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        return f"{self.value}"

    def as_string(self) -> str:
        return f"{self.value}"


class SQLLiteralStringExpression(SQLLiteralExpression):
    """字符串字面值"""

    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        return f"'{self.value}'"

    def as_int(self) -> Optional[int]:
        if self.value.isdigit():
            return int(self.value)
        return None

    def as_string(self) -> Optional[str]:
        return self.value


class SQLLiteralHexExpression(SQLLiteralExpression):
    """十六进制字面值"""

    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        return f"x'{self._value}'"

    def as_string(self) -> str:
        return f"{self._value}"


class SQLLiteralBitExpression(SQLLiteralExpression):
    """位值字面值"""

    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        return f"b'{self._value}'"

    def as_string(self) -> str:
        return f"{self._value}"


class SQLLiteralBoolExpression(SQLLiteralExpression):
    """布尔值字面值"""

    def __init__(self, value: bool):
        self._value = value

    @property
    def value(self) -> bool:
        return self._value

    def as_int(self) -> int:
        return 1 if self.value is True else 0

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        return "TRUE" if self._value is True else "FALSE"


class SQLLiteralNullExpression(SQLLiteralExpression):
    """空值字面值"""

    @property
    def value(self) -> None:
        return None

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        return "NULL"
