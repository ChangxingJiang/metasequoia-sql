"""
线程优先级短语（thread priority phrase）
"""

from typing import Optional

from metasequoia_sql.ast.base import Node

__all__ = [
    "ThreadPriority",
]


class ThreadPriority(Node):
    """
    线程优先级的抽象语法树节点。
    
    语法规则：
        THREAD_PRIORITY [=] signed_num
    """

    __slots__ = (
        "_value",
    )

    def __init__(self, value: int):
        """
        初始化线程优先级节点。

        Parameters
        ----------
        value : int
            优先级值
        """
        self._value = value

    @property
    def value(self) -> int:
        """
        获取优先级值。

        Returns
        -------
        int
            优先级值
        """
        return self._value 