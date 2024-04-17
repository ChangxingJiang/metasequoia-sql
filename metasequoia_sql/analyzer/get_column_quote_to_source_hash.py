"""
构造下游表字段到上游表字段的映射关系
"""

from typing import Optional, List, Dict

from metasequoia_sql.analyzer.base import AnalyzerBase
from metasequoia_sql.analyzer.tool import SourceColumn, check_node_type, SelectColumn, QuoteColumn
from metasequoia_sql.core import SQLSingleSelectStatement


class GetColumnQuoteToSourceHash(AnalyzerBase):
    """构造应用字段到上游表字段的映射关系"""

    @classmethod
    @check_node_type(SQLSingleSelectStatement)
    def handle(cls, node: SQLSingleSelectStatement) -> Dict[QuoteColumn, List[SourceColumn]]:
        """处理字段类型"""
        result = {}
        for column_idx, column_expression in enumerate(node.select_clause.columns):
            alias_name = column_expression.alias.name
            source_column = SourceColumn(column_nam)

    @classmethod
    def custom_handle_node(cls, node: SQLBase) -> Optional[List[SourceColumn]]:
        """自定义的处理规则"""
        if (isinstance(node, SQLColumnNameExpression)
                and node.source(DataSource.DEFAULT) not in GLOBAL_VARIABLE_NAME_SET):
            return [SourceColumn(table_name=node.table, column_name=node.column)]
        if isinstance(node, SQLSingleSelectStatement):
            return cls.handle_node(node.select_clause) + cls.handle_node(node.where_clause)

        return None
