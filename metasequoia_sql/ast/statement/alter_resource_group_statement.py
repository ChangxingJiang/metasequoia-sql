"""
ALTER RESOURCE GROUP 语句（alter resource group statement）
"""

from typing import Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.fixed_enum import EnumEnableDisable
    from metasequoia_sql.ast.phrase.thread_priority import ThreadPriority
    from metasequoia_sql.ast.phrase.cpu_range import CpuRange

__all__ = [
    "AlterResourceGroupStatement",
]


class AlterResourceGroupStatement(Statement):
    """
    ALTER RESOURCE GROUP 语句的抽象语法树节点。
    
    语法规则：
        ALTER RESOURCE GROUP ident [opt_resource_group_vcpu_list] 
        [opt_resource_group_priority] [opt_resource_group_enable_disable] [opt_force]
    """

    __slots__ = (
        "_group_name",
        "_vcpu_list",
        "_priority",
        "_enable_disable",
        "_force",
    )

    def __init__(self,
                 group_name: str,
                 vcpu_list: Optional["CpuRange"] = None,
                 priority: Optional["ThreadPriority"] = None,
                 enable_disable: "EnumEnableDisable" = None,
                 force: bool = False):
        # pylint: disable=R0913,R0917
        """
        初始化ALTER RESOURCE GROUP语句节点。

        Parameters
        ----------
        group_name : str
            资源组名称
        vcpu_list : Optional[CpuRange]
            VCPU列表
        priority : Optional[ThreadPriority]
            线程优先级
        enable_disable : EnumEnableDisable
            启用/禁用状态
        force : bool
            是否强制执行
        """
        self._group_name = group_name
        self._vcpu_list = vcpu_list
        self._priority = priority
        self._enable_disable = enable_disable
        self._force = force

    @property
    def group_name(self) -> str:
        """
        获取资源组名称。

        Returns
        -------
        Identifier
            资源组名称
        """
        return self._group_name

    @property
    def vcpu_list(self) -> Optional["CpuRange"]:
        """
        获取VCPU列表。

        Returns
        -------
        Optional[str]
            VCPU列表
        """
        return self._vcpu_list

    @property
    def priority(self) -> Optional["ThreadPriority"]:
        """
        获取线程优先级。

        Returns
        -------
        Optional[ThreadPriority]
            线程优先级
        """
        return self._priority

    @property
    def enable_disable(self) -> "EnumEnableDisable":
        """
        获取启用/禁用状态。

        Returns
        -------
        EnumEnableDisable
            启用/禁用状态
        """
        return self._enable_disable

    @property
    def force(self) -> bool:
        """
        获取是否强制执行。

        Returns
        -------
        bool
            是否强制执行
        """
        return self._force
