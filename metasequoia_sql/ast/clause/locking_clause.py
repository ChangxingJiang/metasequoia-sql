"""
LOCKING 子句（locking clause）
"""

from enum import IntEnum
from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier

__all__ = [
    "LockStrength",
    "LockedRowAction",
    "LockingClause",
]


class LockStrength(IntEnum):
    """锁类型"""

    UPDATE = 1  # UPDATE（排他锁）
    SHARE = 2  # SHARE（共享锁）


class LockedRowAction(IntEnum):
    """锁的行行为"""

    WAIT = 1  # %empty
    SKIP_LOCKED = 2  # SKIP LOCKED
    NOWAIT = 3  # NOWAIT


class LockingClause(Node):
    """锁指定子句

    目前令 LOCK IN SHARE MODE 等价于 FOR SHARE
    """

    __slots__ = ["_lock_strength", "_table_list", "_locked_row_action"]

    def __init__(self, lock_strength: LockStrength, table_list: List["Identifier"], locked_row_action: LockedRowAction):
        self._lock_strength = lock_strength
        self._table_list = table_list
        self._locked_row_action = locked_row_action

    @property
    def lock_strength(self) -> LockStrength:
        return self._lock_strength

    @property
    def table_list(self) -> List["Identifier"]:
        return self._table_list

    @property
    def locked_row_action(self) -> LockedRowAction:
        return self._locked_row_action
