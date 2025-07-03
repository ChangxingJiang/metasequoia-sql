"""
KILL 语句（kill statement）
"""

from typing import TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.fixed_enum import EnumKillOptionType

__all__ = [
    "KillStatement",
]


class KillStatement(Statement):
    """KILL 语句"""

    __slots__ = (
        "_option_type",
        "_target_id",
    )

    def __init__(self, option_type: "EnumKillOptionType", target_id: Expression):
        self._option_type = option_type
        self._target_id = target_id

    @property
    def option_type(self) -> "EnumKillOptionType":
        """
        选项类型

        Returns
        -------
        EnumKillOptionType
            选项类型
        """
        return self._option_type

    @property
    def target_id(self) -> Expression:
        """
        目标 ID

        Returns
        -------
        Expression
            目标 ID
        """
        return self._target_id
