"""
DO 语句（do statement）
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Statement

__all__ = [
    "DoStatement"
]


class DoStatement(Statement):
    """
    DO 语句的抽象语法树节点。

    语法规则：
        DO select_item_list
    """

    __slots__ = (
        "_expressions"
    )

    def __init__(self, expressions: List[Expression]) -> None:
        """
        初始化 DO 语句节点。

        Parameters
        ----------
        expressions : List[Expression]
            要执行的表达式列表
        """
        self._expressions = expressions

    @property
    def expressions(self) -> List[Expression]:
        """
        获取要执行的表达式列表。

        Returns
        -------
        List[Expression]
            要执行的表达式列表
        """
        return self._expressions 