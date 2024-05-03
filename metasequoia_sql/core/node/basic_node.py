"""
抽象语法树（AST）节点：属性均非 ASTBase 的子类的节点
"""

import dataclasses
import enum
from typing import Optional

from metasequoia_sql.common.basic import is_int_literal
from metasequoia_sql.core.node.abc_node import ASTBase, ASTExpressionBase
from metasequoia_sql.core.sql_type import SQLType
from metasequoia_sql.errors import SqlParseError

__all__ = [
    "ASTColumnNameExpression",  # 列名表达式
    "ASTTableNameExpression",  # 表名表达式
    "ASTFunctionNameExpression",  # 函数名表达式
    "ASTLiteralExpression",  # 字面值表达式
    "EnumWindowRowType", "ASTWindowRowItem", "ASTWindowRow",  # 窗口函数的行数限制表达式
    "ASTWildcardExpression",  # 通配符表达式
    "ASTAlisaExpression",  # 别名表达式
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


# ---------------------------------------- 函数名表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTFunctionNameExpression(ASTBase):
    """表名表达式"""

    schema_name: Optional[str] = dataclasses.field(kw_only=True, default=None)
    function_name: str = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return f"`{self.schema_name}`.{self.function_name}" if self.schema_name is not None else f"{self.function_name}"


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


# ---------------------------------------- 窗口函数的行数限制 ----------------------------------------


class EnumWindowRowType(enum.Enum):
    """窗口函数中的行限制的类型"""
    PRECEDING = "PRECEDING"
    CURRENT_ROW = "CURRENT ROW"
    FOLLOWING = "FOLLOWING"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTWindowRowItem(ASTBase):
    """窗口函数中的行限制

    unbounded preceding = 当前行的所有行
    n preceding = 当前行之前的 n 行
    current row = 当前行
    n following = 当前行之后的 n行
    unbounded following = 当前行之后的所有行
    """

    row_type: EnumWindowRowType = dataclasses.field(kw_only=True)
    is_unbounded: bool = dataclasses.field(kw_only=True, default=False)
    row_num: Optional[int] = dataclasses.field(kw_only=True, default=None)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        if self.row_type == EnumWindowRowType.CURRENT_ROW:
            return "CURRENT ROW"
        row_type_str = self.row_type.value
        if self.is_unbounded is True:
            return f"UNBOUNDED {row_type_str}"
        return f"{self.row_num} {row_type_str}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTWindowRow(ASTBase):
    """窗口函数中的行限制表达式

    ROWS BETWEEN {SQLWindowRow} AND {SQLWindowRow}
    """

    from_row: ASTWindowRowItem = dataclasses.field(kw_only=True)
    to_row: ASTWindowRowItem = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return f"ROWS BETWEEN {self.from_row.source(sql_type)} AND {self.to_row.source(sql_type)}"


# ---------------------------------------- 通配符表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTWildcardExpression(ASTExpressionBase):
    """通配符表达式"""

    table_name: Optional[str] = dataclasses.field(kw_only=True, default=None)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.table_name}.*" if self.table_name is not None else "*"


# ---------------------------------------- 别名表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTAlisaExpression(ASTBase):
    """别名表达式"""

    name: str = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return f"AS {self.name}"
