"""
所有层级中，获取使用的引用表列表
"""

from typing import Optional, List

from metasequoia_sql.analyzer.base import (AnalyzerRecursionListBase, AnalyzerSelectListBase)
from metasequoia_sql.analyzer.tool import QuoteTable
from metasequoia_sql.core import (SQLBase, SQLTableNameExpression, SQLSingleSelectStatement)

__all__ = ["AllUsedQuoteTables",
           "AllFromClauseUsedQuoteColumn",
           "AllJoinClauseUsedQuoteColumn"]


class AllUsedQuoteTables(AnalyzerRecursionListBase):
    """"获取所有层级（递归分析子查询）中，直接使用的表名（仅包含原始表名）"""

    @classmethod
    def custom_handle_node(cls, node: SQLBase) -> Optional[List[QuoteTable]]:
        """自定义的处理规则"""
        if isinstance(node, SQLTableNameExpression):
            return [QuoteTable(schema_name=node.schema, table_name=node.table)]
        return None


class AllFromClauseUsedQuoteColumn(AnalyzerSelectListBase):
    """获取所有层级（递归分析子查询）的 FROM 子句中，直接使用的表名（仅包含原始表名）"""

    @classmethod
    def _handle_single_select_statement(cls, node: SQLSingleSelectStatement) -> List[QuoteTable]:
        """处理逻辑"""
        return AllUsedQuoteTables.handle(node.from_clause)


class AllJoinClauseUsedQuoteColumn(AnalyzerSelectListBase):
    """获取所有层级（递归分析子查询）的 JOIN 子句中，直接使用的表名（仅包含原始表名）"""

    @classmethod
    def _handle_single_select_statement(cls, node: SQLSingleSelectStatement) -> List[QuoteTable]:
        """处理逻辑"""
        return AllUsedQuoteTables.handle(node.join_clauses)
