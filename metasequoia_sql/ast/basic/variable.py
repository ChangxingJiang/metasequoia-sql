"""
变量（variable）
"""

from enum import IntEnum
from typing import Optional

from metasequoia_sql.ast.base import Expression

__all__ = [
    "Variable",
    "LocalVariable",
    "UserVariable",
    "EnumSystemVariableType",
    "SystemVariable",
    "UserVariableAssignment",
]


class Variable(Expression):
    """变量的抽象基类"""

    __slots__ = ["_variable_name"]

    def __init__(self, variable_name: str):
        """
        初始化变量

        Parameters
        ----------
        variable_name : str
            变量名称
        """
        self._variable_name = variable_name

    @property
    def variable_name(self) -> str:
        """
        获取变量名称

        Returns
        -------
        str
            变量名称
        """
        return self._variable_name


class LocalVariable(Variable):
    """本地变量（没有 @ 前缀）"""


class UserVariable(Variable):
    """用户变量（包含 @ 前缀）"""


class EnumSystemVariableType(IntEnum):
    """系统变量的类型"""

    DEFAULT = 0  # %empty
    GLOBAL = 1  # GLOBAL
    LOCAL = 2  # LOCAL
    SESSION = 3  # SESSION


class SystemVariable(Variable):
    """系统变量（包含 @@ 前缀）"""

    __slots__ = ["_variable_type", "_variable_namespace"]

    def __init__(self, variable_type: EnumSystemVariableType, variable_namespace: Optional[str], variable_name: str):
        """
        初始化系统变量

        Parameters
        ----------
        variable_type : EnumSystemVariableType
            系统变量类型
        variable_namespace : Optional[str]
            变量命名空间，可选
        variable_name : str
            变量名称
        """
        super().__init__(variable_name)
        self._variable_type = variable_type
        self._variable_namespace = variable_namespace

    @property
    def variable_type(self) -> EnumSystemVariableType:
        """
        获取变量类型

        Returns
        -------
        EnumSystemVariableType
            变量类型
        """
        return self._variable_type

    @property
    def variable_namespace(self) -> Optional[str]:
        """
        获取变量命名空间

        Returns
        -------
        Optional[str]
            变量命名空间，如果没有则返回 None
        """
        return self._variable_namespace


class UserVariableAssignment(Expression):
    """用户变量赋值"""

    __slots__ = ["_variable_name", "_variable_value"]

    def __init__(self, variable_name: str, variable_value: Expression):
        """
        初始化用户变量赋值

        Parameters
        ----------
        variable_name : str
            变量名称
        variable_value : Expression
            变量值表达式
        """
        self._variable_name = variable_name
        self._variable_value = variable_value

    @property
    def variable_name(self) -> str:
        """
        获取变量名称

        Returns
        -------
        str
            变量名称
        """
        return self._variable_name

    @property
    def variable_value(self) -> Expression:
        """
        获取变量值

        Returns
        -------
        Expression
            变量值表达式
        """
        return self._variable_value
