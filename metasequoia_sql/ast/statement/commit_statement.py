"""
COMMIT 语句（commit statement）
"""

from typing import TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.fixed_enum import EnumChainType, EnumReleaseType

__all__ = [
    "CommitStatement",
]


class CommitStatement(Statement):
    """COMMIT 语句"""

    __slots__ = (
        "_chain_type",
        "_release_type",
    )

    def __init__(self, chain_type: "EnumChainType", release_type: "EnumReleaseType"):
        self._chain_type = chain_type
        self._release_type = release_type

    @property
    def chain_type(self) -> "EnumChainType":
        return self._chain_type

    @property
    def release_type(self) -> "EnumReleaseType":
        return self._release_type
