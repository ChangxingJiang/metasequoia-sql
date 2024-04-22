"""
当前层级基于元数据的分析器
"""

import collections
from typing import List, Dict, Optional

from metasequoia_sql.analyzer.base import AnalyzerBase, AnalyzerMetaBase
from metasequoia_sql.analyzer.current_level_common_column import CurrentColumnSelectToDirectQuoteHash
from metasequoia_sql.analyzer.current_level_common_table import CurrentTableAliasToQuoteHash, \
    CurrentTableAliasToSubQueryHash
from metasequoia_sql.analyzer.tool import check_node_type, SelectColumn, SourceColumn, QuoteTable, \
    SourceTable, QuoteNameColumn
from metasequoia_sql.core import SQLSelectStatement, SQLCreateTableStatement, SQLInsertStatement, DataSource, SQLInsertValuesStatement, SQLInsertSelectStatement
from metasequoia_sql.errors import AnalyzerError


class SelectColumnFromCreateTableStatement(AnalyzerBase):
    """根据建表语句，构造 SelectColumn 到 SourceColumn 的映射关系"""

    @classmethod
    @check_node_type(SQLCreateTableStatement)
    def handle(cls, node: SQLCreateTableStatement) -> Dict[SelectColumn, List[SourceColumn]]:
        """处理逻辑"""
        result = {}
        schema_name = node.table_name_expression.schema if node.table_name_expression.schema is not None else ""
        table_name = node.table_name_expression.table
        for column_idx, column_expression in enumerate(node.columns):
            column_name = column_expression.column_name
            select_column = SelectColumn(column_idx=column_idx, column_name=column_name)
            source_column = SourceColumn(schema_name=schema_name, table_name=table_name, column_name=column_name)
            result[select_column] = [source_column]
        return result


class SelectColumnToSourceColumnHash(AnalyzerMetaBase):
    """分析 SELECT 语句中，从 SelectColumn 到 SourceColumn 的映射关系

    - SelectColumn：包含结果表中的列名和列序号
    - SourceColumn：包含源表中的模式名、表名和列名

    TODO 兼容通配符
    TODO 兼容相关子查询
    """

    @check_node_type(SQLSelectStatement)
    def handle(self, node: SQLSelectStatement) -> Dict[SelectColumn, List[SourceColumn]]:
        """处理逻辑"""
        if node.with_clause is None:
            return self._handle_select_without_with_clause(node, {})

        # 逐个处理 WITH 语句中的临时表
        with_clauses_hash = {}
        for table_name, select_statement in node.with_clause.tables:
            with_clauses_hash[table_name] = self._handle_select_without_with_clause(select_statement, with_clauses_hash)

        return self._handle_select_without_with_clause(node, with_clauses_hash)

    def _handle_select_without_with_clause(self, node: SQLSelectStatement,
                                           with_clauses_hash: Dict[str, Dict[SelectColumn, List[SourceColumn]]]):
        # 计算当前层级的源表信息
        alias_to_quote_hash: Dict[QuoteTable, SourceTable] = CurrentTableAliasToQuoteHash.handle(node)
        alias_to_sub_query_hash: Dict[QuoteTable, SQLSelectStatement] = CurrentTableAliasToSubQueryHash.handle(node)

        # 计算当前所有源表汇总的 QuoteColumn 到 SourceColumn 的映射关系
        table_name_to_column_detail_hash = {}

        # -------------------- 获取所有表表名到表中字段信息的映射关系 --------------------
        # 遍历所有别名到引用名的哈希关系
        for quote_table, source_table in alias_to_quote_hash.items():
            if quote_table.table_name in with_clauses_hash:
                table_name_to_column_detail_hash[quote_table] = with_clauses_hash[quote_table.table_name]
            else:
                create_table_statement = self.create_table_statement_getter.get_statement(source_table.source())
                select_column_to_source_column_hash = SelectColumnFromCreateTableStatement.handle(
                    create_table_statement)
                table_name_to_column_detail_hash[quote_table] = select_column_to_source_column_hash

        # 遍历所有别名到子查询的哈希关系
        for quote_table, select_statement in alias_to_sub_query_hash.items():
            select_column_to_source_column_hash = self.handle(select_statement)
            table_name_to_column_detail_hash[quote_table] = select_column_to_source_column_hash

        # -------------------- 构造每个字段名到源字段的映射关系 --------------------
        quote_column_to_source_column_hash = collections.defaultdict(list)
        for quote_table, select_column_to_source_column_hash in table_name_to_column_detail_hash.items():
            for select_column, source_column_list in select_column_to_source_column_hash.items():
                quote_table_column = QuoteNameColumn(table_name=quote_table.table_name,
                                                     column_name=select_column.column_name)
                quote_column = QuoteNameColumn(column_name=select_column.column_name)
                if quote_table in alias_to_quote_hash:
                    quote_column_to_source_column_hash[quote_table_column].append(source_column_list)
                    quote_column_to_source_column_hash[quote_column].append(source_column_list)

        # 获取当前层级所有结果字段和源字段的映射关系
        result = {}
        for select_column, quote_column_list in CurrentColumnSelectToDirectQuoteHash.handle(node).items():
            source_column_list = []
            for quote_column in quote_column_list:
                source_column_group = quote_column_to_source_column_hash.get(quote_column)
                if source_column_group is None or len(source_column_group) != 1:
                    raise AnalyzerError(f"引用字段 {quote_column} 无法找到唯一的源字段: {source_column_group}")
                for source_column in source_column_group[0]:
                    if source_column not in source_column_list:
                        source_column_list.extend(source_column_group[0])
            result[select_column] = source_column_list

        return result


class InsertColumnToSourceColumnHash(AnalyzerMetaBase):
    """分析 SELECT 语句中，从 SelectColumn 到 SourceColumn 的映射关系

    - SelectColumn：包含结果表中的列名和列序号
    - SourceColumn：包含源表中的模式名、表名和列名

    TODO 兼容通配符
    TODO 兼容相关子查询
    TODO 兼容 COUNT(*) 的场景
    """

    @check_node_type(SQLInsertSelectStatement)
    def handle(self, node: SQLInsertSelectStatement) -> Dict[SourceColumn, List[SourceColumn]]:
        """处理逻辑"""
        if node.columns is not None:
            insert_columns = [SourceColumn(schema_name=node.table_name.schema,
                                           table_name=node.table_name.table,
                                           column_name=column.column)
                              for column in node.columns]
        else:
            full_table_name = node.table_name.source(DataSource.DEFAULT)
            create_table_statement = self.create_table_statement_getter.get_statement(full_table_name)
            # TODO 兼容动态分区和非动态分区
            insert_columns = [SourceColumn(schema_name=node.table_name.schema,
                                           table_name=node.table_name.table,
                                           column_name=column.column_name)
                              for column in create_table_statement.columns]

        select_statement = node.select_statement.set_with_clauses(node.with_clause)
        select_column_to_source_column_hash = SelectColumnToSourceColumnHash(
            self.create_table_statement_getter
        ).handle(select_statement)

        if len(insert_columns) != len(select_column_to_source_column_hash):
            raise AnalyzerError("写入字段数量与读取字段数量不一致")

        # 获取 SELECT 每个列顺序对应的源字段
        select_columns: List[Optional[List[SourceColumn]]] = [None] * len(insert_columns)
        for select_column, source_column_list in select_column_to_source_column_hash.items():
            select_columns[select_column.column_idx] = source_column_list

        result = {}
        for idx, insert_column in enumerate(insert_columns):
            result[insert_column] = select_columns[idx]
        return result
