"""
当前层级表明相关分析器
"""

from typing import Dict, Optional, List

from metasequoia_sql import core
from metasequoia_sql.analyzer.base import AnalyzerRecursionASTToDictBase
from metasequoia_sql.analyzer.node import StandardTable


__all__ = ["CurrentLevelTableNameAnalyzer"]


class CurrentLevelTableNameAnalyzer(AnalyzerRecursionASTToDictBase):
    """表名规分析器"""

    def __init__(self, select_statement: core.ASTSelectStatement):
        self._alias_name_to_standard_table_hash = self.handle(select_statement)

    def get_standard_table(self, alias_name: Optional[str]) -> Optional[StandardTable]:
        """根据表别名，获取标准表名对象"""
        return self._alias_name_to_standard_table_hash[alias_name] if alias_name is not None else None

    def get_all_table_name(self) -> List[str]:
        """获取所有的表别名"""
        return list(self._alias_name_to_standard_table_hash.keys())

    def get_all_standard_table(self) -> List[StandardTable]:
        """获取所有的标准表对象"""
        return list(self._alias_name_to_standard_table_hash.values())

    @classmethod
    def handle(cls, node: object) -> Dict[str, StandardTable]:
        """TODO 待支持无别名子查询"""
        if isinstance(node, core.ASTFromTableExpression):
            if isinstance(node.name, core.ASTTableName):
                alias_name = node.alias.name if node.alias is not None else node.name.table_name
                standard_table = StandardTable(schema_name=node.name.schema_name, table_name=node.name.table_name)
                return {alias_name: standard_table}
            if isinstance(node.name, core.ASTSubQueryExpression):
                alias_name = node.alias.name  #
                standard_table = StandardTable(schema_name=None, table_name=alias_name)  # 待增加中间表标记
                return {alias_name: standard_table}
        if isinstance(node, (core.ASTSubQueryExpression, core.ASTWithClause)):
            return {}
        return cls.default_handle_node(node)

    def __repr__(self):
        return ", ".join([f"{key}>{value}" for key, value in self._alias_name_to_standard_table_hash.items()])
