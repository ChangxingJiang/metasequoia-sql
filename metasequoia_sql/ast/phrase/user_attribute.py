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
        """
        初始化用户属性文本。

        Parameters
        ----------
        text : str
            用户属性文本内容
        """
        self._text = text

    @property
    def text(self) -> str:
        """
        获取用户属性文本内容。

        Returns
        -------
        str
            用户属性文本内容
        """
        return self._text


class UserComment(UserAttribute):
    """用户注释"""

    __slots__ = ["_comment"]

    def __init__(self, comment: str):
        """
        初始化用户注释。

        Parameters
        ----------
        comment : str
            用户注释内容
        """
        self._comment = comment

    @property
    def comment(self) -> str:
        """
        获取用户注释内容。

        Returns
        -------
        str
            用户注释内容
        """
        return self._comment
