"""
字符集相关节点
"""

import enum
import typing

from metasequoia_sql_new.ast.base import Node

__all__ = [
    "CharsetTypeEnum",
    "Charset",
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
