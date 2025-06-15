"""
RESTART 语句（restart statement）
"""

from metasequoia_sql.ast.base import Statement

__all__ = [
    "RestartStatement",
]


class RestartStatement(Statement):
    """RESTART 语句"""
