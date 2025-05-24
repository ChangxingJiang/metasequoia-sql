"""
表达式相关抽象语法树节点
"""

from typing import List, Optional

from metasequoia_sql_new.ast.base import BinaryExpression, Expression

__all__ = [
    "UdfExpression",
    "OperatorCollate",
    "OperatorConcat",
    "Row",
    "OdbcDate",
]


class UdfExpression(Expression):
    """UDF 表达式"""

    def __init__(self, expression: Expression, alias: Optional[str]):
        self._expression = expression
        self._alias = alias

    def attr_list(self) -> List[str]:
        return ["expression", "alias"]

    @property
    def expression(self) -> Expression:
        return self._expression

    @property
    def alias(self) -> Optional[str]:
        return self._alias


class OperatorCollate(Expression):
    """内置 COLLATE 关键字运算符（指定排序规则）

    collation_operand COLLATE collation_name
    """

    def __init__(self, collation_operand: Expression, collation_name: str):
        self._collation_operand = collation_operand  # 需要指定排序规则的表达式
        self._collation_name = collation_name  # 排序规则名称

    def attr_list(self) -> List[str]:
        return ["collation_operand", "collation_name"]

    @property
    def collation_operand(self) -> Expression:
        return self._collation_operand

    @property
    def collation_name(self) -> str:
        return self._collation_name


class OperatorConcat(BinaryExpression):
    """内置 || 运算符（字符串合并）

    left_operand || right_operand
    """


class Row(Expression):
    """行表达式"""

    def __init__(self, value_list: List[Expression]):
        self._value_list = value_list

    def attr_list(self) -> List[str]:
        return ["value_list"]

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

    def attr_list(self) -> List[str]:
        return ["odbc_type", "odbc_value"]

    @property
    def odbc_type(self) -> str:
        return self._odbc_type

    @property
    def odbc_value(self) -> Expression:
        return self._odbc_value
