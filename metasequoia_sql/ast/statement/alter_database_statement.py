"""
ALTER DATABASE 语句（alter database statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.phrase.ddl_option import DdlOption

__all__ = [
    "AlterDatabaseStatement",
]


class AlterDatabaseStatement(Statement):
    """ALTER DATABASE 语句"""

    __slots__ = (
        "_database_name",
        "_option_list",
    )

    def __init__(self, database_name: Optional[str], option_list: List["DdlOption"]):
        self._database_name = database_name
        self._option_list = option_list

    @property
    def database_name(self) -> Optional[str]:
        """
        数据库名称

        Returns
        -------
        Optional[str]
            数据库名称，如果为 None 则表示当前数据库
        """
        return self._database_name

    @property
    def option_list(self) -> List["DdlOption"]:
        """
        DDL 选项列表

        Returns
        -------
        List[DdlOption]
            DDL 选项列表
        """
        return self._option_list
