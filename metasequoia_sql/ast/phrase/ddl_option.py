"""
DDL 选项（ddl option）
"""

from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier
    from metasequoia_sql.ast.basic.charset_name import Charset

__all__ = [
    "DdlOption",
    "DdlStrOptionBase",
    "DdlIntOptionBase",
    "DdlExpressionOptionBase",
    "DdlCharsetOptionBase",
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
    "EnumRowFormat",
    "DdlOptionRowFormat",
    "DdlOptionUnion",
    "DdlOptionDefaultCharset",
    "DdlOptionDefaultCollate",
    "EnumMergeInsertType",
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


class EnumRowFormat(IntEnum):
    """行格式类型的枚举值"""

    DEFAULT = 0  # DEFAULT
    FIXED = 1  # FIXED
    DYNAMIC = 2  # DYNAMIC
    COMPRESSED = 3  # COMPRESSED
    REDUNDANT = 4  # REDUNDANT
    COMPACT = 5  # COMPACT


class DdlOptionRowFormat(DdlOption):
    """DDL 选项：ROW_FORMAT（表属性）"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: EnumRowFormat):
        self._value = value

    @property
    def value(self) -> EnumRowFormat:
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


class EnumMergeInsertType(IntEnum):
    """向 MERGE 表插入数据的类型的枚举值"""

    NO = 1  # NO：不允许向 MERGE 表插入数据，尝试插入会报错
    FIRST = 2  # FIRST：将新记录插入到第一个底层的 MyISAM 表中
    LAST = 3  # LAST：将新记录插入到最后一个底层的 MyISAM 表中


class DdlOptionInsertMethod(DdlOption):
    """DDL 选项：INSERT_METHOD（表属性）"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: EnumMergeInsertType):
        self._value = value

    @property
    def value(self) -> EnumMergeInsertType:
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
