"""
CREATE TABLESPACE 语句（create tablespace statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.phrase.ddl_option import DdlOption

__all__ = [
    "CreateTablespaceStatement"
]


class CreateTablespaceStatement(Statement):
    """
    CREATE TABLESPACE 语句
    
    Parameters
    ----------
    tablespace_name : str
        表空间名称
    datafile : Optional[str]
        数据文件路径
    logfile_group_name : Optional[str]
        日志文件组名称
    options : List[DdlOption]
        表空间选项列表
    """

    __slots__ = ("_tablespace_name", "_datafile", "_logfile_group_name", "_options")

    def __init__(self,
                 tablespace_name: str,
                 datafile: Optional[str],
                 logfile_group_name: Optional[str],
                 options: List["DdlOption"]):
        self._tablespace_name = tablespace_name
        self._datafile = datafile
        self._logfile_group_name = logfile_group_name
        self._options = options

    @property
    def tablespace_name(self) -> str:
        """表空间名称"""
        return self._tablespace_name

    @property
    def datafile(self) -> Optional[str]:
        """数据文件路径"""
        return self._datafile

    @property
    def logfile_group_name(self) -> Optional[str]:
        """日志文件组名称"""
        return self._logfile_group_name

    @property
    def options(self) -> List["DdlOption"]:
        """表空间选项列表"""
        return self._options
