"""
SET ROLE 语句（set role statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.literal import RoleName, UserName

__all__ = [
    "SetRoleStatement",
    "SetRoleListStatement",
    "SetRoleNoneStatement",
    "SetRoleDefaultStatement",
    "SetRoleAllStatement",
    "SetDefaultRoleStatement",
    "SetDefaultRoleNoneStatement",
    "SetDefaultRoleAllStatement",
]


class SetRoleStatement(Statement):
    """SET ROLE 语句的抽象基类"""


class SetRoleListStatement(SetRoleStatement):
    """SET ROLE role_list 语句"""

    __slots__ = ["_role_list"]

    def __init__(self, role_list: List["RoleName"]):
        """
        构造 SET ROLE role_list 语句节点

        Parameters
        ----------
        role_list : List[RoleName]
            角色列表
        """
        self._role_list = role_list

    @property
    def role_list(self) -> List["RoleName"]:
        """
        角色列表

        Returns
        -------
        List[RoleName]
            角色列表
        """
        return self._role_list


class SetRoleNoneStatement(SetRoleStatement):
    """SET ROLE NONE 语句"""

    __slots__ = []

    def __init__(self):
        """
        构造 SET ROLE NONE 语句节点
        """


class SetRoleDefaultStatement(SetRoleStatement):
    """SET ROLE DEFAULT 语句"""

    __slots__ = []

    def __init__(self):
        """
        构造 SET ROLE DEFAULT 语句节点
        """


class SetRoleAllStatement(SetRoleStatement):
    """SET ROLE ALL [EXCEPT role_list] 语句"""

    __slots__ = ["_except_role_list"]

    def __init__(self, except_role_list: Optional[List["RoleName"]]):
        """
        构造 SET ROLE ALL [EXCEPT role_list] 语句节点

        Parameters
        ----------
        except_role_list : Optional[List[RoleName]]
            排除的角色列表
        """
        self._except_role_list = except_role_list

    @property
    def except_role_list(self) -> Optional[List["RoleName"]]:
        """
        排除的角色列表

        Returns
        -------
        Optional[List[RoleName]]
            排除的角色列表
        """
        return self._except_role_list


class SetDefaultRoleStatement(SetRoleStatement):
    """SET DEFAULT ROLE role_list TO role_list 语句"""

    __slots__ = ["_role_list", "_user_list"]

    def __init__(self, role_list: List["RoleName"], user_list: List["UserName"]):
        """
        构造 SET DEFAULT ROLE role_list TO role_list 语句节点

        Parameters
        ----------
        role_list : List[RoleName]
            角色列表
        user_list : List[UserName]
            用户列表
        """
        self._role_list = role_list
        self._user_list = user_list

    @property
    def role_list(self) -> List["RoleName"]:
        """
        角色列表

        Returns
        -------
        List[RoleName]
            角色列表
        """
        return self._role_list

    @property
    def user_list(self) -> List["UserName"]:
        """
        用户列表

        Returns
        -------
        List[UserName]
            用户列表
        """
        return self._user_list


class SetDefaultRoleNoneStatement(SetRoleStatement):
    """SET DEFAULT ROLE NONE TO role_list 语句"""

    __slots__ = ["_user_list"]

    def __init__(self, user_list: List["UserName"]):
        """
        构造 SET DEFAULT ROLE NONE TO role_list 语句节点

        Parameters
        ----------
        user_list : List[UserName]
            用户列表
        """
        self._user_list = user_list

    @property
    def user_list(self) -> List["UserName"]:
        """
        用户列表

        Returns
        -------
        List[UserName]
            用户列表
        """
        return self._user_list


class SetDefaultRoleAllStatement(SetRoleStatement):
    """SET DEFAULT ROLE ALL TO role_list 语句"""

    __slots__ = ["_user_list"]

    def __init__(self, user_list: List["UserName"]):
        """
        构造 SET DEFAULT ROLE ALL TO role_list 语句节点

        Parameters
        ----------
        user_list : List[UserName]
            用户列表
        """
        self._user_list = user_list

    @property
    def user_list(self) -> List["UserName"]:
        """
        用户列表

        Returns
        -------
        List[UserName]
            用户列表
        """
        return self._user_list
