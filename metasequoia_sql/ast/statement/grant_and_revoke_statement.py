"""
GRANT 和 REVOKE 语句（grant and revoke statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Node, Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.literal import UserName
    from metasequoia_sql.ast.basic.fixed_enum import EnumAclType

__all__ = [
    "RoleOrPrivilege",
    "RoleOrDynamicPrivilege",
    "RoleAtHost",
    "StaticPrivilege",
    "WithRole",
    "WithRoleList",
    "WithRoleAll",
    "WithRoleNone",
    "WithRoleDefault",
    "GrantIdentifier",
    "GrantIdentifierGlobal",
    "GrantIdentifierDatabase",
    "GrantIdentifierTable",
    "GrantStatement",
    "GrantRolesStatement",
    "GrantPrivilegesStatement",
    "GrantAllPrivilegesStatement",
    "GrantProxyStatement",
    "RevokeStatement",
    "RevokeRolesStatement",
    "RevokePrivilegesStatement",
    "RevokeAllPrivilegesStatement",
    "RevokeProxyStatement",
]


class RoleOrPrivilege(Node):
    """角色或权限的抽象语法树节点基类"""


class RoleOrDynamicPrivilege(RoleOrPrivilege):
    """
    角色或动态权限的抽象语法树节点。

    语法规则：
        role_ident_or_text [opt_column_list]
    """

    __slots__ = (
        "_privilege_name",
        "_column_list",
    )

    def __init__(self, privilege_name: str, column_list: Optional[List["Identifier"]]):
        """
        初始化角色或动态权限节点。

        Parameters
        ----------
        privilege_name : str
            权限名称
        column_list : Optional[List[Identifier]]
            可选的列名列表
        """
        self._privilege_name = privilege_name
        self._column_list = column_list

    @property
    def privilege_name(self) -> str:
        """
        获取权限名称。

        Returns
        -------
        str
            权限名称
        """
        return self._privilege_name

    @property
    def column_list(self) -> Optional[List["Identifier"]]:
        """
        获取列名列表。

        Returns
        -------
        Optional[List[Identifier]]
            列名列表
        """
        return self._column_list


class RoleAtHost(RoleOrPrivilege):
    """
    指定主机的角色的抽象语法树节点。

    语法规则：
        role_ident_or_text @ ident_or_text
    """

    __slots__ = (
        "_role_name",
        "_host_name",
    )

    def __init__(self, role_name: str, host_name: str):
        """
        初始化指定主机的角色节点。

        Parameters
        ----------
        role_name : str
            角色名称
        host_name : str
            主机名称
        """
        self._role_name = role_name
        self._host_name = host_name

    @property
    def role_name(self) -> str:
        """
        获取角色名称。

        Returns
        -------
        str
            角色名称
        """
        return self._role_name

    @property
    def host_name(self) -> str:
        """
        获取主机名称。

        Returns
        -------
        str
            主机名称
        """
        return self._host_name


class StaticPrivilege(RoleOrPrivilege):
    """
    静态权限的抽象语法树节点。

    语法规则：
        特定的静态权限关键字 [opt_column_list]
    """

    __slots__ = (
        "_privilege_type",
        "_column_list",
    )

    def __init__(self, privilege_type: str, column_list: Optional[List["Identifier"]]):
        """
        初始化静态权限节点。

        Parameters
        ----------
        privilege_type : str
            权限类型
        column_list : Optional[List[Identifier]]
            可选的列名列表
        """
        self._privilege_type = privilege_type
        self._column_list = column_list

    @property
    def privilege_type(self) -> str:
        """
        获取权限类型。

        Returns
        -------
        str
            权限类型
        """
        return self._privilege_type

    @property
    def column_list(self) -> Optional[List["Identifier"]]:
        """
        获取列名列表。

        Returns
        -------
        Optional[List[Identifier]]
            列名列表
        """
        return self._column_list


class WithRole(Node):
    """WITH ROLE 子句的抽象语法树节点基类"""


class WithRoleList(WithRole):
    """
    WITH ROLE role_list 的抽象语法树节点。
    """

    __slots__ = (
        "_role_list",
    )

    def __init__(self, role_list: List["UserName"]):
        """
        初始化角色列表节点。

        Parameters
        ----------
        role_list : List[UserName]
            角色列表
        """
        self._role_list = role_list

    @property
    def role_list(self) -> List["UserName"]:
        """
        获取角色列表。

        Returns
        -------
        List[UserName]
            角色列表
        """
        return self._role_list


class WithRoleAll(WithRole):
    """
    WITH ROLE ALL [EXCEPT role_list] 的抽象语法树节点。
    """

    __slots__ = (
        "_except_role_list",
    )

    def __init__(self, except_role_list: Optional[List["UserName"]]):
        """
        初始化 WITH ROLE ALL 节点。

        Parameters
        ----------
        except_role_list : Optional[List[UserName]]
            EXCEPT 后的角色列表
        """
        self._except_role_list = except_role_list

    @property
    def except_role_list(self) -> Optional[List["UserName"]]:
        """
        获取EXCEPT后的角色列表。

        Returns
        -------
        Optional[List[UserName]]
            EXCEPT后的角色列表
        """
        return self._except_role_list


class WithRoleNone(WithRole):
    """WITH ROLE NONE 的抽象语法树节点"""


class WithRoleDefault(WithRole):
    """WITH ROLE DEFAULT 的抽象语法树节点"""


class GrantIdentifier(Node):
    """GRANT 语句中标识符的抽象语法树节点基类"""


class GrantIdentifierGlobal(GrantIdentifier):
    """
    全局权限标识符 (*.*) 的抽象语法树节点。
    """


class GrantIdentifierDatabase(GrantIdentifier):
    """
    数据库权限标识符 (database.* 或 *) 的抽象语法树节点。
    """

    __slots__ = (
        "_database_name",
    )

    def __init__(self, database_name: Optional[str]):
        """
        初始化数据库权限标识符节点。

        Parameters
        ----------
        database_name : Optional[str]
            数据库名称，None表示当前数据库
        """
        self._database_name = database_name

    @property
    def database_name(self) -> Optional[str]:
        """
        获取数据库名称。

        Returns
        -------
        Optional[str]
            数据库名称
        """
        return self._database_name


class GrantIdentifierTable(GrantIdentifier):
    """
    表权限标识符 (table_ident) 的抽象语法树节点。
    """

    __slots__ = (
        "_table_identifier",
    )

    def __init__(self, table_identifier: "Identifier"):
        """
        初始化表权限标识符节点。

        Parameters
        ----------
        table_identifier : Identifier
            表标识符
        """
        self._table_identifier = table_identifier

    @property
    def table_identifier(self) -> "Identifier":
        """
        获取表标识符。

        Returns
        -------
        Identifier
            表标识符
        """
        return self._table_identifier


class GrantStatement(Statement):
    """GRANT 语句的抽象语法树节点基类"""


class GrantRolesStatement(GrantStatement):
    """
    GRANT 角色语句的抽象语法树节点。

    语法规则：
        GRANT role_or_privilege_list TO user_list opt_with_admin_option
    """

    __slots__ = (
        "_roles",
        "_users",
        "_with_admin_option",
    )

    def __init__(self, roles: List[RoleOrPrivilege], users: List["UserName"], with_admin_option: bool):
        """
        初始化GRANT角色语句节点。

        Parameters
        ----------
        roles : List[RoleOrPrivilege]
            角色或权限列表
        users : List[UserName]
            用户列表
        with_admin_option : bool
            是否包含WITH ADMIN OPTION
        """
        self._roles = roles
        self._users = users
        self._with_admin_option = with_admin_option

    @property
    def roles(self) -> List[RoleOrPrivilege]:
        """
        获取角色或权限列表。

        Returns
        -------
        List[RoleOrPrivilege]
            角色或权限列表
        """
        return self._roles

    @property
    def users(self) -> List["UserName"]:
        """
        获取用户列表。

        Returns
        -------
        List[UserName]
            用户列表
        """
        return self._users

    @property
    def with_admin_option(self) -> bool:
        """
        获取是否包含WITH ADMIN OPTION。

        Returns
        -------
        bool
            是否包含WITH ADMIN OPTION
        """
        return self._with_admin_option


class GrantPrivilegesStatement(GrantStatement):
    """
    GRANT 权限语句的抽象语法树节点。

    语法规则：
        GRANT role_or_privilege_list ON opt_acl_type grant_ident TO user_list grant_options opt_grant_as
    """

    __slots__ = (
        "_privileges",
        "_acl_type",
        "_grant_identifier",
        "_users",
        "_with_grant_option",
        "_grant_as",
    )

    def __init__(self, privileges: List[RoleOrPrivilege], acl_type: "EnumAclType",
                 grant_identifier: GrantIdentifier, users: List["UserName"],
                 with_grant_option: bool, grant_as: Optional["UserName"]):
        """
        初始化GRANT权限语句节点。

        Parameters
        ----------
        privileges : List[RoleOrPrivilege]
            权限列表
        acl_type : EnumAclType
            ACL类型
        grant_identifier : GrantIdentifier
            授权标识符
        users : List[UserName]
            用户列表
        with_grant_option : bool
            是否包含WITH GRANT OPTION
        grant_as : Optional[UserName]
            GRANT AS用户
        """
        self._privileges = privileges
        self._acl_type = acl_type
        self._grant_identifier = grant_identifier
        self._users = users
        self._with_grant_option = with_grant_option
        self._grant_as = grant_as

    @property
    def privileges(self) -> List[RoleOrPrivilege]:
        """
        获取权限列表。

        Returns
        -------
        List[RoleOrPrivilege]
            权限列表
        """
        return self._privileges

    @property
    def acl_type(self) -> "EnumAclType":
        """
        获取ACL类型。

        Returns
        -------
        EnumAclType
            ACL类型
        """
        return self._acl_type

    @property
    def grant_identifier(self) -> GrantIdentifier:
        """
        获取授权标识符。

        Returns
        -------
        GrantIdentifier
            授权标识符
        """
        return self._grant_identifier

    @property
    def users(self) -> List["UserName"]:
        """
        获取用户列表。

        Returns
        -------
        List[UserName]
            用户列表
        """
        return self._users

    @property
    def with_grant_option(self) -> bool:
        """
        获取是否包含WITH GRANT OPTION。

        Returns
        -------
        bool
            是否包含WITH GRANT OPTION
        """
        return self._with_grant_option

    @property
    def grant_as(self) -> Optional["UserName"]:
        """
        获取GRANT AS用户。

        Returns
        -------
        Optional[UserName]
            GRANT AS用户
        """
        return self._grant_as


class GrantAllPrivilegesStatement(GrantStatement):
    """
    GRANT ALL PRIVILEGES 语句的抽象语法树节点。

    语法规则：
        GRANT ALL [PRIVILEGES] ON opt_acl_type grant_ident TO user_list grant_options opt_grant_as
    """

    __slots__ = (
        "_acl_type",
        "_grant_identifier",
        "_users",
        "_with_grant_option",
        "_grant_as",
    )

    def __init__(self, acl_type: "EnumAclType", grant_identifier: GrantIdentifier,
                 users: List["UserName"], with_grant_option: bool, grant_as: Optional["UserName"]):
        """
        初始化GRANT ALL PRIVILEGES语句节点。

        Parameters
        ----------
        acl_type : EnumAclType
            ACL类型
        grant_identifier : GrantIdentifier
            授权标识符
        users : List[UserName]
            用户列表
        with_grant_option : bool
            是否包含WITH GRANT OPTION
        grant_as : Optional[UserName]
            GRANT AS用户
        """
        self._acl_type = acl_type
        self._grant_identifier = grant_identifier
        self._users = users
        self._with_grant_option = with_grant_option
        self._grant_as = grant_as

    @property
    def acl_type(self) -> "EnumAclType":
        """
        获取ACL类型。

        Returns
        -------
        EnumAclType
            ACL类型
        """
        return self._acl_type

    @property
    def grant_identifier(self) -> GrantIdentifier:
        """
        获取授权标识符。

        Returns
        -------
        GrantIdentifier
            授权标识符
        """
        return self._grant_identifier

    @property
    def users(self) -> List["UserName"]:
        """
        获取用户列表。

        Returns
        -------
        List[UserName]
            用户列表
        """
        return self._users

    @property
    def with_grant_option(self) -> bool:
        """
        获取是否包含WITH GRANT OPTION。

        Returns
        -------
        bool
            是否包含WITH GRANT OPTION
        """
        return self._with_grant_option

    @property
    def grant_as(self) -> Optional["UserName"]:
        """
        获取GRANT AS用户。

        Returns
        -------
        Optional[UserName]
            GRANT AS用户
        """
        return self._grant_as


class GrantProxyStatement(GrantStatement):
    """
    GRANT PROXY 语句的抽象语法树节点。

    语法规则：
        GRANT PROXY ON user TO user_list opt_grant_option
    """

    __slots__ = (
        "_proxy_user",
        "_users",
        "_with_grant_option",
    )

    def __init__(self, proxy_user: "UserName", users: List["UserName"], with_grant_option: bool):
        """
        初始化GRANT PROXY语句节点。

        Parameters
        ----------
        proxy_user : UserName
            代理用户
        users : List[UserName]
            用户列表
        with_grant_option : bool
            是否包含WITH GRANT OPTION
        """
        self._proxy_user = proxy_user
        self._users = users
        self._with_grant_option = with_grant_option

    @property
    def proxy_user(self) -> "UserName":
        """
        获取代理用户。

        Returns
        -------
        UserName
            代理用户
        """
        return self._proxy_user

    @property
    def users(self) -> List["UserName"]:
        """
        获取用户列表。

        Returns
        -------
        List[UserName]
            用户列表
        """
        return self._users

    @property
    def with_grant_option(self) -> bool:
        """
        获取是否包含WITH GRANT OPTION。

        Returns
        -------
        bool
            是否包含WITH GRANT OPTION
        """
        return self._with_grant_option


class RevokeStatement(Statement):
    """REVOKE 语句的抽象语法树节点基类"""


class RevokeRolesStatement(RevokeStatement):
    """
    REVOKE 角色语句的抽象语法树节点。

    语法规则：
        REVOKE [IF EXISTS] role_or_privilege_list FROM user_list opt_ignore_unknown_user
    """

    __slots__ = (
        "_if_exists",
        "_roles",
        "_users",
        "_ignore_unknown_user",
    )

    def __init__(self, if_exists: bool, roles: List[RoleOrPrivilege],
                 users: List["UserName"], ignore_unknown_user: bool):
        """
        初始化REVOKE角色语句节点。

        Parameters
        ----------
        if_exists : bool
            是否包含IF EXISTS
        roles : List[RoleOrPrivilege]
            角色或权限列表
        users : List[UserName]
            用户列表
        ignore_unknown_user : bool
            是否忽略未知用户
        """
        self._if_exists = if_exists
        self._roles = roles
        self._users = users
        self._ignore_unknown_user = ignore_unknown_user

    @property
    def if_exists(self) -> bool:
        """
        获取是否包含IF EXISTS。

        Returns
        -------
        bool
            是否包含IF EXISTS
        """
        return self._if_exists

    @property
    def roles(self) -> List[RoleOrPrivilege]:
        """
        获取角色或权限列表。

        Returns
        -------
        List[RoleOrPrivilege]
            角色或权限列表
        """
        return self._roles

    @property
    def users(self) -> List["UserName"]:
        """
        获取用户列表。

        Returns
        -------
        List[UserName]
            用户列表
        """
        return self._users

    @property
    def ignore_unknown_user(self) -> bool:
        """
        获取是否忽略未知用户。

        Returns
        -------
        bool
            是否忽略未知用户
        """
        return self._ignore_unknown_user


class RevokePrivilegesStatement(RevokeStatement):
    """
    REVOKE 权限语句的抽象语法树节点。

    语法规则：
        REVOKE [IF EXISTS] role_or_privilege_list ON opt_acl_type grant_ident FROM user_list opt_ignore_unknown_user
    """

    __slots__ = (
        "_if_exists",
        "_privileges",
        "_acl_type",
        "_grant_identifier",
        "_users",
        "_ignore_unknown_user",
    )

    def __init__(self, if_exists: bool, privileges: List[RoleOrPrivilege],
                 acl_type: "EnumAclType", grant_identifier: GrantIdentifier,
                 users: List["UserName"], ignore_unknown_user: bool):
        """
        初始化REVOKE权限语句节点。

        Parameters
        ----------
        if_exists : bool
            是否包含IF EXISTS
        privileges : List[RoleOrPrivilege]
            权限列表
        acl_type : EnumAclType
            ACL类型
        grant_identifier : GrantIdentifier
            授权标识符
        users : List[UserName]
            用户列表
        ignore_unknown_user : bool
            是否忽略未知用户
        """
        self._if_exists = if_exists
        self._privileges = privileges
        self._acl_type = acl_type
        self._grant_identifier = grant_identifier
        self._users = users
        self._ignore_unknown_user = ignore_unknown_user

    @property
    def if_exists(self) -> bool:
        """
        获取是否包含IF EXISTS。

        Returns
        -------
        bool
            是否包含IF EXISTS
        """
        return self._if_exists

    @property
    def privileges(self) -> List[RoleOrPrivilege]:
        """
        获取权限列表。

        Returns
        -------
        List[RoleOrPrivilege]
            权限列表
        """
        return self._privileges

    @property
    def acl_type(self) -> "EnumAclType":
        """
        获取ACL类型。

        Returns
        -------
        EnumAclType
            ACL类型
        """
        return self._acl_type

    @property
    def grant_identifier(self) -> GrantIdentifier:
        """
        获取授权标识符。

        Returns
        -------
        GrantIdentifier
            授权标识符
        """
        return self._grant_identifier

    @property
    def users(self) -> List["UserName"]:
        """
        获取用户列表。

        Returns
        -------
        List[UserName]
            用户列表
        """
        return self._users

    @property
    def ignore_unknown_user(self) -> bool:
        """
        获取是否忽略未知用户。

        Returns
        -------
        bool
            是否忽略未知用户
        """
        return self._ignore_unknown_user


class RevokeAllPrivilegesStatement(RevokeStatement):
    """
    REVOKE ALL PRIVILEGES 语句的抽象语法树节点。

    语法规则：
        REVOKE [IF EXISTS] ALL [PRIVILEGES] ON opt_acl_type grant_ident FROM user_list opt_ignore_unknown_user
    """

    __slots__ = (
        "_if_exists",
        "_acl_type",
        "_grant_identifier",
        "_users",
        "_ignore_unknown_user",
    )

    def __init__(self, if_exists: bool, acl_type: "EnumAclType",
                 grant_identifier: GrantIdentifier, users: List["UserName"], ignore_unknown_user: bool):
        """
        初始化REVOKE ALL PRIVILEGES语句节点。

        Parameters
        ----------
        if_exists : bool
            是否包含IF EXISTS
        acl_type : EnumAclType
            ACL类型
        grant_identifier : GrantIdentifier
            授权标识符
        users : List[UserName]
            用户列表
        ignore_unknown_user : bool
            是否忽略未知用户
        """
        self._if_exists = if_exists
        self._acl_type = acl_type
        self._grant_identifier = grant_identifier
        self._users = users
        self._ignore_unknown_user = ignore_unknown_user

    @property
    def if_exists(self) -> bool:
        """
        获取是否包含IF EXISTS。

        Returns
        -------
        bool
            是否包含IF EXISTS
        """
        return self._if_exists

    @property
    def acl_type(self) -> "EnumAclType":
        """
        获取ACL类型。

        Returns
        -------
        EnumAclType
            ACL类型
        """
        return self._acl_type

    @property
    def grant_identifier(self) -> GrantIdentifier:
        """
        获取授权标识符。

        Returns
        -------
        GrantIdentifier
            授权标识符
        """
        return self._grant_identifier

    @property
    def users(self) -> List["UserName"]:
        """
        获取用户列表。

        Returns
        -------
        List[UserName]
            用户列表
        """
        return self._users

    @property
    def ignore_unknown_user(self) -> bool:
        """
        获取是否忽略未知用户。

        Returns
        -------
        bool
            是否忽略未知用户
        """
        return self._ignore_unknown_user


class RevokeProxyStatement(RevokeStatement):
    """
    REVOKE PROXY 语句的抽象语法树节点。

    语法规则：
        REVOKE [IF EXISTS] PROXY ON user FROM user_list opt_ignore_unknown_user
    """

    __slots__ = (
        "_if_exists",
        "_proxy_user",
        "_users",
        "_ignore_unknown_user",
    )

    def __init__(self, if_exists: bool, proxy_user: "UserName",
                 users: List["UserName"], ignore_unknown_user: bool):
        """
        初始化REVOKE PROXY语句节点。

        Parameters
        ----------
        if_exists : bool
            是否包含IF EXISTS
        proxy_user : UserName
            代理用户
        users : List[UserName]
            用户列表
        ignore_unknown_user : bool
            是否忽略未知用户
        """
        self._if_exists = if_exists
        self._proxy_user = proxy_user
        self._users = users
        self._ignore_unknown_user = ignore_unknown_user

    @property
    def if_exists(self) -> bool:
        """
        获取是否包含IF EXISTS。

        Returns
        -------
        bool
            是否包含IF EXISTS
        """
        return self._if_exists

    @property
    def proxy_user(self) -> "UserName":
        """
        获取代理用户。

        Returns
        -------
        UserName
            代理用户
        """
        return self._proxy_user

    @property
    def users(self) -> List["UserName"]:
        """
        获取用户列表。

        Returns
        -------
        List[UserName]
            用户列表
        """
        return self._users

    @property
    def ignore_unknown_user(self) -> bool:
        """
        获取是否忽略未知用户。

        Returns
        -------
        bool
            是否忽略未知用户
        """
        return self._ignore_unknown_user
