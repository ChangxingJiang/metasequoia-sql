"""
PREPARE 语句（prepare statement）
"""

from typing import TYPE_CHECKING, Union

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.literal import StringLiteral
    from metasequoia_sql.ast.basic.variable import UserVariable

__all__ = [
    "PrepareStatement"
]


class PrepareStatement(Statement):
    """
    PREPARE 语句的抽象语法树节点。

    语法规则：
        PREPARE statement_name FROM prepare_source
    """

    __slots__ = (
        "_statement_name",
        "_prepare_source"
    )

    def __init__(self, statement_name: str, prepare_source: Union["StringLiteral", "UserVariable"]) -> None:
        """
        初始化 PREPARE 语句节点。

        Parameters
        ----------
        statement_name : str
            预处理语句的名称
        prepare_source : Union[StringLiteral, UserVariable]
            预处理语句的源代码，可以是字符串字面值或用户变量
        """
        self._statement_name = statement_name
        self._prepare_source = prepare_source

    @property
    def statement_name(self) -> str:
        """
        获取预处理语句的名称。

        Returns
        -------
        Identifier
            预处理语句的名称
        """
        return self._statement_name

    @property
    def prepare_source(self) -> Union["StringLiteral", "UserVariable"]:
        """
        获取预处理语句的源代码。

        Returns
        -------
        Union[StringLiteral, UserVariable]
            预处理语句的源代码
        """
        return self._prepare_source
