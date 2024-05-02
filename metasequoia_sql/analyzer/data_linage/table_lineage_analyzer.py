"""
表数据血缘分析器
"""

from typing import Optional, List, Tuple

from metasequoia_sql import core
from metasequoia_sql.analyzer.node import StandardColumn, QuoteColumn, SourceColumn
from metasequoia_sql.analyzer.data_linage.table_lineage import SelectTableLineage, InsertTableLineage
from metasequoia_sql.analyzer.data_linage.table_lineage_storage import TableLineageStorage
from metasequoia_sql.analyzer.tool import CreateTableStatementGetter
from metasequoia_sql.analyzer.toolkit import CurrentLevelSubQuery, CurrentLevelTableNameAnalyzer, \
    CurrentNodeUsedQuoteColumn
from metasequoia_sql.errors import AnalyzerError

__all__ = ["TableLineageAnalyzer"]


class TableLineageAnalyzer:
    """表数据血缘管理器

    TODO 兼容 COUNT(*) 的场景
    """

    def __init__(self, create_table_statement_getter: CreateTableStatementGetter):
        self._create_table_statement_getter = create_table_statement_getter  # 建表语句查询器

    def get_select_table_lineage(self,
                                 select_statement: core.ASTSelectStatement,
                                 table_lineage_storage: Optional[TableLineageStorage] = None) -> SelectTableLineage:
        """获取 SELECT 语句中的表数据血缘对象

        TODO 增加对相关子查询的支持

        Parameters
        ----------
        select_statement: core.ASTSelectStatement
            查询语句
        table_lineage_storage: Optional[TableLineageStorage], default = None
            在这个表之前的 WITH 临时表存储器（用于递归调用）
        """
        # 初始化表数据血缘存储器
        if table_lineage_storage is None:
            table_lineage_storage = TableLineageStorage(self._create_table_statement_getter)

        # 逐个遍历 WITH 子句
        for table_name, with_select_statement in select_statement.with_clause.tables:
            table_lineage = self.get_select_table_lineage(with_select_statement, table_lineage_storage)
            table_lineage_storage.add_with_table(table_name=table_name, table_lineage=table_lineage)

        # 遍历当前层级的所有子查询
        current_level_sub_query = CurrentLevelSubQuery(select_statement)
        for alias_name in current_level_sub_query.get_all_sub_query_alias_name():
            sub_query_select_statement = current_level_sub_query.get_sub_query_statement(alias_name)
            table_lineage = self.get_select_table_lineage(sub_query_select_statement, table_lineage_storage)
            table_lineage_storage.add_sub_query_table(table_name=alias_name, table_lineage=table_lineage)

        # 初始化当前层级的表名规范器
        table_name_analyzer = CurrentLevelTableNameAnalyzer(select_statement)

        # 获取当前层级使用的 LATERAL VIEW 字段属性
        lateral_view_columns = dict(self.get_lateral_view_clause_column_name_to_quote_columns(select_statement))

        # 处理当前层级的引用字段逻辑
        data_lineage = []
        for standard_column, quote_columns in self.get_current_level_stand_column_used_quote_columns(
                select_statement=select_statement,
                table_lineage_storage=table_lineage_storage,
                table_name_analyzer=table_name_analyzer):
            # 处理使用 LATERAL VIEW 子句中字段的情况
            new_quote_column = []
            for quote_column in quote_columns:
                if quote_column.table_name is None and quote_column.column_name in lateral_view_columns:
                    new_quote_column.extend(lateral_view_columns[quote_column.column_name])
                else:
                    new_quote_column.append(quote_column)

            # 使用不包含 LATERAL VIEW 子句的其他字段
            source_column_list = []
            for quote_column in new_quote_column:
                if quote_column.table_name is not None:
                    from_standard_table = table_name_analyzer.get_standard_table(quote_column.table_name)
                    from_table_lineage = table_lineage_storage.get_table_lineage(from_standard_table)
                    source_column_list.extend(
                        from_table_lineage.get_source_column_list_by_name(quote_column.column_name))
                elif quote_column.column_name is None:  # 兼容聚集函数的参数中没有直接使用字段的情况，则直接标记引用了所有上游表
                    for from_standard_table in table_name_analyzer.get_all_standard_table():
                        from_table_lineage = table_lineage_storage.get_table_lineage(from_standard_table)
                        for source_table in from_table_lineage.get_standard_table_list():
                            source_column_list.append(SourceColumn(schema_name=source_table.schema_name,
                                                                   table_name=source_table.table_name,
                                                                   column_name=None))
                else:
                    already_match = False  # 是否已经匹配到上游表
                    for from_standard_table in table_name_analyzer.get_all_standard_table():
                        from_table_lineage = table_lineage_storage.get_table_lineage(from_standard_table)
                        if not from_table_lineage.has_column(quote_column.column_name):
                            continue
                        if already_match is True:
                            raise AnalyzerError("同一个字段可以匹配到多个上游表")
                        already_match = True
                        source_column_list.extend(
                            from_table_lineage.get_source_column_list_by_name(quote_column.column_name))
                    if already_match is False:
                        for from_standard_table in table_name_analyzer.get_all_standard_table():
                            from_table_lineage = table_lineage_storage.get_table_lineage(from_standard_table)
                            print(from_standard_table.table_name, ":", from_table_lineage.all_columns())
                        raise AnalyzerError(f"没有匹配到合适的上游表字段: 字段={quote_column}, "
                                            f"上游表={table_name_analyzer.get_all_standard_table()}")
            data_lineage.append((standard_column, source_column_list))
        return SelectTableLineage(data_lineage=data_lineage)

    def get_insert_table_lineage(self, insert_statement: core.ASTInsertSelectStatement) -> InsertTableLineage:
        """获取 INSERT 语句中的表数据血缘对象"""
        if insert_statement.columns is not None:
            insert_columns = [SourceColumn(schema_name=insert_statement.table_name.schema,
                                           table_name=insert_statement.table_name.table,
                                           column_name=column.column)
                              for column in insert_statement.columns]
        else:
            full_table_name = insert_statement.table_name.source(core.SQLType.DEFAULT)
            create_table_statement = self._create_table_statement_getter.get_statement(full_table_name)
            insert_columns = [SourceColumn(schema_name=insert_statement.table_name.schema,
                                           table_name=insert_statement.table_name.table,
                                           column_name=column.column_name)
                              for column in create_table_statement.columns]

        select_statement = insert_statement.select_statement.set_with_clauses(insert_statement.with_clause)
        select_table_lineage = self.get_select_table_lineage(select_statement=select_statement)

        if len(insert_columns) != len(select_table_lineage.all_columns()):
            raise AnalyzerError("写入字段数量与读取字段数量不一致")

        # 获取 INSERT 每个字段对应的上游源字段
        data_lineage = []
        for column_idx, down_column in enumerate(insert_columns):
            data_lineage.append((down_column, select_table_lineage.get_source_column_list_by_idx(column_idx + 1)))
        return InsertTableLineage(data_lineage=data_lineage)

    def get_current_level_stand_column_used_quote_columns(
            self,
            select_statement: core.ASTSelectStatement,
            table_lineage_storage: TableLineageStorage,
            table_name_analyzer: CurrentLevelTableNameAnalyzer
    ) -> List[Tuple[StandardColumn, List[QuoteColumn]]]:
        """获取 ASTSelectStatement 节点当前层级标准字段对象和使用的应用字段对象的映射关系"""
        if isinstance(select_statement, core.ASTSingleSelectStatement):
            return self.get_single_current_level_standard_column_used_quote_columns(
                select_statement=select_statement,
                table_lineage_storage=table_lineage_storage,
                table_name_analyzer=table_name_analyzer
            )
        # 处理 UNION 多个 SELECT 语句
        if isinstance(select_statement, core.ASTUnionSelectStatement):
            result = None
            for element in select_statement.elements:
                if not isinstance(element, core.ASTSingleSelectStatement):
                    continue
                if result is None:
                    result = self.get_single_current_level_standard_column_used_quote_columns(
                        select_statement=element,
                        table_lineage_storage=table_lineage_storage,
                        table_name_analyzer=table_name_analyzer
                    )
                else:
                    merge = self.get_single_current_level_standard_column_used_quote_columns(
                        select_statement=element,
                        table_lineage_storage=table_lineage_storage,
                        table_name_analyzer=table_name_analyzer
                    )
                    assert len(result) == len(merge), "UNION的多个SELECT语句的字段数不同"
                    for i in range(len(result)):
                        standard_column, quote_column_list = result[i]
                        quote_column_list.extend(merge[i][1])
                        result[i] = (standard_column, quote_column_list)
            return result
        raise AnalyzerError("未知的SELECT语句类型")

    @classmethod
    def get_single_current_level_standard_column_used_quote_columns(
            cls,
            select_statement: core.ASTSingleSelectStatement,
            table_lineage_storage: TableLineageStorage,
            table_name_analyzer: CurrentLevelTableNameAnalyzer
    ) -> List[Tuple[StandardColumn, List[QuoteColumn]]]:
        """获取 ASTSingleSelectStatement 节点当前层级标准字段对象和使用的应用字段对象的映射关系

        TODO 待修改属性名：column.column_value.column_name
        TODO 多个表的有序性
        """
        result = []
        column_idx = 1
        for column in select_statement.select_clause.columns:
            if column.alias is not None:  # 有别名的情况（此时一定不是通配符）
                standard_column = StandardColumn(column_name=column.alias.name, column_idx=column_idx)
                column_idx += 1
                result.append((standard_column, CurrentNodeUsedQuoteColumn.handle(column.column)))
            elif isinstance(column.column, core.ASTColumnNameExpression):  # 直接使用字段的情况
                if column.column.column == "*":  # 通配符
                    if column.column.table is not None:  # 有表名的通配符
                        standard_table = table_name_analyzer.get_standard_table(column.column.table)
                        table_lineage = table_lineage_storage.get_table_lineage(standard_table)
                        for from_standard_column in table_lineage.get_all_standard_columns():
                            standard_column = StandardColumn(column_name=from_standard_column.column_name,
                                                             column_idx=column_idx)
                            column_idx += 1
                            quote_column = QuoteColumn(table_name=standard_table.table_name,
                                                       column_name=from_standard_column.column_name)
                            result.append((standard_column, [quote_column]))
                    else:  # 没有表名的通配符
                        for standard_table in table_name_analyzer.get_all_standard_table():
                            table_lineage = table_lineage_storage.get_table_lineage(standard_table)
                            for from_standard_column in table_lineage.get_all_standard_columns():
                                standard_column = StandardColumn(column_name=from_standard_column.column_name,
                                                                 column_idx=column_idx)
                                column_idx += 1
                                quote_column = QuoteColumn(table_name=standard_table.table_name,
                                                           column_name=from_standard_column.column_name)
                                result.append((standard_column, [quote_column]))
                else:  # 非通配符
                    standard_column = StandardColumn(column_name=column.column.column, column_idx=column_idx)
                    column_idx += 1
                    quote_column = QuoteColumn(table_name=column.column.table,
                                               column_name=column.column.column)
                    result.append((standard_column, [quote_column]))
            else:  # 不是字段名的情况（此时一定不是通配符）
                standard_column = StandardColumn(column_name=column.column.source(core.SQLType.DEFAULT),
                                                 column_idx=column_idx)
                column_idx += 1
                result.append((standard_column, CurrentNodeUsedQuoteColumn.handle(column.column)))
        return result

    def get_lateral_view_clause_column_name_to_quote_columns(
            self,
            select_statement: core.ASTSelectStatement
    ) -> List[Tuple[str, List[QuoteColumn]]]:
        """获取 ASTSelectStatement 节点的 LATERAL VIEW 子句中所有字段到引用字段对象列表的映射关系"""
        if isinstance(select_statement, core.ASTSingleSelectStatement):
            return self.get_single_lateral_view_clause_column_name_to_quote_columns(select_statement)
        # 处理 UNION 多个 SELECT 语句
        if isinstance(select_statement, core.ASTUnionSelectStatement):
            result: Optional[List[Tuple[str, List[QuoteColumn]]]] = None
            for element in select_statement.elements:
                if not isinstance(element, core.ASTSingleSelectStatement):
                    continue
                if result is None:
                    result = self.get_single_lateral_view_clause_column_name_to_quote_columns(element)
                else:
                    merge = self.get_single_lateral_view_clause_column_name_to_quote_columns(element)
                    assert len(result) == len(merge), "UNION的多个SELECT语句的字段数不同"
                    for i in range(len(result)):
                        column_name, quote_column_list = result[i]
                        quote_column_list.extend(merge[i][1])
                        result[i] = (column_name, quote_column_list)
            return result
        raise AnalyzerError("未知的SELECT语句类型")

    @classmethod
    def get_single_lateral_view_clause_column_name_to_quote_columns(
            cls,
            select_statement: core.ASTSingleSelectStatement
    ) -> List[Tuple[str, List[QuoteColumn]]]:
        """获取 ASTSingleSelectStatement 节点的 LATERAL VIEW 子句中所有字段到引用字段对象列表的映射关系"""
        result = []
        for lateral_view_clause in select_statement.lateral_view_clauses:  # 遍历 LATERAL VIEW 子句中的所有字段
            result.append((lateral_view_clause.alias.name,
                           CurrentNodeUsedQuoteColumn.handle(lateral_view_clause.function)))
        return result
