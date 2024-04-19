"""
当前层级，基于 SQL 语句的表相关分析器
"""

from typing import Optional, List, Dict

from metasequoia_sql.analyzer.base import (AnalyzerRecursionListBase, AnalyzerRecursionDictBase)
from metasequoia_sql.analyzer.tool import QuoteTable, SourceTable
from metasequoia_sql.core import (SQLBase, SQLSubQueryExpression, SQLTableExpression, SQLTableNameExpression,
                                  SQLSelectStatement)

__all__ = ["CurrentUsedQuoteWithAliasTables",
           "CurrentTableAliasToQuoteHash",
           "CurrentTableAliasToSubQueryHash", ]


class CurrentUsedQuoteWithAliasTables(AnalyzerRecursionListBase):
    """"获取当前层级（不递归分析子查询）中，直接使用的表名（包含原始表名、别名）"""

    @classmethod
    def custom_handle_node(cls, node: SQLBase) -> Optional[List[QuoteTable]]:
        """自定义的处理规则"""
        if isinstance(node, SQLTableExpression):
            if node.alias is not None:
                return [QuoteTable(table_name=node.alias.name)]
            else:
                table_name = node.table
                return [QuoteTable(schema_name=table_name.schema, table_name=table_name.table)]
        if isinstance(node, SQLSubQueryExpression):
            return []
        return None


class CurrentTableAliasToQuoteHash(AnalyzerRecursionDictBase):
    """"获取当前层级（不递归分析子查询）中，表的表名或别名到源表名的映射关系（未设置别名则未源表名到源表名的映射）"""

    @classmethod
    def custom_handle_node(cls, node: SQLBase) -> Optional[Dict[QuoteTable, SourceTable]]:
        """自定义的处理规则"""
        if isinstance(node, SQLTableExpression) and isinstance(node.table, SQLTableNameExpression):
            if node.alias is not None:
                alias_name = QuoteTable(table_name=node.alias.name)
                table_name = SourceTable(schema_name=node.table.schema, table_name=node.table.table)
                return {alias_name: table_name}
            else:
                alias_name = QuoteTable(table_name=node.table.table)
                table_name = SourceTable(schema_name=node.table.schema, table_name=node.table.table)
                return {alias_name: table_name}
        if isinstance(node, SQLSubQueryExpression):
            return {}
        return None


class CurrentTableAliasToSubQueryHash(AnalyzerRecursionDictBase):
    """"获取当前层级（不递归分析子查询）中，表的表名到子查询语法节点的映射关系"""

    @classmethod
    def custom_handle_node(cls, node: SQLBase) -> Optional[Dict[QuoteTable, SQLSelectStatement]]:
        """自定义的处理规则"""
        if (isinstance(node, SQLTableExpression)
                and node.alias is not None and isinstance(node.table, SQLSubQueryExpression)):  # 子查询必须包含别名
            alias_name = QuoteTable(table_name=node.alias.name)
            return {alias_name: node.table.select_statement}
        if isinstance(node, SQLSubQueryExpression):
            return {}
        return None
