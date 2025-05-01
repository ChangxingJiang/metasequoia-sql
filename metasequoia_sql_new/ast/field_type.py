"""
字段类型相关节点
"""

import decimal
import enum
import typing

from metasequoia_sql_new.ast.base import Node

__all__ = [
    "CharsetTypeEnum",
    "Charset",
    "FieldTypeParams",
]


class CharsetTypeEnum(enum.IntEnum):
    """字符集类型的枚举类型"""

    DEFAULT = enum.auto()
    ASCII = enum.auto()  # ASCII
    BINARY_ASCII = enum.auto()  # BINARY ASCII
    ASCII_BINARY = enum.auto()  # ASCII BINARY
    UNICODE = enum.auto()  # UNICODE
    BINARY_UNICODE = enum.auto()  # BINARY UNICODE
    UNICODE_BINARY = enum.auto()  # UNICODE BINARY
    BYTE = enum.auto()  # BYTE
    BINARY = enum.auto()  # BINARY
    CHARSET_NAME = enum.auto()  # [CHARSET | CHAR SET] 字符集名称
    CHARSET_NAME_BINARY = enum.auto()  # [CHARSET | CHAR SET] 字符集名称 BINARY
    BINARY_CHARSET_NAME = enum.auto()  # BINARY [CHARSET | CHAR SET] 字符集名称


class Charset(Node):
    """字符集类型"""

    def __init__(self, charset_type: CharsetTypeEnum, charset_name: typing.Optional[str]):
        self._charset_type = charset_type
        self._charset_name = charset_name

    def attr_list(self) -> typing.List[str]:
        return ["charset_type", "charset_name"]

    @property
    def charset_type(self) -> CharsetTypeEnum:
        return self._charset_type

    @property
    def charset_name(self) -> typing.Optional[str]:
        return self._charset_name


class FieldTypeParams(Node):
    """字段类型的参数"""

    def __init__(self,
                 option_1: typing.Optional[decimal.Decimal] = None,
                 option_2: typing.Optional[decimal.Decimal] = None):
        self._option_1 = option_1  # 第 1 个参数
        self._option_2 = option_2  # 第 2 个参数

    def attr_list(self) -> typing.List[str]:
        return ["option_1", "option_2"]

    @property
    def length(self) -> typing.Optional[decimal.Decimal]:
        return self._option_1

    @property
    def decimal(self) -> typing.Optional[decimal.Decimal]:
        return self._option_2
