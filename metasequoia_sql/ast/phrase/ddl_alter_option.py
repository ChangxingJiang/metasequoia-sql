"""
DDL 修改表选项（ddl alter option）
"""

from typing import Optional, List

from metasequoia_sql.ast.base import Node

__all__ = [
    "AlterOption",
    "AlterStrOptionBase",
    "AlterOptionLock",
    "AlterOptionAlgorithm",
    "AlterOptionWithValidation",
    "TempAlterOptionList",
]


class AlterOption(Node):
    """DDL 修改表选项"""


class AlterStrOptionBase(AlterOption):
    """字符串类型的 DDL 修改选项"""

    __slots__ = (
        "_value",
    )

    def __init__(self, value: str):
        """
        初始化字符串类型的 DDL 修改选项。

        Parameters
        ----------
        value : str
            选项值
        """
        self._value = value

    @property
    def value(self) -> str:
        """
        获取选项值。

        Returns
        -------
        str
            选项值
        """
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
        "_value",
    )

    def __init__(self, value: Optional[bool]):
        """
        初始化 WITH/WITHOUT VALIDATION 选项。

        Parameters
        ----------
        value : Optional[bool]
            验证选项值，True 表示 WITH VALIDATION，False 表示 WITHOUT VALIDATION，None 表示未指定
        """
        self._value = value

    @property
    def value(self) -> Optional[bool]:
        """
        获取验证选项值。

        Returns
        -------
        Optional[bool]
            验证选项值，True 表示 WITH VALIDATION，False 表示 WITHOUT VALIDATION，None 表示未指定
        """
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
        """
        初始化临时 DDL 修改表选项列表。

        Parameters
        ----------
        lock : Optional[AlterOptionLock], optional
            锁选项，默认为 None
        algorithm : Optional[AlterOptionAlgorithm], optional
            算法选项，默认为 None
        validation : Optional[AlterOptionWithValidation], optional
            验证选项，默认为 None
        """
        self._lock = lock
        self._algorithm = algorithm
        self._validation = validation

    @property
    def lock(self) -> Optional[AlterOptionLock]:
        """
        获取锁选项。

        Returns
        -------
        Optional[AlterOptionLock]
            锁选项
        """
        return self._lock

    @property
    def algorithm(self) -> Optional[AlterOptionAlgorithm]:
        """
        获取算法选项。

        Returns
        -------
        Optional[AlterOptionAlgorithm]
            算法选项
        """
        return self._algorithm

    @property
    def validation(self) -> Optional[AlterOptionWithValidation]:
        """
        获取验证选项。

        Returns
        -------
        Optional[AlterOptionWithValidation]
            验证选项
        """
        return self._validation

    def merge(self, other: "TempAlterOptionList") -> "TempAlterOptionList":
        """
        合并两个 TempAlterOptionList。

        Parameters
        ----------
        other : TempAlterOptionList
            另一个 TempAlterOptionList 对象

        Returns
        -------
        TempAlterOptionList
            合并后的 TempAlterOptionList 对象
        """
        return TempAlterOptionList(
            lock=other.lock or self.lock,
            algorithm=other.algorithm or self.algorithm,
            validation=other.validation or self.validation
        )

    def get_list(self) -> List[AlterOption]:
        """
        获取所有非空的 DDL 修改选项列表。

        Returns
        -------
        List[AlterOption]
            包含所有非空选项的列表
        """
        result = []
        if self._lock is not None:
            result.append(self._lock)
        if self._algorithm is not None:
            result.append(self._algorithm)
        if self._validation is not None:
            result.append(self._validation)
        return result
