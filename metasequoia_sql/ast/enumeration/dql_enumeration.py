"""
DQL 语句中的枚举类型
"""

from enum import IntEnum, IntFlag

__all__ = [
    # 比较运算符
    "EnumCompareOperator",

    # 全文本索引选项
    "EnumFulltextOption",

    # 窗口函数的窗口方向选项
    "EnumFromFirstOrLastOption",

    # 窗口函数的空值处理选项
    "EnumNullTreatmentOption",

    # 排序方向类型
    "EnumOrderDirectionType",
]


class EnumCompareOperator(IntEnum):
    """比较运算符的枚举类"""

    EQ = 1  # =
    EQUAL = 2  # <=>
    GE = 3  # >=
    GT = 4  # >
    LE = 5  # <=
    LT = 6  # <
    NE = 7  # <> 或 !=


class EnumFulltextOption(IntFlag):
    """全文本索引选项"""

    DEFAULT = 0  # %empty
    IN_NATURAL_LANGUAGE_MODE = 1  # IN NATURAL LANGUAGE MODE
    WITH_QUERY_EXPANSION = 2  # WITH QUERY EXPANSION
    IN_BOOLEAN_MODE = 4  # IN BOOLEAN MODE


class EnumFromFirstOrLastOption(IntEnum):
    """窗口函数的窗口方向选项

    `NTH_VALUE` 窗口函数中指定窗口方向的 `FROM` 子句
    """

    NONE = 0  # %empty
    FROM_FIRST = 1  # FROM FIRST
    FROM_LAST = 2  # FROM LAST


class EnumNullTreatmentOption(IntEnum):
    """窗口函数的空值处理选项

    窗口函数中指定 `NULL` 值处理策略的 `RESPECT NULLS` 或 `IGNORE NULLS` 子句
    """

    NONE = 0  # %empty
    RESPECT_NULLS = 1  # RESPECT NULLS
    IGNORE_NULLS = 2  # IGNORE NULLS


class EnumOrderDirectionType(IntEnum):
    """排序方向

    使用场景：ORDER BY 子句
    """

    DEFAULT = 0  # %empty
    ASC = 1  # ASC
    DESC = 2  # DESC
