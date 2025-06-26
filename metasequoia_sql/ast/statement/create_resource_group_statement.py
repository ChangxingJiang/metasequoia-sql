"""
CREATE RESOURCE GROUP 语句（create resource group statement）
"""

from typing import Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.fixed_enum import EnumResourceGroupType, EnumEnableDisable
    from metasequoia_sql.ast.phrase.thread_priority import ThreadPriority
    from metasequoia_sql.ast.phrase.cpu_range import CpuRange

__all__ = [
    "CreateResourceGroupStatement",
]


class CreateResourceGroupStatement(Statement):
    """
    CREATE RESOURCE GROUP 语句的抽象语法树节点。
    
    语法规则：
        CREATE RESOURCE GROUP ident TYPE [=] resource_group_type 
        [opt_resource_group_vcpu_list] [opt_resource_group_priority] 
        [opt_resource_group_enable_disable]
    """

    __slots__ = (
        "_group_name",
        "_resource_group_type",
        "_vcpu_list",
        "_priority",
        "_enable_disable",
    )

    def __init__(self,
                 group_name: str,
                 resource_group_type: "EnumResourceGroupType",
                 vcpu_list: Optional["CpuRange"] = None,
                 priority: Optional["ThreadPriority"] = None,
                 enable_disable: "EnumEnableDisable" = None):
        # pylint: disable=R0913
        """
        初始化CREATE RESOURCE GROUP语句节点。

        Parameters
        ----------
        group_name : Identifier
            资源组名称
        resource_group_type : EnumResourceGroupType
            资源组类型
        vcpu_list : Optional[CpuRange]
            VCPU列表
        priority : Optional[ThreadPriority]
            线程优先级
        enable_disable : EnumEnableDisable
            启用/禁用状态
        """
        self._group_name = group_name
        self._resource_group_type = resource_group_type
        self._vcpu_list = vcpu_list
        self._priority = priority
        self._enable_disable = enable_disable

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
    def resource_group_type(self) -> "EnumResourceGroupType":
        """
        获取资源组类型。

        Returns
        -------
        EnumResourceGroupType
            资源组类型
        """
        return self._resource_group_type

    @property
    def vcpu_list(self) -> Optional["CpuRange"]:
        """
        获取VCPU列表。

        Returns
        -------
        Optional[CpuRange]
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
