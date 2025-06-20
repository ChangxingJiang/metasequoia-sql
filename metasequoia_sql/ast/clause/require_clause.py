"""
REQUIRE 子句（require clause）
"""

from typing import List, Optional

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
        self._value = value

    @property
    def value(self) -> str:
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

    __slots__ = []

    def __init__(self):
        pass


class RequireSsl(RequireClause):
    """REQUIRE SSL 子句"""

    __slots__ = []

    def __init__(self):
        pass


class RequireX509(RequireClause):
    """REQUIRE X509 子句"""

    __slots__ = []

    def __init__(self):
        pass


class RequireList(RequireClause):
    """REQUIRE 列表子句"""

    __slots__ = ["_require_list"]

    def __init__(self, require_list: List[RequireListElement]):
        self._require_list = require_list

    @property
    def require_list(self) -> List[RequireListElement]:
        return self._require_list 