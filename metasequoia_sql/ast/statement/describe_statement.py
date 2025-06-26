"""
DESCRIBE 语句（describe statement）
"""

from typing import Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier

__all__ = [
    "DescribeStatement"
]


class DescribeStatement(Statement):
    """`DESCRIBE` 语句"""

    __slots__ = (
        "_table_name",
        "_describe_column"
    )

    def __init__(self,
                 table_name: "Identifier",
                 describe_column: Optional[str]):
        self._table_name = table_name
        self._describe_column = describe_column

    @property
    def table_name(self) -> "Identifier":
        """
        表名标识符

        Returns
        -------
        Identifier
            表名标识符
        """
        return self._table_name

    @property
    def describe_column(self) -> Optional[str]:
        """
        描述的列名

        Returns
        -------
        Optional[str]
            描述的列名
        """
        return self._describe_column
