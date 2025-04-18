"""
抽象语法树（AST）的抽象节点
"""

import abc

__all__ = [
    "Node",
    "Expression",
    "Statement",
]


class Node(abc.ABC):
    """抽象语法树节点的抽象基类"""


class Expression(Node, abc.ABC):
    """抽象语法树节点的抽象类：表达式"""


class Statement(Node, abc.ABC):
    """抽象语法树节点的抽象类：语句"""
