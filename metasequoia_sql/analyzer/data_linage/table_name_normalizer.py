"""
表名规范化器
"""

from typing import Dict

from metasequoia_sql import core
from metasequoia_sql.analyzer.base import AnalyzerRecursionASTToDictBase
from metasequoia_sql.analyzer.data_linage.node import StandardTable


class TableNameNormalizer(AnalyzerRecursionASTToDictBase):
    """表名规范化器"""

    def __init__(self, select_statement: core.ASTSelectStatement):
        self._alias_hash = self.handle(select_statement)

    def get_standard_table(self, alias_name: str) -> str:
        """获取标准表名对象"""
        return self._alias_hash[alias_name]

    @classmethod
    def handle(cls, node: object) -> Dict[str, str]:
        if isinstance(node, core.ASTTableExpression) and isinstance(node.table, core.ASTTableNameExpression):
            alias_name = node.alias.name if node.alias is not None else node.table.table
            standard_table = StandardTable(schema_name=node.table.schema, table_name=node.table.table)
            return {alias_name: standard_table}
        if isinstance(node, core.ASTSubQueryExpression) or isinstance(node, core.ASTWithClause):
            return {}
        return cls.default_handle_node(node)
