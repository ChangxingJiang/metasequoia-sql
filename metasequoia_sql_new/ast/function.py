"""
函数类型节点
"""

from metasequoia_sql_new.ast.base import UnaryExpression

__all__ = [
    "FuncNegative",
    "FuncBitNot",
]


class FuncNegative(UnaryExpression):
    """内置函数：取相反数（`-` 运算符）"""


class FuncBitNot(UnaryExpression):
    """内置函数：按位取反（`~` 运算符）"""
