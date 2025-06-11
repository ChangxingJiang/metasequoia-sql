"""
SHOW 语句（show statement）
"""

from metasequoia_sql.ast.base import Statement

__all__ = [
    "ShowBinaryLogStatusStatement"
]


class ShowBinaryLogStatusStatement(Statement):
    """SHOW BINARY LOG STATUS 语句"""
