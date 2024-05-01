"""
表名规范化器
"""

from typing import Dict, Optional, List

from metasequoia_sql import core
from metasequoia_sql.analyzer.base import AnalyzerRecursionASTToDictBase
from metasequoia_sql.analyzer.data_linage.node import StandardTable


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
        if isinstance(node, core.ASTTableExpression):
            if isinstance(node.table, core.ASTTableNameExpression):
                alias_name = node.alias.name if node.alias is not None else node.table.table
                standard_table = StandardTable(schema_name=node.table.schema, table_name=node.table.table)
                return {alias_name: standard_table}
            if isinstance(node.table, core.ASTSubQueryExpression):
                alias_name = node.alias.name  # TODO 待支持无别名子查询
                standard_table = StandardTable(schema_name=None, table_name=alias_name)  # 待增加中间表标记
                return {alias_name: standard_table}
        if isinstance(node, core.ASTSubQueryExpression) or isinstance(node, core.ASTWithClause):
            return {}
        return cls.default_handle_node(node)

    def __repr__(self):
        return ", ".join([f"{key}>{value}" for key, value in self._alias_name_to_standard_table_hash.items()])
