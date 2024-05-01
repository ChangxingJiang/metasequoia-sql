"""
语法树递归分析器的抽象基类
"""

import abc
import dataclasses
from typing import Any, Optional, List, Dict

from metasequoia_sql.analyzer.tool import check_node_type, CreateTableStatementGetter
from metasequoia_sql.core.node import ASTBase, ASTSelectStatement, ASTSingleSelectStatement, ASTUnionSelectStatement
from metasequoia_sql.errors import AnalyzerError

__all__ = ["AnalyzerBase",
           "AnalyzerRecursionBase", "AnalyzerRecursionListBase", "AnalyzerRecursionDictBase",
           "AnalyzerSelectASTToDictBase", "AnalyzerSelectListBase", "AnalyzerSelectDictBase",
           "AnalyzerMetaBase",
           "AnalyzerRecursionASTToDictBase"]


class AnalyzerBase(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def handle(cls, node: ASTBase) -> Any:
        """入口函数"""


class AnalyzerRecursionBase(abc.ABC):
    """语法树递归分析器的抽象基类"""

    @classmethod
    def handle(cls, node: object) -> Any:
        """入口函数"""
        return cls._collector_get(cls.handle_node(node))

    @classmethod
    def handle_node(cls, node: object) -> Any:
        """处理 node 节点"""
        result = cls.custom_handle_node(node)
        if result is not None:
            return result
        return cls.default_handle_node(node)

    @classmethod
    @abc.abstractmethod
    def custom_handle_node(cls, node: object) -> Optional[Any]:
        """自定义的处理规则

        如果需要使用处理结果，则返回列表；否则返回 None，由默认规则处理
        """

    @classmethod
    def default_handle_node(cls, obj: object) -> Any:
        """默认的处理规则（递归聚合包含元素的结果）"""
        if obj is None:
            return cls._collector_init()
        if isinstance(obj, ASTBase):
            collector = cls._collector_init()
            for field in dataclasses.fields(obj):
                next_node = getattr(obj, field.name)
                cls._collector_merge(collector, cls.handle_node(next_node))
            return collector
        if isinstance(obj, (list, set, tuple)):
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


class AnalyzerRecursionDictBase(AnalyzerRecursionBase, abc.ABC):
    """最终返回字典类型的递归分析器"""

    @classmethod
    def _collector_init(cls) -> Dict[Any, Any]:
        """初始化收集器"""
        return {}

    @classmethod
    def _collector_merge(cls, collector1: Dict[Any, Any], collector2: Dict[Any, Any]) -> None:
        """将 collector2 合并到 collector1 上"""
        collector1.update(collector2)

    @classmethod
    def _collector_get(cls, collector: Dict[Any, Any]) -> Dict[Any, Any]:
        """返回收集器的结果"""
        return collector


class AnalyzerSelectBase(abc.ABC):
    """SELECT 语句通用分析器的抽象基类"""

    @classmethod
    @check_node_type(ASTSelectStatement)
    def handle(cls, node: ASTSelectStatement) -> Any:
        """处理逻辑"""
        if isinstance(node, ASTSingleSelectStatement):
            return cls._collector_get(cls._handle_single_select_statement(node))
        if isinstance(node, ASTUnionSelectStatement):
            return cls._collector_get(cls._handle_union_select_statement(node))
        raise AnalyzerError(f"不满足条件的参数类型: {node.__class__.__name__}")

    @classmethod
    @abc.abstractmethod
    def _handle_single_select_statement(cls, node: ASTSingleSelectStatement) -> Any:
        """处理 SQLSingleSelectStatement 类型节点"""

    @classmethod
    def _handle_union_select_statement(cls, node: ASTUnionSelectStatement):
        collector = cls._collector_init()
        for element in node.elements:
            if isinstance(element, ASTSingleSelectStatement):
                cls._collector_merge(collector, cls._handle_single_select_statement(element))
        return collector

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


class AnalyzerSelectListBase(AnalyzerSelectBase, abc.ABC):
    """生成列表的 SELECT 语句通用分析器的抽象基类"""

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


class AnalyzerSelectDictBase(AnalyzerSelectBase, abc.ABC):
    """生成字典的 SELECT 语句通用分析器的抽象基类"""

    @classmethod
    def _collector_init(cls) -> Dict[Any, Any]:
        """初始化收集器"""
        return {}

    @classmethod
    def _collector_merge(cls, collector1: Dict[Any, Any], collector2: Dict[Any, Any]) -> None:
        """将 collector2 合并到 collector1 上"""
        collector1.update(collector2)

    @classmethod
    def _collector_get(cls, collector: Dict[Any, Any]) -> Dict[Any, Any]:
        """返回收集器的结果"""
        return collector


class AnalyzerMetaBase(AnalyzerBase, abc.ABC):
    """数据血缘分析器"""

    def __init__(self, create_table_statement_getter: CreateTableStatementGetter):
        self.create_table_statement_getter = create_table_statement_getter

    @abc.abstractmethod
    def handle(self, node: ASTBase) -> Any:
        """入口函数"""


class AnalyzerRecursionASTToDictBase(abc.ABC):
    """语法树递归，并返回字典的分析器的抽象基类"""

    @classmethod
    @abc.abstractmethod
    def handle(cls, node: object) -> dict:
        """入口函数"""

    @classmethod
    def default_handle_node(cls, obj: object) -> dict:
        """默认的处理规则（递归聚合包含元素的结果）"""
        if obj is None:
            return {}
        if isinstance(obj, ASTBase):
            collector = {}
            for field in dataclasses.fields(obj):
                collector.update(cls.handle(getattr(obj, field.name)))
            return collector
        if isinstance(obj, (list, set, tuple)):
            collector = {}
            for item in obj:
                collector.update(cls.handle(item))
            return collector
        return {}


class AnalyzerRecursionASTToListBase(abc.ABC):
    """语法树递归，并返回列表的分析器的抽象基类"""

    @classmethod
    @abc.abstractmethod
    def handle(cls, node: object) -> list:
        """入口函数"""

    @classmethod
    def default_handle_node(cls, obj: object) -> list:
        """默认的处理规则（递归聚合包含元素的结果）"""
        if obj is None:
            return []
        if isinstance(obj, ASTBase):
            collector = []
            for field in dataclasses.fields(obj):
                collector.extend(cls.handle(getattr(obj, field.name)))
            return collector
        if isinstance(obj, (list, set, tuple)):
            collector = []
            for item in obj:
                collector.extend(cls.handle(item))
            return collector
        return []


class AnalyzerSelectASTToDictBase(abc.ABC):
    """SELECT 语句通用分析器的抽象基类"""

    @classmethod
    @check_node_type(ASTSelectStatement)
    def handle(cls, node: ASTSelectStatement) -> dict:
        """处理逻辑"""
        if isinstance(node, ASTSingleSelectStatement):
            return cls.handle_single_select_statement(node)
        if isinstance(node, ASTUnionSelectStatement):
            return cls.handle_union_select_statement(node)
        raise AnalyzerError(f"不满足条件的参数类型: {node.__class__.__name__}")

    @classmethod
    @abc.abstractmethod
    def handle_single_select_statement(cls, node: ASTSingleSelectStatement) -> dict:
        """处理 SQLSingleSelectStatement 类型节点"""

    @classmethod
    def handle_union_select_statement(cls, node: ASTUnionSelectStatement) -> dict:
        collector = {}
        for element in node.elements:
            if isinstance(element, ASTSingleSelectStatement):
                collector.update(cls.handle_single_select_statement(element))
        return collector
