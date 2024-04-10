"""
SQL 语句对象节点的抽象基类
"""

import abc

from metasequoia_sql.common import TokenScanner
from metasequoia_sql.core.data_source import DataSource

__all__ = ["SQLBase", "SQLBaseTemp"]


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


class SQLBaseTemp(SQLBase, abc.ABC):
    """
    开发中的临时抽象节点，部分不使用参数的节点可以继承它

    TODO 待全部节点开发完成后移除
    """

    @staticmethod
    @abc.abstractmethod
    def check(scanner: TokenScanner) -> bool:
        """检查扫描器当前位置是否为目标元素"""
        return True

    @staticmethod
    @abc.abstractmethod
    def parse(scanner: TokenScanner) -> "SQLBaseTemp":
        """从扫描器当前位置解析目标元素"""
