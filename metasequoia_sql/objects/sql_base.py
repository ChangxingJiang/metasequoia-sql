"""
所有 SQL 语句对象节点的抽象基类
"""

import abc

from metasequoia_sql.objects.data_source import DataSource

__all__ = ["SQLBase"]


class SQLBase(abc.ABC):
    """SQL 语句对象节点的抽象基类

    TODO 待增加 parse 和 check 两个抽象静态方法
    """

    @abc.abstractmethod
    def source(self, data_source: DataSource) -> str:
        """返回 SQL 源码

        TODO 待将 MySQL 修改为自动指定
        """

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        """
        TODO 修改 source 生成规则
        """
        return f"<{self.__class__.__name__} source={self.source(DataSource.MYSQL)}>"
