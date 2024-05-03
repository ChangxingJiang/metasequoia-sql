"""
基础工具

TODO 整理工具函数，将其中的对象移动到 core 中
"""

import abc
import dataclasses
from typing import Type

from metasequoia_sql.core import ASTCreateTableStatement, SQLParser, ASTBase
from metasequoia_sql.errors import AnalyzerError

__all__ = ["CreateTableStatementGetter", "check_node_type", "QuoteColumn", "QuoteIndexColumn"]


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class QuoteColumn:
    """引用字段（在 GROUP BY、ORDER BY 等子句中使用）"""

    @abc.abstractmethod
    def source(self):
        """引用字段的源代码"""


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class QuoteIndexColumn(QuoteColumn):
    """使用顺序下标引用的字段"""
    column_index: int = dataclasses.field(kw_only=True)

    def source(self):
        """引用字段的源代码"""
        return f"{self.column_index}"


class CreateTableStatementGetter(abc.ABC):
    """建表语句获取器的抽象类"""

    def __init__(self):
        self._cache = {}

    def get_statement(self, full_table_name: str) -> ASTCreateTableStatement:
        """获取 table_name 的语法树节点"""
        if full_table_name not in self._cache:
            self._cache[full_table_name] = SQLParser.parse_create_table_statement(self.get_sql(full_table_name))
        return self._cache[full_table_name]

    @abc.abstractmethod
    def get_sql(self, full_table_name: str) -> str:
        """获取 table_name 表的建表语句"""


def check_node_type(node_type: Type[ASTBase]):
    """检查节点类型"""

    def wrapper(func):
        def inner_wrapper(self, node):
            if not isinstance(node, node_type):
                raise AnalyzerError(f"分析器类型不匹配: 预期={node_type.__name__}, 实际={node.__class__.__name__}")
            return func(self, node)

        return inner_wrapper

    return wrapper
