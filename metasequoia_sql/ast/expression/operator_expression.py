"""
函数类型节点
"""

from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import BinaryExpression, Expression, TernaryExpression, UnaryExpression
from metasequoia_sql.ast.enumeration import EnumCompareOperator, EnumFulltextOption

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Ident
    from metasequoia_sql.ast.phrase.time_interval import TimeInterval
    from metasequoia_sql.ast.statement.select_statement import QueryExpression

__all__ = [
    "OperatorNegative",
    "OperatorBitNot",
    "OperatorBitOr",
    "OperatorBitAnd",
    "OperatorShiftLeft",
    "OperatorShiftRight",
    "OperatorPlus",
    "OperatorDatePlus",
    "OperatorPlusDate",
    "OperatorMinus",
    "OperatorMinusDate",
    "OperatorMul",
    "OperatorDiv",
    "OperatorMod",
    "OperatorDivInt",
    "OperatorBitXor",
    "OperatorMemberOf",
    "OperatorBetween",
    "OperatorNotBetween",
    "OperatorSoundsLike",
    "OperatorLike",
    "OperatorNotLike",
    "OperatorRegexp",
    "OperatorNotRegexp",
    "OperatorIsNull",
    "OperatorIsNotNull",
    "OperatorCompare",
    "OperatorCompareAllOrAnyBase",
    "OperatorCompareAll",
    "OperatorCompareAny",
    "OperatorOr",
    "OperatorXor",
    "OperatorAnd",
    "OperatorNot",
    "OperatorIsTrue",
    "OperatorIsNotTrue",
    "OperatorIsFalse",
    "OperatorIsNotFalse",
    "OperatorIsUnknown",
    "OperatorIsUnknown",
    "OperatorIsNotUnknown",
    "OperatorTruthTransform",
    "OperatorCollate",
    "OperatorConcat",
    "EnumFulltextOption",
    "OperatorMatch",
    "OperatorBinary",
    "OperatorJsonSeparator",
    "OperatorInSubSelect",
    "OperatorNotInSubSelect",
    "OperatorInValues",
    "OperatorNotInValues",
]


class OperatorNegative(UnaryExpression):
    """内置函数：取相反数（`-` 运算符）"""


class OperatorBitNot(UnaryExpression):
    """内置函数：按位取反（`~` 运算符）"""


class OperatorBitOr(BinaryExpression):
    """内置函数：按位或（`|` 运算符）"""


class OperatorBitAnd(BinaryExpression):
    """内置函数：按位与（`&` 运算符）"""


class OperatorShiftLeft(BinaryExpression):
    """内置函数：左移位（`<<` 运算符）"""


class OperatorShiftRight(BinaryExpression):
    """内置函数：右移位（`>>` 运算符）"""


class OperatorPlus(BinaryExpression):
    """内置函数：加法（`+` 运算符）"""


class OperatorDatePlus(Expression):
    """内置 + 运算符，但 left_operand 为 time_interval 类型"""

    __slots__ = ["_left_operand", "_right_operand"]

    def __init__(self, left_operand: "TimeInterval", right_operand: Expression):
        """初始化日期加法运算符
        
        Parameters
        ----------
        left_operand : TimeInterval
            左操作数（时间间隔）
        right_operand : Expression
            右操作数
        """
        self._left_operand = left_operand
        self._right_operand = right_operand

    @property
    def left_operand(self) -> "TimeInterval":
        """获取左操作数
        
        Returns
        -------
        TimeInterval
            左操作数（时间间隔）
        """
        return self._left_operand

    @property
    def right_operand(self) -> Expression:
        """获取右操作数
        
        Returns
        -------
        Expression
            右操作数
        """
        return self._right_operand


class OperatorPlusDate(Expression):
    """内置 + 运算符，但 right_operand 为 time_interval 类型"""

    __slots__ = ["_left_operand", "_right_operand"]

    def __init__(self, left_operand: Expression, right_operand: "TimeInterval"):
        """初始化加日期运算符
        
        Parameters
        ----------
        left_operand : Expression
            左操作数
        right_operand : TimeInterval
            右操作数（时间间隔）
        """
        self._left_operand = left_operand
        self._right_operand = right_operand

    @property
    def left_operand(self) -> Expression:
        """获取左操作数
        
        Returns
        -------
        Expression
            左操作数
        """
        return self._left_operand

    @property
    def right_operand(self) -> "TimeInterval":
        """获取右操作数
        
        Returns
        -------
        TimeInterval
            右操作数（时间间隔）
        """
        return self._right_operand


class OperatorMinus(BinaryExpression):
    """内置函数：减法（`-` 运算符）"""


class OperatorMinusDate(Expression):
    """内置 - 运算符，但 right_operand 为 time_interval 类型"""

    __slots__ = ["_left_operand", "_right_operand"]

    def __init__(self, left_operand: Expression, right_operand: "TimeInterval"):
        """初始化减日期运算符
        
        Parameters
        ----------
        left_operand : Expression
            左操作数
        right_operand : TimeInterval
            右操作数（时间间隔）
        """
        self._left_operand = left_operand
        self._right_operand = right_operand

    @property
    def left_operand(self) -> Expression:
        """获取左操作数
        
        Returns
        -------
        Expression
            左操作数
        """
        return self._left_operand

    @property
    def right_operand(self) -> "TimeInterval":
        """获取右操作数
        
        Returns
        -------
        TimeInterval
            右操作数（时间间隔）
        """
        return self._right_operand


class OperatorMul(BinaryExpression):
    """内置函数：乘法（`*` 运算符）"""


class OperatorDiv(BinaryExpression):
    """内置函数：除法（`/` 运算符）"""


class OperatorMod(BinaryExpression):
    """内置函数：取模（`%` 运算符）"""


class OperatorDivInt(BinaryExpression):
    """内置函数：整数除法（`DIV` 关键字）"""


class OperatorBitXor(BinaryExpression):
    """内置函数：异或（`^` 关键字）"""


class OperatorMemberOf(BinaryExpression):
    """内置函数：MEMBER OF 关键字

    {left_operand} MEMBER [OF] ( {right_operand} )
    """


class OperatorBetween(TernaryExpression):
    """内置函数 BETWEEN 关键字

    {first_operand} BETWEEN {second_operand} AND {third_operand}
    """


class OperatorNotBetween(TernaryExpression):
    """内置函数 NOT BETWEEN 关键字

    {first_operand} NOT BETWEEN {second_operand} AND {third_operand}
    """


class OperatorSoundsLike(BinaryExpression):
    """内置函数 SOUNDS LIKE 关键字

    {left_operand} SOUNDS LIKE {right_operand}
    """


class OperatorLike(TernaryExpression):
    """内置函数 LIKE 关键字

    {first_operand} LIKE {second_operand} [ ESCAPE {third_operand} ]
    """


class OperatorNotLike(TernaryExpression):
    """内置函数 NOT LIKE 关键字

    {first_operand} NOT LIKE {second_operand} [ ESCAPE {third_operand} ]
    """


class OperatorRegexp(BinaryExpression):
    """内置函数 REGEXP 关键字

    {left_operand} REGEXP {right_operand}
    """


class OperatorNotRegexp(BinaryExpression):
    """内置函数 NOT REGEXP 关键字

    {left_operand} NOT REGEXP {right_operand}
    """


class OperatorIsNull(UnaryExpression):
    """内置函数 IS NULL 关键字

    {operand} IS NULL
    """


class OperatorIsNotNull(UnaryExpression):
    """内置函数 IS NOT NULL 关键字

    {operand} IS NOT NULL
    """


class OperatorCompare(BinaryExpression):
    """内置函数：比较运算符

    {left_operand} comp_op {right_operand}

    - 其中 comp_op 为比较运算符
    """

    __slots__ = ["_operator"]

    def __init__(self,
                 left_operand: Optional[Expression],
                 right_operand: Optional[Expression],
                 operator: EnumCompareOperator):
        """初始化比较运算符
        
        Parameters
        ----------
        left_operand : Optional[Expression]
            左操作数
        right_operand : Optional[Expression]
            右操作数
        operator : EnumCompareOperator
            比较运算符类型
        """
        super().__init__(left_operand, right_operand)
        self._operator = operator

    @property
    def operator(self) -> EnumCompareOperator:
        """获取比较运算符类型
        
        Returns
        -------
        EnumCompareOperator
            比较运算符类型
        """
        return self._operator


class OperatorCompareAllOrAnyBase(Expression):
    """内置 compare_operator ALL 运算符或 compare_operator ANY 运算符"""

    __slots__ = ["_operand", "_operator", "_subquery_expression"]

    def __init__(self, operand: Expression, operator: EnumCompareOperator, subquery_expression: "QueryExpression"):
        """初始化比较 ALL/ANY 运算符基类
        
        Parameters
        ----------
        operand : Expression
            操作数
        operator : EnumCompareOperator
            比较运算符类型
        subquery_expression : QueryExpression
            子查询表达式
        """
        self._operand = operand
        self._operator = operator
        self._subquery_expression = subquery_expression

    @property
    def operand(self) -> Expression:
        """获取操作数
        
        Returns
        -------
        Expression
            操作数
        """
        return self._operand

    @property
    def operator(self) -> EnumCompareOperator:
        """获取比较运算符类型
        
        Returns
        -------
        EnumCompareOperator
            比较运算符类型
        """
        return self._operator

    @property
    def subquery_expression(self) -> "QueryExpression":
        """获取子查询表达式
        
        Returns
        -------
        QueryExpression
            子查询表达式
        """
        return self._subquery_expression


class OperatorCompareAll(OperatorCompareAllOrAnyBase):
    """内置 compare_operator ALL 运算符"""


class OperatorCompareAny(OperatorCompareAllOrAnyBase):
    """内置 compare_operator ANY 运算符"""


class OperatorOr(BinaryExpression):
    """内置函数：逻辑或（`OR` 关键字）

    {left_operand} OR {right_operand}
    """


class OperatorXor(BinaryExpression):
    """内置函数：逻辑异或（`XOR` 关键字）

    {left_operand} XOR {right_operand}
    """


class OperatorAnd(BinaryExpression):
    """内置函数：逻辑与（`AND` 关键字）

    {left_operand} AND {right_operand}
    """


class OperatorNot(UnaryExpression):
    """内置函数：逻辑非（`NOT` 关键字）

    NOT {operand}
    """


class OperatorIsTrue(UnaryExpression):
    """内置函数 IS TRUE 关键字

    {operand} IS TRUE
    """


class OperatorIsNotTrue(UnaryExpression):
    """内置函数 IS NOT TRUE 关键字

    {operand} IS NOT TRUE
    """


class OperatorIsFalse(UnaryExpression):
    """内置函数 IS FALSE 关键字

    {operand} IS FALSE
    """


class OperatorIsNotFalse(UnaryExpression):
    """内置函数 IS NOT FALSE 关键字

    {operand} IS NOT FALSE
    """


class OperatorIsUnknown(UnaryExpression):
    """内置函数 IS UNKNOWN 关键字

    {operand} IS UNKNOWN
    """


class OperatorIsNotUnknown(UnaryExpression):
    """内置函数 IS NOT UNKNOWN 关键字

    {operand} IS NOT UNKNOWN
    """


class OperatorTruthTransform(UnaryExpression):
    """内置函数：真值变换（临时节点）"""


class OperatorCollate(Expression):
    """内置 COLLATE 关键字运算符（指定排序规则）

    collation_operand COLLATE collation_name
    """

    __slots__ = ["_collation_operand", "_collation_name"]

    def __init__(self, collation_operand: Expression, collation_name: str):
        """初始化 COLLATE 运算符
        
        Parameters
        ----------
        collation_operand : Expression
            排序操作数
        collation_name : str
            排序规则名称
        """
        self._collation_operand = collation_operand
        self._collation_name = collation_name

    @property
    def collation_operand(self) -> Expression:
        """获取排序操作数
        
        Returns
        -------
        Expression
            排序操作数
        """
        return self._collation_operand

    @property
    def collation_name(self) -> str:
        """获取排序规则名称
        
        Returns
        -------
        str
            排序规则名称
        """
        return self._collation_name


class OperatorConcat(BinaryExpression):
    """内置函数：字符串连接（`||` 运算符）

    {left_operand} || {right_operand}
    """


class OperatorMatch(Expression):
    """内置 MATCH 运算符（全文本索引搜索）

    MATCH column_list AGAINST ( sub_string fulltext_options )
    """

    __slots__ = ["_column_list", "_sub_string", "_fulltext_options"]

    def __init__(self, column_list: List["Ident"], sub_string: Expression, fulltext_options: EnumFulltextOption):
        """初始化 MATCH 运算符
        
        Parameters
        ----------
        column_list : List[Ident]
            列标识符列表
        sub_string : Expression
            子字符串表达式
        fulltext_options : EnumFulltextOption
            全文搜索选项
        """
        self._column_list = column_list
        self._sub_string = sub_string
        self._fulltext_options = fulltext_options

    @property
    def column_list(self) -> List["Ident"]:
        """获取列标识符列表
        
        Returns
        -------
        List[Ident]
            列标识符列表
        """
        return self._column_list

    @property
    def sub_string(self) -> Expression:
        """获取子字符串表达式
        
        Returns
        -------
        Expression
            子字符串表达式
        """
        return self._sub_string

    @property
    def fulltext_options(self) -> EnumFulltextOption:
        """获取全文搜索选项
        
        Returns
        -------
        EnumFulltextOption
            全文搜索选项
        """
        return self._fulltext_options


class OperatorBinary(UnaryExpression):
    """内置 BINARY 关键字运算符（指定二进制排序）"""


class OperatorJsonSeparator(Expression):
    """内置 JSON_SEPARATOR 运算符或 JSON_UNQUOTED_SEPARATOR 运算符（提取 Json 元素）

    expression JSON_SEPARATOR path
    expression JSON_UNQUOTED_SEPARATOR path
    """

    __slots__ = ["_expression", "_path", "_is_unquoted"]

    def __init__(self, expression: Expression, path: str, is_unquoted: bool):
        """初始化 JSON 分隔符运算符
        
        Parameters
        ----------
        expression : Expression
            表达式
        path : str
            JSON 路径
        is_unquoted : bool
            是否为无引号类型
        """
        self._expression = expression
        self._path = path
        self._is_unquoted = is_unquoted

    @property
    def expression(self) -> Expression:
        """获取表达式
        
        Returns
        -------
        Expression
            表达式
        """
        return self._expression

    @property
    def path(self) -> str:
        """获取 JSON 路径
        
        Returns
        -------
        str
            JSON 路径
        """
        return self._path

    @property
    def is_unquoted(self) -> bool:
        """获取是否为无引号类型
        
        Returns
        -------
        bool
            是否为无引号类型
        """
        return self._is_unquoted


class OperatorInSubSelect(Expression):
    """内置 IN 子查询运算符（判断目标值是否在子查询结果集中存在）"""

    __slots__ = ["_operand", "_subquery_expression"]

    def __init__(self, operand: Expression, subquery_expression: "QueryExpression"):
        """初始化 IN 子查询运算符
        
        Parameters
        ----------
        operand : Expression
            操作数
        subquery_expression : QueryExpression
            子查询表达式
        """
        self._operand = operand
        self._subquery_expression = subquery_expression

    @property
    def operand(self) -> Expression:
        """获取操作数
        
        Returns
        -------
        Expression
            操作数
        """
        return self._operand

    @property
    def subquery_expression(self) -> "QueryExpression":
        """获取子查询表达式
        
        Returns
        -------
        QueryExpression
            子查询表达式
        """
        return self._subquery_expression


class OperatorNotInSubSelect(Expression):
    """内置 NOT IN 子查询运算符（判断目标值是否在子查询结果集中存在）"""

    __slots__ = ["_operand", "_subquery_expression"]

    def __init__(self, operand: Expression, subquery_expression: "QueryExpression"):
        """初始化 NOT IN 子查询运算符
        
        Parameters
        ----------
        operand : Expression
            操作数
        subquery_expression : QueryExpression
            子查询表达式
        """
        self._operand = operand
        self._subquery_expression = subquery_expression

    @property
    def operand(self) -> Expression:
        """获取操作数
        
        Returns
        -------
        Expression
            操作数
        """
        return self._operand

    @property
    def subquery_expression(self) -> "QueryExpression":
        """获取子查询表达式
        
        Returns
        -------
        QueryExpression
            子查询表达式
        """
        return self._subquery_expression


class OperatorInValues(Expression):
    """内置 IN 运算符（判断目标值是否在备选值中存在）"""

    __slots__ = ["_operand", "_value_list"]

    def __init__(self, operand: Expression, value_list: List[Expression]):
        """初始化 IN 值列表运算符
        
        Parameters
        ----------
        operand : Expression
            操作数
        value_list : List[Expression]
            值列表
        """
        self._operand = operand
        self._value_list = value_list

    @property
    def operand(self) -> Expression:
        """获取操作数
        
        Returns
        -------
        Expression
            操作数
        """
        return self._operand

    @property
    def value_list(self) -> List[Expression]:
        """获取值列表
        
        Returns
        -------
        List[Expression]
            值列表
        """
        return self._value_list


class OperatorNotInValues(Expression):
    """内置 NOT IN 运算符（判断目标值是否不在备选值中存在）"""

    __slots__ = ["_operand", "_value_list"]

    def __init__(self, operand: Expression, value_list: List[Expression]):
        """初始化 NOT IN 值列表运算符
        
        Parameters
        ----------
        operand : Expression
            操作数
        value_list : List[Expression]
            值列表
        """
        self._operand = operand
        self._value_list = value_list

    @property
    def operand(self) -> Expression:
        """获取操作数
        
        Returns
        -------
        Expression
            操作数
        """
        return self._operand

    @property
    def value_list(self) -> List[Expression]:
        """获取值列表
        
        Returns
        -------
        List[Expression]
            值列表
        """
        return self._value_list
