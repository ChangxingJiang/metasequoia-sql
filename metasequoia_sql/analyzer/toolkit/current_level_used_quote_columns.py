"""
当前层级使用的引用字段对象分析器
"""

from typing import List

from metasequoia_sql import core
from metasequoia_sql.analyzer.base import AnalyzerRecursionASTToListBase
from metasequoia_sql.analyzer.node import QuoteColumn
from metasequoia_sql.common import name_set


class CurrentNodeUsedQuoteColumn(AnalyzerRecursionASTToListBase):
    """获取当前即节点（不递归分析子查询）中，直接使用的引用字段对象"""

    @classmethod
    def handle(cls, node: core.ASTBase) -> List[QuoteColumn]:
        """自定义的处理规则"""
        # 兼容类似 COUNT(1) 这样的场景：如果是聚集函数，但参数中没有引用字段，则返回一个 column_name 为空的引用
        if isinstance(node, core.ASTAggregationFunctionExpression):
            quote_column_list = cls.default_handle_node(node)
            if len(quote_column_list) > 0:
                return quote_column_list
            return [QuoteColumn(column_name=None)]
        if (isinstance(node, core.ASTColumnNameExpression)
                and node.source(core.SQLType.DEFAULT) not in name_set.GLOBAL_VARIABLE_NAME_SET):
            return [QuoteColumn(table_name=node.table_name, column_name=node.column_name)]
        if isinstance(node, core.ASTSubQueryExpression):
            return []
        return cls.default_handle_node(node)
