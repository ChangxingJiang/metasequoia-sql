"""
AST 对外暴露的辅助函数
"""

from typing import List

from metasequoia_sql.ast.old_nodes import AST


def iter_child_nodes(node: AST) -> List[AST]:
    """有序地产生 node 所有的直接子节点的列表"""
    return node.children


def dump(node: AST) -> str:
    """返回 node 中树结构的格式化转储。这主要适用于调试目的"""
    return node.source
