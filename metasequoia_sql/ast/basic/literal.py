"""
字面值类型节点
"""

from abc import abstractmethod
from decimal import Decimal
from enum import IntEnum
from typing import Optional

from metasequoia_sql.ast.base import Expression
from metasequoia_sql.ast.base import Literal

__all__ = [
    "StringLiteral",
    "HexStringLiteral",
    "BinStringLiteral",
    "IntLiteral",
    "DecimalLiteral",
    "FloatLiteral",
    "TemporalLiteral",
    "FalseLiteral",
    "TrueLiteral",
    "NullLiteral",
    "Param",
    "Hostname",
]


class StringLiteral(Literal):
    """字符串字面值"""

    def __init__(self, value: str, charset: Optional[str] = None):
        self._value = value
        self._charset = charset  # 字符集（如果没有指定字符集则为 None）

    @property
    def value(self) -> str:
        return self._value

    @property
    def charset(self) -> Optional[str]:
        return self._charset

    def get_str_value(self) -> Optional[str]:
        return self._value


class HexStringLiteral(StringLiteral):
    """十六进制字符串字面值"""


class BinStringLiteral(StringLiteral):
    """二进制字符串字面值"""


class NumberLiteral(Literal):
    """数值字面值（包括整数、小数、浮点数）"""

    @abstractmethod
    def neg(self) -> "NumberLiteral":
        """计算当前数值字面值的值置为相反数，并返回当前数值字面值"""


class IntLiteral(NumberLiteral):
    """整数字面值"""

    def __init__(self, value: int):
        self._value = value

    @staticmethod
    def from_oct_string(oct_num: str) -> "IntLiteral":
        """根据十进制字符串构造整数"""
        return IntLiteral(int(oct_num))

    @staticmethod
    def from_hex_string(hex_num: str) -> "IntLiteral":
        """根据十六进制字符串构造整数"""
        return IntLiteral(int(hex_num, base=16))

    @property
    def value(self) -> int:
        return self._value

    def neg(self) -> "IntLiteral":
        self._value *= -1
        return self

    def get_decimal_value(self) -> Decimal:
        return Decimal(self._value)


class DecimalLiteral(NumberLiteral):
    """小数字面值"""

    def __init__(self, value: Decimal):
        self._value: Decimal = value

    @staticmethod
    def create(source_string: str):
        return DecimalLiteral(Decimal(source_string))

    @property
    def value(self) -> Decimal:
        return self._value

    def neg(self) -> "DecimalLiteral":
        self._value *= -1
        return self

    def get_decimal_value(self) -> Decimal:
        return self._value


class FloatLiteral(NumberLiteral):
    """浮点数字面值"""

    def __init__(self, value: str):
        self._value: float = float(value)

    @property
    def value(self) -> float:
        return self._value

    def neg(self) -> "FloatLiteral":
        self._value *= -1
        return self

    def get_decimal_value(self) -> Decimal:
        return Decimal.from_float(self._value)


class TemporalLiteral(Literal):
    """时间类型字面值"""

    class EnumTemporalType(IntEnum):
        """时间类型字面值的枚举值"""
        DATE = 1
        TIME = 2
        DATETIME = 3

    def __init__(self, temporal_type: "TemporalLiteral.EnumTemporalType", value: str):
        self._temporal_type: TemporalLiteral.EnumTemporalType = temporal_type
        self._value = value

    @staticmethod
    def create_date_literal(value: str) -> "TemporalLiteral":
        return TemporalLiteral(
            temporal_type=TemporalLiteral.EnumTemporalType.DATE,
            value=value
        )

    @staticmethod
    def create_time_literal(value: str) -> "TemporalLiteral":
        return TemporalLiteral(
            temporal_type=TemporalLiteral.EnumTemporalType.TIME,
            value=value
        )

    @staticmethod
    def create_datetime_literal(value: str) -> "TemporalLiteral":
        return TemporalLiteral(
            temporal_type=TemporalLiteral.EnumTemporalType.DATETIME,
            value=value
        )

    @property
    def temporal_type(self) -> "TemporalLiteral.EnumTemporalType":
        return self._temporal_type

    @property
    def value(self) -> str:
        return self._value


class FalseLiteral(Literal):
    """假值字面值"""


class TrueLiteral(Literal):
    """真值字面值"""


class NullLiteral(Literal):
    """空值字面值"""


class Param(Expression):
    """参数占位符"""


class Hostname(Expression):
    """@ 之后的 Token"""

    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def get_str_value(self) -> Optional[str]:
        return self._value
