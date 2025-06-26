"""
窗口函数表达式（window function expression）
"""

from enum import IntEnum, auto
from typing import Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import Expression, Node

if TYPE_CHECKING:
    from metasequoia_sql.ast.clause import Window

__all__ = [
    # 窗口函数表达式的组成元素
    "FromFirstOrLast",
    "NullTreatment",
    "LeadOrLagInfo",

    # 窗口函数表达式
    "FuncWindowRowNumber",
    "FuncWindowRank",
    "FuncWindowDenseRank",
    "FuncWindowCumeDist",
    "FuncWindowPercentRank",
    "FuncWindowNtile",
    "FuncWindowLead",
    "FuncWindowLag",
    "FuncWindowFirstValue",
    "FuncWindowLastValue",
    "FuncWindowNthValue",
]


class FromFirstOrLast(IntEnum):
    """NTH_VALUE 窗口函数的 FROM 子句"""

    NONE = auto()  # %empty
    FROM_FIRST = auto()  # FROM FIRST
    FROM_LAST = auto()  # FROM LAST


class NullTreatment(IntEnum):
    """窗口函数中指定 NULL 值处理策略的 RESPECT NULLS 或 IGNORE NULLS 子句"""

    NONE = auto()  # %empty
    RESPECT_NULLS = auto()  # RESPECT NULLS
    IGNORE_NULLS = auto()  # IGNORE NULLS


class LeadOrLagInfo(Node):
    """LEAD 和 LAG 窗口函数中偏移量及默认值信息（解析过程中临时使用）"""

    __slots__ = ["_offset", "_default_value"]

    def __init__(self, offset: Optional[Expression], default_value: Optional[Expression]):
        """初始化 LEAD/LAG 信息
        
        Parameters
        ----------
        offset : Optional[Expression]
            偏移量表达式
        default_value : Optional[Expression]
            默认值表达式
        """
        self._offset = offset
        self._default_value = default_value

    @property
    def offset(self) -> Optional[Expression]:
        """获取偏移量表达式
        
        Returns
        -------
        Optional[Expression]
            偏移量表达式
        """
        return self._offset

    @property
    def default_value(self) -> Optional[Expression]:
        """获取默认值表达式
        
        Returns
        -------
        Optional[Expression]
            默认值表达式
        """
        return self._default_value


class FuncWindowBase(Expression):
    """窗口函数的基类"""

    __slots__ = ["_window_clause"]

    def __init__(self, window_clause: "Window"):
        """初始化窗口函数基类
        
        Parameters
        ----------
        window_clause : Window
            窗口子句
        """
        self._window_clause = window_clause

    @property
    def window_clause(self) -> "Window":
        """获取窗口子句
        
        Returns
        -------
        Window
            窗口子句
        """
        return self._window_clause


class FuncWindowRowNumber(FuncWindowBase):
    """ROW_NUMBER 窗口函数"""


class FuncWindowRank(FuncWindowBase):
    """RANK 窗口函数"""


class FuncWindowDenseRank(FuncWindowBase):
    """DENSE_RANK 窗口函数"""


class FuncWindowCumeDist(FuncWindowBase):
    """CUME_DIST 窗口函数"""


class FuncWindowPercentRank(FuncWindowBase):
    """PERCENT_RANK 窗口函数"""


class FuncWindowNtile(FuncWindowBase):
    """NTILE 窗口函数"""

    __slots__ = ["_param"]

    def __init__(self, param: Expression, window_clause: "Window"):
        """初始化 NTILE 窗口函数
        
        Parameters
        ----------
        param : Expression
            参数表达式
        window_clause : Window
            窗口子句
        """
        super().__init__(window_clause)
        self._param = param

    @property
    def param(self) -> Expression:
        """获取参数表达式
        
        Returns
        -------
        Expression
            参数表达式
        """
        return self._param


class FuncWindowLeadOrLag(FuncWindowBase):
    """LEAD 窗口函数和 LAG 窗口函数的抽象类"""

    __slots__ = ["_param", "_offset", "_default_value", "_null_treatment"]

    def __init__(self, param: Expression, offset: Optional[Expression], default_value: Optional[Expression],
                 null_treatment: NullTreatment, window_clause: "Window"):
        # pylint: disable=R0913
        """初始化 LEAD/LAG 窗口函数基类
        
        Parameters
        ----------
        param : Expression
            参数表达式
        offset : Optional[Expression]
            偏移量表达式
        default_value : Optional[Expression]
            默认值表达式
        null_treatment : NullTreatment
            NULL 处理策略
        window_clause : Window
            窗口子句
        """
        super().__init__(window_clause)
        self._param = param
        self._offset = offset
        self._default_value = default_value
        self._null_treatment = null_treatment

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
    def offset(self) -> Optional[Expression]:
        """获取偏移量表达式
        
        Returns
        -------
        Optional[Expression]
            偏移量表达式
        """
        return self._offset

    @property
    def default_value(self) -> Optional[Expression]:
        """获取默认值表达式
        
        Returns
        -------
        Optional[Expression]
            默认值表达式
        """
        return self._default_value

    @property
    def null_treatment(self) -> NullTreatment:
        """获取 NULL 处理策略
        
        Returns
        -------
        NullTreatment
            NULL 处理策略
        """
        return self._null_treatment


class FuncWindowLead(FuncWindowLeadOrLag):
    """LEAD 窗口函数"""


class FuncWindowLag(FuncWindowLeadOrLag):
    """LAG 窗口函数"""


class FuncWindowFirstValueOrLastValue(FuncWindowBase):
    """FIRST_VALUE 窗口函数和 LAST_VALUE 窗口函数的抽象类"""

    __slots__ = ["_param", "_null_treatment"]

    def __init__(self, param: Expression, null_treatment: NullTreatment, window_clause: "Window"):
        """初始化 FIRST_VALUE/LAST_VALUE 窗口函数基类
        
        Parameters
        ----------
        param : Expression
            参数表达式
        null_treatment : NullTreatment
            NULL 处理策略
        window_clause : Window
            窗口子句
        """
        super().__init__(window_clause)
        self._param = param
        self._null_treatment = null_treatment

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
    def null_treatment(self) -> NullTreatment:
        """获取 NULL 处理策略
        
        Returns
        -------
        NullTreatment
            NULL 处理策略
        """
        return self._null_treatment


class FuncWindowFirstValue(FuncWindowFirstValueOrLastValue):
    """FIRST_VALUE 窗口函数"""


class FuncWindowLastValue(FuncWindowFirstValueOrLastValue):
    """LAST_VALUE 窗口函数"""


class FuncWindowNthValue(FuncWindowBase):
    """NTH_VALUE 窗口函数"""

    __slots__ = ["_param1", "_param2", "_from_first_or_last", "_null_treatment"]

    def __init__(self, param_1: Expression, param_2: Expression, from_first_or_last: FromFirstOrLast,
                 null_treatment: NullTreatment, window_clause: "Window"):
        # pylint: disable=R0913
        """初始化 NTH_VALUE 窗口函数
        
        Parameters
        ----------
        param_1 : Expression
            第一个参数表达式
        param_2 : Expression
            第二个参数表达式
        from_first_or_last : FromFirstOrLast
            FROM FIRST/LAST 选项
        null_treatment : NullTreatment
            NULL 处理策略
        window_clause : Window
            窗口子句
        """
        super().__init__(window_clause)
        self._param1 = param_1
        self._param2 = param_2
        self._from_first_or_last = from_first_or_last
        self._null_treatment = null_treatment

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
    def from_first_or_last(self) -> FromFirstOrLast:
        """获取 FROM FIRST/LAST 选项
        
        Returns
        -------
        FromFirstOrLast
            FROM FIRST/LAST 选项
        """
        return self._from_first_or_last

    @property
    def null_treatment(self) -> NullTreatment:
        """获取 NULL 处理策略
        
        Returns
        -------
        NullTreatment
            NULL 处理策略
        """
        return self._null_treatment
