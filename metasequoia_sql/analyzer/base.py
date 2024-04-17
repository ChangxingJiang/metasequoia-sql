"""
语法树递归分析器的抽象基类
"""

import abc
import dataclasses
from typing import Any, Optional, List

from metasequoia_sql.core.objects import SQLBase

__all__ = ["AnalyzerBase", "AnalyzerRecursionBase", "AnalyzerRecursionListBase"]


class AnalyzerBase(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def handle(cls, node: SQLBase) -> Any:
        """入口函数"""


class AnalyzerRecursionBase(abc.ABC):
    """语法树递归分析器的抽象基类"""

    @classmethod
    def handle(cls, node: SQLBase) -> Any:
        """入口函数"""
        return cls._collector_get(cls.handle_node(node))

    @classmethod
    def handle_node(cls, node: SQLBase) -> Any:
        """处理 node 节点"""
        result = cls.custom_handle_node(node)
        if result is not None:
            return result
        return cls.default_handle_node(node)

    @classmethod
    @abc.abstractmethod
    def custom_handle_node(cls, node: SQLBase) -> Optional[Any]:
        """自定义的处理规则

        如果需要使用处理结果，则返回列表；否则返回 None，由默认规则处理
        """

    @classmethod
    def default_handle_node(cls, obj: object) -> Any:
        """默认的处理规则（递归聚合包含元素的结果）"""
        if obj is None:
            return cls._collector_init()
        if isinstance(obj, SQLBase):
            collector = cls._collector_init()
            for field in dataclasses.fields(obj):
                next_node = getattr(obj, field.name)
                cls._collector_merge(collector, cls.handle_node(next_node))
            return collector
        if isinstance(obj, (list, set)):
            collector = cls._collector_init()
            for item in obj:
                cls._collector_merge(collector, cls.handle_node(item))
            return collector
        return cls._collector_init()

    @classmethod
    @abc.abstractmethod
    def _collector_init(cls) -> Any:
        """初始化收集器"""

    @classmethod
    @abc.abstractmethod
    def _collector_merge(cls, collector1: Any, collector2: Any) -> Any:
        """合并返回结果（在实现上可以修改 collector1 或 collector 并返回，也可以构造新的收集器）"""

    @classmethod
    @abc.abstractmethod
    def _collector_get(cls, collector: Any) -> Any:
        """返回收集器的结果"""


class AnalyzerRecursionListBase(AnalyzerRecursionBase, abc.ABC):
    """最终返回列表类型的递归分析器"""

    @classmethod
    def _collector_init(cls) -> List[Any]:
        """初始化收集器"""
        return []

    @classmethod
    def _collector_merge(cls, collector1: List[Any], collector2: List[Any]) -> None:
        """将 collector2 合并到 collector1 上"""
        collector1.extend(collector2)

    @classmethod
    def _collector_get(cls, collector: List[Any]) -> List[Any]:
        """返回收集器的结果"""
        return collector
