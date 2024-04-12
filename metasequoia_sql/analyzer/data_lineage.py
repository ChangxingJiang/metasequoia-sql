"""
数据血缘分析器
"""

from typing import List

from metasequoia_sql.common import *
from metasequoia_sql.core import *


class DataLineageAnalyzer:
    def __init__(self, sql: str, data_source: DataSource):
        # 过滤所有的 INSERT 语句
        self.statements: List[SQLInsertStatement] = [
            statement for statement in parse_statements(build_token_scanner(sql))
            if isinstance(statement, SQLInsertStatement)]

        # 统计所有 INSERT 语句中涉及的表名
        self.used_table_set = set()
        for statement in self.statements:
            self.used_table_set.add(statement.table_name.source(data_source))
            self.used_table_set |= set(statement.get_used_table_list())

        # 定义建表语句的清单
        self.create_table_statements = {}

    def get_table_list(self) -> List[str]:
        return list(self.used_table_set)