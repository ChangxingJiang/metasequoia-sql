"""
函数类型节点
"""

from enum import IntFlag
from typing import List, Optional, TYPE_CHECKING

from metasequoia_sql.ast.base import BinaryExpression, Expression, TernaryExpression, UnaryExpression
from metasequoia_sql.ast.other_operator import EnumOperatorCompare

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.ident import Ident
    from metasequoia_sql.ast.phrase.time_interval import TimeInterval

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
    "FulltextOption",
    "OperatorMatch",
    "OperatorBinary",
    "OperatorJsonSeparator",
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
        self._left_operand = left_operand
        self._right_operand = right_operand

    @property
    def left_operand(self) -> "TimeInterval":
        return self._left_operand

    @property
    def right_operand(self) -> Expression:
        return self._right_operand


class OperatorPlusDate(Expression):
    """内置 + 运算符，但 right_operand 为 time_interval 类型"""

    __slots__ = ["_left_operand", "_right_operand"]

    def __init__(self, left_operand: Expression, right_operand: "TimeInterval"):
        self._left_operand = left_operand
        self._right_operand = right_operand

    @property
    def left_operand(self) -> Expression:
        return self._left_operand

    @property
    def right_operand(self) -> "TimeInterval":
        return self._right_operand


class OperatorMinus(BinaryExpression):
    """内置函数：减法（`-` 运算符）"""


class OperatorMinusDate(Expression):
    """内置 - 运算符，但 right_operand 为 time_interval 类型"""

    __slots__ = ["_left_operand", "_right_operand"]

    def __init__(self, left_operand: Expression, right_operand: "TimeInterval"):
        self._left_operand = left_operand
        self._right_operand = right_operand

    @property
    def left_operand(self) -> Expression:
        return self._left_operand

    @property
    def right_operand(self) -> "TimeInterval":
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
    """内置函数：IS NULL 关键字

    {operand} IS NULL
    """


class OperatorIsNotNull(UnaryExpression):
    """内置函数：IS NOT NULL 关键字

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
                 operator: EnumOperatorCompare):
        super().__init__(left_operand, right_operand)
        self._operator = operator

    @property
    def operator(self) -> EnumOperatorCompare:
        return self._operator


class OperatorOr(BinaryExpression):
    """内置函数：逻辑或

    {left_operand} OR {right_operand}
    """


class OperatorXor(BinaryExpression):
    """内置函数：逻辑异或

    {left_operand} OR {right_operand}
    """


class OperatorAnd(BinaryExpression):
    """内置函数：逻辑与

    {left_operand} AND {right_operand}
    """


class OperatorNot(UnaryExpression):
    """内置函数：逻辑否

    NOT {operand}
    """


class OperatorIsTrue(UnaryExpression):
    """内置函数：IS TRUE 关键字

    {operand} IS TRUE
    """


class OperatorIsNotTrue(UnaryExpression):
    """内置函数：IS NOT TRUE

    {operand} IS NOT TRUE
    """


class OperatorIsFalse(UnaryExpression):
    """内置函数：IS FALSE

    {operand} IS FALSE
    """


class OperatorIsNotFalse(UnaryExpression):
    """内置函数：IS NOT FALSE

    {operand} IS NOT FALSE
    """


class OperatorIsUnknown(UnaryExpression):
    """内置函数：IS UNKNOWN

    {operand} IS UNKNOWN
    """


class OperatorIsNotUnknown(UnaryExpression):
    """内置函数：IS NOT UNKNOWN

    {operand} IS NOT UNKNOWN
    """


class OperatorTruthTransform(UnaryExpression):
    """内置 ! 运算符（逻辑取反）"""


class OperatorCollate(Expression):
    """内置 COLLATE 关键字运算符（指定排序规则）

    collation_operand COLLATE collation_name
    """

    __slots__ = ["_collation_operand", "_collation_name"]

    def __init__(self, collation_operand: Expression, collation_name: str):
        self._collation_operand = collation_operand  # 需要指定排序规则的表达式
        self._collation_name = collation_name  # 排序规则名称

    @property
    def collation_operand(self) -> Expression:
        return self._collation_operand

    @property
    def collation_name(self) -> str:
        return self._collation_name


class OperatorConcat(BinaryExpression):
    """内置 || 运算符（字符串合并）

    left_operand || right_operand
    """


class FulltextOption(IntFlag):
    """全文本索引选项"""

    DEFAULT = 0
    IN_NATURAL_LANGUAGE_MODE = 1  # IN NATURAL LANGUAGE MODE
    WITH_QUERY_EXPANSION = 2  # WITH QUERY EXPANSION
    IN_BOOLEAN_MODE = 4  # IN BOOLEAN MODE


class OperatorMatch(Expression):
    """内置 MATCH 运算符（全文本索引搜索）

    MATCH column_list AGAINST ( sub_string fulltext_options )
    """

    __slots__ = ["_column_list", "_sub_string", "_fulltext_options"]

    def __init__(self, column_list: List["Ident"], sub_string: Expression, fulltext_options: FulltextOption):
        self._column_list = column_list
        self._sub_string = sub_string
        self._fulltext_options = fulltext_options

    @property
    def column_list(self) -> List["Ident"]:
        return self._column_list

    @property
    def sub_string(self) -> Expression:
        return self._sub_string

    @property
    def fulltext_options(self) -> FulltextOption:
        return self._fulltext_options


class OperatorBinary(UnaryExpression):
    """内置 BINARY 运算符"""


class OperatorJsonSeparator(Expression):
    """内置 JSON_SEPARATOR 运算符或 JSON_UNQUOTED_SEPARATOR 运算符（提取 Json 元素）

    expression JSON_SEPARATOR path
    expression JSON_UNQUOTED_SEPARATOR path
    """

    __slots__ = ["_expression", "_path", "_is_unquoted"]

    def __init__(self, expression: Expression, path: str, is_unquoted: bool):
        self._expression = expression
        self._path = path
        self._is_unquoted = is_unquoted

    @property
    def expression(self) -> Expression:
        return self._expression

    @property
    def path(self) -> str:
        return self._path

    @property
    def is_unquoted(self) -> bool:
        return self._is_unquoted
