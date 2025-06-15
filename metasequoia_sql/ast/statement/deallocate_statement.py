"""
DEALLOCATE 语句（deallocate statement）
"""

from typing import TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier

__all__ = [
    "DeallocateStatement"
]


class DeallocateStatement(Statement):
    """
    DEALLOCATE 语句的抽象语法树节点。

    语法规则：
        DEALLOCATE PREPARE statement_name
        DROP PREPARE statement_name
    """

    __slots__ = (
        "_statement_name"
    )

    def __init__(self, statement_name: str) -> None:
        """
        初始化 DEALLOCATE 语句节点。

        Parameters
        ----------
        statement_name : Identifier
            要释放的预处理语句的名称
        """
        self._statement_name = statement_name

    @property
    def statement_name(self) -> str:
        """
        获取要释放的预处理语句的名称。

        Returns
        -------
        Identifier
            要释放的预处理语句的名称
        """
        return self._statement_name
