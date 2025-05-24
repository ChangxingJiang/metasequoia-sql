"""
LIMIT 子句（limit clause）
"""

from typing import List, Optional

from metasequoia_sql.ast.base import Expression, Node

__all__ = [
    "LimitClause"
]


class LimitClause(Node):
    """LIMIT 子句"""

    def __init__(self, offset: Optional[Expression], limit: Expression):
        self._offset = offset
        self._limit = limit

    @property
    def offset(self) -> Optional[Expression]:
        return self._offset

    @property
    def limit(self) -> Expression:
        return self._limit
