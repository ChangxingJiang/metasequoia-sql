"""
JSON 表选项的抽象语法树节点
"""

import enum
import typing

from metasequoia_sql.ast.base import Expression
from metasequoia_sql.ast.base import Node

__all__ = [
    "JsonOnResponseTypeEnum",
    "JsonOnResponse",
    "JsonOnEmptyOnError"
]


class JsonOnResponseTypeEnum(enum.IntEnum):
    """Json 解析失败时的返回值类型的枚举类"""

    IMPLICIT = enum.auto()  # 默认值（未指定）
    ERROR = enum.auto()  # ERROR
    NULL = enum.auto()  # NULL
    DEFAULT = enum.auto()  # DEFAULT


class JsonOnResponse(Node):
    """Json 解析失败时的返回值"""

    def __init__(self,
                 response_type: JsonOnResponseTypeEnum,
                 default_value: typing.Optional[Expression] = None):
        self._response_type = response_type
        self._default_value = default_value  # 默认值（仅当 response_type == DEFAULT 时需要）

    @staticmethod
    def implicit() -> "JsonOnResponse":
        """构造未指定的默认值对象"""
        return JsonOnResponse(response_type=JsonOnResponseTypeEnum.DEFAULT)

    @property
    def response_type(self) -> JsonOnResponseTypeEnum:
        return self._response_type

    @property
    def default_value(self) -> typing.Optional[Expression]:
        return self._default_value


class JsonOnEmptyOnError(Node):
    """Json 解析遇到空值或错误时的处理方法"""

    def __init__(self, on_empty: JsonOnResponse, on_error: JsonOnResponse):
        self._on_empty = on_empty
        self._on_error = on_error

    @property
    def on_empty(self) -> JsonOnResponse:
        return self._on_empty

    @property
    def on_error(self) -> JsonOnResponse:
        return self._on_error
