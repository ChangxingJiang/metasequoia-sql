"""
ALTER USER 相关的 AST 节点类
"""

from typing import TYPE_CHECKING

from metasequoia_sql.ast.base import Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.phrase.identification import Identification
    from metasequoia_sql.ast.basic.ident import UserName

__all__ = [
    "AlterUser",
    "AlterUserIdentifiedByPassword",
    "AlterUserIdentifiedByPasswordReplace",
    "AlterUserIdentifiedByRandomPassword",
    "AlterUserIdentifiedByRandomPasswordReplace",
    "AlterUserIdentifiedWithPlugin",
    "AlterUserIdentifiedWithPluginAsAuth",
    "AlterUserIdentifiedWithPluginByPassword",
    "AlterUserIdentifiedWithPluginByPasswordReplace",
    "AlterUserIdentifiedWithPluginByRandomPassword",
    "AlterUserDiscardOldPassword",
    "AlterUserAddFactor",
    "AlterUserAddTwoFactors",
    "AlterUserModifyFactor",
    "AlterUserModifyTwoFactors",
    "AlterUserDropFactor",
    "AlterUserDropTwoFactors",
]


class AlterUser(Node):
    """
    ALTER USER 操作的基类
    
    Parameters
    ----------
    user : UserName
        用户名
    """
    __slots__ = ("_user",)

    def __init__(self, user: "UserName"):
        self._user = user

    @property
    def user(self) -> "UserName":
        """用户名"""
        return self._user


class AlterUserIdentifiedByPassword(AlterUser):
    """
    用户通过密码认证：user identified_by_password opt_retain_current_password
    
    Parameters
    ----------
    user : UserName
        用户名
    identification : Identification
        认证信息
    retain_current_password : bool
        是否保留当前密码
    """
    __slots__ = ("_identification", "_retain_current_password")

    def __init__(
            self,
            user: "UserName",
            identification: "Identification",
            retain_current_password: bool
    ):
        super().__init__(user)
        self._identification = identification
        self._retain_current_password = retain_current_password

    @property
    def identification(self) -> "Identification":
        """认证信息"""
        return self._identification

    @property
    def retain_current_password(self) -> bool:
        """是否保留当前密码"""
        return self._retain_current_password


class AlterUserIdentifiedByPasswordReplace(AlterUser):
    """
    用户通过密码认证并替换：user identified_by_password REPLACE TEXT_STRING_password opt_retain_current_password
    
    Parameters
    ----------
    user : UserName
        用户名
    identification : Identification
        认证信息
    current_password : str
        当前密码
    retain_current_password : bool
        是否保留当前密码
    """
    __slots__ = ("_identification", "_current_password", "_retain_current_password")

    def __init__(
            self,
            user: "UserName",
            identification: "Identification",
            current_password: str,
            retain_current_password: bool
    ):
        super().__init__(user)
        self._identification = identification
        self._current_password = current_password
        self._retain_current_password = retain_current_password

    @property
    def identification(self) -> "Identification":
        """认证信息"""
        return self._identification

    @property
    def current_password(self) -> str:
        """当前密码"""
        return self._current_password

    @property
    def retain_current_password(self) -> bool:
        """是否保留当前密码"""
        return self._retain_current_password


class AlterUserIdentifiedByRandomPassword(AlterUser):
    """
    用户通过随机密码认证：user identified_by_random_password opt_retain_current_password
    
    Parameters
    ----------
    user : UserName
        用户名
    identification : Identification
        认证信息
    retain_current_password : bool
        是否保留当前密码
    """
    __slots__ = ("_identification", "_retain_current_password")

    def __init__(
            self,
            user: "UserName",
            identification: "Identification",
            retain_current_password: bool
    ):
        super().__init__(user)
        self._identification = identification
        self._retain_current_password = retain_current_password

    @property
    def identification(self) -> "Identification":
        """认证信息"""
        return self._identification

    @property
    def retain_current_password(self) -> bool:
        """是否保留当前密码"""
        return self._retain_current_password


class AlterUserIdentifiedByRandomPasswordReplace(AlterUser):
    """
    用户通过随机密码认证并替换：user identified_by_random_password REPLACE TEXT_STRING_password opt_retain_current_password
    
    Parameters
    ----------
    user : UserName
        用户名
    identification : Identification
        认证信息
    current_password : str
        当前密码
    retain_current_password : bool
        是否保留当前密码
    """
    __slots__ = ("_identification", "_current_password", "_retain_current_password")

    def __init__(
            self,
            user: "UserName",
            identification: "Identification",
            current_password: str,
            retain_current_password: bool
    ):
        super().__init__(user)
        self._identification = identification
        self._current_password = current_password
        self._retain_current_password = retain_current_password

    @property
    def identification(self) -> "Identification":
        """认证信息"""
        return self._identification

    @property
    def current_password(self) -> str:
        """当前密码"""
        return self._current_password

    @property
    def retain_current_password(self) -> bool:
        """是否保留当前密码"""
        return self._retain_current_password


class AlterUserIdentifiedWithPlugin(AlterUser):
    """
    用户通过插件认证：user identified_with_plugin
    
    Parameters
    ----------
    user : UserName
        用户名
    identification : Identification
        认证信息
    """
    __slots__ = ("_identification",)

    def __init__(self, user: "UserName", identification: "Identification"):
        super().__init__(user)
        self._identification = identification

    @property
    def identification(self) -> "Identification":
        """认证信息"""
        return self._identification


class AlterUserIdentifiedWithPluginAsAuth(AlterUser):
    """
    用户通过插件认证：user identified_with_plugin_as_auth opt_retain_current_password
    
    Parameters
    ----------
    user : UserName
        用户名
    identification : Identification
        认证信息
    retain_current_password : bool
        是否保留当前密码
    """
    __slots__ = ("_identification", "_retain_current_password")

    def __init__(
            self,
            user: "UserName",
            identification: "Identification",
            retain_current_password: bool
    ):
        super().__init__(user)
        self._identification = identification
        self._retain_current_password = retain_current_password

    @property
    def identification(self) -> "Identification":
        """认证信息"""
        return self._identification

    @property
    def retain_current_password(self) -> bool:
        """是否保留当前密码"""
        return self._retain_current_password


class AlterUserIdentifiedWithPluginByPassword(AlterUser):
    """
    用户通过插件和密码认证：user identified_with_plugin_by_password opt_retain_current_password
    
    Parameters
    ----------
    user : UserName
        用户名
    identification : Identification
        认证信息
    retain_current_password : bool
        是否保留当前密码
    """
    __slots__ = ("_identification", "_retain_current_password")

    def __init__(
            self,
            user: "UserName",
            identification: "Identification",
            retain_current_password: bool
    ):
        super().__init__(user)
        self._identification = identification
        self._retain_current_password = retain_current_password

    @property
    def identification(self) -> "Identification":
        """认证信息"""
        return self._identification

    @property
    def retain_current_password(self) -> bool:
        """是否保留当前密码"""
        return self._retain_current_password


class AlterUserIdentifiedWithPluginByPasswordReplace(AlterUser):
    """
    用户通过插件和密码认证并替换：user identified_with_plugin_by_password REPLACE TEXT_STRING_password opt_retain_current_password
    
    Parameters
    ----------
    user : UserName
        用户名
    identification : Identification
        认证信息
    current_password : str
        当前密码
    retain_current_password : bool
        是否保留当前密码
    """
    __slots__ = ("_identification", "_current_password", "_retain_current_password")

    def __init__(
            self,
            user: "UserName",
            identification: "Identification",
            current_password: str,
            retain_current_password: bool
    ):
        super().__init__(user)
        self._identification = identification
        self._current_password = current_password
        self._retain_current_password = retain_current_password

    @property
    def identification(self) -> "Identification":
        """认证信息"""
        return self._identification

    @property
    def current_password(self) -> str:
        """当前密码"""
        return self._current_password

    @property
    def retain_current_password(self) -> bool:
        """是否保留当前密码"""
        return self._retain_current_password


class AlterUserIdentifiedWithPluginByRandomPassword(AlterUser):
    """
    用户通过插件和随机密码认证：user identified_with_plugin_by_random_password opt_retain_current_password
    
    Parameters
    ----------
    user : UserName
        用户名
    identification : Identification
        认证信息
    retain_current_password : bool
        是否保留当前密码
    """
    __slots__ = ("_identification", "_retain_current_password")

    def __init__(
            self,
            user: "UserName",
            identification: "Identification",
            retain_current_password: bool
    ):
        super().__init__(user)
        self._identification = identification
        self._retain_current_password = retain_current_password

    @property
    def identification(self) -> "Identification":
        """认证信息"""
        return self._identification

    @property
    def retain_current_password(self) -> bool:
        """是否保留当前密码"""
        return self._retain_current_password


class AlterUserDiscardOldPassword(AlterUser):
    """
    用户丢弃旧密码：user opt_discard_old_password
    
    Parameters
    ----------
    user : UserName
        用户名
    discard_old_password : bool
        是否丢弃旧密码
    """
    __slots__ = ("_discard_old_password",)

    def __init__(self, user: "UserName", discard_old_password: bool):
        super().__init__(user)
        self._discard_old_password = discard_old_password

    @property
    def discard_old_password(self) -> bool:
        """是否丢弃旧密码"""
        return self._discard_old_password


class AlterUserAddFactor(AlterUser):
    """
    用户添加单个因子：user ADD factor identification
    
    Parameters
    ----------
    user : UserName
        用户名
    factor : int
        因子编号（2 或 3）
    identification : Identification
        认证信息
    """
    __slots__ = ("_factor", "_identification")

    def __init__(self, user: "UserName", factor: int, identification: "Identification"):
        super().__init__(user)
        self._factor = factor
        self._identification = identification

    @property
    def factor(self) -> int:
        """因子编号"""
        return self._factor

    @property
    def identification(self) -> "Identification":
        """认证信息"""
        return self._identification


class AlterUserAddTwoFactors(AlterUser):
    """
    用户添加两个因子：user ADD factor identification ADD factor identification
    
    Parameters
    ----------
    user : UserName
        用户名
    first_factor : int
        第一个因子编号
    first_identification : Identification
        第一个认证信息
    second_factor : int
        第二个因子编号
    second_identification : Identification
        第二个认证信息
    """
    __slots__ = ("_first_factor", "_first_identification", "_second_factor", "_second_identification")

    def __init__(
            self,
            user: "UserName",
            first_factor: int,
            first_identification: "Identification",
            second_factor: int,
            second_identification: "Identification"
    ):
        super().__init__(user)
        self._first_factor = first_factor
        self._first_identification = first_identification
        self._second_factor = second_factor
        self._second_identification = second_identification

    @property
    def first_factor(self) -> int:
        """第一个因子编号"""
        return self._first_factor

    @property
    def first_identification(self) -> "Identification":
        """第一个认证信息"""
        return self._first_identification

    @property
    def second_factor(self) -> int:
        """第二个因子编号"""
        return self._second_factor

    @property
    def second_identification(self) -> "Identification":
        """第二个认证信息"""
        return self._second_identification


class AlterUserModifyFactor(AlterUser):
    """
    用户修改单个因子：user MODIFY factor identification
    
    Parameters
    ----------
    user : UserName
        用户名
    factor : int
        因子编号（2 或 3）
    identification : Identification
        认证信息
    """
    __slots__ = ("_factor", "_identification")

    def __init__(self, user: "UserName", factor: int, identification: "Identification"):
        super().__init__(user)
        self._factor = factor
        self._identification = identification

    @property
    def factor(self) -> int:
        """因子编号"""
        return self._factor

    @property
    def identification(self) -> "Identification":
        """认证信息"""
        return self._identification


class AlterUserModifyTwoFactors(AlterUser):
    """
    用户修改两个因子：user MODIFY factor identification MODIFY factor identification
    
    Parameters
    ----------
    user : UserName
        用户名
    first_factor : int
        第一个因子编号
    first_identification : Identification
        第一个认证信息
    second_factor : int
        第二个因子编号
    second_identification : Identification
        第二个认证信息
    """
    __slots__ = ("_first_factor", "_first_identification", "_second_factor", "_second_identification")

    def __init__(
            self,
            user: "UserName",
            first_factor: int,
            first_identification: "Identification",
            second_factor: int,
            second_identification: "Identification"
    ):
        super().__init__(user)
        self._first_factor = first_factor
        self._first_identification = first_identification
        self._second_factor = second_factor
        self._second_identification = second_identification

    @property
    def first_factor(self) -> int:
        """第一个因子编号"""
        return self._first_factor

    @property
    def first_identification(self) -> "Identification":
        """第一个认证信息"""
        return self._first_identification

    @property
    def second_factor(self) -> int:
        """第二个因子编号"""
        return self._second_factor

    @property
    def second_identification(self) -> "Identification":
        """第二个认证信息"""
        return self._second_identification


class AlterUserDropFactor(AlterUser):
    """
    用户删除单个因子：user DROP factor
    
    Parameters
    ----------
    user : UserName
        用户名
    factor : int
        因子编号（2 或 3）
    """
    __slots__ = ("_factor",)

    def __init__(self, user: "UserName", factor: int):
        super().__init__(user)
        self._factor = factor

    @property
    def factor(self) -> int:
        """因子编号"""
        return self._factor


class AlterUserDropTwoFactors(AlterUser):
    """
    用户删除两个因子：user DROP factor DROP factor
    
    Parameters
    ----------
    user : UserName
        用户名
    first_factor : int
        第一个因子编号
    second_factor : int
        第二个因子编号
    """
    __slots__ = ("_first_factor", "_second_factor")

    def __init__(self, user: "UserName", first_factor: int, second_factor: int):
        super().__init__(user)
        self._first_factor = first_factor
        self._second_factor = second_factor

    @property
    def first_factor(self) -> int:
        """第一个因子编号"""
        return self._first_factor

    @property
    def second_factor(self) -> int:
        """第二个因子编号"""
        return self._second_factor
