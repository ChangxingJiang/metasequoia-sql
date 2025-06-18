"""
DDL 选项（ddl option）
"""

from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.charset_name import Charset
    from metasequoia_sql.ast.basic.fixed_enum import EnumRowFormatType, EnumMergeInsertType

__all__ = [
    # DDL 选项的抽象基类
    "DdlOption",

    # DDL 选项的指定类型变量的基类
    "DdlStrOptionBase",
    "DdlIntOptionBase",
    "DdlExpressionOptionBase",
    "DdlCharsetOptionBase",
    "DdlBoolOptionBase",

    # DDL 选项的具体类型
    "DdlOptionEngine",
    "DdlOptionSecondaryEngine",
    "DdlOptionMaxRows",
    "DdlOptionMinRows",
    "DdlOptionAvgRowLength",
    "DdlOptionPassword",
    "DdlOptionComment",
    "DdlOptionCompression",
    "DdlOptionEncryption",
    "DdlOptionAutoIncrement",
    "DdlOptionPackKey",
    "DdlOptionStatsAutoRecalc",
    "DdlOptionStatsPersistent",
    "DdlOptionStatsSamplePages",
    "DdlOptionChecksum",
    "DdlOptionTableChecksum",
    "DdlOptionDelayKeyWrite",
    "DdlOptionRowFormat",
    "DdlOptionUnion",
    "DdlOptionDefaultCharset",
    "DdlOptionDefaultCollate",
    "DdlOptionDefaultEncryption",
    "DdlOptionReadOnly",
    "DdlOptionInsertMethod",
    "DdlOptionDataDirectory",
    "DdlOptionIndexDirectory",
    "DdlOptionTableSpace",
    "EnumStorageType",
    "DdlOptionStorage",
    "DdlOptionConnection",
    "DdlOptionKeyBlockSize",
    "DdlOptionStartTransaction",
    "DdlOptionEngineAttribute",
    "DdlOptionSecondaryEngineAttribute",
    "DdlOptionAutoextendSize",
    "DdlOptionStorageEngine",
    "DdlOptionWait",
    "DdlOptionInitialSize",
    "DdlOptionMaxSize",
    "DdlOptionTablespaceEncryption",
    "DdlOptionTablespaceEngineAttribute",
]


class DdlOption(Node):
    """DDL 选项"""


class DdlStrOptionBase(DdlOption):
    """字符串类型的 DDL 选项"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: Optional[str]) -> None:
        self._value = value

    @property
    def value(self) -> Optional[str]:
        return self._value


class DdlIntOptionBase(DdlOption):
    """整数类型的 DDL 选项"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: int) -> None:
        self._value = value

    @property
    def value(self) -> int:
        return self._value


class DdlExpressionOptionBase(DdlOption):
    """表达式类型的 DDL 选项"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: Expression):
        self._value = value

    @property
    def value(self) -> Expression:
        return self._value


class DdlCharsetOptionBase(DdlOption):
    """字符集类型的 DDL 选项"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: "Charset"):
        self._value = value

    @property
    def value(self) -> "Charset":
        return self._value


class DdlBoolOptionBase(DdlOption):
    """布尔值类型的 DDL 选项"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: bool):
        self._value = value

    @property
    def value(self) -> bool:
        return self._value


class DdlOptionEngine(DdlStrOptionBase):
    """DDL 选项：ENGINE（表属性）"""


class DdlOptionSecondaryEngine(DdlStrOptionBase):
    """DDL 选项：SECONDARY_ENGINE（表属性）"""


class DdlOptionMaxRows(DdlIntOptionBase):
    """DDL 选项：MAX_ROWS（表属性）"""


class DdlOptionMinRows(DdlIntOptionBase):
    """DDL 选项：MIN_ROWS（表属性）"""


class DdlOptionAvgRowLength(DdlIntOptionBase):
    """DDL 选项：AVG_ROW_LENGTH（表属性）"""


class DdlOptionPassword(DdlStrOptionBase):
    """DDL 选项：PASSWORD（表属性）"""


class DdlOptionComment(DdlStrOptionBase):
    """DDL 选项：COMMENT（表属性）"""


class DdlOptionCompression(DdlStrOptionBase):
    """DDL 选项：COMPRESSION（表属性）"""


class DdlOptionEncryption(DdlStrOptionBase):
    """DDL 选项：ENCRYPTION（表属性）"""


class DdlOptionAutoIncrement(DdlIntOptionBase):
    """DDL 选项：AUTO_INCREMENT（表属性）"""


class DdlOptionPackKey(DdlExpressionOptionBase):
    """DDL 选项：PACK_KEY（表属性）"""


class DdlOptionStatsAutoRecalc(DdlExpressionOptionBase):
    """DDL 选项：STATS_AUTO_RECALC（表属性）"""


class DdlOptionStatsPersistent(DdlIntOptionBase):
    """DDL 选项：STATS_PERSISTENT（表属性）"""


class DdlOptionStatsSamplePages(DdlExpressionOptionBase):
    """DDL 选项：STATS_SAMPLE_PAGES（表属性）"""


class DdlOptionChecksum(DdlIntOptionBase):
    """DDL 选项：CHECKSUM（表属性）"""


class DdlOptionTableChecksum(DdlIntOptionBase):
    """DDL 选项：TABLE_CHECKSUM（表属性）"""


class DdlOptionDelayKeyWrite(DdlIntOptionBase):
    """DDL 选项：DELAY_KEY_WRITE"""


class DdlOptionRowFormat(DdlOption):
    """DDL 选项：ROW_FORMAT（表属性）"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: "EnumRowFormatType"):
        self._value = value

    @property
    def value(self) -> "EnumRowFormatType":
        return self._value


class DdlOptionUnion(DdlOption):
    """DDL 选项：UNION（表属性）"""

    __slots__ = (
        "_table_list"
    )

    def __init__(self, table_list: List["Identifier"]):
        self._table_list = table_list

    @property
    def table_list(self) -> List["Identifier"]:
        return self._table_list


class DdlOptionDefaultCharset(DdlCharsetOptionBase):
    """DDL 选项：DEFAULT CHARSET（表属性或数据库属性）"""


class DdlOptionDefaultCollate(DdlCharsetOptionBase):
    """DDL 选项：DEFAULT COLLATE（表属性或数据库属性）"""


class DdlOptionDefaultEncryption(DdlStrOptionBase):
    """DDL 选项：DEFAULT ENCRYPTION（数据库属性）"""


class DdlOptionReadOnly(DdlOption):
    """DDL 选项：READ ONLY（数据库属性）"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: Expression):
        self._value = value

    @property
    def value(self) -> Expression:
        return self._value


class DdlOptionInsertMethod(DdlOption):
    """DDL 选项：INSERT_METHOD（表属性）"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: "EnumMergeInsertType"):
        self._value = value

    @property
    def value(self) -> "EnumMergeInsertType":
        return self._value


class DdlOptionDataDirectory(DdlStrOptionBase):
    """DDL 选项：DATA DIRECTORY（表属性）"""


class DdlOptionIndexDirectory(DdlStrOptionBase):
    """DDL 选项：INDEX DIRECTORY（表属性）"""


class DdlOptionTableSpace(DdlStrOptionBase):
    """DDL 选项：TABLESPACE（表属性）"""


class EnumStorageType(IntEnum):
    """表的存储类型的枚举值"""

    DISK = 1  # DISK：使用磁盘存储
    MEMORY = 2  # MEMORY：使用内存存储


class DdlOptionStorage(DdlOption):
    """DDL 选项：STORAGE（表属性）"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: EnumStorageType):
        self._value = value

    @property
    def value(self) -> EnumStorageType:
        return self._value


class DdlOptionConnection(DdlStrOptionBase):
    """DDL 选项：CONNECTION（表属性）"""


class DdlOptionKeyBlockSize(DdlIntOptionBase):
    """DDL 选项：KEY_BLOCK_SIZE（表属性）"""


class DdlOptionStartTransaction(DdlOption):
    """DDL 选项：START TRANSACTION（表属性）"""


class DdlOptionEngineAttribute(DdlStrOptionBase):
    """DDL 选项：ENGINE_ATTRIBUTE（表属性）"""


class DdlOptionSecondaryEngineAttribute(DdlStrOptionBase):
    """DDL 选项：SECONDARY_ENGINE_ATTRIBUTE（表属性）"""


class DdlOptionAutoextendSize(DdlExpressionOptionBase):
    """DDL 选项：AUTOEXTEND_SIZE（表属性）"""


class DdlOptionStorageEngine(DdlStrOptionBase):
    """DDL 选项：[Storage] ENGINE（TableSpace 属性）"""


class DdlOptionWait(DdlBoolOptionBase):
    """DDL 选项：WAIT 或 NO_WAIT"""


class DdlOptionInitialSize(DdlExpressionOptionBase):
    """DDL 选项：INITIAL_SIZE（表空间属性）"""


class DdlOptionMaxSize(DdlExpressionOptionBase):
    """DDL 选项：MAX_SIZE（表空间属性）"""


class DdlOptionTablespaceEncryption(DdlStrOptionBase):
    """DDL 选项：ENCRYPTION（表空间属性）"""


class DdlOptionTablespaceEngineAttribute(DdlStrOptionBase):
    """DDL 选项：ENGINE_ATTRIBUTE（表空间属性）"""
