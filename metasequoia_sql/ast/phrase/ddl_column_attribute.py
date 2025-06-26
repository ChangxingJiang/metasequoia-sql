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
        "_default_value",
    )

    def __init__(self, default_value: Expression):
        """
        初始化默认值属性。

        Parameters
        ----------
        default_value : Expression
            默认值表达式
        """
        self._default_value = default_value

    @property
    def default_value(self) -> Expression:
        """
        获取默认值表达式。

        Returns
        -------
        Expression
            默认值表达式
        """
        return self._default_value


class ColumnAttrDefaultExpression(ColumnAttribute):
    """DEFAULT ( expression )"""

    __slots__ = (
        "_default_expression",
    )

    def __init__(self, default_expression: Expression):
        """
        初始化默认表达式属性。

        Parameters
        ----------
        default_expression : Expression
            默认表达式
        """
        self._default_expression = default_expression

    @property
    def default_expression(self) -> Expression:
        """
        获取默认表达式。

        Returns
        -------
        Expression
            默认表达式
        """
        return self._default_expression


class ColumnAttrOnUpdate(ColumnAttribute):
    """ON UPDATE on_update_value"""

    __slots__ = (
        "_on_update_value",
    )

    def __init__(self, on_update_value: Expression):
        """
        初始化 ON UPDATE 属性。

        Parameters
        ----------
        on_update_value : Expression
            ON UPDATE 值表达式
        """
        self._on_update_value = on_update_value

    @property
    def on_update_expression(self) -> Expression:
        """
        获取 ON UPDATE 表达式。

        Returns
        -------
        Expression
            ON UPDATE 表达式
        """
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
        "_comment",
    )

    def __init__(self, comment: str):
        """
        初始化注释属性。

        Parameters
        ----------
        comment : str
            注释内容
        """
        self._comment = comment

    @property
    def comment(self) -> str:
        """
        获取注释内容。

        Returns
        -------
        str
            注释内容
        """
        return self._comment


class ColumnAttrCollate(ColumnAttribute):
    """COLLATE charset"""

    __slots__ = (
        "_charset",
    )

    def __init__(self, charset: "Charset"):
        """
        初始化字符集属性。

        Parameters
        ----------
        charset : Charset
            字符集
        """
        self._charset = charset

    @property
    def charset(self) -> "Charset":
        """
        获取字符集。

        Returns
        -------
        Charset
            字符集
        """
        return self._charset


class EnumColumnFormat(IntEnum):
    """DDL 字段存储格式"""

    DEFAULT = 1  # DEFAULT
    FIXED = 2  # FIXED
    DYNAMIC = 3  # DYNAMIC


class ColumnAttrColumnFormat(ColumnAttribute):
    """COLUMN_FORMAT column_format"""

    __slots__ = (
        "_format_column",
    )

    def __init__(self, column_format: EnumColumnFormat):
        """
        初始化列格式属性。

        Parameters
        ----------
        column_format : EnumColumnFormat
            列格式
        """
        self._format_column = column_format

    @property
    def format(self) -> EnumColumnFormat:
        """
        获取列格式。

        Returns
        -------
        EnumColumnFormat
            列格式
        """
        return self._format_column


class EnumStorageMedia(IntEnum):
    """字段存储介质"""

    DEFAULT = 1  # DEFAULT
    DISK = 2  # DISK
    MEMORY = 3  # MEMORY


class ColumnAttrStorageMedia(ColumnAttribute):
    """STORAGE_MEDIA storage_media"""

    __slots__ = (
        "_storage_media",
    )

    def __init__(self, storage_media: EnumStorageMedia):
        """
        初始化存储介质属性。

        Parameters
        ----------
        storage_media : EnumStorageMedia
            存储介质
        """
        self._storage_media = storage_media

    @property
    def storage_media(self) -> EnumStorageMedia:
        """
        获取存储介质。

        Returns
        -------
        EnumStorageMedia
            存储介质
        """
        return self._storage_media


class ColumnAttrSrid(ColumnAttribute):
    """SRID srid"""

    __slots__ = (
        "_srid",
    )

    def __init__(self, srid: int):
        """
        初始化 SRID 属性。

        Parameters
        ----------
        srid : int
            空间参考标识符
        """
        self._srid = srid

    @property
    def srid(self) -> int:
        """
        获取空间参考标识符。

        Returns
        -------
        int
            空间参考标识符
        """
        return self._srid


class ColumnAttrConstraint(ColumnAttribute):
    """CONSTRAINT constraint_name CHECK ( check_expression )"""

    __slots__ = (
        "_constraint_name",
        "_check_expression"
    )

    def __init__(self, constraint_name: str, check_expression: Expression):
        """
        初始化约束属性。

        Parameters
        ----------
        constraint_name : str
            约束名称
        check_expression : Expression
            检查表达式
        """
        self._constraint_name = constraint_name
        self._check_expression = check_expression

    @property
    def constraint_name(self) -> str:
        """
        获取约束名称。

        Returns
        -------
        str
            约束名称
        """
        return self._constraint_name

    @property
    def check_expression(self) -> Expression:
        """
        获取检查表达式。

        Returns
        -------
        Expression
            检查表达式
        """
        return self._check_expression


class ColumnAttrEnforced(ColumnAttribute):
    """ENFORCED"""


class ColumnAttrNotEnforced(ColumnAttribute):
    """NOT ENFORCED"""


class ColumnAttrEngineAttribute(ColumnAttribute):
    """ENGINE_ATTRIBUTE attribute"""

    __slots__ = (
        "_attribute",
    )

    def __init__(self, attribute: str):
        """
        初始化引擎属性。

        Parameters
        ----------
        attribute : str
            引擎属性值
        """
        self._attribute = attribute

    @property
    def attribute(self) -> str:
        """
        获取引擎属性值。

        Returns
        -------
        str
            引擎属性值
        """
        return self._attribute


class ColumnAttrSecondaryEngineAttribute(ColumnAttribute):
    """SECONDARY_ENGINE_ATTRIBUTE attribute"""

    __slots__ = (
        "_attribute",
    )

    def __init__(self, attribute: str):
        """
        初始化副引擎属性。

        Parameters
        ----------
        attribute : str
            副引擎属性值
        """
        self._attribute = attribute

    @property
    def attribute(self) -> str:
        """
        获取副引擎属性值。

        Returns
        -------
        str
            副引擎属性值
        """
        return self._attribute


class ColumnAttrVisible(ColumnAttribute):
    """VISIBLE"""


class ColumnAttrInvisible(ColumnAttribute):
    """INVISIBLE"""
