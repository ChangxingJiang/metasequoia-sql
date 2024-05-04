"""
基础工具
"""

import abc
import dataclasses
import os
from typing import Optional

from metasequoia_sql.core import ASTCreateTableStatement, SQLParser

__all__ = ["CreateTableStatementGetter", "QuoteColumn", "QuoteIndexColumn"]


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

    def __init__(self, disk_path: Optional[str]):
        self._disk_path = disk_path  # 本地磁盘暂存地址
        self._memory_cache = {}  # 内存缓存

        # 如果指定了本地暂存地址，则读取本地磁盘暂存的表名
        if self._disk_path is not None:
            self._disk_cache = {file_name.replace(".sql", "") for file_name in os.listdir(self._disk_path)}
        else:
            self._disk_cache = set()

    def get_statement(self, full_table_name: str) -> ASTCreateTableStatement:
        """获取 table_name 的语法树节点"""
        if full_table_name not in self._memory_cache:
            # 设置本地磁盘暂存的情况
            if self._disk_path is not None:
                if full_table_name in self._disk_cache:
                    sql = self.load_from_disk(full_table_name)  # 从本地磁盘暂存读取建表语句
                else:
                    sql = self.get_sql(full_table_name)
                    self.save_to_disk(full_table_name, sql)  # 从本地磁盘读取暂存的建表语句
            # 没有设置本地磁盘暂存的情况
            else:
                sql = self.get_sql(full_table_name)
            self._memory_cache[full_table_name] = SQLParser.parse_create_table_statement(sql)
        return self._memory_cache[full_table_name]

    def load_from_disk(self, full_table_name: str) -> str:
        """从本地磁盘读取暂存的建表语句"""
        with open(os.path.join(self._disk_path, f"{full_table_name}.sql"), "r", encoding="UTF-8") as file:
            return file.read()

    def save_to_disk(self, full_table_name: str, sql: str) -> None:
        """从本地磁盘读取暂存的建表语句"""
        self._disk_cache.add(full_table_name)
        with open(os.path.join(self._disk_path, f"{full_table_name}.sql"), "w", encoding="UTF-8") as file:
            file.write(sql)

    @abc.abstractmethod
    def get_sql(self, full_table_name: str) -> str:
        """获取 table_name 表的建表语句"""
