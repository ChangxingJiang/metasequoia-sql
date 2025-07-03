"""
SET PASSWORD 语句（set password statement）
"""

from typing import Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.literal import UserName

__all__ = [
    "SetPasswordStatement",
    "SetPasswordCurrentUserStatement",
    "SetPasswordCurrentUserRandomStatement",
    "SetPasswordForUserStatement",
    "SetPasswordForUserRandomStatement",
]


class SetPasswordStatement(Statement):
    """SET PASSWORD 语句的基类
    
    Parameters
    ----------
    replace_password : str, optional
        替换的当前密码
    retain_current_password : bool
        是否保留当前密码
    """

    __slots__ = ["_replace_password", "_retain_current_password"]

    def __init__(self, replace_password: Optional[str], retain_current_password: bool):
        self._replace_password = replace_password
        self._retain_current_password = retain_current_password

    @property
    def replace_password(self) -> Optional[str]:
        """替换的当前密码"""
        return self._replace_password

    @property
    def retain_current_password(self) -> bool:
        """是否保留当前密码"""
        return self._retain_current_password


class SetPasswordCurrentUserStatement(SetPasswordStatement):
    """SET PASSWORD 语句：为当前用户设置密码
    
    对应MySQL规则：PASSWORD equal TEXT_STRING_password opt_replace_password opt_retain_current_password
    
    Parameters
    ----------
    password : str
        新密码
    replace_password : str, optional
        替换的当前密码
    retain_current_password : bool
        是否保留当前密码
    """

    __slots__ = ["_password"]

    def __init__(self, password: str, replace_password: Optional[str], retain_current_password: bool):
        super().__init__(replace_password, retain_current_password)
        self._password = password

    @property
    def password(self) -> str:
        """新密码"""
        return self._password


class SetPasswordCurrentUserRandomStatement(SetPasswordStatement):
    """SET PASSWORD 语句：为当前用户设置随机密码
    
    对应MySQL规则：PASSWORD TO_SYM RANDOM_SYM opt_replace_password opt_retain_current_password
    
    Parameters
    ----------
    replace_password : str, optional
        替换的当前密码
    retain_current_password : bool
        是否保留当前密码
    """

    __slots__ = []


class SetPasswordForUserStatement(SetPasswordStatement):
    """SET PASSWORD 语句：为指定用户设置密码
    
    对应MySQL规则：PASSWORD FOR_SYM user equal TEXT_STRING_password opt_replace_password opt_retain_current_password
    
    Parameters
    ----------
    user : UserName
        目标用户
    password : str
        新密码
    replace_password : str, optional
        替换的当前密码
    retain_current_password : bool
        是否保留当前密码
    """

    __slots__ = ["_user", "_password"]

    def __init__(self, user: "UserName", password: str, replace_password: Optional[str], retain_current_password: bool):
        super().__init__(replace_password, retain_current_password)
        self._user = user
        self._password = password

    @property
    def user(self) -> "UserName":
        """目标用户"""
        return self._user

    @property
    def password(self) -> str:
        """新密码"""
        return self._password


class SetPasswordForUserRandomStatement(SetPasswordStatement):
    """SET PASSWORD 语句：为指定用户设置随机密码
    
    对应MySQL规则：PASSWORD FOR_SYM user TO_SYM RANDOM_SYM opt_replace_password opt_retain_current_password
    
    Parameters
    ----------
    user : UserName
        目标用户
    replace_password : str, optional
        替换的当前密码
    retain_current_password : bool
        是否保留当前密码
    """

    __slots__ = ["_user"]

    def __init__(self, user: "UserName", replace_password: Optional[str], retain_current_password: bool):
        super().__init__(replace_password, retain_current_password)
        self._user = user

    @property
    def user(self) -> "UserName":
        """目标用户"""
        return self._user
