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
    "ASTFuncInsert",  # INSERT() 函数（字符串插入）
    "ASTFuncInterval",  # INTERVAL() 函数

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


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTFuncInsert(ASTFunctionExpressionBase):
    """【MySQL】Insert 函数（字符串插入）

    语法：
    INSERT(expr, expr, expr, expr)
    """

    expr_1: ASTExpressionBase = dataclasses.field(kw_only=True)
    expr_2: ASTExpressionBase = dataclasses.field(kw_only=True)
    expr_3: ASTExpressionBase = dataclasses.field(kw_only=True)
    expr_4: ASTExpressionBase = dataclasses.field(kw_only=True)

    @staticmethod
    def create_by(expr_1: ASTExpressionBase,
                  expr_2: ASTExpressionBase,
                  expr_3: ASTExpressionBase,
                  expr_4: ASTExpressionBase) -> "ASTFuncInsert":
        """

        Parameters
        ----------
        expr_1 : ASTExpressionBase
            原始字符串
        expr_2 : ASTExpressionBase
            要插入新字符的位置
        expr_3 : ASTExpressionBase
            要替换的字符数量（通常为 0）
        expr_4 : ASTExpressionBase
            要插入的新字符
        """
        return ASTFuncInsert(
            name=ASTFunctionNameExpression(function_name="insert"),
            expr_1=expr_1,
            expr_2=expr_2,
            expr_3=expr_3,
            expr_4=expr_4
        )

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return (f"{self.name.source(sql_type)}("
                f"{self.expr_1.source(sql_type)}, "
                f"{self.expr_2.source(sql_type)}, "
                f"{self.expr_3.source(sql_type)}, "
                f"{self.expr_4.source(sql_type)})")


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTFuncInterval(ASTFunctionExpressionBase):
    """【MySQL】Interval 函数

    语法：
    INTERVAL(expr, expr)
    INTERVAL(expr, expr, expr_list)
    """

    expr_1: ASTExpressionBase = dataclasses.field(kw_only=True)
    expr_2: ASTExpressionBase = dataclasses.field(kw_only=True)
    expr_list: Optional[Tuple[ASTExpressionBase, ...]] = dataclasses.field(kw_only=True)

    @staticmethod
    def create_by(expr_1: ASTExpressionBase,
                  expr_2: ASTExpressionBase,
                  expr_list: Optional[Tuple[ASTExpressionBase, ...]]) -> "ASTFuncInterval":
        return ASTFuncInterval(
            name=ASTFunctionNameExpression(function_name="interval"),
            expr_1=expr_1,
            expr_2=expr_2,
            expr_list=expr_list
        )

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        if self.expr_list is None:
            return f"{self.name.source(sql_type)}({self.expr_1.source(sql_type)}, {self.expr_2.source(sql_type)})"
        expr_list_str = ", ".join(expr.source(sql_type) for expr in self.expr_list)
        return (f"{self.name.source(sql_type)}({self.expr_1.source(sql_type)}, {self.expr_2.source(sql_type)}, "
                f"{expr_list_str})")


# 参数值为 (expr) 的函数映射表
FUNC_HASH_ONE_EXPR = {
    "DATE": ASTFuncDate,
    "DAY": ASTFuncDay,
    "HOUR": ASTFuncHour,
}
