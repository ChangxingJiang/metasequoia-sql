"""
LIMIT 子句（limit clause）
"""

from typing import Optional

from metasequoia_sql.ast.base import Expression, Node

__all__ = [
    "LimitClause"
]


class LimitClause(Node):
    """LIMIT 子句"""

    __slots__ = ["_offset", "_limit"]

    def __init__(self, offset: Optional[Expression], limit: Expression):
        """初始化 LIMIT 子句
        
        Parameters
        ----------
        offset : Optional[Expression]
            偏移量表达式
        limit : Expression
            限制数量表达式
        """
        self._offset = offset
        self._limit = limit

    @property
    def offset(self) -> Optional[Expression]:
        """获取偏移量表达式
        
        Returns
        -------
        Optional[Expression]
            偏移量表达式
        """
        return self._offset

    @property
    def limit(self) -> Expression:
        """获取限制数量表达式
        
        Returns
        -------
        Expression
            限制数量表达式
        """
        return self._limit
