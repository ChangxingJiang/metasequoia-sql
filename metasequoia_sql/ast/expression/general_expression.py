"""
表达式相关抽象语法树节点
"""

from typing import List, Optional

from metasequoia_sql.ast.base import Expression

__all__ = [
    "UdfExpression",
    "Row",
    "OdbcDate",
]


class UdfExpression(Expression):
    """UDF 表达式"""

    def __init__(self, expression: Expression, alias: Optional[str]):
        self._expression = expression
        self._alias = alias

    @property
    def expression(self) -> Expression:
        return self._expression

    @property
    def alias(self) -> Optional[str]:
        return self._alias


class Row(Expression):
    """行表达式"""

    def __init__(self, value_list: List[Expression]):
        self._value_list = value_list

    @property
    def value_list(self) -> List[Expression]:
        return self._value_list


class OdbcDate(Expression):
    """ODBC 日期格式

    { odbc_type odbc_value }

    """

    def __init__(self, odbc_type: str, odbc_value: Expression):
        self._odbc_type = odbc_type
        self._odbc_value = odbc_value

    @property
    def odbc_type(self) -> str:
        return self._odbc_type

    @property
    def odbc_value(self) -> Expression:
        return self._odbc_value
