"""
其他场景下的近似表达式（app expression）
"""

from metasequoia_sql.ast.base import Expression

__all__ = [
    "OnExpression"
]


class OnExpression(Expression):
    """ON 关键字表达式

    适用于 INSTALL 语句中的等式之后
    """
