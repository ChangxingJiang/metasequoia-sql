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
        """
        初始化 CPU 范围。

        Parameters
        ----------
        start : int
            起始 CPU 编号
        end : Optional[int]
            结束 CPU 编号，如果为 None 则表示单个 CPU
        """
        self._start = start
        self._end = end

    @property
    def start(self) -> int:
        """
        获取起始 CPU 编号。

        Returns
        -------
        int
            起始 CPU 编号
        """
        return self._start

    @property
    def end(self) -> int:
        """
        获取结束 CPU 编号。

        Returns
        -------
        int
            结束 CPU 编号
        """
        return self._end
