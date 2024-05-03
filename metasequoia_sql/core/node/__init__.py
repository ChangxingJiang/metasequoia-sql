"""
抽象语法树（AST）节点

在设计上，要求每个节点都是不可变节点，从而保证节点是可哈希的。同时，我们提供专门的修改方法：
- 当前，我们使用复制并返回新元素的方法，且不提供 inplace 参数
- 未来，我们为每个元素提供 .changeable() 方法，返回该元素的可变节点形式

TODO 尽可能移除固定数量的元组
"""

from metasequoia_sql.core.node.abc_node import ASTBase, ASTExpressionBase, ASTStatementBase
from metasequoia_sql.core.node.enum_node import *
from metasequoia_sql.core.node.common_expression import *
from metasequoia_sql.core.node.statement_create_table import *
from metasequoia_sql.core.node.statement_drop_table import ASTDropTableStatement
from metasequoia_sql.core.node.statement_insert import *
from metasequoia_sql.core.node.statement_select import *
from metasequoia_sql.core.node.statement_set import *
