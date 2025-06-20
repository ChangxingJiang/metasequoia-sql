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

    def __init__(self, tablespace_name: str, datafile: str, options: List["DdlOption"]):
        self._tablespace_name = tablespace_name
        self._datafile = datafile
        self._options = options

    @property
    def tablespace_name(self) -> str:
        return self._tablespace_name

    @property
    def datafile(self) -> str:
        return self._datafile

    @property
    def options(self) -> List["DdlOption"]:
        return self._options
