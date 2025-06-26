"""
字面值类型节点
"""

from abc import abstractmethod
from decimal import Decimal
from enum import IntEnum
from typing import Optional

from metasequoia_sql.ast.base import Expression, Literal, Node

__all__ = [
    "StringLiteral",
    "HexStringLiteral",
    "BinStringLiteral",
    "NumberLiteral",
    "IntLiteral",
    "DecimalLiteral",
    "FloatLiteral",
    "TemporalLiteral",
    "FalseLiteral",
    "TrueLiteral",
    "NullLiteral",
    "Param",
    "Hostname",
    "RoleName",
    "UserName",
]


class StringLiteral(Literal):
    """字符串字面值"""

    __slots__ = ["_value", "_charset"]

    def __init__(self, value: str, charset: Optional[str] = None):
        """
        初始化字符串字面值

        Parameters
        ----------
        value : str
            字符串值
        charset : Optional[str], optional
            字符集，如果没有指定字符集则为 None
        """
        self._value = value
        self._charset = charset  # 字符集（如果没有指定字符集则为 None）

    @property
    def value(self) -> str:
        """
        获取字符串值

        Returns
        -------
        str
            字符串值
        """
        return self._value

    @property
    def charset(self) -> Optional[str]:
        """
        获取字符集

        Returns
        -------
        Optional[str]
            字符集，如果没有则返回 None
        """
        return self._charset

    def get_str_value(self) -> Optional[str]:
        """
        获取字符串值

        Returns
        -------
        Optional[str]
            字符串值
        """
        return self._value


class HexStringLiteral(StringLiteral):
    """十六进制字符串字面值"""


class BinStringLiteral(StringLiteral):
    """二进制字符串字面值"""


class NumberLiteral(Literal):
    """数值字面值（包括整数、小数、浮点数）"""

    @abstractmethod
    def neg(self) -> "NumberLiteral":
        """
        计算当前数值字面值的值置为相反数，并返回当前数值字面值

        Returns
        -------
        NumberLiteral
            当前数值字面值对象
        """


class IntLiteral(NumberLiteral):
    """整数字面值"""

    __slots__ = ["_value"]

    def __init__(self, value: int):
        """
        初始化整数字面值

        Parameters
        ----------
        value : int
            整数值
        """
        self._value = value

    @staticmethod
    def from_oct_string(oct_num: str) -> "IntLiteral":
        """
        根据十进制字符串构造整数

        Parameters
        ----------
        oct_num : str
            十进制数字字符串

        Returns
        -------
        IntLiteral
            整数字面值对象
        """
        return IntLiteral(int(oct_num))

    @staticmethod
    def from_hex_string(hex_num: str) -> "IntLiteral":
        """
        根据十六进制字符串构造整数

        Parameters
        ----------
        hex_num : str
            十六进制数字字符串

        Returns
        -------
        IntLiteral
            整数字面值对象
        """
        return IntLiteral(int(hex_num, base=16))

    @property
    def value(self) -> int:
        """
        获取整数值

        Returns
        -------
        int
            整数值
        """
        return self._value

    def neg(self) -> "IntLiteral":
        """
        将当前整数值置为相反数

        Returns
        -------
        IntLiteral
            当前整数字面值对象
        """
        self._value *= -1
        return self

    def get_decimal_value(self) -> Decimal:
        """
        获取 Decimal 类型的数值

        Returns
        -------
        Decimal
            Decimal 类型的数值
        """
        return Decimal(self._value)


class DecimalLiteral(NumberLiteral):
    """小数字面值"""

    __slots__ = ["_value"]

    def __init__(self, value: Decimal):
        """
        初始化小数字面值

        Parameters
        ----------
        value : Decimal
            小数值
        """
        self._value: Decimal = value

    @staticmethod
    def create(source_string: str):
        """
        根据字符串创建小数字面值

        Parameters
        ----------
        source_string : str
            数字字符串

        Returns
        -------
        DecimalLiteral
            小数字面值对象
        """
        return DecimalLiteral(Decimal(source_string))

    @property
    def value(self) -> Decimal:
        """
        获取小数值

        Returns
        -------
        Decimal
            小数值
        """
        return self._value

    def neg(self) -> "DecimalLiteral":
        """
        将当前小数值置为相反数

        Returns
        -------
        DecimalLiteral
            当前小数字面值对象
        """
        self._value *= -1
        return self

    def get_decimal_value(self) -> Decimal:
        """
        获取 Decimal 类型的数值

        Returns
        -------
        Decimal
            Decimal 类型的数值
        """
        return self._value


class FloatLiteral(NumberLiteral):
    """浮点数字面值"""

    __slots__ = ["_value"]

    def __init__(self, value: str):
        """
        初始化浮点数字面值

        Parameters
        ----------
        value : str
            浮点数字符串
        """
        self._value: float = float(value)

    @property
    def value(self) -> float:
        """
        获取浮点数值

        Returns
        -------
        float
            浮点数值
        """
        return self._value

    def neg(self) -> "FloatLiteral":
        """
        将当前浮点数值置为相反数

        Returns
        -------
        FloatLiteral
            当前浮点数字面值对象
        """
        self._value *= -1
        return self

    def get_decimal_value(self) -> Decimal:
        """
        获取 Decimal 类型的数值

        Returns
        -------
        Decimal
            Decimal 类型的数值
        """
        return Decimal.from_float(self._value)


class TemporalLiteral(Literal):
    """时间类型字面值"""

    class EnumTemporalType(IntEnum):
        """时间类型字面值的枚举值"""
        DATE = 1
        TIME = 2
        DATETIME = 3

    __slots__ = ["_temporal_type", "_value"]

    def __init__(self, temporal_type: "TemporalLiteral.EnumTemporalType", value: str):
        """
        初始化时间类型字面值

        Parameters
        ----------
        temporal_type : TemporalLiteral.EnumTemporalType
            时间类型枚举值
        value : str
            时间值字符串
        """
        self._temporal_type: TemporalLiteral.EnumTemporalType = temporal_type
        self._value = value

    @staticmethod
    def create_date_literal(value: str) -> "TemporalLiteral":
        """
        创建日期字面值

        Parameters
        ----------
        value : str
            日期值字符串

        Returns
        -------
        TemporalLiteral
            时间类型字面值对象
        """
        return TemporalLiteral(
            temporal_type=TemporalLiteral.EnumTemporalType.DATE,
            value=value
        )

    @staticmethod
    def create_time_literal(value: str) -> "TemporalLiteral":
        """
        创建时间字面值

        Parameters
        ----------
        value : str
            时间值字符串

        Returns
        -------
        TemporalLiteral
            时间类型字面值对象
        """
        return TemporalLiteral(
            temporal_type=TemporalLiteral.EnumTemporalType.TIME,
            value=value
        )

    @staticmethod
    def create_datetime_literal(value: str) -> "TemporalLiteral":
        """
        创建日期时间字面值

        Parameters
        ----------
        value : str
            日期时间值字符串

        Returns
        -------
        TemporalLiteral
            时间类型字面值对象
        """
        return TemporalLiteral(
            temporal_type=TemporalLiteral.EnumTemporalType.DATETIME,
            value=value
        )

    @property
    def temporal_type(self) -> "TemporalLiteral.EnumTemporalType":
        """
        获取时间类型

        Returns
        -------
        TemporalLiteral.EnumTemporalType
            时间类型枚举值
        """
        return self._temporal_type

    @property
    def value(self) -> str:
        """
        获取时间值

        Returns
        -------
        str
            时间值字符串
        """
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

    __slots__ = ["_value"]

    def __init__(self, value: str):
        """
        初始化主机名

        Parameters
        ----------
        value : str
            主机名值
        """
        self._value = value

    @property
    def value(self) -> str:
        """
        获取主机名值

        Returns
        -------
        str
            主机名值
        """
        return self._value

    def get_str_value(self) -> Optional[str]:
        """
        获取主机名字符串值

        Returns
        -------
        Optional[str]
            主机名字符串值
        """
        return self._value


class RoleName(Node):
    """角色名称"""

    __slots__ = (
        "_role_name",
        "_role_host"
    )

    def __init__(self, role_name: str, role_host: Optional[str]):
        """
        初始化角色名称

        Parameters
        ----------
        role_name : str
            角色名称
        role_host : Optional[str]
            角色主机，可选
        """
        self._role_name = role_name
        self._role_host = role_host

    @property
    def role_name(self) -> str:
        """
        获取角色名称

        Returns
        -------
        str
            角色名称
        """
        return self._role_name

    @property
    def role_host(self) -> Optional[str]:
        """
        获取角色主机

        Returns
        -------
        Optional[str]
            角色主机，如果没有则返回 None
        """
        return self._role_host


class UserName(Node):
    """用户名称"""

    __slots__ = (
        "_is_current",
        "_user_name",
        "_user_host"
    )

    def __init__(self, is_current: bool, user_name: Optional[str], user_host: Optional[str]):
        """
        初始化用户名称

        Parameters
        ----------
        is_current : bool
            是否为当前用户
        user_name : Optional[str]
            用户名，可选
        user_host : Optional[str]
            用户主机，可选
        """
        self._is_current = is_current
        self._user_name = user_name
        self._user_host = user_host

    @staticmethod
    def create_by_user_name(user_name: str, user_host: Optional[str]) -> "UserName":
        """
        根据用户名创建用户名称对象

        Parameters
        ----------
        user_name : str
            用户名
        user_host : Optional[str]
            用户主机，可选

        Returns
        -------
        UserName
            用户名称对象
        """
        return UserName(is_current=False, user_name=user_name, user_host=user_host)

    @staticmethod
    def create_by_current_user() -> "UserName":
        """
        创建当前用户的用户名称对象

        Returns
        -------
        UserName
            当前用户的用户名称对象
        """
        return UserName(is_current=True, user_name=None, user_host=None)

    @property
    def is_current(self) -> bool:
        """
        获取是否为当前用户

        Returns
        -------
        bool
            是否为当前用户
        """
        return self._is_current

    @property
    def user_name(self) -> str:
        """
        获取用户名

        Returns
        -------
        str
            用户名
        """
        return self._user_name

    @property
    def user_host(self) -> Optional[str]:
        """
        获取用户主机

        Returns
        -------
        Optional[str]
            用户主机，如果没有则返回 None
        """
        return self._user_host
