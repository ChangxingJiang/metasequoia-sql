"""
ROLLBACK 语句（rollback statement）
"""

from typing import TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.fixed_enum import EnumChainType, EnumReleaseType

__all__ = [
    "RollbackStatement",
    "RollbackTransactionStatement",
    "RollbackToSavepointStatement"
]


class RollbackStatement(Statement):
    """
    ROLLBACK 语句的抽象语法树节点基类。
    """


class RollbackTransactionStatement(RollbackStatement):
    """
    ROLLBACK 事务语句的抽象语法树节点。

    语法规则：
        ROLLBACK [WORK] [AND [NO] CHAIN] [AND [NO] RELEASE]
    """

    __slots__ = (
        "_chain",
        "_release"
    )

    def __init__(self, chain: "EnumChainType", release: "EnumReleaseType") -> None:
        """
        初始化 ROLLBACK 事务语句节点。

        Parameters
        ----------
        chain : EnumChainType
            是否使用 CHAIN 选项，默认为 False
        release : EnumReleaseType
            是否使用 RELEASE 选项，默认为 False
        """
        self._chain = chain
        self._release = release

    @property
    def chain(self) -> "EnumChainType":
        """
        获取是否使用 CHAIN 选项。

        Returns
        -------
        bool
            是否使用 CHAIN 选项
        """
        return self._chain

    @property
    def release(self) -> "EnumReleaseType":
        """
        获取是否使用 RELEASE 选项。

        Returns
        -------
        bool
            是否使用 RELEASE 选项
        """
        return self._release


class RollbackToSavepointStatement(RollbackStatement):
    """
    ROLLBACK TO SAVEPOINT 语句的抽象语法树节点。

    语法规则：
        ROLLBACK [WORK] TO [SAVEPOINT] savepoint_name
    """

    __slots__ = (
        "_savepoint_name"
    )

    def __init__(self, savepoint_name: str) -> None:
        """
        初始化 ROLLBACK TO SAVEPOINT 语句节点。

        Parameters
        ----------
        savepoint_name : Identifier
            保存点的名称
        """
        self._savepoint_name = savepoint_name

    @property
    def savepoint_name(self) -> str:
        """
        获取保存点的名称。

        Returns
        -------
        Identifier
            保存点的名称
        """
        return self._savepoint_name
