from typing import Optional, List

from metasequoia_sql import core
from metasequoia_sql.analyzer.base import AnalyzerRecursionASTToListBase
from metasequoia_sql.analyzer.data_linage.node import QuoteColumn


class CurrentUsedQuoteWithAliasIndexColumns(AnalyzerRecursionASTToListBase):
    """获取当前层级（不递归分析子查询）中，直接使用的引用字段对象"""

    @classmethod
    def handle(cls, node: core.ASTBase) -> Optional[List[QuoteColumn]]:
        """自定义的处理规则"""
        if (isinstance(node, core.ASTColumnNameExpression)
                and node.source(core.SQLType.DEFAULT) not in core.GLOBAL_VARIABLE_NAME_SET):
            return [QuoteColumn(table_name=node.table, column_name=node.column)]
        if isinstance(node, core.ASTSubQueryExpression):
            return []
        return cls.default_handle_node(node)
