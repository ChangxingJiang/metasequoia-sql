"""
REQUIRE 子句（require clause）
"""

from typing import List

from metasequoia_sql.ast.base import Node

__all__ = [
    "RequireListElement",
    "RequireSubject",
    "RequireIssuer",
    "RequireCipher",
    "RequireClause",
    "RequireNone",
    "RequireSsl",
    "RequireX509",
    "RequireList",
]


class RequireListElement(Node):
    """REQUIRE 列表元素的抽象基类"""

    __slots__ = ["_value"]

    def __init__(self, value: str):
        """初始化 REQUIRE 列表元素
        
        Parameters
        ----------
        value : str
            元素值
        """
        self._value = value

    @property
    def value(self) -> str:
        """获取元素值
        
        Returns
        -------
        str
            元素值
        """
        return self._value


class RequireSubject(RequireListElement):
    """REQUIRE SUBJECT 元素"""


class RequireIssuer(RequireListElement):
    """REQUIRE ISSUER 元素"""


class RequireCipher(RequireListElement):
    """REQUIRE CIPHER 元素"""


class RequireClause(Node):
    """REQUIRE 子句的抽象基类"""


class RequireNone(RequireClause):
    """REQUIRE NONE 子句"""


class RequireSsl(RequireClause):
    """REQUIRE SSL 子句"""


class RequireX509(RequireClause):
    """REQUIRE X509 子句"""


class RequireList(RequireClause):
    """REQUIRE 列表子句"""

    __slots__ = ["_require_list"]

    def __init__(self, require_list: List[RequireListElement]):
        """初始化 REQUIRE 列表子句
        
        Parameters
        ----------
        require_list : List[RequireListElement]
            REQUIRE 列表元素列表
        """
        self._require_list = require_list

    @property
    def require_list(self) -> List[RequireListElement]:
        """获取 REQUIRE 列表元素列表
        
        Returns
        -------
        List[RequireListElement]
            REQUIRE 列表元素列表
        """
        return self._require_list
