"""
SHUTDOWN 语句（shutdown statement）
"""

from metasequoia_sql.ast.base import Statement

__all__ = [
    "ShutdownStatement",
]


class ShutdownStatement(Statement):
    """SHUTDOWN 语句"""
