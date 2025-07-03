"""
DQL 语句中的枚举类型
"""

from enum import IntEnum, IntFlag

__all__ = [
    "EnumCompareOperator",
    "EnumFulltextOption"
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
