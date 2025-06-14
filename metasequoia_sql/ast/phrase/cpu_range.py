"""
CPU 范围（cpu range）
"""

from typing import Optional

from metasequoia_sql.ast.base import Node

__all__ = [
    "CpuRange",
]


class CpuRange(Node):
    """CPU 范围"""

    __slots__ = (
        "_start",
        "_end",
    )

    def __init__(self, start: int, end: Optional[int]):
        self._start = start
        self._end = end

    @property
    def start(self) -> int:
        return self._start

    @property
    def end(self) -> int:
        return self._end
