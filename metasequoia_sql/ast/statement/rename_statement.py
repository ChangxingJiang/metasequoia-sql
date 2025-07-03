"""
重命名语句的抽象语法树节点。
"""

from typing import List, TYPE_CHECKING, Tuple

from metasequoia_sql.ast.base import Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.literal import UserName

__all__ = [
    "RenameStatement",
    "RenameTableStatement",
    "RenameUserStatement"
]


class RenameStatement(Statement):
    """`RENAME` 语句"""


class RenameTableStatement(RenameStatement):
    """
    重命名表语句的抽象语法树节点。

    语法规则：
        RENAME TABLE table_to_table_list
    """

    __slots__ = (
        "_table_pairs",
    )

    def __init__(self, table_pairs: List[Tuple["Identifier", "Identifier"]]) -> None:
        self._table_pairs = table_pairs

    @property
    def table_pairs(self) -> List[Tuple["Identifier", "Identifier"]]:
        """
        表重命名对列表

        Returns
        -------
        List[Tuple[Identifier, Identifier]]
            表重命名对列表
        """
        return self._table_pairs


class RenameUserStatement(RenameStatement):
    """
    重命名用户语句的抽象语法树节点。

    语法规则：
        RENAME USER rename_list
    """

    __slots__ = (
        "_user_pairs",
    )

    def __init__(self, user_pairs: List[Tuple["UserName", "UserName"]]) -> None:
        self._user_pairs = user_pairs

    @property
    def user_pairs(self) -> List[Tuple["UserName", "UserName"]]:
        """
        用户重命名对列表

        Returns
        -------
        List[Tuple[UserName, UserName]]
            用户重命名对列表
        """
        return self._user_pairs
