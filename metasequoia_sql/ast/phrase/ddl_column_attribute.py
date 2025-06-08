"""
DDL 字段属性（ddl column attribute）
"""

from enum import IntEnum
from typing import TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.charset_name import Charset


__all__ = [
    "ColumnAttribute",
    "ColumnAttrNull",
    "ColumnAttrNotNull",
    "ColumnAttrNotSecondary",
    "ColumnAttrDefaultValue",
    "ColumnAttrDefaultExpression",
    "ColumnAttrOnUpdate",
    "ColumnAttrAutoIncrement",
    "ColumnAttrSerialDefaultValue",
    "ColumnAttrPrimaryKey",
    "ColumnAttrKey",
    "ColumnAttrUnique",
    "ColumnAttrUniqueKey",
    "ColumnAttrComment",
    "ColumnAttrCollate",
    "ColumnAttrColumnFormat",
    "ColumnAttrStorageMedia",
    "ColumnAttrSrid",
    "ColumnAttrConstraint",
    "ColumnAttrEnforced",
    "ColumnAttrNotEnforced",
    "ColumnAttrEngineAttribute",
    "ColumnAttrSecondaryEngineAttribute",
    "ColumnAttrVisible",
    "ColumnAttrInvisible",
    "EnumColumnFormat",
    "EnumStorageMedia"
]


class ColumnAttribute(Node):
    """DDL 字段属性"""


class ColumnAttrNull(ColumnAttribute):
    """NULL"""


class ColumnAttrNotNull(ColumnAttribute):
    """NOT NULL"""


class ColumnAttrNotSecondary(ColumnAttribute):
    """NOT SECONDARY"""


class ColumnAttrDefaultValue(ColumnAttribute):
    """DEFAULT default_value"""

    __slots__ = (
        "_default_value"
    )

    def __init__(self, default_value: Expression):
        self._default_value = default_value

    @property
    def default_value(self) -> Expression:
        return self._default_value


class ColumnAttrDefaultExpression(ColumnAttribute):
    """DEFAULT ( expression )"""

    __slots__ = (
        "_default_expression"
    )

    def __init__(self, default_expression: Expression):
        self._default_expression = default_expression

    @property
    def default_expression(self) -> Expression:
        return self._default_expression


class ColumnAttrOnUpdate(ColumnAttribute):
    """ON UPDATE on_update_value"""

    __slots__ = (
        "_on_update_value"
    )

    def __init__(self, on_update_value: Expression):
        self._on_update_value = on_update_value

    @property
    def on_update_expression(self) -> Expression:
        return self._on_update_value


class ColumnAttrAutoIncrement(ColumnAttribute):
    """AUTO INCREMENT"""


class ColumnAttrSerialDefaultValue(ColumnAttribute):
    """SERIAL DEFAULT VALUE"""


class ColumnAttrPrimaryKey(ColumnAttribute):
    """PRIMARY KEY"""


class ColumnAttrKey(ColumnAttribute):
    """KEY"""


class ColumnAttrUnique(ColumnAttribute):
    """UNIQUE"""


class ColumnAttrUniqueKey(ColumnAttribute):
    """UNIQUE KEY"""


class ColumnAttrComment(ColumnAttribute):
    """COMMENT 'comment'"""

    __slots__ = (
        "_comment"
    )

    def __init__(self, comment: str):
        self._comment = comment

    @property
    def comment(self) -> str:
        return self._comment


class ColumnAttrCollate(ColumnAttribute):
    """COLLATE charset"""

    __slots__ = (
        "_charset"
    )

    def __init__(self, charset: "Charset"):
        self._charset = charset

    @property
    def charset(self) -> "Charset":
        return self._charset


class EnumColumnFormat(IntEnum):
    """DDL 字段存储格式"""

    DEFAULT = 1  # DEFAULT
    FIXED = 2  # FIXED
    DYNAMIC = 3  # DYNAMIC


class ColumnAttrColumnFormat(ColumnAttribute):
    """COLUMN_FORMAT column_format"""

    __slots__ = (
        "_format_column"
    )

    def __init__(self, column_format: EnumColumnFormat):
        self._format_column = column_format

    @property
    def format(self) -> EnumColumnFormat:
        return self._format_column


class EnumStorageMedia(IntEnum):
    """字段存储介质"""

    DEFAULT = 1  # DEFAULT
    DISK = 2  # DISK
    MEMORY = 3  # MEMORY


class ColumnAttrStorageMedia(ColumnAttribute):
    """STORAGE_MEDIA storage_media"""

    __slots__ = (
        "_storage_media"
    )

    def __init__(self, storage_media: EnumStorageMedia):
        self._storage_media = storage_media

    @property
    def storage_media(self) -> EnumStorageMedia:
        return self._storage_media


class ColumnAttrSrid(ColumnAttribute):
    """SRID srid"""

    __slots__ = (
        "_srid"
    )

    def __init__(self, srid: int):
        self._srid = srid

    @property
    def srid(self) -> int:
        return self._srid


class ColumnAttrConstraint(ColumnAttribute):
    """CONSTRAINT constraint_name CHECK ( check_expression )"""

    __slots__ = (
        "_constraint_name",
        "_check_expression"
    )

    def __init__(self, constraint_name: str, check_expression: Expression):
        self._constraint_name = constraint_name
        self._check_expression = check_expression

    @property
    def constraint_name(self) -> str:
        return self._constraint_name

    @property
    def check_expression(self) -> Expression:
        return self._check_expression


class ColumnAttrEnforced(ColumnAttribute):
    """ENFORCED"""


class ColumnAttrNotEnforced(ColumnAttribute):
    """NOT ENFORCED"""


class ColumnAttrEngineAttribute(ColumnAttribute):
    """ENGINE_ATTRIBUTE attribute"""

    __slots__ = (
        "_attribute"
    )

    def __init__(self, attribute: str):
        self._attribute = attribute

    @property
    def attribute(self) -> str:
        return self._attribute


class ColumnAttrSecondaryEngineAttribute(ColumnAttribute):
    """SECONDARY_ENGINE_ATTRIBUTE attribute"""

    __slots__ = (
        "_attribute"
    )

    def __init__(self, attribute: str):
        self._attribute = attribute

    @property
    def attribute(self) -> str:
        return self._attribute


class ColumnAttrVisible(ColumnAttribute):
    """VISIBLE"""


class ColumnAttrInvisible(ColumnAttribute):
    """INVISIBLE"""
