"""
表达式（expression）：SQL 语法树的中间节点或叶子节点，节点均继承自抽象节点 `Expression`；用于表示通用场景下可以计算出一个值的组合；表达式节点的属性中仅包含其他表达式节点、短语节点或基础元素节点。
"""

from metasequoia_sql.ast.expression.function_expression import *
from metasequoia_sql.ast.expression.general_expression import *
from metasequoia_sql.ast.expression.operator_expression import *
from metasequoia_sql.ast.expression.sum_expression import *
from metasequoia_sql.ast.expression.window_function_expression import *
