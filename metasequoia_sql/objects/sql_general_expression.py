"""
一般表达式的抽象基类
"""

import abc
from typing import List

from metasequoia_sql.objects.data_source import DataSource
from metasequoia_sql.objects.sql_base import SQLBase

__all__ = ["SQLGeneralExpression"]


# ---------------------------------------- 一般表达式的抽象基类 ----------------------------------------


class SQLGeneralExpression(SQLBase, abc.ABC):
    """一般表达式"""

    @abc.abstractmethod
    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """TODO 待移除"""

    @abc.abstractmethod
    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
