"""
DDL 修改表选项（ddl alter option）
"""

from typing import Optional

from metasequoia_sql.ast.base import Node

__all__ = [
    "AlterOption",
    "AlterStrOptionBase",
    "AlterLockOption",
    "AlterAlgorithmOption",
    "TempAlterOptionList"
]


class AlterOption(Node):
    """DDL 修改表选项"""


class AlterStrOptionBase(AlterOption):
    """字符串类型的 DDL 修改表选项"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        return self._value


class AlterLockOption(AlterStrOptionBase):
    """DDL 修改表选项：LOCK（指定创建索引时对表施加的锁类型）"""


class AlterAlgorithmOption(AlterStrOptionBase):
    """DDL 修改表选项：ALGORITHM（创建索引时使用的算法或机制）"""


class TempAlterOptionList(Node):
    """【临时】DDL 修改表选项"""

    __slots__ = (
        "_lock",
        "_algorithm"
    )

    def __init__(self,
                 lock: Optional[AlterLockOption],
                 algorithm: Optional[AlterAlgorithmOption]):
        self._lock = lock
        self._algorithm = algorithm

    @property
    def lock(self) -> Optional[AlterLockOption]:
        return self._lock

    @property
    def algorithm(self) -> Optional[AlterAlgorithmOption]:
        return self._algorithm
