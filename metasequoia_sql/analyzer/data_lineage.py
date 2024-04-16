"""
数据血缘分析器
"""

from typing import List, Any

from metasequoia_sql.core import SQLInsertStatement
from metasequoia_sql.analyzer.base import AnalyzerBase
from metasequoia_sql.analyzer.tool import CreateTableStatementGetter, check_node_type


class DataLineageAnalyzer(AnalyzerBase):
    """数据血缘分析器"""

    def __init__(self, create_table_statement_getter: CreateTableStatementGetter):
        self.create_table_statement_getter = create_table_statement_getter

    @check_node_type(SQLInsertStatement)
    def handle(self, node: SQLInsertStatement) -> List[Any]:
        """入口函数"""
        # 解析 INSERT INTO 语句中的字段顺序
        if node.columns is not None:
            insert_columns = [column for column in node.columns]
