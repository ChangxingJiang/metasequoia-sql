"""
ALTER USER 语句相关的 AST 节点类
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.phrase.alter_user import AlterUser
    from metasequoia_sql.ast.phrase.user_registration import UserRegistration
    from metasequoia_sql.ast.phrase.identification import Identification
    from metasequoia_sql.ast.phrase.connect_option import ConnectOption
    from metasequoia_sql.ast.phrase.account_lock_expire_option import AccountLockExpireOption
    from metasequoia_sql.ast.phrase.user_attribute import UserAttribute
    from metasequoia_sql.ast.clause.require_clause import RequireClause
    from metasequoia_sql.ast.basic.ident import UserName, RoleName

__all__ = [
    "AlterUserStatement",
    "AlterUserStandardStatement",
    "AlterUserCurrentUserRandomPasswordStatement",
    "AlterUserCurrentUserPasswordStatement",
    "AlterUserCurrentUserDiscardPasswordStatement",
    "AlterUserDefaultRoleAllStatement",
    "AlterUserDefaultRoleNoneStatement",
    "AlterUserDefaultRoleListStatement",
    "AlterUserRegistrationStatement",
    "AlterUserCurrentUserRegistrationStatement",
]


class AlterUserStatement(Statement):
    """
    ALTER USER 语句的基类
    
    Parameters
    ----------
    if_exists : bool
        是否包含 IF EXISTS 选项
    """
    __slots__ = ("_if_exists",)

    def __init__(self, if_exists: bool):
        self._if_exists = if_exists

    @property
    def if_exists(self) -> bool:
        """是否包含 IF EXISTS 选项"""
        return self._if_exists


class AlterUserStandardStatement(AlterUserStatement):
    """
    标准的 ALTER USER 语句：
    alter_user_command alter_user_list require_clause connect_options opt_account_lock_password_expire_options
    opt_user_attribute
    
    Parameters
    ----------
    if_exists : bool
        是否包含 IF EXISTS 选项
    user_list : List[AlterUser]
        用户修改列表
    require_clause : RequireClause
        REQUIRE 子句
    connect_options : List[ConnectOption]
        连接选项列表
    account_lock_expire_options : List[AccountLockExpireOption]
        账户锁定和密码过期选项列表
    user_attribute : UserAttribute, optional
        用户属性
    """
    __slots__ = (
        "_user_list", "_require_clause", "_connect_options",
        "_account_lock_expire_options", "_user_attribute"
    )

    def __init__(
            self,
            if_exists: bool,
            user_list: List["AlterUser"],
            require_clause: "RequireClause",
            connect_options: List["ConnectOption"],
            account_lock_expire_options: List["AccountLockExpireOption"],
            user_attribute: Optional["UserAttribute"]
    ):
        # pylint: disable=R0913
        super().__init__(if_exists)
        self._user_list = user_list
        self._require_clause = require_clause
        self._connect_options = connect_options
        self._account_lock_expire_options = account_lock_expire_options
        self._user_attribute = user_attribute

    @property
    def user_list(self) -> List["AlterUser"]:
        """用户修改列表"""
        return self._user_list

    @property
    def require_clause(self) -> "RequireClause":
        """REQUIRE 子句"""
        return self._require_clause

    @property
    def connect_options(self) -> List["ConnectOption"]:
        """连接选项列表"""
        return self._connect_options

    @property
    def account_lock_expire_options(self) -> List["AccountLockExpireOption"]:
        """账户锁定和密码过期选项列表"""
        return self._account_lock_expire_options

    @property
    def user_attribute(self) -> Optional["UserAttribute"]:
        """用户属性"""
        return self._user_attribute


class AlterUserCurrentUserRandomPasswordStatement(AlterUserStatement):
    """
    当前用户随机密码认证：
    alter_user_command user_func identified_by_random_password opt_replace_password opt_retain_current_password
    
    Parameters
    ----------
    if_exists : bool
        是否包含 IF EXISTS 选项
    identification : Identification
        认证信息
    replace_password : str, optional
        替换的当前密码
    retain_current_password : bool
        是否保留当前密码
    """
    __slots__ = ("_identification", "_replace_password", "_retain_current_password")

    def __init__(
            self,
            if_exists: bool,
            identification: "Identification",
            replace_password: Optional[str],
            retain_current_password: bool
    ):
        super().__init__(if_exists)
        self._identification = identification
        self._replace_password = replace_password
        self._retain_current_password = retain_current_password

    @property
    def identification(self) -> "Identification":
        """认证信息"""
        return self._identification

    @property
    def replace_password(self) -> Optional[str]:
        """替换的当前密码"""
        return self._replace_password

    @property
    def retain_current_password(self) -> bool:
        """是否保留当前密码"""
        return self._retain_current_password


class AlterUserCurrentUserPasswordStatement(AlterUserStatement):
    """
    当前用户密码认证：
    alter_user_command user_func identified_by_password opt_replace_password opt_retain_current_password
    
    Parameters
    ----------
    if_exists : bool
        是否包含 IF EXISTS 选项
    identification : Identification
        认证信息
    replace_password : str, optional
        替换的当前密码
    retain_current_password : bool
        是否保留当前密码
    """
    __slots__ = ("_identification", "_replace_password", "_retain_current_password")

    def __init__(
            self,
            if_exists: bool,
            identification: "Identification",
            replace_password: Optional[str],
            retain_current_password: bool
    ):
        super().__init__(if_exists)
        self._identification = identification
        self._replace_password = replace_password
        self._retain_current_password = retain_current_password

    @property
    def identification(self) -> "Identification":
        """认证信息"""
        return self._identification

    @property
    def replace_password(self) -> Optional[str]:
        """替换的当前密码"""
        return self._replace_password

    @property
    def retain_current_password(self) -> bool:
        """是否保留当前密码"""
        return self._retain_current_password


class AlterUserCurrentUserDiscardPasswordStatement(AlterUserStatement):
    """
    当前用户丢弃旧密码：
    alter_user_command user_func DISCARD OLD PASSWORD
    
    Parameters
    ----------
    if_exists : bool
        是否包含 IF EXISTS 选项
    """


class AlterUserDefaultRoleAllStatement(AlterUserStatement):
    """
    设置用户默认角色为全部：
    alter_user_command user DEFAULT ROLE ALL
    
    Parameters
    ----------
    if_exists : bool
        是否包含 IF EXISTS 选项
    user : UserName
        用户名
    """
    __slots__ = ("_user",)

    def __init__(self, if_exists: bool, user: "UserName"):
        super().__init__(if_exists)
        self._user = user

    @property
    def user(self) -> "UserName":
        """用户名"""
        return self._user


class AlterUserDefaultRoleNoneStatement(AlterUserStatement):
    """
    设置用户默认角色为无：
    alter_user_command user DEFAULT ROLE NONE
    
    Parameters
    ----------
    if_exists : bool
        是否包含 IF EXISTS 选项
    user : UserName
        用户名
    """
    __slots__ = ("_user",)

    def __init__(self, if_exists: bool, user: "UserName"):
        super().__init__(if_exists)
        self._user = user

    @property
    def user(self) -> "UserName":
        """用户名"""
        return self._user


class AlterUserDefaultRoleListStatement(AlterUserStatement):
    """
    设置用户默认角色列表：
    alter_user_command user DEFAULT ROLE role_list
    
    Parameters
    ----------
    if_exists : bool
        是否包含 IF EXISTS 选项
    user : UserName
        用户名
    role_list : List[RoleName]
        角色名列表
    """
    __slots__ = ("_user", "_role_list")

    def __init__(self, if_exists: bool, user: "UserName", role_list: List["RoleName"]):
        super().__init__(if_exists)
        self._user = user
        self._role_list = role_list

    @property
    def user(self) -> "UserName":
        """用户名"""
        return self._user

    @property
    def role_list(self) -> List["RoleName"]:
        """角色名列表"""
        return self._role_list


class AlterUserRegistrationStatement(AlterUserStatement):
    """
    用户注册操作：
    alter_user_command user opt_user_registration
    
    Parameters
    ----------
    if_exists : bool
        是否包含 IF EXISTS 选项
    user : UserName
        用户名
    user_registration : UserRegistration
        用户注册操作
    """
    __slots__ = ("_user", "_user_registration")

    def __init__(self, if_exists: bool, user: "UserName", user_registration: "UserRegistration"):
        super().__init__(if_exists)
        self._user = user
        self._user_registration = user_registration

    @property
    def user(self) -> "UserName":
        """用户名"""
        return self._user

    @property
    def user_registration(self) -> "UserRegistration":
        """用户注册操作"""
        return self._user_registration


class AlterUserCurrentUserRegistrationStatement(AlterUserStatement):
    """
    当前用户注册操作：
    alter_user_command user_func opt_user_registration
    
    Parameters
    ----------
    if_exists : bool
        是否包含 IF EXISTS 选项
    user_registration : UserRegistration
        用户注册操作
    """
    __slots__ = ("_user_registration",)

    def __init__(self, if_exists: bool, user_registration: "UserRegistration"):
        super().__init__(if_exists)
        self._user_registration = user_registration

    @property
    def user_registration(self) -> "UserRegistration":
        """用户注册操作"""
        return self._user_registration
