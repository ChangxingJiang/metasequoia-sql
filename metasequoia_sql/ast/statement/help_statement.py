"""
HELP 语句（help statement）
"""

from metasequoia_sql.ast.base import Statement

__all__ = [
    "HelpStatement"
]


class HelpStatement(Statement):
    """
    HELP 语句的抽象语法树节点。

    语法规则：
        HELP 'search_string'
    """

    __slots__ = (
        "_search_string",
    )

    def __init__(self, search_string: str) -> None:
        """
        初始化 HELP 语句节点。

        Parameters
        ----------
        search_string : str
            要搜索的帮助主题
        """
        self._search_string = search_string

    @property
    def search_string(self) -> str:
        """
        获取要搜索的帮助主题。

        Returns
        -------
        str
            要搜索的帮助主题
        """
        return self._search_string
