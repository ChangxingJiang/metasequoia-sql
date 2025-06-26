"""
字符集相关节点
"""

from enum import IntEnum, auto
from typing import Optional

from metasequoia_sql.ast.base import Node

__all__ = [
    "CharsetTypeEnum",
    "Charset",
]


class CharsetTypeEnum(IntEnum):
    """字符集类型的枚举类型"""

    DEFAULT = auto()
    ASCII = auto()  # ASCII
    BINARY_ASCII = auto()  # BINARY ASCII
    ASCII_BINARY = auto()  # ASCII BINARY
    UNICODE = auto()  # UNICODE
    BINARY_UNICODE = auto()  # BINARY UNICODE
    UNICODE_BINARY = auto()  # UNICODE BINARY
    BYTE = auto()  # BYTE
    BINARY = auto()  # BINARY
    CHARSET_NAME = auto()  # [CHARSET | CHAR SET] 字符集名称
    CHARSET_NAME_BINARY = auto()  # [CHARSET | CHAR SET] 字符集名称 BINARY
    BINARY_CHARSET_NAME = auto()  # BINARY [CHARSET | CHAR SET] 字符集名称


class Charset(Node):
    """字符集类型"""

    __slots__ = ["_charset_type", "_charset_name"]

    def __init__(self, charset_type: CharsetTypeEnum, charset_name: Optional[str]):
        self._charset_type = charset_type
        self._charset_name = charset_name

    @property
    def charset_type(self) -> CharsetTypeEnum:
        return self._charset_type

    @property
    def charset_name(self) -> Optional[str]:
        return self._charset_name

    def add_back_binary(self) -> "Charset":
        """
        在当前字符集对象的基础上，添加后置的 `BINARY` 关键字，并返回新的字符集对象
        
        该方法会修改字符集类型，如果当前类型为CHARSET_NAME，则转换为CHARSET_NAME_BINARY。
        
        Returns
        -------
        Charset
            修改后的字符集对象（返回self以支持链式调用）
        """
        if self._charset_type == CharsetTypeEnum.CHARSET_NAME:
            self._charset_type = CharsetTypeEnum.CHARSET_NAME_BINARY
        return self

    def add_front_binary(self) -> "Charset":
        """
        在当前字符集对象的基础上，添加前置的 `BINARY` 关键字，并返回新的字符集对象
        
        该方法会修改字符集类型，如果当前类型为CHARSET_NAME，则转换为BINARY_CHARSET_NAME。
        
        Returns
        -------
        Charset
            修改后的字符集对象（返回self以支持链式调用）
        """
        if self._charset_type == CharsetTypeEnum.CHARSET_NAME:
            self._charset_type = CharsetTypeEnum.BINARY_CHARSET_NAME
        return self
