"""
IMPORT TABLE 语句（import table statement）
"""

from typing import List

from metasequoia_sql.ast.base import Statement

__all__ = [
    "ImportTableStatement",
]


class ImportTableStatement(Statement):
    """IMPORT TABLE 语句"""

    __slots__ = (
        "_file_list",
    )

    def __init__(self, file_list: List[str]):
        self._file_list = file_list

    @property
    def file_list(self) -> List[str]:
        """
        文件列表

        Returns
        -------
        List[str]
            文件列表
        """
        return self._file_list
