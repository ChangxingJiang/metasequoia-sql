"""
表达式相关抽象语法树节点
"""

from typing import List, Optional

from metasequoia_sql.ast.base import Expression, Node

__all__ = [
    "UdfExpression",
    "Row",
    "OdbcDate",
    "WhenItem",
    "Case",
    "TableWild",
    "ExpressionWithAlias",
    "Wild",
]


class UdfExpression(Expression):
    """UDF 表达式"""

    __slots__ = ["_expression", "_alias"]

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

    __slots__ = ["_value_list"]

    def __init__(self, value_list: List[Expression]):
        self._value_list = value_list

    @property
    def value_list(self) -> List[Expression]:
        return self._value_list


class OdbcDate(Expression):
    """ODBC 日期格式

    { odbc_type odbc_value }
    """

    __slots__ = ["_odbc_type", "_odbc_value"]

    def __init__(self, odbc_type: str, odbc_value: Expression):
        self._odbc_type = odbc_type
        self._odbc_value = odbc_value

    @property
    def odbc_type(self) -> str:
        return self._odbc_type

    @property
    def odbc_value(self) -> Expression:
        return self._odbc_value


class WhenItem(Node):
    """CASE 结构中 WHEN 条件"""

    __slots__ = ["_condition", "_expression"]

    def __init__(self, condition: Expression, expression: Expression):
        self._condition = condition
        self._expression = expression

    @property
    def condition(self) -> Expression:
        return self._condition

    @property
    def expression(self) -> Expression:
        return self._expression


class Case(Expression):
    """CASE 结构"""

    __slots__ = ["_case_expression", "_when_list", "_else_expression"]

    def __init__(self, case_expression: Expression, when_list: List[WhenItem], else_expression: Expression):
        self._case_expression = case_expression
        self._when_list = when_list
        self._else_expression = else_expression

    @property
    def case_expression(self) -> Expression:
        return self._case_expression

    @property
    def when_list(self) -> List[WhenItem]:
        return self._when_list

    @property
    def else_expression(self) -> Expression:
        return self._else_expression


class TableWild(Expression):
    """表中所有字段的通配符

    table_name.*
    schema_name.table_name.*
    """

    __slots__ = ["_schema_name", "_table_name"]

    def __init__(self, schema_name: Optional[str], table_name: str):
        self._schema_name = schema_name
        self._table_name = table_name

    @property
    def schema_name(self) -> Optional[str]:
        return self._schema_name

    @property
    def table_name(self) -> Optional[str]:
        return self._table_name


class ExpressionWithAlias(Expression):
    """包含别名的表达式"""

    __slots__ = ["_expression", "_alias"]

    def __init__(self, expression: Expression, alias: Optional[str]):
        self._expression = expression
        self._alias = alias

    @property
    def expression(self) -> Expression:
        return self._expression

    @property
    def alias(self) -> Optional[str]:
        return self._alias


class Wild(Expression):
    """通配符"""
