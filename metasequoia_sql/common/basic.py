"""
基础工具类
"""

from typing import List, Any

__all__ = ["ordered_distinct"]


def ordered_distinct(elements: List[Any]):
    """保证顺序不变的情况下实现去重"""
    visited = set()
    result = []
    for element in elements:
        if element not in visited:
            result.append(element)
            visited.add(element)
    return result
