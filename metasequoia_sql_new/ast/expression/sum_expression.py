"""
聚集函数表达式（sum expression）
"""

from typing import List, Optional
from typing import TYPE_CHECKING

from metasequoia_sql_new.ast.base import Expression

if TYPE_CHECKING:
    from metasequoia_sql_new.ast.clause import OverClause
    from metasequoia_sql_new.ast.clause import OrderByClause
    from metasequoia_sql_new.ast.basic import StringLiteral


class FuncSumBase(Expression):
    """聚集函数的基类"""

    def __init__(self, param: Expression, window_clause: Optional["OverClause"]):
        self._param = param
        self._window_clause = window_clause

    def attr_list(self) -> List[str]:
        return ["param", "window_clause"]

    @property
    def param(self) -> Expression:
        return self._param

    @property
    def window_clause(self) -> Optional["OverClause"]:
        return self._window_clause


class FuncSumDistinctBase(FuncSumBase):
    """包含可选的 DISTINCT 关键字的聚集函数的基类"""

    def __init__(self, param: Expression, distinct: bool, window_clause: Optional["OverClause"]):
        super().__init__(param, window_clause)
        self._distinct = distinct

    def attr_list(self) -> List[str]:
        return super().attr_list() + ["distinct"]

    @property
    def distinct(self) -> bool:
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

    def __init__(self, param1: Expression, param2: Expression, window_clause: Optional["OverClause"]):
        self._param1 = param1
        self._param2 = param2
        self._window_clause = window_clause

    def attr_list(self) -> List[str]:
        return ["param1", "param2", "window_clause"]

    @property
    def param1(self) -> Expression:
        return self._param1

    @property
    def param2(self) -> Expression:
        return self._param2

    @property
    def window_clause(self) -> Optional["OverClause"]:
        return self._window_clause


class FuncSumStCollect(FuncSumDistinctBase):
    """聚集函数：st_collect()"""


class FuncSumBitXor(FuncSumBase):
    """聚集函数：bit_xor()"""


class FuncSumCountStar(Expression):
    """聚集函数：count(*)"""

    def __init__(self, window_clause: Optional["OverClause"]):
        self._window_clause = window_clause

    def attr_list(self) -> List[str]:
        return ["window_clause"]

    @property
    def window_clause(self) -> Optional["OverClause"]:
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

    def __init__(self,
                 distinct: bool,
                 param_list: List[Expression],
                 order_by_clause: Optional["OrderByClause"],
                 separator: Optional["StringLiteral"],
                 window_clause: Optional["OverClause"]):
        self._distinct = distinct
        self._param_list = param_list
        self._order_by_clause = order_by_clause
        self._separator = separator
        self._window_clause = window_clause

    def attr_list(self) -> List[str]:
        return ["distinct", "param_list", "order_by_clause", "separator", "window_clause"]

    @property
    def distinct(self) -> bool:
        return self._distinct

    @property
    def param_list(self) -> List[Expression]:
        return self._param_list

    @property
    def order_by_clause(self) -> Optional["OrderByClause"]:
        return self._order_by_clause

    @property
    def separator(self) -> Optional["StringLiteral"]:
        return self._separator

    @property
    def window_clause(self) -> Optional["OverClause"]:
        return self._window_clause
