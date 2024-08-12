"""
抽象语法树（AST）节点：函数类节点
"""

import dataclasses
from typing import Optional, Tuple

from metasequoia_sql.core.node.major import ASTFunctionExpressionBase, ASTExpressionBase, ASTFunctionNameExpression
from metasequoia_sql.core.sql_type import SQLType

__all__ = [
    # ------------------------------ MySQL 关键字函数 ------------------------------
    "ASTFuncChar",  # CHAR() 函数
    "ASTFuncCurrentUser",  # CURRENT_USER() 函数
    "ASTFuncUser",  # USER() 函数
    "ASTFuncDate",  # DATE() 函数
    "ASTFuncDay",  # DAY() 函数
    "ASTFuncHour",  # HOUR() 函数

    "FUNC_HASH_ONE_EXPR",  # 参数值为 (expr) 的函数映射表
]


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTFuncChar(ASTFunctionExpressionBase):
    """【MySQL】CHAR 函数

    原型：
    CHAR(expr_list)
    CHAR(expr_list USING charset_name)
    """

    expr_list: Tuple[ASTExpressionBase, ...] = dataclasses.field(kw_only=True)  # 参数值的列表
    charset_name: Optional[str] = dataclasses.field(kw_only=True)  # 字符集

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        expr_list_str = ", ".join(expr.source(sql_type) for expr in self.expr_list)
        if self.charset_name is not None:
            return f"char({expr_list_str} USING {self.charset_name})"
        return f"char({expr_list_str})"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTFuncCurrentUser(ASTFunctionExpressionBase):
    """【MySQL】CURRENT_USER 函数

    原型：
    CURRENT_USER()
    CURRENT_USER
    """

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return "CURRENT_USER()"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTFuncUser(ASTFunctionExpressionBase):
    """【MySQL】USER 函数

    原型：
    USER()
    """

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return "USER()"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTFuncDate(ASTFunctionExpressionBase):
    """【MySQL】Date 函数

    语法：
    DATE(expr)
    """

    expr: ASTExpressionBase = dataclasses.field(kw_only=True)

    @staticmethod
    def create_by(expr: ASTExpressionBase) -> "ASTFuncDate":
        return ASTFuncDate(
            name=ASTFunctionNameExpression(function_name="date"),
            expr=expr
        )

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.name.source(sql_type)}({self.expr.source(sql_type)})"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTFuncDay(ASTFunctionExpressionBase):
    """【MySQL】Day 函数（day of month）

    语法：
    DAY(expr)
    """

    expr: ASTExpressionBase = dataclasses.field(kw_only=True)

    @staticmethod
    def create_by(expr: ASTExpressionBase) -> "ASTFuncDay":
        return ASTFuncDay(
            name=ASTFunctionNameExpression(function_name="day"),
            expr=expr
        )

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.name.source(sql_type)}({self.expr.source(sql_type)})"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTFuncHour(ASTFunctionExpressionBase):
    """【MySQL】Hour 函数

    语法：
    HOUR(expr)
    """

    expr: ASTExpressionBase = dataclasses.field(kw_only=True)

    @staticmethod
    def create_by(expr: ASTExpressionBase) -> "ASTFuncHour":
        return ASTFuncHour(
            name=ASTFunctionNameExpression(function_name="hour"),
            expr=expr
        )

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.name.source(sql_type)}({self.expr.source(sql_type)})"


# 参数值为 (expr) 的函数映射表
FUNC_HASH_ONE_EXPR = {
    "DATE": ASTFuncDate,
    "DAY": ASTFuncDay,
    "HOUR": ASTFuncHour,
}
