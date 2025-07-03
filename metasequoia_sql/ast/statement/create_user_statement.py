"""
CREATE USER 语句
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.literal import RoleName, UserName
    from metasequoia_sql.ast.phrase.identification import Identification
    from metasequoia_sql.ast.clause.require_clause import RequireClause
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
    # pylint: disable=R0903
    """初始认证的抽象基类"""

    __slots__ = ["_identification"]

    def __init__(self, identification: "Identification"):
        self._identification = identification

    @property
    def identification(self) -> "Identification":
        """
        身份认证信息

        Returns
        -------
        Identification
            身份认证信息
        """
        return self._identification


class InitialAuthPassword(InitialAuth):
    # pylint: disable=R0903
    """基于密码的初始认证"""


class InitialAuthPlugin(InitialAuth):
    # pylint: disable=R0903
    """基于插件的初始认证"""


class InitialAuthRandom(InitialAuth):
    # pylint: disable=R0903
    """基于随机密码的初始认证"""


class CreateUser:
    """创建用户项"""

    __slots__ = ["_user", "_first_identification", "_mfa_identifications", "_initial_auth"]

    def __init__(
            self,
            user: "UserName",
            first_identification: Optional["Identification"] = None,
            mfa_identifications: Optional[List["Identification"]] = None,
            initial_auth: Optional["InitialAuth"] = None
    ):
        self._user = user
        self._first_identification = first_identification
        self._mfa_identifications = mfa_identifications if mfa_identifications is not None else []
        self._initial_auth = initial_auth

    @property
    def user(self) -> "UserName":
        """
        用户名

        Returns
        -------
        UserName
            用户名
        """
        return self._user

    @property
    def first_identification(self) -> Optional["Identification"]:
        """
        首次身份认证信息

        Returns
        -------
        Optional["Identification"]
            首次身份认证信息
        """
        return self._first_identification

    @property
    def mfa_identifications(self) -> List["Identification"]:
        """
        多因素认证信息列表

        Returns
        -------
        List["Identification"]
            多因素认证信息列表
        """
        return self._mfa_identifications

    @property
    def initial_auth(self) -> Optional["InitialAuth"]:
        """
        初始认证信息

        Returns
        -------
        Optional["InitialAuth"]
            初始认证信息
        """
        return self._initial_auth


class DefaultRoleClause:
    # pylint: disable=R0903
    """默认角色子句"""

    __slots__ = ["_role_list"]

    def __init__(self, role_list: List["RoleName"]):
        self._role_list = role_list

    @property
    def role_list(self) -> List["RoleName"]:
        """
        角色列表

        Returns
        -------
        List["RoleName"]
            角色列表
        """
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
        # pylint: disable=R0913,R0917
        self._if_not_exists = if_not_exists
        self._user_list = user_list
        self._default_role_clause = default_role_clause
        self._require_clause = require_clause
        self._connect_options = connect_options
        self._account_lock_expire_options = account_lock_expire_options
        self._user_attribute = user_attribute

    @property
    def if_not_exists(self) -> bool:
        """
        是否使用 IF NOT EXISTS 选项

        Returns
        -------
        bool
            是否使用 IF NOT EXISTS 选项
        """
        return self._if_not_exists

    @property
    def user_list(self) -> List[CreateUser]:
        """
        创建用户列表

        Returns
        -------
        List[CreateUser]
            创建用户列表
        """
        return self._user_list

    @property
    def default_role_clause(self) -> Optional[DefaultRoleClause]:
        """
        默认角色子句

        Returns
        -------
        Optional[DefaultRoleClause]
            默认角色子句
        """
        return self._default_role_clause

    @property
    def require_clause(self) -> Optional["RequireClause"]:
        """
        要求子句

        Returns
        -------
        Optional["RequireClause"]
            要求子句
        """
        return self._require_clause

    @property
    def connect_options(self) -> List["ConnectOption"]:
        """
        连接选项列表

        Returns
        -------
        List["ConnectOption"]
            连接选项列表
        """
        return self._connect_options

    @property
    def account_lock_expire_options(self) -> List["AccountLockExpireOption"]:
        """
        账户锁定过期选项列表

        Returns
        -------
        List["AccountLockExpireOption"]
            账户锁定过期选项列表
        """
        return self._account_lock_expire_options

    @property
    def user_attribute(self) -> Optional["UserAttribute"]:
        """
        用户属性

        Returns
        -------
        Optional["UserAttribute"]
            用户属性
        """
        return self._user_attribute
