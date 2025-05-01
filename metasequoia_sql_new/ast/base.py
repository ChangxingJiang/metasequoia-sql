"""
抽象语法树（AST）的抽象节点
"""

import abc
import typing

__all__ = [
    "Node",
    "Expression",
    "UnaryExpression",
    "BinaryExpression",
    "TernaryExpression",
    "ExpressionList",
    "Statement",
]


class Node(abc.ABC):
    """抽象语法树节点的抽象基类"""

    @abc.abstractmethod
    def attr_list(self) -> typing.List[str]:
        """返回属性名称的列表"""

    def __str__(self):
        result = []
        for attr_name in self.attr_list():
            result.append(f"{attr_name}={repr(getattr(self, attr_name))}")
        if not result:
            return f"<{self.__class__.__name__}>"
        result_str = ", ".join(result)
        return f"<{self.__class__.__name__} {result_str}>"

    __repr__ = __str__

    def get_str_value(self) -> typing.Optional[str]:
        return None


class Expression(Node, abc.ABC):
    """抽象语法树节点的抽象类：表达式"""


class UnaryExpression(Expression, abc.ABC):
    """抽象语法树节点的抽象类：一元表达式"""

    def __init__(self, operand: typing.Optional[Expression]):
        self._operand = operand

    def attr_list(self) -> typing.List[str]:
        return ["operand"]

    @property
    def operand(self) -> typing.Optional[Expression]:
        return self._operand


class BinaryExpression(Expression, abc.ABC):
    """抽象语法树节点的抽象类：二元表达式"""

    def __init__(self, left_operand: typing.Optional[Expression], right_operand: typing.Optional[Expression]):
        self._left_operand = left_operand
        self._right_operand = right_operand

    def attr_list(self) -> typing.List[str]:
        return ["left_operand", "right_operand"]

    @property
    def left_operand(self) -> typing.Optional[Expression]:
        return self._left_operand

    @property
    def right_operand(self) -> typing.Optional[Expression]:
        return self._right_operand


class TernaryExpression(Expression, abc.ABC):
    """抽象语法树节点的抽象类：三元表达式"""

    def __init__(self,
                 first_operand: typing.Optional[Expression],
                 second_operand: typing.Optional[Expression],
                 third_operand: typing.Optional[Expression]):
        self._first_operand = first_operand
        self._second_operand = second_operand
        self._third_operand = third_operand

    def attr_list(self) -> typing.List[str]:
        return ["first_operand", "second_operand", "third_operand"]

    @property
    def first_operand(self) -> typing.Optional[Expression]:
        return self._first_operand

    @property
    def second_operand(self) -> typing.Optional[Expression]:
        return self._second_operand

    @property
    def third_operand(self) -> typing.Optional[Expression]:
        return self._third_operand


class ExpressionList(Node):
    """逗号分隔的表达式列表"""

    def __init__(self, expression_list: typing.List[Expression]):
        self._expression_list = expression_list

    def attr_list(self) -> typing.List[str]:
        return ["expression_list"]

    @property
    def expression_list(self) -> typing.List[Expression]:
        return self._expression_list

    def append(self, expression: Expression) -> "ExpressionList":
        self._expression_list.append(expression)
        return self


class Statement(Node, abc.ABC):
    """抽象语法树节点的抽象类：语句"""
