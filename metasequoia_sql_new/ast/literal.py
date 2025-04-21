"""
字面值类型节点
"""

import decimal
import enum
import typing

from metasequoia_sql_new.ast.base import Expression

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
]


class StringLiteral(Expression):
    """字符串字面值"""

    def __init__(self, value: str, charset: typing.Optional[str] = None):
        self._value = value
        self._charset = charset  # 字符集（如果没有指定字符集则为 None）

    def attr_list(self) -> typing.List[str]:
        return ["value", "charset"]

    @property
    def value(self) -> str:
        return self._value

    @property
    def charset(self) -> typing.Optional[str]:
        return self._charset


class HexStringLiteral(StringLiteral):
    """十六进制字符串字面值"""


class BinStringLiteral(StringLiteral):
    """二进制字符串字面值"""


class IntLiteral(Expression):
    """整数字面值"""

    def __init__(self, value: str):
        self._value: int = int(value)

    def attr_list(self) -> typing.List[str]:
        return ["value"]

    @property
    def value(self) -> int:
        return self._value


class DecimalLiteral(Expression):
    """小数字面值"""

    def __init__(self, value: str):
        self._value: decimal.Decimal = decimal.Decimal(value)

    def attr_list(self) -> typing.List[str]:
        return ["value"]

    @property
    def value(self) -> decimal.Decimal:
        return self._value


class FloatLiteral(Expression):
    """浮点数字面值"""

    def __init__(self, value: str):
        self._value: float = float(value)

    def attr_list(self) -> typing.List[str]:
        return ["value"]

    @property
    def value(self) -> float:
        return self._value


class TemporalLiteral(Expression):
    """时间类型字面值"""

    class EnumTemporalType(enum.IntEnum):
        """时间类型字面值的枚举值"""
        DATE = 1
        TIME = 2
        DATETIME = 3

    def __init__(self, temporal_type: "TemporalLiteral.EnumTemporalType", value: str):
        self._temporal_type: TemporalLiteral.EnumTemporalType = temporal_type
        self._value = value

    def attr_list(self) -> typing.List[str]:
        return ["temporal_type", "value"]

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


class FalseLiteral(Expression):
    """假值字面值"""

    def attr_list(self) -> typing.List[str]:
        return []


class TrueLiteral(Expression):
    """真值字面值"""

    def attr_list(self) -> typing.List[str]:
        return []


class NullLiteral(Expression):
    """空值字面值"""

    def attr_list(self) -> typing.List[str]:
        return []
