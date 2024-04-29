"""
表数据血缘分析器
"""

from typing import Optional

from metasequoia_sql import core
from metasequoia_sql.analyzer.data_linage.table_lineage import TableLineage
from metasequoia_sql.analyzer.data_linage.table_lineage_storage import TableLineageStorage
from metasequoia_sql.analyzer.tool import CreateTableStatementGetter
from metasequoia_sql.analyzer.toolkit import CurrentLevelSubQuery

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
        sub_query_lineage = {}
        for alias_name in current_level_sub_query.get_all_sub_query_alias_name():
            sub_query_select_statement = current_level_sub_query.get_sub_query_statement(alias_name)
            sub_query_lineage[alias_name] = self.get_table_lineage(sub_query_select_statement, table_lineage_storage)

        # 处理当前层级的引用字段逻辑
