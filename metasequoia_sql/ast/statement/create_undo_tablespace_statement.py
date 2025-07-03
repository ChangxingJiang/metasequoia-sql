"""
CREATE UNDO TABLESPACE 语句（create undo tablespace statement）
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.phrase.ddl_option import DdlOption

__all__ = [
    "CreateUndoTablespaceStatement"
]


class CreateUndoTablespaceStatement(Statement):
    """CREATE UNDO TABLESPACE 语句"""

    __slots__ = (
        "_tablespace_name",
        "_datafile",
        "_options",
    )

    def __init__(self, tablespace_name: str, datafile: str, options: List["DdlOption"]):
        self._tablespace_name = tablespace_name
        self._datafile = datafile
        self._options = options

    @property
    def tablespace_name(self) -> str:
        """
        撤销表空间名称

        Returns
        -------
        str
            撤销表空间名称
        """
        return self._tablespace_name

    @property
    def datafile(self) -> str:
        """
        数据文件路径

        Returns
        -------
        str
            数据文件路径
        """
        return self._datafile

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
