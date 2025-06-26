"""
ALTER LOGFILE GROUP 语句（alter logfile statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.phrase.ddl_option import DdlOption

__all__ = [
    "AlterLogfileStatement",
]


class AlterLogfileStatement(Statement):
    """ALTER LOGFILE GROUP 语句"""

    __slots__ = ["_group_name", "_undofile", "_option_list"]

    def __init__(self, group_name: str, undofile: str, option_list: Optional[List["DdlOption"]]):
        self._group_name = group_name
        self._undofile = undofile
        self._option_list = option_list if option_list is not None else []

    @property
    def group_name(self) -> str:
        """
        日志文件组名称

        Returns
        -------
        str
            日志文件组名称
        """
        return self._group_name

    @property
    def undofile(self) -> str:
        """
        撤销文件路径

        Returns
        -------
        str
            撤销文件路径
        """
        return self._undofile

    @property
    def option_list(self) -> List["DdlOption"]:
        """
        DDL 选项列表

        Returns
        -------
        List["DdlOption"]
            DDL 选项列表
        """
        return self._option_list
