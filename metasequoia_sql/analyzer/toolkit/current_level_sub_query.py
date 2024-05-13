"""
当前层级子查询分析器
"""

from typing import Dict, List

from metasequoia_sql import core
from metasequoia_sql.analyzer.base import AnalyzerRecursionASTToDictBase

__all__ = ["CurrentLevelSubQuery"]


class CurrentLevelSubQuery(AnalyzerRecursionASTToDictBase):
    """获取当前层的所有子查询的列表"""

    def __init__(self, select_statement: core.ASTSelectStatement):
        self._alias_hash = self.handle(select_statement)

    def get_all_sub_query_alias_name(self) -> List[str]:
        """获取所有子查询的别名列表"""
        return list(self._alias_hash)

    def get_sub_query_statement(self, alias_name: str) -> core.ASTSelectStatement:
        """获取指定别名的子查询的 SELECT 语句"""
        return self._alias_hash[alias_name]

    @classmethod
    def handle(cls, node: object) -> Dict[str, core.ASTSelectStatement]:
        """TODO 待支持不包含别名的子查询"""
        if (isinstance(node, core.ASTFromTable)
                and node.alias is not None and isinstance(node.name, core.ASTSubQueryExpression)):
            return {node.alias.name: node.name.statement}
        if isinstance(node, (core.ASTSubQueryExpression, core.ASTWithClause)):
            return {}
        return cls.default_handle_node(node)
