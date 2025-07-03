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
        """
        初始化标识符节点

        Parameters
        ----------
        value : str
            标识符的值
        """
        self._value = value

    @property
    def value(self) -> str:
        """
        获取标识符的值

        Returns
        -------
        str
            标识符的值
        """
        return self._value

    def get_str_value(self) -> Optional[str]:
        """
        获取标识符的字符串值

        Returns
        -------
        Optional[str]
            标识符的字符串值
        """
        return self._value


class Ident2D(Expression):
    """ident.ident"""

    __slots__ = ["_value1", "_value2"]

    def __init__(self, value1: str, value2: str):
        """
        初始化二维标识符节点

        Parameters
        ----------
        value1 : str
            第一个标识符的值
        value2 : str
            第二个标识符的值
        """
        self._value1 = value1
        self._value2 = value2

    @property
    def value1(self) -> str:
        """
        获取第一个标识符的值

        Returns
        -------
        str
            第一个标识符的值
        """
        return self._value1

    @property
    def value2(self) -> str:
        """
        获取第二个标识符的值

        Returns
        -------
        str
            第二个标识符的值
        """
        return self._value2


class Ident3D(Expression):
    """ident.ident.ident"""

    __slots__ = ["_value1", "_value2", "_value3"]

    def __init__(self, value1: str, value2: str, value3: str):
        """
        初始化三维标识符节点

        Parameters
        ----------
        value1 : str
            第一个标识符的值
        value2 : str
            第二个标识符的值
        value3 : str
            第三个标识符的值
        """
        self._value1 = value1
        self._value2 = value2
        self._value3 = value3

    @property
    def value1(self) -> str:
        """
        获取第一个标识符的值

        Returns
        -------
        str
            第一个标识符的值
        """
        return self._value1

    @property
    def value2(self) -> str:
        """
        获取第二个标识符的值

        Returns
        -------
        str
            第二个标识符的值
        """
        return self._value2

    @property
    def value3(self) -> str:
        """
        获取第三个标识符的值

        Returns
        -------
        str
            第三个标识符的值
        """
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
        """
        初始化通用标识符

        Parameters
        ----------
        schema_name : Optional[str]
            模式名称，可选
        object_name : str
            对象名称
        """
        self._schema_name = schema_name
        self._object_name = object_name

    @property
    def schema_name(self) -> Optional[str]:
        """
        获取模式名称

        Returns
        -------
        Optional[str]
            模式名称，如果没有则返回 None
        """
        return self._schema_name

    @property
    def object_name(self) -> str:
        """
        获取对象名称

        Returns
        -------
        str
            对象名称
        """
        return self._object_name
