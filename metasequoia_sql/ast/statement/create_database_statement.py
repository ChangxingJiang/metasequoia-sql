"""
CREATE DATABASE 语句（create database statement）
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.phrase.ddl_option import DdlOption

__all__ = [
    "CreateDatabaseStatement"
]


class CreateDatabaseStatement(Statement):
    """CREATE DATABASE 语句"""

    __slots__ = (
        "_if_not_exists",
        "_database_name",
        "_options",
    )

    def __init__(self,
                 if_not_exists: bool,
                 database_name: str,
                 options: List["DdlOption"]):
        self._if_not_exists = if_not_exists
        self._database_name = database_name
        self._options = options

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
    def database_name(self) -> str:
        """
        数据库名称

        Returns
        -------
        str
            数据库名称
        """
        return self._database_name

    @property
    def options(self) -> List["DdlOption"]:
        """
        DDL 选项列表

        Returns
        -------
        List["DdlOption"]
            DDL 选项列表
        """
        return self._options
