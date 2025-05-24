"""
抽象语法树（AST）的抽象节点
"""

from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional

__all__ = [
    "Node",
    "Expression",
    "Literal",
    "UnaryExpression",
    "BinaryExpression",
    "TernaryExpression",
    "Statement",
]


class Node(ABC):
    """抽象语法树节点的抽象基类"""

    @abstractmethod
    def attr_list(self) -> List[str]:
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

    def get_str_value(self) -> Optional[str]:
        return None

    def get_decimal_value(self) -> Optional[Decimal]:
        return None


class Expression(Node, ABC):
    """抽象语法树节点的抽象类：表达式"""


class Literal(Expression, ABC):
    """抽象语法树节点的抽象类：字面值"""


class UnaryExpression(Expression, ABC):
    """抽象语法树节点的抽象类：一元表达式"""

    def __init__(self, operand: Optional[Expression]):
        self._operand = operand

    def attr_list(self) -> List[str]:
        return ["operand"]

    @property
    def operand(self) -> Optional[Expression]:
        return self._operand


class BinaryExpression(Expression, ABC):
    """抽象语法树节点的抽象类：二元表达式"""

    def __init__(self, left_operand: Optional[Expression], right_operand: Optional[Expression]):
        self._left_operand = left_operand
        self._right_operand = right_operand

    def attr_list(self) -> List[str]:
        return ["left_operand", "right_operand"]

    @property
    def left_operand(self) -> Optional[Expression]:
        return self._left_operand

    @property
    def right_operand(self) -> Optional[Expression]:
        return self._right_operand


class TernaryExpression(Expression, ABC):
    """抽象语法树节点的抽象类：三元表达式"""

    def __init__(self,
                 first_operand: Optional[Expression],
                 second_operand: Optional[Expression],
                 third_operand: Optional[Expression]):
        self._first_operand = first_operand
        self._second_operand = second_operand
        self._third_operand = third_operand

    def attr_list(self) -> List[str]:
        return ["first_operand", "second_operand", "third_operand"]

    @property
    def first_operand(self) -> Optional[Expression]:
        return self._first_operand

    @property
    def second_operand(self) -> Optional[Expression]:
        return self._second_operand

    @property
    def third_operand(self) -> Optional[Expression]:
        return self._third_operand


class Statement(Node, ABC):
    """抽象语法树节点的抽象类：语句"""
