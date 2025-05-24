"""
函数类型节点
"""

import typing

from metasequoia_sql_new.ast.base import BinaryExpression
from metasequoia_sql_new.ast.base import Expression
from metasequoia_sql_new.ast.base import TernaryExpression
from metasequoia_sql_new.ast.base import UnaryExpression
from metasequoia_sql_new.ast.other_operator import EnumOperatorCompare

__all__ = [
    "FuncNegative",
    "FuncBitNot",
    "FuncBitOr",
    "FuncBitAnd",
    "FuncShiftLeft",
    "FuncShiftRight",
    "FuncPlus",
    "FuncMinus",
    "FuncMul",
    "FuncDiv",
    "FuncMod",
    "FuncDivInt",
    "FuncBitXor",
    "FuncMemberOf",
    "FuncBetween",
    "FuncNotBetween",
    "FuncSoundsLike",
    "FuncLike",
    "FuncNotLike",
    "FuncRegexp",
    "FuncNotRegexp",
    "FuncIsNull",
    "FuncIsNotNull",
    "FuncCompare",
    "FuncOr",
    "FuncXor",
    "FuncAnd",
    "FuncNot",
    "FuncIsTrue",
    "FuncIsNotTrue",
    "FuncIsFalse",
    "FuncIsNotFalse",
    "FuncIsUnknown",
    "FuncIsNotUnknown",
    "OperatorTruthTransform",
]


class FuncNegative(UnaryExpression):
    """内置函数：取相反数（`-` 运算符）"""


class FuncBitNot(UnaryExpression):
    """内置函数：按位取反（`~` 运算符）"""


class FuncBitOr(BinaryExpression):
    """内置函数：按位或（`|` 运算符）"""


class FuncBitAnd(BinaryExpression):
    """内置函数：按位与（`&` 运算符）"""


class FuncShiftLeft(BinaryExpression):
    """内置函数：左移位（`<<` 运算符）"""


class FuncShiftRight(BinaryExpression):
    """内置函数：右移位（`>>` 运算符）"""


class FuncPlus(BinaryExpression):
    """内置函数：加法（`+` 运算符）"""


class FuncMinus(BinaryExpression):
    """内置函数：减法（`-` 运算符）"""


class FuncMul(BinaryExpression):
    """内置函数：乘法（`*` 运算符）"""


class FuncDiv(BinaryExpression):
    """内置函数：除法（`/` 运算符）"""


class FuncMod(BinaryExpression):
    """内置函数：取模（`%` 运算符）"""


class FuncDivInt(BinaryExpression):
    """内置函数：整数除法（`DIV` 关键字）"""


class FuncBitXor(BinaryExpression):
    """内置函数：异或（`^` 关键字）"""


class FuncMemberOf(BinaryExpression):
    """内置函数：MEMBER OF 关键字

    {left_operand} MEMBER [OF] ( {right_operand} )
    """


class FuncBetween(TernaryExpression):
    """内置函数 BETWEEN 关键字

    {first_operand} BETWEEN {second_operand} AND {third_operand}
    """


class FuncNotBetween(TernaryExpression):
    """内置函数 NOT BETWEEN 关键字

    {first_operand} NOT BETWEEN {second_operand} AND {third_operand}
    """


class FuncSoundsLike(BinaryExpression):
    """内置函数 SOUNDS LIKE 关键字

    {left_operand} SOUNDS LIKE {right_operand}
    """


class FuncLike(TernaryExpression):
    """内置函数 LIKE 关键字

    {first_operand} LIKE {second_operand} [ ESCAPE {third_operand} ]
    """


class FuncNotLike(TernaryExpression):
    """内置函数 NOT LIKE 关键字

    {first_operand} NOT LIKE {second_operand} [ ESCAPE {third_operand} ]
    """


class FuncRegexp(BinaryExpression):
    """内置函数 REGEXP 关键字

    {left_operand} REGEXP {right_operand}
    """


class FuncNotRegexp(BinaryExpression):
    """内置函数 NOT REGEXP 关键字

    {left_operand} NOT REGEXP {right_operand}
    """


class FuncIsNull(UnaryExpression):
    """内置函数：IS NULL 关键字

    {operand} IS NULL
    """


class FuncIsNotNull(UnaryExpression):
    """内置函数：IS NOT NULL 关键字

    {operand} IS NOT NULL
    """


class FuncCompare(BinaryExpression):
    """内置函数：比较运算符

    {left_operand} comp_op {right_operand}

    - 其中 comp_op 为比较运算符
    """

    def __init__(self,
                 left_operand: typing.Optional[Expression],
                 right_operand: typing.Optional[Expression],
                 operator: EnumOperatorCompare):
        super().__init__(left_operand, right_operand)
        self._operator = operator

    def attr_list(self) -> typing.List[str]:
        return ["left_operand", "right_operand", "operator"]

    @property
    def operator(self) -> EnumOperatorCompare:
        return self._operator


class FuncOr(BinaryExpression):
    """内置函数：逻辑或

    {left_operand} OR {right_operand}
    """


class FuncXor(BinaryExpression):
    """内置函数：逻辑异或

    {left_operand} OR {right_operand}
    """


class FuncAnd(BinaryExpression):
    """内置函数：逻辑与

    {left_operand} AND {right_operand}
    """


class FuncNot(UnaryExpression):
    """内置函数：逻辑否

    NOT {operand}
    """


class FuncIsTrue(UnaryExpression):
    """内置函数：IS TRUE 关键字

    {operand} IS TRUE
    """


class FuncIsNotTrue(UnaryExpression):
    """内置函数：IS NOT TRUE

    {operand} IS NOT TRUE
    """


class FuncIsFalse(UnaryExpression):
    """内置函数：IS FALSE

    {operand} IS FALSE
    """


class FuncIsNotFalse(UnaryExpression):
    """内置函数：IS NOT FALSE

    {operand} IS NOT FALSE
    """


class FuncIsUnknown(UnaryExpression):
    """内置函数：IS UNKNOWN

    {operand} IS UNKNOWN
    """


class FuncIsNotUnknown(UnaryExpression):
    """内置函数：IS NOT UNKNOWN

    {operand} IS NOT UNKNOWN
    """


class OperatorTruthTransform(UnaryExpression):
    """内置 ! 运算符（逻辑取反）"""
