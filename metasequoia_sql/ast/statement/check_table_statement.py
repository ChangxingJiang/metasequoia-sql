"""
CHECK TABLE 语句（check table statement）
"""

from typing import List, TYPE_CHECKING

from metasequoia_sql.ast.base import Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.fixed_enum import EnumCheckType

__all__ = [
    "CheckTableStatement"
]


class CheckTableStatement(Node):
    """CHECK TABLE 语句"""

    __slots__ = (
        "_table_list",
        "_check_type"
    )

    def __init__(self, table_list: List["Identifier"], check_type: "EnumCheckType"):
        self._table_list = table_list
        self._check_type = check_type

    @property
    def table_list(self) -> List["Identifier"]:
        """
        表标识符列表

        Returns
        -------
        List["Identifier"]
            表标识符列表
        """
        return self._table_list

    @property
    def check_type(self) -> "EnumCheckType":
        """
        检查类型

        Returns
        -------
        EnumCheckType
            检查类型
        """
        return self._check_type
