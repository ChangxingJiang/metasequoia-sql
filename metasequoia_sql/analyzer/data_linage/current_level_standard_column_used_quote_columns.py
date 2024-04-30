"""
当前层级，标准字段名到使用的
"""

from typing import Dict, List

from metasequoia_sql import core
from metasequoia_sql.analyzer.base import AnalyzerSelectASTToDictBase
from metasequoia_sql.analyzer.data_linage.node import StandardColumn, QuoteColumn
from metasequoia_sql.analyzer.toolkit.current_level_used_quote_columns import CurrentUsedQuoteWithAliasIndexColumns


class CurrentLevelStandardColumnUsedQuoteColumns(AnalyzerSelectASTToDictBase):
    """表名规范化器"""

    def __init__(self, select_statement: core.ASTSelectStatement):
        self._standard_hash = self.handle(select_statement)

    def get_by_standard_column(self, standard_colum: str) -> str:
        """使用标准字段对象获取引用字段列表"""
        return self._standard_hash[standard_colum]

    @classmethod
    def handle_single_select_statement(cls, node: core.ASTSingleSelectStatement
                                       ) -> Dict[StandardColumn, List[QuoteColumn]]:
        result = {}
        for column_idx, column_expression in enumerate(node.select_clause.columns):
            if column_expression.alias is not None:
                select_column = StandardColumn(column_name=column_expression.alias.name, column_idx=column_idx)
            elif isinstance(column_expression.column, core.ASTColumnNameExpression):
                select_column = StandardColumn(column_name=column_expression.column.column, column_idx=column_idx)
            else:
                select_column = StandardColumn(column_name=column_expression.column.source(core.SQLType.DEFAULT),
                                               column_idx=column_idx)
            result[select_column] = CurrentUsedQuoteWithAliasIndexColumns.handle(column_expression.column)
        return result
