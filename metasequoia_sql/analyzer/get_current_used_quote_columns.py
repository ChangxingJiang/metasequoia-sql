"""
获取使用的字段列表
"""

from typing import Optional, List

from metasequoia_sql.analyzer.base import AnalyzerRecursionListBase
from metasequoia_sql.analyzer.tool import QuoteNameColumn, QuoteIndexColumn, QuoteColumn
from metasequoia_sql.core import (SQLBase, SQLColumnNameExpression, DataSource, GLOBAL_VARIABLE_NAME_SET,
                                  SQLNormalGroupByClause, SQLLiteralExpression)


class GetCurrentUsedQuoteColumns(AnalyzerRecursionListBase):
    """获取当前层级（即不包含子查询）中直接使用的引用字段名称（保留别名、序号等用法）"""

    @classmethod
    def custom_handle_node(cls, node: SQLBase) -> Optional[List[QuoteColumn]]:
        """自定义的处理规则"""
        if (isinstance(node, SQLColumnNameExpression)
                and node.source(DataSource.DEFAULT) not in GLOBAL_VARIABLE_NAME_SET):
            return [QuoteNameColumn(table_name=node.table, column_name=node.column)]
        if isinstance(node, SQLNormalGroupByClause):
            result = []
            for column in node.columns:
                if isinstance(column, SQLLiteralExpression):
                    result.append(QuoteIndexColumn(column_index=column.as_int()))
                else:
                    result.extend(cls.handle_node(column))
            return result
        return None
