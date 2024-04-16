"""
数据血缘分析器
"""

import abc
from typing import List, Optional, Any

from metasequoia_sql import SQLBase, SQLInsertStatement
from metasequoia_sql.analyzer.base import AnalyzerRecursionBase


class CreateTableStatementGetter(abc.ABC):
    """建表语句获取器的抽象类"""

    @abc.abstractmethod
    def get_create_table_statement(self, table_name: str) -> str:
        """获取 table_name 表的建表语句"""


class DataLineageAnalyzer(AnalyzerRecursionBase):
    """数据血缘分析器"""

    def __init__(self, create_table_statement_getter: CreateTableStatementGetter):
        self.create_table_statement_getter = create_table_statement_getter

    def handle(self, node: SQLInsertStatement) -> List[Any]:
        """入口函数"""

    def custom_handle_node(self, node: SQLBase) -> Optional[List[Any]]:
        pass
