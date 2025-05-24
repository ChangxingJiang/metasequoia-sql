"""
变量（variable）
"""

from enum import IntEnum
from typing import Optional

from metasequoia_sql.ast.base import Expression

__all__ = [
    "UserVariable",
    "EnumSystemVariableType",
    "SystemVariable",
    "UserVariableAssignment",
]


class UserVariable(Expression):
    """用户变量"""

    __slots__ = ["_variable_name"]

    def __init__(self, variable_name: str):
        self._variable_name = variable_name

    @property
    def variable_name(self) -> str:
        return self._variable_name


class EnumSystemVariableType(IntEnum):
    """系统变量的类型"""

    DEFAULT = 0  # %empty
    GLOBAL = 1  # GLOBAL
    LOCAL = 2  # LOCAL
    SESSION = 3  # SESSION


class SystemVariable(Expression):
    """系统变量"""

    __slots__ = ["_variable_type", "_variable_namespace", "_variable_name"]

    def __init__(self, variable_type: EnumSystemVariableType, variable_namespace: Optional[str], variable_name: str):
        self._variable_type = variable_type
        self._variable_namespace = variable_namespace
        self._variable_name = variable_name

    @property
    def variable_type(self) -> EnumSystemVariableType:
        return self._variable_type

    @property
    def variable_namespace(self) -> Optional[str]:
        return self._variable_namespace

    @property
    def variable_name(self) -> str:
        return self._variable_name


class UserVariableAssignment(Expression):
    """用户变量赋值"""

    __slots__ = ["_variable_name", "_variable_value"]

    def __init__(self, variable_name: str, variable_value: Expression):
        self._variable_name = variable_name
        self._variable_value = variable_value

    @property
    def variable_name(self) -> str:
        return self._variable_name

    @property
    def variable_value(self) -> Expression:
        return self._variable_value
