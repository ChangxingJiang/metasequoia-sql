"""
USE 语句（use statement）
"""

from metasequoia_sql.ast.base import Statement

__all__ = [
    "UseStatement",
]


class UseStatement(Statement):
    """USE 语句"""

    __slots__ = (
        "_database_name",
    )

    def __init__(self, database_name: str):
        """
        初始化 USE 语句

        Parameters
        ----------
        database_name : str
            数据库名称
        """
        self._database_name = database_name

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
