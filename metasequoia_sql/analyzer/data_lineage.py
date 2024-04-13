"""
数据血缘分析器
"""

from typing import List

from metasequoia_sql.core import DataSource, parse_statements, SQLInsertStatement


class DataLineageAnalyzer:
    """
    数据血缘分析器
    """

    def __init__(self, sql: str, data_source: DataSource):
        # 过滤所有的 INSERT 语句
        self.statements: List[SQLInsertStatement] = [
            statement for statement in parse_statements(sql)
            if isinstance(statement, SQLInsertStatement)]

        # 统计所有 INSERT 语句中涉及的表名
        self.used_table_set = set()
        for statement in self.statements:
            self.used_table_set.add(statement.table_name.source(data_source))
            self.used_table_set |= set(statement.get_used_table_list())

        # 定义建表语句的清单
        self.create_table_statements = {}

    def get_table_list(self) -> List[str]:
        """获取上下游表的列表"""
        return list(self.used_table_set)
