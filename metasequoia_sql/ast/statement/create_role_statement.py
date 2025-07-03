"""
CREATE ROLE 语句（create role statement）
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.literal import RoleName

__all__ = [
    "CreateRoleStatement",
]


class CreateRoleStatement(Statement):
    """CREATE ROLE 语句"""

    __slots__ = (
        "_if_not_exists",
        "_role_list",
    )

    def __init__(self, if_not_exists: bool, role_list: List["RoleName"]):
        self._if_not_exists = if_not_exists
        self._role_list = role_list

    @property
    def if_not_exists(self) -> bool:
        """
        是否使用 IF NOT EXISTS 选项

        Returns
        -------
        bool
            是否使用 IF NOT EXISTS 选项
        """
        return self._if_not_exists

    @property
    def role_list(self) -> List["RoleName"]:
        """
        角色名称列表

        Returns
        -------
        List["RoleName"]
            角色名称列表
        """
        return self._role_list
