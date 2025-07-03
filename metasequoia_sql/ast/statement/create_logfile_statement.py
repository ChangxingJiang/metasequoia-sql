"""
CREATE LOGFILE GROUP 语句（create logfile statement）
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.phrase.ddl_option import DdlOption

__all__ = [
    "CreateLogfileStatement"
]


class CreateLogfileStatement(Statement):
    """
    CREATE LOGFILE GROUP 语句
    
    Parameters
    ----------
    logfile_group_name : str
        日志文件组名称
    undofile : str
        撤销文件路径
    options : List[DdlOption]
        日志文件组选项列表
    """

    __slots__ = ("_logfile_group_name", "_undofile", "_options")

    def __init__(self,
                 logfile_group_name: str,
                 undofile: str,
                 options: List["DdlOption"]):
        self._logfile_group_name = logfile_group_name
        self._undofile = undofile
        self._options = options

    @property
    def logfile_group_name(self) -> str:
        """日志文件组名称"""
        return self._logfile_group_name

    @property
    def undofile(self) -> str:
        """撤销文件路径"""
        return self._undofile

    @property
    def options(self) -> List["DdlOption"]:
        """日志文件组选项列表"""
        return self._options
