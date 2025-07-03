"""
聚集函数表达式（sum expression）
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression

if TYPE_CHECKING:
    from metasequoia_sql.ast.clause import Window
    from metasequoia_sql.ast.clause import OrderByClause
    from metasequoia_sql.ast.basic import StringLiteral

__all__ = [
    "FuncSumDistinctBase",
    "FuncSumAvg",
    "FuncSumBitAnd",
    "FuncSumBitOr",
    "FuncSumJsonArrayAgg",
    "FuncSumJsonObjectAgg",
    "FuncSumStCollect",
    "FuncSumBitXor",
    "FuncSumCountStar",
    "FuncSumCount",
    "FuncSumMin",
    "FuncSumMax",
    "FuncSumStd",
    "FuncSumVariance",
    "FuncSumStddevSamp",
    "FuncSumVarSamp",
    "FuncSumSum",
    "FuncSumGroupConcat",
    "FunctionSumGrouping",
]


class FuncSumBase(Expression):
    """聚集函数的基类"""

    __slots__ = ["_param", "_window_clause"]

    def __init__(self, param: Expression, window_clause: Optional["Window"]):
        """初始化聚集函数基类
        
        Parameters
        ----------
        param : Expression
            参数表达式
        window_clause : Optional[Window]
            窗口子句
        """
        self._param = param
        self._window_clause = window_clause

    @property
    def param(self) -> Expression:
        """获取参数表达式
        
        Returns
        -------
        Expression
            参数表达式
        """
        return self._param

    @property
    def window_clause(self) -> Optional["Window"]:
        """获取窗口子句
        
        Returns
        -------
        Optional[Window]
            窗口子句
        """
        return self._window_clause


class FuncSumDistinctBase(FuncSumBase):
    """包含可选的 DISTINCT 关键字的聚集函数的基类"""

    __slots__ = ["_param", "_distinct"]

    def __init__(self, param: Expression, distinct: bool, window_clause: Optional["Window"]):
        """初始化包含 DISTINCT 的聚集函数基类
        
        Parameters
        ----------
        param : Expression
            参数表达式
        distinct : bool
            是否为 DISTINCT
        window_clause : Optional[Window]
            窗口子句
        """
        super().__init__(param, window_clause)
        self._distinct = distinct

    @property
    def distinct(self) -> bool:
        """获取是否为 DISTINCT
        
        Returns
        -------
        bool
            是否为 DISTINCT
        """
        return self._distinct


class FuncSumAvg(FuncSumDistinctBase):
    """聚集函数：avg() """


class FuncSumBitAnd(FuncSumBase):
    """聚集函数：bit_and()"""


class FuncSumBitOr(FuncSumBase):
    """聚集函数：bit_or()"""


class FuncSumJsonArrayAgg(FuncSumBase):
    """聚集函数：json_arrayagg()"""


class FuncSumJsonObjectAgg(Expression):
    """聚集函数：json_objectagg()"""

    __slots__ = ["_param1", "_param2", "_window_clause"]

    def __init__(self, param1: Expression, param2: Expression, window_clause: Optional["Window"]):
        """初始化 JSON_OBJECTAGG 聚集函数
        
        Parameters
        ----------
        param1 : Expression
            第一个参数表达式
        param2 : Expression
            第二个参数表达式
        window_clause : Optional[Window]
            窗口子句
        """
        self._param1 = param1
        self._param2 = param2
        self._window_clause = window_clause

    @property
    def param1(self) -> Expression:
        """获取第一个参数表达式
        
        Returns
        -------
        Expression
            第一个参数表达式
        """
        return self._param1

    @property
    def param2(self) -> Expression:
        """获取第二个参数表达式
        
        Returns
        -------
        Expression
            第二个参数表达式
        """
        return self._param2

    @property
    def window_clause(self) -> Optional["Window"]:
        """获取窗口子句
        
        Returns
        -------
        Optional[Window]
            窗口子句
        """
        return self._window_clause


class FuncSumStCollect(FuncSumDistinctBase):
    """聚集函数：st_collect()"""


class FuncSumBitXor(FuncSumBase):
    """聚集函数：bit_xor()"""


class FuncSumCountStar(Expression):
    """聚集函数：count(*)"""

    __slots__ = ["_window_clause"]

    def __init__(self, window_clause: Optional["Window"]):
        """初始化 COUNT(*) 聚集函数
        
        Parameters
        ----------
        window_clause : Optional[Window]
            窗口子句
        """
        self._window_clause = window_clause

    @property
    def window_clause(self) -> Optional["Window"]:
        """获取窗口子句
        
        Returns
        -------
        Optional[Window]
            窗口子句
        """
        return self._window_clause


class FuncSumCount(FuncSumDistinctBase):
    """聚集函数：count()"""


class FuncSumMin(FuncSumDistinctBase):
    """聚集函数：min()"""


class FuncSumMax(FuncSumDistinctBase):
    """聚集函数：max()"""


class FuncSumStd(FuncSumBase):
    """聚集函数：std()"""


class FuncSumVariance(FuncSumBase):
    """聚集函数：variance()"""


class FuncSumStddevSamp(FuncSumBase):
    """聚集函数：stddev_samp()"""


class FuncSumVarSamp(FuncSumBase):
    """聚集函数：var_samp()"""


class FuncSumSum(FuncSumDistinctBase):
    """聚集函数：sum()"""


class FuncSumGroupConcat(Expression):
    """聚集函数：group_concat()"""

    __slots__ = ("_distinct", "_param_list", "_order_by_clause", "_separator", "_window_clause")

    def __init__(self,
                 distinct: bool,
                 param_list: List[Expression],
                 order_by_clause: Optional["OrderByClause"],
                 separator: Optional["StringLiteral"],
                 window_clause: Optional["Window"]):
        # pylint: disable=R0913,R0917
        """初始化 GROUP_CONCAT 聚集函数
        
        Parameters
        ----------
        distinct : bool
            是否为 DISTINCT
        param_list : List[Expression]
            参数列表
        order_by_clause : Optional[OrderByClause]
            ORDER BY 子句
        separator : Optional[StringLiteral]
            分隔符
        window_clause : Optional[Window]
            窗口子句
        """
        self._distinct = distinct
        self._param_list = param_list
        self._order_by_clause = order_by_clause
        self._separator = separator
        self._window_clause = window_clause

    @property
    def distinct(self) -> bool:
        """获取是否为 DISTINCT
        
        Returns
        -------
        bool
            是否为 DISTINCT
        """
        return self._distinct

    @property
    def param_list(self) -> List[Expression]:
        """获取参数列表
        
        Returns
        -------
        List[Expression]
            参数列表
        """
        return self._param_list

    @property
    def order_by_clause(self) -> Optional["OrderByClause"]:
        """获取 ORDER BY 子句
        
        Returns
        -------
        Optional[OrderByClause]
            ORDER BY 子句
        """
        return self._order_by_clause

    @property
    def separator(self) -> Optional["StringLiteral"]:
        """获取分隔符
        
        Returns
        -------
        Optional[StringLiteral]
            分隔符
        """
        return self._separator

    @property
    def window_clause(self) -> Optional["Window"]:
        """获取窗口子句
        
        Returns
        -------
        Optional[Window]
            窗口子句
        """
        return self._window_clause


class FunctionSumGrouping(Expression):
    """GROUPING 函数"""

    __slots__ = ("_param_list",)

    def __init__(self, param_list: List[Expression]):
        """初始化 GROUPING 函数
        
        Parameters
        ----------
        param_list : List[Expression]
            参数列表
        """
        self._param_list = param_list

    @property
    def param_list(self) -> List[Expression]:
        """获取参数列表
        
        Returns
        -------
        List[Expression]
            参数列表
        """
        return self._param_list
