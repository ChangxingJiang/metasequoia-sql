"""
抽象语法树（AST）的 SET 语句节点
"""

import dataclasses

from metasequoia_sql.core.node.abc_node import ASTBase
from metasequoia_sql.core.node.objects import ASTConfigNameExpression, ASTConfigValueExpression
from metasequoia_sql.core.node.sql_type import SQLType

__all__ = [
    "ASTSetStatement",  # SET 语句
]


# ---------------------------------------- SET 语句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTSetStatement(ASTBase):
    """SQL 语句"""

    config_name: ASTConfigNameExpression = dataclasses.field(kw_only=True)
    config_value: ASTConfigValueExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"SET {self.config_name.source(data_source)} = {self.config_value.source(data_source)}"
