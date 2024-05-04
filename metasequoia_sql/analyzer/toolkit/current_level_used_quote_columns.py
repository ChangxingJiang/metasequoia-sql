"""
当前层级使用的引用字段对象分析器
"""

from typing import List, Union

from metasequoia_sql import core
from metasequoia_sql.analyzer.base import AnalyzerRecursionASTToListBase
from metasequoia_sql.analyzer.node import QuoteColumn
from metasequoia_sql.common import name_set
from metasequoia_sql.common.basic import is_int_literal


__all__ = ["CurrentNodeUsedQuoteColumn"]


class CurrentNodeUsedQuoteColumn(AnalyzerRecursionASTToListBase):
    """获取当前即节点（不递归分析子查询）中，直接使用的引用字段对象"""

    @classmethod
    def handle(cls, node: Union[core.ASTBase, tuple]) -> List[QuoteColumn]:
        # pylint: disable=R0911
        # pylint: disable=R0912
        """自定义的处理规则"""
        # 处理类似 COUNT(1) 的场景：如果是聚集函数，但参数中没有引用字段，则返回一个 column_name 为空的引用
        if isinstance(node, core.ASTAggregationFunctionExpression):
            quote_column_list = cls.default_handle_node(node)
            if len(quote_column_list) > 0:
                return quote_column_list
            return [QuoteColumn(column_name=None)]

        # 处理通配符场景
        if isinstance(node, core.ASTWildcardExpression):
            return [QuoteColumn(table_name=node.table_name, column_name="*")]

        # 处理普通表名引用场景
        if isinstance(node, core.ASTColumnName) and node.source() not in name_set.GLOBAL_VARIABLE_NAME_SET:
            return [QuoteColumn(table_name=node.table_name, column_name=node.column_name)]

        # 如果是 GROUP BY 子句，则需要兼容使用字段序号的情况
        if isinstance(node, core.ASTNormalGroupByClause):
            quote_column_list = []
            for column in node.columns:
                if is_int_literal(column.source()):
                    quote_column_list.append(QuoteColumn(column_name=None, column_idx=int(column.source())))
                else:
                    quote_column_list.extend(cls.handle(column))
            return quote_column_list

        # 如果是 ORDER BY 子句，则需要兼容使用字段序号的情况
        if isinstance(node, core.ASTOrderByClause):
            quote_column_list = []
            for column in node.columns:
                if is_int_literal(column.column.source()):
                    quote_column_list.append(QuoteColumn(column_name=None, column_idx=int(column.column.source())))
                else:
                    quote_column_list.extend(cls.handle(column))
            return quote_column_list

        # 不递归处理子查询
        if isinstance(node, core.ASTSubQueryExpression):
            return []

        return cls.default_handle_node(node)
