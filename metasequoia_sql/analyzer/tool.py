"""
基础工具

TODO 整理工具函数，将其中的对象移动到 core 中
"""

import abc
import dataclasses
from typing import Type, Optional

from metasequoia_sql.core import SQLCreateTableStatement, SQLParser, SQLBase
from metasequoia_sql.errors import AnalyzerError

__all__ = ["CreateTableStatementGetter", "check_node_type",
           "SelectColumn", "SourceColumn", "QuoteColumn", "QuoteNameColumn", "QuoteIndexColumn",
           "QuoteTable", "SourceTable"]


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class SelectColumn:
    """下游表字段（SELECT 子句中的字段）"""

    column_name: str = dataclasses.field(kw_only=True)  # 字段名称
    column_idx: str = dataclasses.field(kw_only=True)  # 字段顺序下标

    def source(self):
        """引用字段的源代码"""
        return f"{self.column_name}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class SourceColumn:
    """上游表字段"""
    schema_name: Optional[str] = dataclasses.field(kw_only=True, default="")
    table_name: Optional[str] = dataclasses.field(kw_only=True, default="")
    column_name: str = dataclasses.field(kw_only=True)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class QuoteColumn:
    """引用字段（在 GROUP BY、ORDER BY 等子句中使用）"""

    @abc.abstractmethod
    def source(self):
        """引用字段的源代码"""


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class QuoteNameColumn(QuoteColumn):
    """使用表名、字段名（这里的字段名可能是别名）引用的字段"""

    table_name: Optional[str] = dataclasses.field(kw_only=True, default="")
    column_name: str = dataclasses.field(kw_only=True)

    def source(self):
        """引用字段的源代码"""
        if self.table_name is not None:
            return f"{self.table_name}.{self.column_name}"
        else:
            return f"{self.column_name}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class QuoteIndexColumn(QuoteColumn):
    """使用顺序下标引用的字段"""
    column_index: int = dataclasses.field(kw_only=True)

    def source(self):
        """引用字段的源代码"""
        return f"{self.column_index}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class QuoteTable:
    """使用模式名、表名引用的表（表名也允许是别名或临时表）"""

    schema_name: Optional[str] = dataclasses.field(kw_only=True, default="")
    table_name: str

    def source(self):
        """引用字段的源代码"""
        if self.schema_name is not None:
            return f"{self.schema_name}.{self.table_name}"
        else:
            return f"{self.table_name}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class SourceTable:
    """使用 "模式名 + 表名" 或 "表名" 引用的源表（别名允许是 with 语句产生的临时表）"""

    schema_name: Optional[str] = dataclasses.field(kw_only=True, default="")
    table_name: str

    def source(self):
        """引用字段的源代码"""
        if self.schema_name is not None:
            return f"{self.schema_name}.{self.table_name}"
        else:
            return f"{self.table_name}"


class CreateTableStatementGetter(abc.ABC):
    """建表语句获取器的抽象类"""

    def __init__(self):
        self._cache = {}

    def get_statement(self, full_table_name: str) -> SQLCreateTableStatement:
        """获取 table_name 的语法树节点"""
        if full_table_name not in self._cache:
            self._cache[full_table_name] = SQLParser.parse_create_table_statement(self.get_sql(full_table_name))
        return self._cache[full_table_name]

    @abc.abstractmethod
    def get_sql(self, full_table_name: str) -> str:
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
