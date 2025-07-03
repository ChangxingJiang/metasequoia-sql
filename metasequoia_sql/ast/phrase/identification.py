"""
身份认证（identification）
"""

from enum import IntEnum
from typing import TYPE_CHECKING

from metasequoia_sql.ast.base import Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier

__all__ = [
    "IdentificationType",
    "Identification",
    "IdentifiedByPassword",
    "IdentifiedByRandomPassword",
    "IdentifiedWithPlugin",
    "IdentifiedWithPluginAsAuth",
    "IdentifiedWithPluginByPassword",
    "IdentifiedWithPluginByRandomPassword",
]


class IdentificationType(IntEnum):
    """身份认证类型"""

    BY_PASSWORD = 1  # IDENTIFIED BY password
    BY_RANDOM_PASSWORD = 2  # IDENTIFIED BY RANDOM PASSWORD
    WITH_PLUGIN = 3  # IDENTIFIED WITH plugin
    WITH_PLUGIN_AS_AUTH = 4  # IDENTIFIED WITH plugin AS auth_string
    WITH_PLUGIN_BY_PASSWORD = 5  # IDENTIFIED WITH plugin BY password
    WITH_PLUGIN_BY_RANDOM_PASSWORD = 6  # IDENTIFIED WITH plugin BY RANDOM PASSWORD


class Identification(Node):
    """身份认证基类

    Parameters
    ----------
    identification_type : IdentificationType
        身份认证类型
    """

    __slots__ = ["_identification_type"]

    def __init__(self, identification_type: IdentificationType):
        self._identification_type = identification_type

    @property
    def identification_type(self) -> IdentificationType:
        """获取身份认证类型。
        
        Returns
        -------
        IdentificationType
            身份认证类型
        """
        return self._identification_type


class IdentifiedByPassword(Identification):
    """使用密码进行身份认证: IDENTIFIED BY password

    Parameters
    ----------
    password : str
        明文密码
    """

    __slots__ = ["_password"]

    def __init__(self, password: str):
        super().__init__(IdentificationType.BY_PASSWORD)
        self._password = password

    @property
    def password(self) -> str:
        """获取明文密码。
        
        Returns
        -------
        str
            明文密码
        """
        return self._password


class IdentifiedByRandomPassword(Identification):
    """使用随机密码进行身份认证: IDENTIFIED BY RANDOM PASSWORD"""

    __slots__ = []

    def __init__(self):
        """
        初始化随机密码身份认证。
        """
        super().__init__(IdentificationType.BY_RANDOM_PASSWORD)


class IdentifiedWithPlugin(Identification):
    """使用插件进行身份认证: IDENTIFIED WITH plugin

    Parameters
    ----------
    plugin : Identifier
        认证插件名称
    """

    __slots__ = ["_plugin"]

    def __init__(self, plugin: str):
        super().__init__(IdentificationType.WITH_PLUGIN)
        self._plugin = plugin

    @property
    def plugin(self) -> str:
        """获取认证插件名称。
        
        Returns
        -------
        str
            认证插件名称
        """
        return self._plugin


class IdentifiedWithPluginAsAuth(Identification):
    """使用插件和认证字符串进行身份认证: IDENTIFIED WITH plugin AS auth_string

    Parameters
    ----------
    plugin : Identifier
        认证插件名称
    auth_string : str
        认证字符串（哈希）
    """

    __slots__ = ["_plugin", "_auth_string"]

    def __init__(self, plugin: str, auth_string: str):
        super().__init__(IdentificationType.WITH_PLUGIN_AS_AUTH)
        self._plugin = plugin
        self._auth_string = auth_string

    @property
    def plugin(self) -> str:
        """获取认证插件名称。
        
        Returns
        -------
        str
            认证插件名称
        """
        return self._plugin

    @property
    def auth_string(self) -> str:
        """获取认证字符串。
        
        Returns
        -------
        str
            认证字符串（哈希）
        """
        return self._auth_string


class IdentifiedWithPluginByPassword(Identification):
    """使用插件和密码进行身份认证: IDENTIFIED WITH plugin BY password

    Parameters
    ----------
    plugin : Identifier
        认证插件名称
    password : str
        明文密码
    """

    __slots__ = ["_plugin", "_password"]

    def __init__(self, plugin: str, password: str):
        super().__init__(IdentificationType.WITH_PLUGIN_BY_PASSWORD)
        self._plugin = plugin
        self._password = password

    @property
    def plugin(self) -> str:
        """获取认证插件名称。
        
        Returns
        -------
        str
            认证插件名称
        """
        return self._plugin

    @property
    def password(self) -> str:
        """获取明文密码。
        
        Returns
        -------
        str
            明文密码
        """
        return self._password


class IdentifiedWithPluginByRandomPassword(Identification):
    """使用插件和随机密码进行身份认证: IDENTIFIED WITH plugin BY RANDOM PASSWORD

    Parameters
    ----------
    plugin : Identifier
        认证插件名称
    """

    __slots__ = ["_plugin"]

    def __init__(self, plugin: str):
        super().__init__(IdentificationType.WITH_PLUGIN_BY_RANDOM_PASSWORD)
        self._plugin = plugin

    @property
    def plugin(self) -> str:
        """获取认证插件名称。
        
        Returns
        -------
        str
            认证插件名称
        """
        return self._plugin
