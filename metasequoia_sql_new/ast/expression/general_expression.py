"""
表达式相关抽象语法树节点
"""

import typing

from metasequoia_sql_new.ast.base import Expression

__all__ = [
    "UdfExpression"
]


class UdfExpression(Expression):
    """UDF 表达式"""

    def __init__(self, expression: Expression, alias: typing.Optional[str]):
        self._expression = expression
        self._alias = alias

    def attr_list(self) -> typing.List[str]:
        return ["expression", "alias"]

    @property
    def expression(self) -> Expression:
        return self._expression

    @property
    def alias(self) -> typing.Optional[str]:
        return self._alias
