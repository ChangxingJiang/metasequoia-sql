"""
ALTER VIEW 语句（alter view statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.fixed_enum import EnumViewAlgorithmType, EnumViewSuidType, EnumViewCheckOption
    from metasequoia_sql.ast.basic.literal import UserName
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.statement.select_statement import QueryExpression

__all__ = [
    "AlterViewStatement"
]


class AlterViewStatement(Statement):
    """ALTER VIEW 语句"""

    __slots__ = (
        "_algorithm",
        "_definer",
        "_suid",
        "_table_ident",
        "_column_list",
        "_query_expression",
        "_check_option"
    )

    def __init__(self,
                 algorithm: "EnumViewAlgorithmType",
                 definer: Optional["UserName"],
                 suid: "EnumViewSuidType",
                 table_ident: "Identifier",
                 column_list: List[str],
                 query_expression: "QueryExpression",
                 check_option: "EnumViewCheckOption"
                 ):
        self._algorithm = algorithm
        self._definer = definer
        self._suid = suid
        self._table_ident = table_ident
        self._column_list = column_list
        self._query_expression = query_expression
        self._check_option = check_option

    @property
    def algorithm(self) -> "EnumViewAlgorithmType":
        return self._algorithm

    @property
    def definer(self) -> Optional["UserName"]:
        return self._definer

    @property
    def suid(self) -> "EnumViewSuidType":
        return self._suid

    @property
    def table_ident(self) -> "Identifier":
        return self._table_ident

    @property
    def column_list(self) -> List[str]:
        return self._column_list

    @property
    def query_expression(self) -> "QueryExpression":
        return self._query_expression

    @property
    def check_option(self) -> "EnumViewCheckOption":
        return self._check_option
