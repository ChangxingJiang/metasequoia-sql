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


class Expression(Node, abc.ABC):
    """抽象语法树节点的抽象类：表达式"""


class UnaryExpression(Expression, abc.ABC):
    """抽象语法树节点的抽象类：一元表达式"""

    def __init__(self, operand: Expression):
        self._operand = operand

    def attr_list(self) -> typing.List[str]:
        return ["operand"]

    @property
    def operand(self) -> Expression:
        return self._operand


class BinaryExpression(Expression, abc.ABC):
    """抽象语法树节点的抽象类：二元表达式"""

    def __init__(self, left_operand: Expression, right_operand: Expression):
        self._left_operand = left_operand
        self._right_operand = right_operand

    def attr_list(self) -> typing.List[str]:
        return ["left_operand", "right_operand"]

    @property
    def left_operand(self) -> Expression:
        return self._left_operand

    @property
    def right_operand(self) -> Expression:
        return self._right_operand


class Statement(Node, abc.ABC):
    """抽象语法树节点的抽象类：语句"""
