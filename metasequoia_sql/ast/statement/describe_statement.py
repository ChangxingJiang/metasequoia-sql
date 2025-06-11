"""
DESCRIBE 语句（describe statement）
"""

from typing import Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import TableIdent

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
                 table_name: "TableIdent",
                 describe_column: Optional[str]):
        self._table_name = table_name
        self._describe_column = describe_column

    @property
    def table_name(self) -> "TableIdent":
        return self._table_name

    @property
    def describe_column(self) -> Optional[str]:
        return self._describe_column
