"""
字面值类型节点
"""

import decimal
import enum
import typing

from metasequoia_sql_new.ast.base import Expression

__all__ = [
    "TextLiteral",
    "IntLiteral",
    "DecimalLiteral",
    "FloatLiteral",
    "TemporalLiteral"
]


class TextLiteral(Expression):
    """字符串字面值"""

    def __init__(self, value: str):
        self._value = value

    def attr_list(self) -> typing.List[str]:
        return ["value"]

    @property
    def value(self) -> str:
        return self._value


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
        return ["value"]

    @property
    def temporal_type(self) -> "TemporalLiteral.EnumTemporalType":
        return self._temporal_type

    @property
    def value(self) -> str:
        return self._value
