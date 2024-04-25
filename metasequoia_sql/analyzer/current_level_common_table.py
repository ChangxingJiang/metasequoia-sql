"""
当前层级，基于 SQL 语句的表相关分析器
"""

from typing import Optional, List, Dict

from metasequoia_sql.analyzer.base import (AnalyzerRecursionListBase, AnalyzerRecursionDictBase)
from metasequoia_sql.analyzer.tool import QuoteTable, SourceTable
from metasequoia_sql.core import (ASTBase, ASTSubQueryExpression, ASTTableExpression, ASTTableNameExpression,
                                  ASTSelectStatement, ASTWithClause)

__all__ = ["CurrentUsedQuoteWithAliasTables",
           "CurrentTableAliasToQuoteHash",
           "CurrentTableAliasToSubQueryHash", ]


class CurrentUsedQuoteWithAliasTables(AnalyzerRecursionListBase):
    """"获取当前层级（不递归分析子查询）中，直接使用的表名（包含原始表名、别名）"""

    @classmethod
    def custom_handle_node(cls, node: ASTBase) -> Optional[List[QuoteTable]]:
        """自定义的处理规则"""
        if isinstance(node, ASTTableExpression):
            if node.alias is not None:
                return [QuoteTable(table_name=node.alias.name)]
            else:
                table_name = node.table
                return [QuoteTable(schema_name=table_name.schema, table_name=table_name.table)]
        if isinstance(node, ASTSubQueryExpression):
            return []
        if isinstance(node, ASTWithClause):
            return []
        return None


class CurrentTableAliasToQuoteHash(AnalyzerRecursionDictBase):
    """"获取当前层级（不递归分析子查询）中，表的表名或别名到源表名的映射关系（未设置别名则未源表名到源表名的映射）"""

    @classmethod
    def custom_handle_node(cls, node: ASTBase) -> Optional[Dict[str, SourceTable]]:
        """自定义的处理规则"""
        if isinstance(node, ASTTableExpression) and isinstance(node.table, ASTTableNameExpression):
            if node.alias is not None:
                table_name = SourceTable(schema_name=node.table.schema, table_name=node.table.table)
                return {node.alias.name: table_name}
            else:
                table_name = SourceTable(schema_name=node.table.schema, table_name=node.table.table)
                return {node.table.table: table_name}
        if isinstance(node, ASTSubQueryExpression):
            return {}
        if isinstance(node, ASTWithClause):
            return {}
        return None


class CurrentTableAliasToSubQueryHash(AnalyzerRecursionDictBase):
    """"获取当前层级（不递归分析子查询）中，表的表名到子查询语法节点的映射关系"""

    @classmethod
    def custom_handle_node(cls, node: ASTBase) -> Optional[Dict[str, ASTSelectStatement]]:
        """自定义的处理规则"""
        if (isinstance(node, ASTTableExpression)
                and node.alias is not None and isinstance(node.table, ASTSubQueryExpression)):  # 子查询必须包含别名
            return {node.alias.name: node.table.select_statement}
        if isinstance(node, ASTSubQueryExpression):
            return {}
        if isinstance(node, ASTWithClause):
            return {}
        return None
