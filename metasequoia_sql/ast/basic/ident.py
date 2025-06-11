"""
标识符类型节点
"""

from typing import Optional

from metasequoia_sql.ast.base import Expression

__all__ = [
    "Ident",
    "Ident2D",
    "Ident3D",
    "Identifier",
]


class Ident(Expression):
    """标识符节点"""

    __slots__ = ["_value"]

    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def get_str_value(self) -> Optional[str]:
        return self._value


class Ident2D(Expression):
    """ident.ident"""

    __slots__ = ["_value1", "_value2"]

    def __init__(self, value1: str, value2: str):
        self._value1 = value1
        self._value2 = value2

    @property
    def value1(self) -> str:
        return self._value1

    @property
    def value2(self) -> str:
        return self._value2


class Ident3D(Expression):
    """ident.ident.ident"""

    __slots__ = ["_value1", "_value2", "_value3"]

    def __init__(self, value1: str, value2: str, value3: str):
        self._value1 = value1
        self._value2 = value2
        self._value3 = value3

    @property
    def value1(self) -> str:
        return self._value1

    @property
    def value2(self) -> str:
        return self._value2

    @property
    def value3(self) -> str:
        return self._value3


class Identifier(Expression):
    """通用标识符

    应用场景：
    1. 表标识符
    2. 存储过程名称

    格式 1: schema_name . [table_name | sp_name]
    格式 2: [table_name | sp_name]
    """

    __slots__ = ["_schema_name", "_object_name"]

    def __init__(self, schema_name: Optional[str], object_name: str):
        self._schema_name = schema_name
        self._object_name = object_name

    @property
    def schema_name(self) -> Optional[str]:
        return self._schema_name

    @property
    def object_name(self) -> str:
        return self._object_name
