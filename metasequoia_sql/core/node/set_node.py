"""
抽象语法树（AST）的 SET 语句节点
"""

import dataclasses

from metasequoia_sql.core.node.abc_node import ASTBase
from metasequoia_sql.core.node.sql_type import SQLType

__all__ = [
    "ASTSetStatement",  # SET 语句
]


# ---------------------------------------- SET 语句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTSetStatement(ASTBase):
    """SQL 语句"""

    config_name: str = dataclasses.field(kw_only=True)
    config_value: str = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"SET {self.config_name} = {self.config_value}"
