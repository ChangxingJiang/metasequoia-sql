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
        "_comment"
    )

    def __init__(self, comment: str):
        self._comment = comment

    @property
    def comment(self) -> str:
        return self._comment


class FunctionOptionLanguageSql(FunctionOption):
    """函数选项：LANGUAGE SQL"""


class FunctionOptionLanguageIdent(FunctionOption):
    """函数选项：LANGUAGE identifier"""

    __slots__ = (
        "_language"
    )

    def __init__(self, language: str):
        self._language = language

    @property
    def language(self) -> str:
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
        "_security"
    )

    def __init__(self, security: "EnumSqlSecurity"):
        self._security = security

    @property
    def security(self) -> "EnumSqlSecurity":
        return self._security


class FunctionOptionDeterministic(FunctionOption):
    """函数选项：DETERMINISTIC 或 NOT DETERMINISTIC"""

    __slots__ = (
        "_is_deterministic"
    )

    def __init__(self, is_deterministic: bool):
        self._is_deterministic = is_deterministic

    @property
    def is_deterministic(self) -> bool:
        return self._is_deterministic
