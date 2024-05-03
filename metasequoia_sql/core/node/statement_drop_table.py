"""
抽象语法树（AST）节点：DROP TABLE 语句
"""

import dataclasses

from metasequoia_sql.core.node.abc_node import ASTStatementBase
from metasequoia_sql.core.node.common_expression import ASTTableNameExpression
from metasequoia_sql.core.sql_type import SQLType

__all__ = ["ASTDropTableStatement"]


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTDropTableStatement(ASTStatementBase):
    """DROP TABLE 语句"""

    if_exists: bool = dataclasses.field(kw_only=True, default=False)  # 是否包含 IF EXISTS 关键字
    table_name: ASTTableNameExpression = dataclasses.field(kw_only=True)  # 表名

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        if_exists_str = "IF EXISTS " if self.if_exists is True else ""
        return f"DROP TABLE {if_exists_str}{self.table_name.source(sql_type)}"
