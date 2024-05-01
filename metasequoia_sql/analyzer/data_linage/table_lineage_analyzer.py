"""
表数据血缘分析器
"""

from typing import Optional, List, Tuple

from metasequoia_sql import core
from metasequoia_sql.analyzer.data_linage.node import StandardColumn, QuoteColumn
from metasequoia_sql.analyzer.data_linage.table_lineage import TableLineage
from metasequoia_sql.analyzer.data_linage.table_lineage_storage import TableLineageStorage
from metasequoia_sql.analyzer.tool import CreateTableStatementGetter
from metasequoia_sql.analyzer.toolkit import CurrentLevelSubQuery, CurrentLevelTableNameAnalyzer, \
    CurrentLevelUsedQuoteColumn
from metasequoia_sql.errors import AnalyzerError

__all__ = ["TableLineageAnalyzer"]


class TableLineageAnalyzer:
    """表数据血缘管理器"""

    def __init__(self, create_table_statement_getter: CreateTableStatementGetter):
        self._create_table_statement_getter = create_table_statement_getter  # 建表语句查询器

    def get_table_lineage(self,
                          select_statement: core.ASTSelectStatement,
                          table_lineage_storage: Optional[TableLineageStorage] = None) -> TableLineage:
        """获取表数据血缘对象

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
            table_lineage = self.get_table_lineage(with_select_statement, table_lineage_storage)
            table_lineage_storage.add_with_table(table_name=table_name, table_lineage=table_lineage)

        # 遍历当前层级的所有子查询
        current_level_sub_query = CurrentLevelSubQuery(select_statement)
        for alias_name in current_level_sub_query.get_all_sub_query_alias_name():
            sub_query_select_statement = current_level_sub_query.get_sub_query_statement(alias_name)
            table_lineage = self.get_table_lineage(sub_query_select_statement, table_lineage_storage)
            table_lineage_storage.add_sub_query_table(table_name=alias_name, table_lineage=table_lineage)

        print(f"time_lineage_storage: {list(table_lineage_storage._with_table.keys())}")

        # 初始化当前层级的表名规范器
        table_name_analyzer = CurrentLevelTableNameAnalyzer(select_statement)
        print(f"table_name_analyzer: {table_name_analyzer}")

        # 处理当前层级的引用字段逻辑
        data_lineage = []
        for standard_column, quote_columns in self.get_current_level_stand_column_used_quote_columns(
                select_statement=select_statement,
                table_lineage_storage=table_lineage_storage,
                table_name_analyzer=table_name_analyzer):
            source_column_list = []
            for quote_column in quote_columns:
                if quote_column.table_name is not None:
                    from_standard_table = table_name_analyzer.get_standard_table(quote_column.table_name)
                    from_table_lineage = table_lineage_storage.get_table_lineage(from_standard_table)
                    source_column_list.extend(from_table_lineage.get_source_column_list(quote_column.column_name))
                else:
                    already_match = False  # 是否已经匹配到上游表
                    for from_standard_table in table_name_analyzer.get_all_standard_table():
                        from_table_lineage = table_lineage_storage.get_table_lineage(from_standard_table)
                        if not from_table_lineage.has_column(quote_column.column_name):
                            continue
                        if already_match is True:
                            raise AnalyzerError("同一个字段可以匹配到多个上游表")
                        already_match = False
                        source_column_list.extend(from_table_lineage.get_source_column_list(quote_column.column_name))
            data_lineage.append((standard_column, source_column_list))
        return TableLineage(data_lineage=data_lineage)

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
        """获取 ASTSingleSelectStatement 节点当前层级标准字段对象和使用的应用字段对象的映射关系"""
        result = []
        column_idx = 1
        for column in select_statement.select_clause.columns:
            if column.alias is not None:  # 有别名的情况（此时一定不是通配符）
                standard_column = StandardColumn(column_name=column.alias.name, column_idx=column_idx)
                column_idx += 1
                result.append((standard_column, CurrentLevelUsedQuoteColumn.handle(column.column)))
            elif isinstance(column.column, core.ASTColumnNameExpression):  # 直接使用字段的情况
                # TODO 待修改属性名：column.column_value.column_name
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
                        # TODO 多个表的有序性
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
                result.append((standard_column, CurrentLevelUsedQuoteColumn.handle(column.column)))
        return result
