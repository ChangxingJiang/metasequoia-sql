"""
BEGIN 语句（begin statement）
"""

from metasequoia_sql.ast.base import Statement

__all__ = [
    "BeginStatement"
]


class BeginStatement(Statement):
    """
    BEGIN 语句的抽象语法树节点。

    语法规则：
        BEGIN [WORK]
    """
