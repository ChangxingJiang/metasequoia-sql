"""
CHECKSUM 语句（checksum statement）
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.fixed_enum import EnumChecksumType

__all__ = [
    "ChecksumStatement",
]


class ChecksumStatement(Statement):
    """CHECKSUM 语句"""

    __slots__ = (
        "_table_list",
        "_checksum_type"
    )

    def __init__(self, table_list: List["Identifier"], checksum_type: "EnumChecksumType"):
        self._table_list = table_list
        self._checksum_type = checksum_type

    @property
    def table_list(self) -> List["Identifier"]:
        return self._table_list

    @property
    def checksum_type(self) -> "EnumChecksumType":
        return self._checksum_type
