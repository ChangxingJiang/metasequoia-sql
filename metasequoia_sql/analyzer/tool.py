"""
基础工具
"""

import abc
import dataclasses
from typing import Type, Optional

from metasequoia_sql.core import SQLCreateTableStatement, SQLParser, SQLBase
from metasequoia_sql.errors import AnalyzerError

__all__ = ["CreateTableStatementGetter", "check_node_type", "SelectColumn", "SourceColumn"]


@dataclasses.dataclass(slots=True, frozen=True)
class SelectColumn:
    """SELECT 子句中查询的字段"""
    column_name: str = dataclasses.field(kw_only=True)  # 字段名称
    column_idx: str = dataclasses.field(kw_only=True)  # 字段顺序下标


@dataclasses.dataclass(slots=True, frozen=True)
class SourceColumn:
    """数据来源字段"""
    schema_name: Optional[str] = dataclasses.field(kw_only=True, default=None)
    table_name: Optional[str] = dataclasses.field(kw_only=True, default=None)
    column_name: str = dataclasses.field(kw_only=True)


class CreateTableStatementGetter(abc.ABC):
    """建表语句获取器的抽象类"""

    def __init__(self):
        self._cache = {}

    def get_create_table_statement(self, table_name: str) -> SQLCreateTableStatement:
        """获取 table_name 的语法树节点"""
        if table_name not in self._cache:
            self._cache[table_name] = SQLParser.parse_statements(self.get_create_table_sql(table_name))
        return self._cache[table_name]

    @abc.abstractmethod
    def get_create_table_sql(self, table_name: str) -> str:
        """获取 table_name 表的建表语句"""


def check_node_type(node_type: Type[SQLBase]):
    """检查节点类型"""

    def wrapper(func):
        def inner_wrapper(self, node):
            if not isinstance(node, node_type):
                raise AnalyzerError(f"分析器类型不匹配: 预期={node_type.__name__}, 实际={node.__class__.__name__}")
            return func(self, node)

        return inner_wrapper

    return wrapper
