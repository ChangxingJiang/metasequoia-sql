"""
函数选项（function option）
"""

from typing import TYPE_CHECKING

from metasequoia_sql.ast.base import Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.fixed_enum import EnumSqlSecurity

__all__ = [
    "FunctionOption",
    "FunctionOptionComment",
    "FunctionOptionLanguageSql",
    "FunctionOptionLanguageIdent",
    "FunctionOptionNoSql",
    "FunctionOptionContainsSql",
    "FunctionOptionReadsSqlData",
    "FunctionOptionModifiesSqlData",
    "FunctionOptionSqlSecurity",
    "FunctionOptionDeterministic",
]


class FunctionOption(Node):
    """函数选项"""


class FunctionOptionComment(FunctionOption):
    """函数选项：COMMENT"""

    __slots__ = (
        "_comment",
    )

    def __init__(self, comment: str):
        """
        初始化函数注释选项。

        Parameters
        ----------
        comment : str
            注释内容
        """
        self._comment = comment

    @property
    def comment(self) -> str:
        """获取注释内容。
        
        Returns
        -------
        str
            注释内容
        """
        return self._comment


class FunctionOptionLanguageSql(FunctionOption):
    """函数选项：LANGUAGE SQL"""


class FunctionOptionLanguageIdent(FunctionOption):
    """函数选项：LANGUAGE identifier"""

    __slots__ = (
        "_language",
    )

    def __init__(self, language: str):
        """
        初始化函数语言标识符选项。

        Parameters
        ----------
        language : str
            语言标识符
        """
        self._language = language

    @property
    def language(self) -> str:
        """获取语言标识符。
        
        Returns
        -------
        str
            语言标识符
        """
        return self._language


class FunctionOptionNoSql(FunctionOption):
    """函数选项：NO SQL"""


class FunctionOptionContainsSql(FunctionOption):
    """函数选项：CONTAINS SQL"""


class FunctionOptionReadsSqlData(FunctionOption):
    """函数选项：READS SQL DATA"""


class FunctionOptionModifiesSqlData(FunctionOption):
    """函数选项：MODIFIES SQL DATA"""


class FunctionOptionSqlSecurity(FunctionOption):
    """函数选项：SQL SECURITY"""

    __slots__ = (
        "_security",
    )

    def __init__(self, security: "EnumSqlSecurity"):
        """
        初始化函数安全选项。

        Parameters
        ----------
        security : EnumSqlSecurity
            SQL安全类型
        """
        self._security = security

    @property
    def security(self) -> "EnumSqlSecurity":
        """获取SQL安全类型。
        
        Returns
        -------
        EnumSqlSecurity
            SQL安全类型
        """
        return self._security


class FunctionOptionDeterministic(FunctionOption):
    """函数选项：DETERMINISTIC 或 NOT DETERMINISTIC"""

    __slots__ = (
        "_is_deterministic",
    )

    def __init__(self, is_deterministic: bool):
        """
        初始化函数确定性选项。

        Parameters
        ----------
        is_deterministic : bool
            是否为确定性函数
        """
        self._is_deterministic = is_deterministic

    @property
    def is_deterministic(self) -> bool:
        """获取是否为确定性函数。
        
        Returns
        -------
        bool
            是否为确定性函数
        """
        return self._is_deterministic
