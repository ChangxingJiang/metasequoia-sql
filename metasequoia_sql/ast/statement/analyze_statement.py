"""
ANALYZE TABLE 语句（analyze table statement）
"""

from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Node, Statement

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Identifier

__all__ = [
    "HistogramUpdateParam",
    "EnumHistogramCommandType",
    "Histogram",
    "AnalyzeTableStatement",
]


class HistogramUpdateParam(Node):
    """直方图的更新参数"""

    __slots__ = (
        "_num_buckets",
        "_data"
    )

    def __init__(self, num_buckets: Optional[int], data: Optional[str]):
        self._num_buckets = num_buckets
        self._data = data

    @property
    def num_buckets(self) -> Optional[int]:
        """
        直方图桶数量

        Returns
        -------
        Optional[int]
            直方图桶数量
        """
        return self._num_buckets

    @property
    def data(self) -> Optional[str]:
        """
        直方图数据

        Returns
        -------
        Optional[str]
            直方图数据
        """
        return self._data


class EnumHistogramCommandType(IntEnum):
    """直方图命令类型的枚举值"""

    NONE = 0
    UPDATE = 1
    DROP = 2


class Histogram(Node):
    """直方图"""

    __slots__ = (
        "_command_type",
        "_column_list",
        "_update_param"
    )

    def __init__(self, command_type: EnumHistogramCommandType, column_list: List[str],
                 update_param: Optional[HistogramUpdateParam]):
        self._command_type = command_type
        self._column_list = column_list
        self._update_param = update_param

    @property
    def command_type(self) -> EnumHistogramCommandType:
        """
        直方图命令类型

        Returns
        -------
        EnumHistogramCommandType
            直方图命令类型
        """
        return self._command_type

    @property
    def column_list(self) -> List[str]:
        """
        列名列表

        Returns
        -------
        List[str]
            列名列表
        """
        return self._column_list

    @property
    def update_param(self) -> Optional[HistogramUpdateParam]:
        """
        直方图更新参数

        Returns
        -------
        Optional[HistogramUpdateParam]
            直方图更新参数
        """
        return self._update_param


class AnalyzeTableStatement(Statement):
    """ANALYZE TABLE 语句"""

    __slots__ = (
        "_no_write_to_binlog",
        "_table_list",
        "_opt_histogram"
    )

    def __init__(self, no_write_to_binlog: bool, table_list: List["Identifier"], opt_histogram: Optional[Histogram]):
        self._no_write_to_binlog = no_write_to_binlog
        self._table_list = table_list
        self._opt_histogram = opt_histogram

    @property
    def no_write_to_binlog(self) -> bool:
        """
        是否不写入二进制日志

        Returns
        -------
        bool
            是否不写入二进制日志
        """
        return self._no_write_to_binlog

    @property
    def table_list(self) -> List["Identifier"]:
        """
        表标识符列表

        Returns
        -------
        List["Identifier"]
            表标识符列表
        """
        return self._table_list

    @property
    def opt_histogram(self) -> Optional[Histogram]:
        """
        可选的直方图

        Returns
        -------
        Optional[Histogram]
            可选的直方图
        """
        return self._opt_histogram
