"""
标识符类型节点
"""

from typing import Optional

from metasequoia_sql.ast.base import Expression

__all__ = [
    "Ident",
    "Ident2D",
    "Ident3D",
]


class Ident(Expression):
    """标识符节点"""

    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def get_str_value(self) -> Optional[str]:
        return self._value


class Ident2D(Expression):
    """ident.ident"""

    def __init__(self, value1: Ident, value2: Ident):
        self._value1 = value1
        self._value2 = value2

    @property
    def value1(self) -> Ident:
        return self._value1

    @property
    def value2(self) -> Ident:
        return self._value2


class Ident3D(Expression):
    """ident.ident.ident"""

    def __init__(self, value1: Ident, value2: Ident, value3: Ident):
        self._value1 = value1
        self._value2 = value2
        self._value3 = value3

    @property
    def value1(self) -> Ident:
        return self._value1

    @property
    def value2(self) -> Ident:
        return self._value2

    @property
    def value3(self) -> Ident:
        return self._value3
