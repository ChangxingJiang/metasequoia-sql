"""
DDL 表属性（ddl table option）
"""

from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import TableIdent
    from metasequoia_sql.ast.basic.charset_name import Charset

__all__ = [
    "TableOption",
    "TableStrOptionBase",
    "TableIntOptionBase",
    "TableExpressionOptionBase",
    "TableCharsetOptionBase",
    "TableOptionEngine",
    "TableOptionSecondaryEngine",
    "TableOptionMaxRows",
    "TableOptionMinRows",
    "TableOptionAvgRowLength",
    "TableOptionPassword",
    "TableOptionComment",
    "TableOptionCompression",
    "TableOptionEncryption",
    "TableOptionAutoIncrement",
    "TableOptionPackKey",
    "TableOptionStatsAutoRecalc",
    "TableOptionStatsPersistent",
    "TableOptionStatsSamplePages",
    "TableOptionChecksum",
    "TableOptionTableChecksum",
    "TableOptionDelayKeyWrite",
    "EnumRowFormat",
    "TableOptionRowFormat",
    "TableOptionUnion",
    "TableOptionDefaultCharset",
    "TableOptionDefaultCollate",
    "EnumMergeInsertType",
    "TableOptionInsertMethod",
    "TableOptionDataDirectory",
    "TableOptionIndexDirectory",
    "TableOptionTableSpace",
    "EnumStorageType",
    "TableOptionStorage",
    "TableOptionConnection",
    "TableOptionKeyBlockSize",
    "TableOptionStartTransaction",
    "TableOptionEngineAttribute",
    "TableOptionSecondaryEngineAttribute",
    "TableOptionAutoextendSize",
]


class TableOption(Node):
    """DDL 表属性"""


class TableStrOptionBase(TableOption):
    """字符串类型的 DDL 表属性"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: Optional[str]) -> None:
        self._value = value

    @property
    def value(self) -> Optional[str]:
        return self._value


class TableIntOptionBase(TableOption):
    """整数类型的 DDL 表属性"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: int) -> None:
        self._value = value

    @property
    def value(self) -> int:
        return self._value


class TableExpressionOptionBase(TableOption):
    """表达式类型的 DDL 表属性"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: Expression):
        self._value = value

    @property
    def value(self) -> Expression:
        return self._value


class TableCharsetOptionBase(TableOption):
    """字符集类型的 DDL 表属性"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: "Charset"):
        self._value = value

    @property
    def value(self) -> "Charset":
        return self._value


class TableOptionEngine(TableStrOptionBase):
    """DDL 表属性：ENGINE"""


class TableOptionSecondaryEngine(TableStrOptionBase):
    """DDL 表属性：SECONDARY_ENGINE"""


class TableOptionMaxRows(TableIntOptionBase):
    """DDL 表属性：MAX_ROWS"""


class TableOptionMinRows(TableIntOptionBase):
    """DDL 表属性：MIN_ROWS"""


class TableOptionAvgRowLength(TableIntOptionBase):
    """DDL 表属性：AVG_ROW_LENGTH"""


class TableOptionPassword(TableStrOptionBase):
    """DDL 表属性：PASSWORD"""


class TableOptionComment(TableStrOptionBase):
    """DDL 表属性：COMMENT"""


class TableOptionCompression(TableStrOptionBase):
    """DDL 表属性：COMPRESSION"""


class TableOptionEncryption(TableStrOptionBase):
    """DDL 表属性：ENCRYPTION"""


class TableOptionAutoIncrement(TableIntOptionBase):
    """DDL 表属性：AUTO_INCREMENT"""


class TableOptionPackKey(TableExpressionOptionBase):
    """DDL 表属性：PACK_KEY"""


class TableOptionStatsAutoRecalc(TableExpressionOptionBase):
    """DDL 表属性：STATS_AUTO_RECALC"""


class TableOptionStatsPersistent(TableIntOptionBase):
    """DDL 表属性：STATS_PERSISTENT"""


class TableOptionStatsSamplePages(TableExpressionOptionBase):
    """DDL 表属性：STATS_SAMPLE_PAGES"""


class TableOptionChecksum(TableIntOptionBase):
    """DDL 表属性：CHECKSUM"""


class TableOptionTableChecksum(TableIntOptionBase):
    """DDL 表属性：TABLE_CHECKSUM"""


class TableOptionDelayKeyWrite(TableIntOptionBase):
    """DDL 表属性：DELAY_KEY_WRITE"""


class EnumRowFormat(IntEnum):
    """行格式类型的枚举值"""

    DEFAULT = 0  # DEFAULT
    FIXED = 1  # FIXED
    DYNAMIC = 2  # DYNAMIC
    COMPRESSED = 3  # COMPRESSED
    REDUNDANT = 4  # REDUNDANT
    COMPACT = 5  # COMPACT


class TableOptionRowFormat(TableOption):
    """DDL 表属性：ROW_FORMAT"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: EnumRowFormat):
        self._value = value

    @property
    def value(self) -> EnumRowFormat:
        return self._value


class TableOptionUnion(TableOption):
    """DDL 表属性：UNION"""

    __slots__ = (
        "_table_list"
    )

    def __init__(self, table_list: List["TableIdent"]):
        self._table_list = table_list

    @property
    def table_list(self) -> List["TableIdent"]:
        return self._table_list


class TableOptionDefaultCharset(TableCharsetOptionBase):
    """DDL 表属性：DEFAULT CHARSET"""


class TableOptionDefaultCollate(TableCharsetOptionBase):
    """DDL 表属性：DEFAULT COLLATE"""


class EnumMergeInsertType(IntEnum):
    """向 MERGE 表插入数据的类型的枚举值"""

    NO = 1  # NO：不允许向 MERGE 表插入数据，尝试插入会报错
    FIRST = 2  # FIRST：将新记录插入到第一个底层的 MyISAM 表中
    LAST = 3  # LAST：将新记录插入到最后一个底层的 MyISAM 表中


class TableOptionInsertMethod(TableOption):
    """DDL 表属性：INSERT_METHOD"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: EnumMergeInsertType):
        self._value = value

    @property
    def value(self) -> EnumMergeInsertType:
        return self._value


class TableOptionDataDirectory(TableStrOptionBase):
    """DDL 表属性：DATA DIRECTORY"""


class TableOptionIndexDirectory(TableStrOptionBase):
    """DDL 表属性：INDEX DIRECTORY"""


class TableOptionTableSpace(TableStrOptionBase):
    """DDL 表属性：TABLESPACE"""


class EnumStorageType(IntEnum):
    """表的存储类型的枚举值"""

    DISK = 1  # DISK：使用磁盘存储
    MEMORY = 2  # MEMORY：使用内存存储


class TableOptionStorage(TableOption):
    """DDL 表属性：STORAGE"""

    __slots__ = (
        "_value"
    )

    def __init__(self, value: EnumStorageType):
        self._value = value

    @property
    def value(self) -> EnumStorageType:
        return self._value


class TableOptionConnection(TableStrOptionBase):
    """DDL 表属性：CONNECTION"""


class TableOptionKeyBlockSize(TableIntOptionBase):
    """DDL 表属性：KEY_BLOCK_SIZE"""


class TableOptionStartTransaction(TableOption):
    """DDL 表属性：START TRANSACTION"""


class TableOptionEngineAttribute(TableStrOptionBase):
    """DDL 表属性：ENGINE_ATTRIBUTE"""


class TableOptionSecondaryEngineAttribute(TableStrOptionBase):
    """DDL 表属性：SECONDARY_ENGINE_ATTRIBUTE"""


class TableOptionAutoextendSize(TableExpressionOptionBase):
    """DDL 表属性：AUTOEXTEND_SIZE"""
