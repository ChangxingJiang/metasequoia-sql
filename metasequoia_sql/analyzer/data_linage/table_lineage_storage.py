"""
表数据血缘分析器
"""

from typing import Dict

from metasequoia_sql.analyzer.data_linage.node import StandardTable
from metasequoia_sql.analyzer.data_linage.table_lineage import TableLineage
from metasequoia_sql.analyzer.tool import CreateTableStatementGetter

__all__ = ["TableLineageStorage"]


class TableLineageStorage:
    """表数据血缘存储器"""

    def __init__(self, create_table_statement_getter: CreateTableStatementGetter):
        self._with_table: Dict[str, TableLineage] = {}  # WITH 语句生成的临时表
        self._create_table_statement_getter = create_table_statement_getter  # 建表语句查询器

    def add_with_table(self, table_name: str, table_lineage: TableLineage):
        """添加一个临时表"""
        self._with_table[table_name] = table_lineage

    def get_table_lineage(self, table: StandardTable):
        """获取表数据血缘对象：优先在 WITH 语句的临时表中查询，如果查询不到则查询建表语句构造"""
        if table.table_name in self._with_table:
            return self._with_table[table.table_name]
        create_table_statement = self._create_table_statement_getter.get_statement(table.source())
        return TableLineage.by_create_table_statement(create_table_statement)
