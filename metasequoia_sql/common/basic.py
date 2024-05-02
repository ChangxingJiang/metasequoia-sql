"""
基础工具类
"""

import re
from typing import List, Any, Iterable

__all__ = ["preproc_sql", "ordered_distinct", "chain_list", "is_hex_literal", "is_bit_literal", "is_float_literal",
           "is_string_literal", "is_int_literal", "is_bool_literal", "is_null_literal"]


def preproc_sql(text: str):
    """预处理 SQL 语句"""
    return text.replace("\r\n", "\n").replace("\t", " ").replace("　", " ")


def ordered_distinct(elements: List[Any]):
    """保证顺序不变的情况下实现去重"""
    visited = set()
    result = []
    for element in elements:
        if element not in visited:
            result.append(element)
            visited.add(element)
    return result


def chain_list(elements: Iterable[List[Any]]):
    """按顺序合并多个列表"""
    result = []
    for element in elements:
        result.extend(element)
    return result


# ------------------------------ 词法元素类型判断工具函数 ------------------------------

HEX_LITERAL_1 = re.compile(r"^[xX]['\"]([0-9ABCDEFabcdef]+)['\"]$")
HEX_LITERAL_2 = re.compile(r"^0x([0-9ABCDEFabcdef]+)$")
BIT_LITERAL_1 = re.compile(r"^[bB]['\"]([01]+)['\"]$")
BIT_LITERAL_2 = re.compile(r"^0b([01]+)$")
FLOAT_LITERAL = re.compile(r"^[+-]?\d+.\d+(E\d+)?$")
INTEGER_LITERAL = re.compile(r"^[+-]?\d+$")


def is_hex_literal(s: str) -> bool:
    """判断是否为十六进制字面值

    常见的十六机制字面值有如下 2 种格式：
    - x'01BF'、X'01BF'、x"01BF"、x"01BF"
    - 0x01BF
    """
    return HEX_LITERAL_1.match(s) is not None or HEX_LITERAL_2.match(s) is not None


def is_bit_literal(s: str) -> bool:
    """判断是否为二进制字面值

    常见的二机制字面值有如下 2 种格式：
    - b'01'、B'01'、b"01"、B"01"
    - 0b01
    """
    return BIT_LITERAL_1.match(s) is not None or BIT_LITERAL_2.match(s) is not None


def is_float_literal(s: str) -> bool:
    """判断是否为浮点数字面值"""
    return FLOAT_LITERAL.match(s) is not None


def is_int_literal(s: str) -> bool:
    """判断是否为整型字面值"""
    return re.match(r"^[+-]?\d+$", s) is not None


def is_string_literal(s: str) -> bool:
    """判断是否为字符串字面值"""
    return (s.startswith("\"") and s.endswith("\"")) or (s.startswith("'") and s.endswith("'"))


def is_bool_literal(s: str) -> bool:
    """判断是否为布尔值字面值"""
    return s.upper() in {"TRUE", "FALSE"}


def is_null_literal(s: str) -> bool:
    """判断是否为空值字面值"""
    return s.upper() == "NULL"
