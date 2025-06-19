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

    def __init__(self,
                 if_not_exists: bool,
                 database_name: str,
                 options: List["DdlOption"]):
        self._if_not_exists = if_not_exists
        self._database_name = database_name
        self._options = options

    @property
    def if_not_exists(self) -> bool:
        return self._if_not_exists

    @property
    def database_name(self) -> str:
        return self._database_name

    @property
    def options(self) -> List["DdlOption"]:
        return self._options
