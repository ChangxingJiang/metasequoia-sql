"""
CREATE USER 语句
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.literal import RoleName, UserName
    from metasequoia_sql.ast.phrase.identification import Identification
    from metasequoia_sql.ast.phrase.require_clause import RequireClause
    from metasequoia_sql.ast.phrase.connect_option import ConnectOption
    from metasequoia_sql.ast.phrase.account_lock_expire_option import AccountLockExpireOption
    from metasequoia_sql.ast.phrase.user_attribute import UserAttribute

__all__ = [
    "InitialAuth",
    "InitialAuthPassword",
    "InitialAuthPlugin",
    "InitialAuthRandom",
    "CreateUser",
    "CreateUserStatement",
    "DefaultRoleClause",
]


class InitialAuth:
    """初始认证的抽象基类"""

    __slots__ = ["_identification"]

    def __init__(self, identification: "Identification"):
        self._identification = identification

    @property
    def identification(self) -> "Identification":
        return self._identification


class InitialAuthPassword(InitialAuth):
    """基于密码的初始认证"""


class InitialAuthPlugin(InitialAuth):
    """基于插件的初始认证"""


class InitialAuthRandom(InitialAuth):
    """基于随机密码的初始认证"""


class CreateUser:
    """创建用户项"""

    __slots__ = ["_user", "_first_identification", "_mfa_identifications", "_initial_auth"]

    def __init__(
            self,
            user: "UserName",
            first_identification: Optional["Identification"] = None,
            mfa_identifications: List["Identification"] = None,
            initial_auth: Optional["InitialAuth"] = None
    ):
        self._user = user
        self._first_identification = first_identification
        self._mfa_identifications = mfa_identifications
        self._initial_auth = initial_auth

    @property
    def user(self) -> "UserName":
        return self._user

    @property
    def first_identification(self) -> Optional["Identification"]:
        return self._first_identification

    @property
    def mfa_identifications(self) -> List["Identification"]:
        return self._mfa_identifications

    @property
    def initial_auth(self) -> Optional["InitialAuth"]:
        return self._initial_auth


class DefaultRoleClause:
    """默认角色子句"""

    __slots__ = ["_role_list"]

    def __init__(self, role_list: List["RoleName"]):
        self._role_list = role_list

    @property
    def role_list(self) -> List["RoleName"]:
        return self._role_list


class CreateUserStatement(Statement):
    """CREATE USER 语句"""

    __slots__ = [
        "_if_not_exists",
        "_user_list",
        "_default_role_clause",
        "_require_clause",
        "_connect_options",
        "_account_lock_expire_options",
        "_user_attribute"
    ]

    def __init__(
            self,
            if_not_exists: bool,
            user_list: List[CreateUser],
            default_role_clause: Optional[DefaultRoleClause],
            require_clause: Optional["RequireClause"],
            connect_options: List["ConnectOption"],
            account_lock_expire_options: List["AccountLockExpireOption"],
            user_attribute: Optional["UserAttribute"]
    ):
        self._if_not_exists = if_not_exists
        self._user_list = user_list
        self._default_role_clause = default_role_clause
        self._require_clause = require_clause
        self._connect_options = connect_options
        self._account_lock_expire_options = account_lock_expire_options
        self._user_attribute = user_attribute

    @property
    def if_not_exists(self) -> bool:
        return self._if_not_exists

    @property
    def user_list(self) -> List[CreateUser]:
        return self._user_list

    @property
    def default_role_clause(self) -> Optional[DefaultRoleClause]:
        return self._default_role_clause

    @property
    def require_clause(self) -> Optional["RequireClause"]:
        return self._require_clause

    @property
    def connect_options(self) -> List["ConnectOption"]:
        return self._connect_options

    @property
    def account_lock_expire_options(self) -> List["AccountLockExpireOption"]:
        return self._account_lock_expire_options

    @property
    def user_attribute(self) -> Optional["UserAttribute"]:
        return self._user_attribute
