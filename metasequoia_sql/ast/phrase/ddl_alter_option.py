"""
DDL 修改表选项（ddl alter option）
"""

from typing import Optional

from metasequoia_sql.ast.base import Node

__all__ = [
    "AlterOption",
    "AlterStrOptionBase",
    "AlterOptionLock",
    "AlterOptionAlgorithm",
    "AlterOptionWithValidation",
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


class AlterOptionLock(AlterStrOptionBase):
    """DDL 修改表选项：LOCK（指定创建索引时对表施加的锁类型）"""


class AlterOptionAlgorithm(AlterStrOptionBase):
    """DDL 修改表选项：ALGORITHM（创建索引时使用的算法或机制）"""


class AlterOptionWithValidation(AlterOption):
    """DDL 修改表选项：WITH VALIDATION 或 WITHOUT VALIDATION

    - 当匹配 WITH VALIDATION 时，value 为 True；
    - 当匹配 WITHOUT VALIDATION 时，value 为 False；
    - 当没有匹配时，value 为 None
    """

    __slots__ = (
        "_value"
    )

    def __init__(self, value: Optional[bool]):
        self._value = value

    @property
    def value(self) -> Optional[bool]:
        return self._value


class TempAlterOptionList(Node):
    """【临时】DDL 修改表选项"""

    __slots__ = (
        "_lock",
        "_algorithm",
        "_validation"
    )

    def __init__(self,
                 lock: Optional[AlterOptionLock] = None,
                 algorithm: Optional[AlterOptionAlgorithm] = None,
                 validation: Optional[AlterOptionWithValidation] = None):
        self._lock = lock
        self._algorithm = algorithm
        self._validation = validation

    @property
    def lock(self) -> Optional[AlterOptionLock]:
        return self._lock

    @property
    def algorithm(self) -> Optional[AlterOptionAlgorithm]:
        return self._algorithm

    @property
    def validation(self) -> Optional[AlterOptionWithValidation]:
        return self._validation

    def merge(self, other: "TempAlterOptionList") -> "TempAlterOptionList":
        """合并两个 TempAlterOptionList"""
        return TempAlterOptionList(
            lock=other.lock or self.lock,
            algorithm=other.algorithm or self.algorithm,
            validation=other.validation or self.validation
        )
