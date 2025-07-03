"""
抽象语法树（AST）的抽象节点
"""

from abc import ABC
from decimal import Decimal
from typing import List, Optional

__all__ = [
    "Node",
    "Expression",
    "Table",
    "QueryBody",
    "Literal",
    "UnaryExpression",
    "BinaryExpression",
    "TernaryExpression",
    "Statement",
]


class Node(ABC):
    """抽象语法树节点的抽象基类"""

    def properties(self) -> List[str]:
        """返回节点中通过 @property 装饰器定义的方法（性能较差，建议仅用于调试场景）"""
        attr_name_list = []
        now_class = self.__class__
        while now_class != Node:
            for name, attr in now_class.__dict__.items():
                if isinstance(attr, property):
                    attr_name_list.append(name)
            now_class = now_class.__base__
        return attr_name_list

    def __str__(self):
        result = []
        for attr_name in self.properties():
            result.append(f"{attr_name}={repr(getattr(self, attr_name))}")
        if not result:
            return f"<{self.__class__.__name__}>"
        result_str = ", ".join(result)
        return f"<{self.__class__.__name__} {result_str}>"

    __repr__ = __str__

    def get_str_value(self) -> Optional[str]:
        """
        获取节点的字符串值表示
        
        Returns
        -------
        Optional[str]
            如果节点可以表示为字符串，则返回字符串值；否则返回 None
        """
        return None

    def get_decimal_value(self) -> Optional[Decimal]:
        """
        获取节点的十进制数值表示
        
        Returns
        -------
        Optional[Decimal]
            如果节点可以表示为十进制数，则返回 Decimal 值；否则返回 None
        """
        return None


class Expression(Node, ABC):
    """抽象语法树节点的抽象类：表达式"""


class Table(Node, ABC):
    """抽象语法树节点的抽象类：表"""


class QueryBody(Node, ABC):
    """抽象语法树节点的抽象类：查询"""


class Literal(Expression, ABC):
    """抽象语法树节点的抽象类：字面值"""


class UnaryExpression(Expression, ABC):
    """抽象语法树节点的抽象类：一元表达式"""

    def __init__(self, operand: Optional[Expression]):
        self._operand = operand

    @property
    def operand(self) -> Optional[Expression]:
        """
        获取一元表达式的操作数
        
        Returns
        -------
        Optional[Expression]
            一元表达式的操作数，如果不存在则返回 None
        """
        return self._operand


class BinaryExpression(Expression, ABC):
    """抽象语法树节点的抽象类：二元表达式"""

    def __init__(self, left_operand: Optional[Expression], right_operand: Optional[Expression]):
        self._left_operand = left_operand
        self._right_operand = right_operand

    @property
    def left_operand(self) -> Optional[Expression]:
        """
        获取二元表达式的左操作数
        
        Returns
        -------
        Optional[Expression]
            二元表达式的左操作数，如果不存在则返回 None
        """
        return self._left_operand

    @property
    def right_operand(self) -> Optional[Expression]:
        """
        获取二元表达式的右操作数
        
        Returns
        -------
        Optional[Expression]
            二元表达式的右操作数，如果不存在则返回 None
        """
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

    @property
    def first_operand(self) -> Optional[Expression]:
        """
        获取三元表达式的第一个操作数
        
        Returns
        -------
        Optional[Expression]
            三元表达式的第一个操作数，如果不存在则返回 None
        """
        return self._first_operand

    @property
    def second_operand(self) -> Optional[Expression]:
        """
        获取三元表达式的第二个操作数
        
        Returns
        -------
        Optional[Expression]
            三元表达式的第二个操作数，如果不存在则返回 None
        """
        return self._second_operand

    @property
    def third_operand(self) -> Optional[Expression]:
        """
        获取三元表达式的第三个操作数
        
        Returns
        -------
        Optional[Expression]
            三元表达式的第三个操作数，如果不存在则返回 None
        """
        return self._third_operand


class Statement(Node, ABC):
    """抽象语法树节点的抽象类：语句"""
