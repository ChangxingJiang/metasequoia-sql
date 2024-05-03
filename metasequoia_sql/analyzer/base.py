"""
语法树递归分析器的抽象基类
"""

import abc
import dataclasses

from metasequoia_sql.common.basic import check_param_type
from metasequoia_sql.core.node import ASTBase, ASTSelectStatement, ASTSingleSelectStatement, ASTUnionSelectStatement
from metasequoia_sql.errors import AnalyzerError

__all__ = ["AnalyzerRecursionASTToDictBase", "AnalyzerRecursionASTToListBase",
           "AnalyzerSelectASTToDictBase", "AnalyzerSelectASTToListBase"]


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
    @check_param_type(ASTSelectStatement)
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
        """处理 ASTUnionSelectStatement 类型节点"""
        collector = {}
        for element in node.elements:
            if isinstance(element, ASTSingleSelectStatement):
                collector.update(cls.handle_single_select_statement(element))
        return collector


class AnalyzerSelectASTToListBase(abc.ABC):
    """SELECT 语句通用分析器的抽象基类"""

    @classmethod
    @check_param_type(ASTSelectStatement)
    def handle(cls, node: ASTSelectStatement) -> list:
        """处理逻辑"""
        if isinstance(node, ASTSingleSelectStatement):
            return cls.handle_single_select_statement(node)
        if isinstance(node, ASTUnionSelectStatement):
            return cls.handle_union_select_statement(node)
        raise AnalyzerError(f"不满足条件的参数类型: {node.__class__.__name__}")

    @classmethod
    @abc.abstractmethod
    def handle_single_select_statement(cls, node: ASTSingleSelectStatement) -> list:
        """处理 SQLSingleSelectStatement 类型节点"""

    @classmethod
    def handle_union_select_statement(cls, node: ASTUnionSelectStatement) -> list:
        """处理 ASTUnionSelectStatement 类型节点"""
        collector = []
        for element in node.elements:
            if isinstance(element, ASTSingleSelectStatement):
                collector.extend(cls.handle_single_select_statement(element))
        return collector
