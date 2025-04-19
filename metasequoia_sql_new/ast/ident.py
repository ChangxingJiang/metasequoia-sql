"""
标识符类型节点
"""
from typing import List

from metasequoia_sql_new.ast.base import Expression

__all__ = [
    "Ident"
]


class Ident(Expression):
    """标识符节点"""

    def __init__(self, value: str):
        self._value = value

    def attr_list(self) -> List[str]:
        return ["value"]

    @property
    def value(self) -> str:
        return self._value
