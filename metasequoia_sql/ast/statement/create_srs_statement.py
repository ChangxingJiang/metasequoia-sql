"""
CREATE SRS 语句（create srs statement）
"""

from enum import Enum
from typing import Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Node, Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.literal import IntLiteral

__all__ = [
    "SrsAttributeType",
    "SrsAttribute",
    "CreateSrsStatement",
]


class SrsAttributeType(Enum):
    """SRS属性类型"""

    NAME = "NAME"
    DEFINITION = "DEFINITION"
    ORGANIZATION = "ORGANIZATION"
    DESCRIPTION = "DESCRIPTION"


class SrsAttribute(Node):
    """SRS属性节点"""

    __slots__ = ["_attribute_type", "_value", "_organization_coordsys_id"]

    def __init__(self,
                 attribute_type: SrsAttributeType,
                 value: str,
                 organization_coordsys_id: Optional[int] = None):
        self._attribute_type = attribute_type
        self._value = value
        self._organization_coordsys_id = organization_coordsys_id

    @property
    def attribute_type(self) -> SrsAttributeType:
        """
        SRS 属性类型

        Returns
        -------
        SrsAttributeType
            SRS 属性类型
        """
        return self._attribute_type

    @property
    def value(self) -> str:
        """
        属性值

        Returns
        -------
        str
            属性值
        """
        return self._value

    @property
    def organization_coordsys_id(self) -> Optional[int]:
        """
        组织坐标系 ID

        Returns
        -------
        Optional[int]
            组织坐标系 ID
        """
        return self._organization_coordsys_id


class CreateSrsStatement(Statement):
    """CREATE SRS 语句"""

    __slots__ = ["_srid", "_attributes", "_or_replace", "_if_not_exists"]

    def __init__(self,
                 srid: int,
                 attributes: list[SrsAttribute],
                 or_replace: bool,
                 if_not_exists: bool):
        self._srid = srid
        self._attributes = attributes
        self._or_replace = or_replace
        self._if_not_exists = if_not_exists

    @property
    def srid(self) -> int:
        """
        空间参考系标识符

        Returns
        -------
        int
            空间参考系标识符
        """
        return self._srid

    @property
    def attributes(self) -> list[SrsAttribute]:
        """
        SRS 属性列表

        Returns
        -------
        list[SrsAttribute]
            SRS 属性列表
        """
        return self._attributes

    @property
    def or_replace(self) -> bool:
        """
        是否使用 OR REPLACE 选项

        Returns
        -------
        bool
            是否使用 OR REPLACE 选项
        """
        return self._or_replace

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
