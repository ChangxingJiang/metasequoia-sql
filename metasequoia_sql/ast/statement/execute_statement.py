"""
EXECUTE 语句（execute statement）
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.variable import UserVariable

__all__ = [
    "ExecuteStatement"
]


class ExecuteStatement(Statement):
    """
    EXECUTE 语句的抽象语法树节点。

    语法规则：
        EXECUTE statement_name [USING variable_list]
    """

    __slots__ = (
        "_statement_name",
        "_using_variables"
    )

    def __init__(self, statement_name: str, using_variables: List["UserVariable"]) -> None:
        """
        初始化 EXECUTE 语句节点。

        Parameters
        ----------
        statement_name : str
            要执行的预处理语句的名称
        using_variables : List["UserVariable"]
            USING 子句中的变量列表
        """
        self._statement_name = statement_name
        self._using_variables = using_variables

    @property
    def statement_name(self) -> str:
        """
        获取要执行的预处理语句的名称。

        Returns
        -------
        Identifier
            要执行的预处理语句的名称
        """
        return self._statement_name

    @property
    def using_variables(self) -> List["UserVariable"]:
        """
        获取 USING 子句中的变量列表。

        Returns
        -------
        List["UserVariable"]
            USING 子句中的变量列表，如果没有 USING 子句则为 None
        """
        return self._using_variables
