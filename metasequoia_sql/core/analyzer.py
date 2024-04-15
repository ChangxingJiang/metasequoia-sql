import abc
import dataclasses
from typing import Any, List, Optional

from metasequoia_sql.core.objects import *


class AnalyzerBase(abc.ABC):
    def handle(self, node: SQLBase) -> List[Any]:
        result = self.custom_handle(node)
        if result is not None:
            return result
        return self.default_handle_node(node)

    @abc.abstractmethod
    def custom_handle(self, node: SQLBase) -> Optional[List[Any]]:
        """用户自定义处理逻辑

        如果需要使用处理结果，则返回列表；否则返回 None，由默认规则处理
        """

    def default_handle_node(self, node: SQLBase) -> List[Any]:
        """默认处理方法，递归聚合包含元素的结果"""
        if node is None:
            return []
        result = []
        for field in dataclasses.fields(node):
            element = getattr(node, field.name)
            result.extend(self._default_handle_element(element))
        return result

    def _default_handle_element(self, element: object) -> List[Any]:
        """默认处理方法，处理任意对象"""
        if isinstance(element, SQLBase):
            return self.handle(element)
        if isinstance(element, list) or isinstance(element, set):
            result = []
            for item in element:
                result.extend(self._default_handle_element(item))
            return result
        return []
