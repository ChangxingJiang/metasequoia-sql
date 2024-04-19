"""
当前层级基于元数据的分析器
"""

import collections
from typing import List, Dict

from metasequoia_sql.analyzer.base import AnalyzerBase, AnalyzerMetaBase
from metasequoia_sql.analyzer.current_level_common_column import CurrentColumnSelectToDirectQuoteHash
from metasequoia_sql.analyzer.current_level_common_table import CurrentTableAliasToQuoteHash, \
    CurrentTableAliasToSubQueryHash
from metasequoia_sql.analyzer.tool import check_node_type, SelectColumn, SourceColumn, QuoteColumn, QuoteTable, \
    SourceTable
from metasequoia_sql.core import SQLSelectStatement, SQLCreateTableStatement


class SelectColumnFromCreateTableStatement(AnalyzerBase):
    """根据建表语句，构造 SelectColumn 到 SourceColumn 的映射关系"""

    @classmethod
    @check_node_type(SQLCreateTableStatement)
    def handle(cls, node: SQLCreateTableStatement) -> Dict[SelectColumn, List[SourceColumn]]:
        """处理逻辑"""
        result = {}
        schema_name = node.table_name_expression.schema
        table_name = node.table_name_expression.table
        for column_idx, column_expression in enumerate(node.columns):
            column_name = column_expression.column_name
            select_column = SelectColumn(column_idx=column_idx, column_name=column_name)
            source_column = SourceColumn(schema_name=schema_name, table_name=table_name, column_name=column_name)
            result[select_column] = [source_column]
        return result


class SelectColumnToSourceColumnHash(AnalyzerMetaBase):
    """分析从 SelectColumn 到 SourceColumn 的映射关系

    - SelectColumn：包含结果表中的列名和列序号
    - SourceColumn：包含源表中的模式名、表名和列名
    """

    @check_node_type(SQLSelectStatement)
    def handle(self, node: SQLSelectStatement) -> Dict[SelectColumn, List[SourceColumn]]:
        """处理逻辑"""
        # 计算当前层级的源表信息
        alias_to_quote_hash: Dict[QuoteTable, SourceTable] = CurrentTableAliasToQuoteHash.handle(node)
        alias_to_sub_query_hash: Dict[QuoteTable, SQLSelectStatement] = CurrentTableAliasToSubQueryHash.handle(node)
        print("alias_to_quote_hash:", alias_to_quote_hash)
        print("alias_to_sub_query_hash:", alias_to_sub_query_hash)

        # 计算当前所有源表汇总的 QuoteColumn 到 SourceColumn 的映射关系
        table_name_to_column_detail_hash = {}
        column_name_to_source_column_hash = collections.defaultdict(list)

        for quote_table, source_table in alias_to_quote_hash.items():
            create_table_statement = self.create_table_statement_getter.get_statement(source_table.source())
            select_column_to_source_column_hash = SelectColumnFromCreateTableStatement.handle(create_table_statement)
            table_name_to_column_detail_hash[quote_table.table_name] = select_column_to_source_column_hash
            for select_column, source_column_list in select_column_to_source_column_hash.items():
                column_name_to_source_column_hash[select_column.column_name] = source_column_list

        for quote_table, select_statement in alias_to_sub_query_hash.items():
            select_column_to_source_column_hash = self.handle(select_statement)
            table_name_to_column_detail_hash[quote_table.table_name] = select_column_to_source_column_hash
            for select_column, source_column_list in select_column_to_source_column_hash.items():
                column_name_to_source_column_hash[select_column.column_name] = source_column_list

        print(table_name_to_column_detail_hash)
        print(column_name_to_source_column_hash)

        # TODO 兼容通配符

        # 获取当前层级所有结果字段和源字段的映射关系
        select_to_direct_hash: Dict[SelectColumn, List[QuoteColumn]] = CurrentColumnSelectToDirectQuoteHash.handle(node)
        for key, value in select_to_direct_hash.items():
            print(key, ":", value)

        # 构造映射关系并
        for select_column, quote_column_list in select_to_direct_hash.items():
            source_column_list = []
            for quote_column in quote_column_list:
                pass


