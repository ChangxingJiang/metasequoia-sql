"""
JSON 表选项的抽象语法树节点
"""

from enum import IntEnum, auto
from typing import Optional

from metasequoia_sql.ast.base import Expression
from metasequoia_sql.ast.base import Node

__all__ = [
    "JsonOnResponseTypeEnum",
    "JsonOnResponse",
    "JsonOnEmptyOnError"
]


class JsonOnResponseTypeEnum(IntEnum):
    """Json 解析失败时的返回值类型的枚举类"""

    IMPLICIT = auto()  # 默认值（未指定）
    ERROR = auto()  # ERROR
    NULL = auto()  # NULL
    DEFAULT = auto()  # DEFAULT


class JsonOnResponse(Node):
    """Json 解析失败时的返回值"""

    __slots__ = ["_response_type", "_default_value"]

    def __init__(self,
                 response_type: JsonOnResponseTypeEnum,
                 default_value: Optional[Expression] = None):
        self._response_type = response_type
        self._default_value = default_value  # 默认值（仅当 response_type == DEFAULT 时需要）

    @staticmethod
    def implicit() -> "JsonOnResponse":
        """构造未指定的默认值对象"""
        return JsonOnResponse(response_type=JsonOnResponseTypeEnum.DEFAULT)

    @property
    def response_type(self) -> JsonOnResponseTypeEnum:
        """获取响应类型。
        
        Returns
        -------
        JsonOnResponseTypeEnum
            响应类型
        """
        return self._response_type

    @property
    def default_value(self) -> Optional[Expression]:
        """获取默认值。
        
        Returns
        -------
        Optional[Expression]
            默认值表达式
        """
        return self._default_value


class JsonOnEmptyOnError(Node):
    """Json 解析遇到空值或错误时的处理方法"""

    __slots__ = ["_on_empty", "_on_error"]

    def __init__(self, on_empty: JsonOnResponse, on_error: JsonOnResponse):
        self._on_empty = on_empty
        self._on_error = on_error

    @property
    def on_empty(self) -> JsonOnResponse:
        """获取空值处理方法。
        
        Returns
        -------
        JsonOnResponse
            空值处理方法
        """
        return self._on_empty

    @property
    def on_error(self) -> JsonOnResponse:
        """获取错误处理方法。
        
        Returns
        -------
        JsonOnResponse
            错误处理方法
        """
        return self._on_error
