"""
所有层级中，获取使用的引用表列表
"""

from typing import List, Union

from metasequoia_sql import core
from metasequoia_sql.analyzer.base import AnalyzerRecursionASTToListBase, AnalyzerSelectASTToListBase
from metasequoia_sql.analyzer.node import StandardTable

__all__ = ["AllUsedQuoteTables",
           "AllFromClauseUsedQuoteColumn",
           "AllJoinClauseUsedQuoteColumn"]


class AllUsedQuoteTables(AnalyzerRecursionASTToListBase):
    """"获取所有层级（递归分析子查询）中，直接使用的表名（仅包含原始表名）"""

    @classmethod
    def handle(cls, node: Union[core.ASTBase, tuple]) -> List[StandardTable]:
        """自定义的处理规则"""
        if isinstance(node, core.ASTTableNameExpression):
            return [StandardTable(schema_name=node.schema_name, table_name=node.table_name)]
        return cls.default_handle_node(node)


class AllFromClauseUsedQuoteColumn(AnalyzerSelectASTToListBase):
    """获取所有层级（递归分析子查询）的 FROM 子句中，直接使用的表名（仅包含原始表名）"""

    @classmethod
    def handle(cls, node: core.ASTSelectStatement) -> List[StandardTable]:
        """重写处理方法主逻辑，以更新返回值的类型标记"""
        return super().handle(node)

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement) -> List[StandardTable]:
        """处理逻辑"""
        return AllUsedQuoteTables.handle(node.from_clause)


class AllJoinClauseUsedQuoteColumn(AnalyzerSelectASTToListBase):
    """获取所有层级（递归分析子查询）的 JOIN 子句中，直接使用的表名（仅包含原始表名）"""

    @classmethod
    def handle(cls, node: core.ASTSelectStatement) -> List[StandardTable]:
        """重写处理方法主逻辑，以更新返回值的类型标记"""
        return super().handle(node)

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement) -> List[StandardTable]:
        """处理逻辑"""
        return AllUsedQuoteTables.handle(node.join_clauses)
