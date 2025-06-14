"""
INSTALL/UNINSTALL 语句（install/uninstall statement）
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement, Expression

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.fixed_enum import EnumInstallOptionType

__all__ = [
    "InstallStatement",
    "InstallPluginStatement",
    "InstallComponentStatement",
    "UninstallStatement",
    "UninstallPluginStatement",
    "UninstallComponentStatement",
    "InstallSetValue",
]


class InstallSetValue:
    """INSTALL COMPONENT 语句中的 SET 子句值"""

    __slots__ = (
        "_option_type",
        "_variable",
        "_value",
    )

    def __init__(self, option_type: "EnumInstallOptionType", variable: "Identifier", value: Expression):
        self._option_type = option_type
        self._variable = variable
        self._value = value

    @property
    def option_type(self) -> "EnumInstallOptionType":
        return self._option_type

    @property
    def variable(self) -> "Identifier":
        return self._variable

    @property
    def value(self) -> Expression:
        return self._value


class InstallStatement(Statement):
    """INSTALL 语句基类"""


class InstallPluginStatement(InstallStatement):
    """INSTALL PLUGIN 语句"""

    __slots__ = (
        "_plugin_name",
        "_soname",
    )

    def __init__(self, plugin_name: "Identifier", soname: str):
        self._plugin_name = plugin_name
        self._soname = soname

    @property
    def plugin_name(self) -> "Identifier":
        return self._plugin_name

    @property
    def soname(self) -> str:
        return self._soname


class InstallComponentStatement(InstallStatement):
    """INSTALL COMPONENT 语句"""

    __slots__ = (
        "_component_list",
        "_set_value_list",
    )

    def __init__(self, component_list: List[str], set_value_list: List[InstallSetValue]):
        self._component_list = component_list
        self._set_value_list = set_value_list or []

    @property
    def component_list(self) -> List[str]:
        return self._component_list

    @property
    def set_value_list(self) -> List[InstallSetValue]:
        return self._set_value_list


class UninstallStatement(Statement):
    """UNINSTALL 语句基类"""


class UninstallPluginStatement(UninstallStatement):
    """UNINSTALL PLUGIN 语句"""

    __slots__ = (
        "_plugin_name",
    )

    def __init__(self, plugin_name: "Identifier"):
        self._plugin_name = plugin_name

    @property
    def plugin_name(self) -> "Identifier":
        return self._plugin_name


class UninstallComponentStatement(UninstallStatement):
    """UNINSTALL COMPONENT 语句"""

    __slots__ = (
        "_component_list",
    )

    def __init__(self, component_list: List[str]):
        self._component_list = component_list

    @property
    def component_list(self) -> List[str]:
        return self._component_list 