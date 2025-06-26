# pylint: disable=R0801

"""
CREATE VIEW 语句（create view statement）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.fixed_enum import EnumViewAlgorithmType, EnumViewSuidType, EnumViewCheckOption
    from metasequoia_sql.ast.basic.literal import UserName
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.statement.select_statement import QueryExpression

__all__ = [
    "CreateViewStatement"
]


class CreateViewStatement(Statement):
    # pylint: disable=R0902
    """CREATE VIEW 语句"""

    __slots__ = (
        "_replace",
        "_algorithm",
        "_definer",
        "_suid",
        "_table_ident",
        "_column_list",
        "_query_expression",
        "_check_option"
    )

    def __init__(self,
                 replace: bool,
                 algorithm: "EnumViewAlgorithmType",
                 definer: Optional["UserName"],
                 suid: "EnumViewSuidType",
                 table_ident: "Identifier",
                 column_list: List[str],
                 query_expression: "QueryExpression",
                 check_option: "EnumViewCheckOption"
                 ):
        # pylint: disable=R0913
        self._replace = replace
        self._algorithm = algorithm
        self._definer = definer
        self._suid = suid
        self._table_ident = table_ident
        self._column_list = column_list
        self._query_expression = query_expression
        self._check_option = check_option

    @property
    def replace(self) -> bool:
        """
        是否使用 REPLACE 选项

        Returns
        -------
        bool
            是否使用 REPLACE 选项
        """
        return self._replace

    @property
    def algorithm(self) -> "EnumViewAlgorithmType":
        """
        视图算法类型

        Returns
        -------
        EnumViewAlgorithmType
            视图算法类型
        """
        return self._algorithm

    @property
    def definer(self) -> Optional["UserName"]:
        """
        视图定义者

        Returns
        -------
        Optional["UserName"]
            视图定义者用户名
        """
        return self._definer

    @property
    def suid(self) -> "EnumViewSuidType":
        """
        视图 SUID 类型

        Returns
        -------
        EnumViewSuidType
            视图 SUID 类型
        """
        return self._suid

    @property
    def table_ident(self) -> "Identifier":
        """
        视图表标识符

        Returns
        -------
        Identifier
            视图表标识符
        """
        return self._table_ident

    @property
    def column_list(self) -> List[str]:
        """
        列名列表

        Returns
        -------
        List[str]
            列名列表
        """
        return self._column_list

    @property
    def query_expression(self) -> "QueryExpression":
        """
        查询表达式

        Returns
        -------
        QueryExpression
            查询表达式
        """
        return self._query_expression

    @property
    def check_option(self) -> "EnumViewCheckOption":
        """
        视图检查选项

        Returns
        -------
        EnumViewCheckOption
            视图检查选项
        """
        return self._check_option
