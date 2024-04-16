"""
语法树递归分析器的抽象基类
"""

import abc
import dataclasses
from typing import Any, Optional, List

from metasequoia_sql.core.objects import SQLBase

__all__ = ["AnalyzerBase", "AnalyzerRecursionBase", "AnalyzerRecursionListBase"]


class AnalyzerBase(abc.ABC):
    @abc.abstractmethod
    def handle(self, node: SQLBase) -> Any:
        """入口函数"""


class AnalyzerRecursionBase(abc.ABC):
    """语法树递归分析器的抽象基类"""

    def handle(self, node: SQLBase) -> Any:
        """入口函数"""
        return self._collector_get(self.handle_node(node))

    def handle_node(self, node: SQLBase) -> Any:
        """处理 node 节点"""
        result = self.custom_handle_node(node)
        if result is not None:
            return result
        return self.default_handle_node(node)

    @abc.abstractmethod
    def custom_handle_node(self, node: SQLBase) -> Optional[Any]:
        """自定义的处理规则

        如果需要使用处理结果，则返回列表；否则返回 None，由默认规则处理
        """

    def default_handle_node(self, obj: object) -> Any:
        """默认的处理规则（递归聚合包含元素的结果）"""
        if obj is None:
            return self._collector_init()
        if isinstance(obj, SQLBase):
            collector = self._collector_init()
            for field in dataclasses.fields(obj):
                next_node = getattr(obj, field.name)
                self._collector_merge(collector, self.handle_node(next_node))
            return collector
        if isinstance(obj, (list, set)):
            collector = self._collector_init()
            for item in obj:
                self._collector_merge(collector, self.handle_node(item))
            return collector
        return self._collector_init()

    @abc.abstractmethod
    def _collector_init(self) -> Any:
        """初始化收集器"""

    @abc.abstractmethod
    def _collector_merge(self, collector1: Any, collector2: Any) -> Any:
        """合并返回结果（在实现上可以修改 collector1 或 collector 并返回，也可以构造新的收集器）"""

    @abc.abstractmethod
    def _collector_get(self, collector: Any) -> Any:
        """返回收集器的结果"""


class AnalyzerRecursionListBase(AnalyzerRecursionBase, abc.ABC):
    """最终返回列表类型的递归分析器"""

    def _collector_init(self) -> List[Any]:
        """初始化收集器"""
        return []

    def _collector_merge(self, collector1: List[Any], collector2: List[Any]) -> None:
        """将 collector2 合并到 collector1 上"""
        collector1.extend(collector2)

    def _collector_get(self, collector: List[Any]) -> List[Any]:
        """返回收集器的结果"""
        return collector
