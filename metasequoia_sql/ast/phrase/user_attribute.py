"""
用户属性（user attribute）
"""

from typing import TYPE_CHECKING

from metasequoia_sql.ast.base import Node

if TYPE_CHECKING:
    pass

__all__ = [
    "UserAttribute",
    "UserAttributeText",
    "UserComment",
]


class UserAttribute(Node):
    """用户属性的抽象基类"""


class UserAttributeText(UserAttribute):
    """用户属性文本"""

    __slots__ = ["_text"]

    def __init__(self, text: str):
        self._text = text

    @property
    def text(self) -> str:
        return self._text


class UserComment(UserAttribute):
    """用户注释"""

    __slots__ = ["_comment"]

    def __init__(self, comment: str):
        self._comment = comment

    @property
    def comment(self) -> str:
        return self._comment
