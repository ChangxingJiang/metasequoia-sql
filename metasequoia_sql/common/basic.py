"""
基础工具类
"""

from typing import List, Any, Iterable

__all__ = ["ordered_distinct", "chain_list"]


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
