"""
抽象语法树（AST）节点：属性均非 ASTBase 的子类的节点
"""

import dataclasses
from typing import Optional

from metasequoia_sql.common.basic import is_int_literal
from metasequoia_sql.core.node.abc_node import ASTBase, ASTExpressionBase
from metasequoia_sql.core.sql_type import SQLType
from metasequoia_sql.errors import SqlParseError

__all__ = [
    "ASTColumnNameExpression",  # 列名表达式
    "ASTTableNameExpression",  # 表名表达式
    "ASTLiteralExpression",  # 字面值表达式
]


# ---------------------------------------- 列名表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTColumnNameExpression(ASTExpressionBase):
    """列名表达式"""

    table_name: Optional[str] = dataclasses.field(kw_only=True, default=None)  # 表名称
    column_name: str = dataclasses.field(kw_only=True)  # 字段名称

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        if self.column_name not in {"*", "CURRENT_DATE", "CURRENT_TIME", "CURRENT_TIMESTAMP"}:
            result = (f"`{self.table_name}`.`{self.column_name}`" if self.table_name is not None
                      else f"`{self.column_name}`")
        else:
            result = f"`{self.table_name}`.{self.column_name}" if self.table_name is not None else f"{self.column_name}"
        if sql_type == SQLType.DB2:
            # 兼容 DB2 的 CURRENT DATE、CURRENT TIME、CURRENT TIMESTAMP 语法
            result = result.replace("CURRENT_DATE", "CURRENT DATE")
            result = result.replace("CURRENT_TIME", "CURRENT TIME")
            result = result.replace("CURRENT_TIMESTAMP", "CURRENT TIMESTAMP")
        return result


# ---------------------------------------- 表名表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTTableNameExpression(ASTBase):
    """表名表达式"""

    schema: Optional[str] = dataclasses.field(kw_only=True, default=None)
    table: str = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return f"`{self.schema}.{self.table}`" if self.schema is not None else f"`{self.table}`"


# ---------------------------------------- 字面值表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTLiteralExpression(ASTExpressionBase):
    """字面值表达式"""

    value: str = dataclasses.field(kw_only=True)  # 字面值

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return self.value

    def as_int(self) -> int:
        """将字面值作为整形返回"""
        if is_int_literal(self.value):
            return int(self.value)
        raise SqlParseError(f"无法字面值 {self.value} 转化为整型")

    def as_string(self) -> str:
        """将字面值作为字符串返回"""
        return self.value
