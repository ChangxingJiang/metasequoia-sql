"""
ast 的解析方法
"""

from metasequoia_sql.ast.nodes import AST


class ASTBuilderError(Exception):
    """AST 构造异常"""


class ASTBuilder(AST):
    """构造中的 AST 节点"""

    @property
    def source(self) -> str:
        raise ASTBuilderError("构造中的 AST 节点不允许调用 source 方法")
