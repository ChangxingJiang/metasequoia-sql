"""
抽象语法树（AST）节点：SELECT 语句
"""

import abc
import dataclasses
import enum
from typing import Optional, Tuple, Union, Set

from metasequoia_sql.common.basic import is_int_literal
from metasequoia_sql.core.node.abc_node import ASTBase, ASTExpressionBase, ASTStatementBase
from metasequoia_sql.core.node.enum_node import (ASTJoinType, ASTOrderType, ASTUnionType, ASTCastDataType,
                                                 ASTComputeOperator, ASTCompareOperator,
                                                 ASTLogicalOperator)
from metasequoia_sql.core.node.common_expression import ASTTableNameExpression
from metasequoia_sql.core.sql_type import SQLType
from metasequoia_sql.errors import UnSupportDataSourceError, SqlParseError

__all__ = [
    # ------------------------------ 一般表达式 ------------------------------
    # 字面值表达式
    "ASTLiteralExpression",

    # 一般表达式：函数表达式
    "ASTFunctionExpression", "ASTNormalFunctionExpression", "ASTAggregationFunctionExpression",
    "ASTCastFunctionExpression", "ASTExtractFunctionExpression",

    # 一般表达式：布尔值表达式
    "ASTBoolExpression", "ASTBoolCompareExpression", "ASTBoolIsExpression", "ASTBoolInExpression",
    "ASTBoolLikeExpression", "ASTBoolExistsExpression", "ASTBoolBetweenExpression", "ASTBoolRlikeExpression",

    # 一般表达式：数组下标表达式
    "ASTArrayIndexExpression",

    # 一般表达式：窗口表达式
    "EnumWindowRowType", "ASTWindowRowItem", "ASTWindowRow", "ASTWindowExpression",

    # 一般表达式：通配符表达式
    "ASTWildcardExpression",

    # 一般表达式：条件表达式
    "ASTConditionExpression",

    # 一般表达式：CASE 表达式
    "ASTCaseExpression", "ASTCaseValueExpression",

    # 一般表达式：计算表达式
    "ASTComputeExpression",

    # 一般表达式：子查询表达式
    "ASTSubQueryExpression",

    # ------------------------------ 专有表达式 ------------------------------
    # 专有表达式：别名表达式
    "ASTAlisaExpression",

    # 专有表达式：关联表达式
    "ASTJoinExpression", "ASTJoinOnExpression", "ASTJoinUsingExpression",

    # 专有表达式：表表达式
    "ASTTableExpression",

    # 专有表达式：列表达式
    "ASTColumnExpression",

    # ------------------------------ 子句节点 ------------------------------
    # 子句节点：SELECT 子句
    "ASTSelectClause",

    # 子句节点：FROM 子句
    "ASTFromClause",

    # 子句节点：LATERAL VIEW 子句
    "ASTLateralViewClause",

    # 子句节点；JOIN 子句
    "ASTJoinClause",

    # 子句节点：WHERE 子句
    "ASTWhereClause",

    # 子句节点：GROUP BY 子句
    "ASTGroupByClause", "ASTNormalGroupByClause", "ASTGroupingSetsGroupByClause",

    # 子句节点：HAVING 子句
    "ASTHavingClause",

    # 子句节点：ORDER BY 子句
    "ASTOrderByClause",

    # 子句节点：LIMIT 子句
    "ASTLimitClause",

    # 子句节点：WITH 子句
    "ASTWithClause",

    # ------------------------------ 语句节点 ------------------------------
    # SELECT 语句
    "ASTSelectStatement", "ASTSingleSelectStatement", "ASTUnionSelectStatement",
]


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


# ---------------------------------------- 函数表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTFunctionExpression(ASTExpressionBase, abc.ABC):
    """函数表达式的抽象基类"""

    schema_name: Optional[str] = dataclasses.field(kw_only=True, default=None)  # 模式名称
    function_name: str = dataclasses.field(kw_only=True)  # 函数名称

    def _get_function_str(self) -> str:
        return f"`{self.schema_name}`.{self.function_name}" if self.schema_name is not None else f"{self.function_name}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTNormalFunctionExpression(ASTFunctionExpression):
    """包含一般参数的函数表达式"""

    function_params: Tuple[ASTExpressionBase] = dataclasses.field(kw_only=True)  # 函数表达式的参数

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self._get_function_str()}({self._get_param_str(sql_type)})"

    def _get_param_str(self, sql_type: SQLType) -> str:
        return ", ".join(param.source(sql_type) for param in self.function_params)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTAggregationFunctionExpression(ASTNormalFunctionExpression):
    """聚合函数表达式"""

    is_distinct: bool = dataclasses.field(kw_only=True)  # 是否包含 DISTINCT 关键字

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        is_distinct = "DISTINCT " if self.is_distinct is True else ""
        return f"{self._get_function_str()}({is_distinct}{self._get_param_str(sql_type)})"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTCastFunctionExpression(ASTFunctionExpression):
    """Cast 函数表达式"""

    function_name: str = dataclasses.field(init=False, default="CAST")  # 函数名称
    column_expression: ASTExpressionBase = dataclasses.field(kw_only=True)  # CAST 表达式中要转换的列表达式
    cast_type: ASTCastDataType = dataclasses.field(kw_only=True)  # CAST 参数中目标要转换的函数类型

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return (f"{self._get_function_str()}"
                f"({self.column_expression.source(sql_type)} AS {self.cast_type.source(sql_type)})")


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTExtractFunctionExpression(ASTFunctionExpression):
    """Extract 函数表达式"""

    function_name: str = dataclasses.field(init=False, default="EXTRACT")  # 函数名称
    extract_name: ASTExpressionBase = dataclasses.field(kw_only=True)  # FROM 关键字之前的提取名称
    column_expression: ASTExpressionBase = dataclasses.field(kw_only=True)  # FROM 关键字之后的一般表达式

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return (f"{self._get_function_str()}({self.extract_name.source(sql_type)} "
                f"FROM {self.column_expression.source(sql_type)})")


# ---------------------------------------- 布尔值表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTBoolExpression(ASTBase, abc.ABC):
    """布尔值表达式"""

    is_not: bool = dataclasses.field(kw_only=True)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class SQLBoolOperatorExpression(ASTBoolExpression, abc.ABC):
    """通过运算符或关键字比较运算符前后两个表达式的布尔值表达式"""

    before_value: ASTExpressionBase = dataclasses.field(kw_only=True)
    after_value: ASTExpressionBase = dataclasses.field(kw_only=True)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTBoolCompareExpression(SQLBoolOperatorExpression):
    """比较运算符布尔值表达式"""

    operator: ASTCompareOperator = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        is_not_str = "NOT " if self.is_not else ""
        return (f"{is_not_str}{self.before_value.source(sql_type)} {self.operator.source(sql_type)} "
                f"{self.after_value.source(sql_type)}")


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTBoolIsExpression(SQLBoolOperatorExpression):
    """IS运算符布尔值表达式"""

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        keyword = "IS NOT" if self.is_not else "IS"
        return f"{self.before_value.source(sql_type)} {keyword} {self.after_value.source(sql_type)}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTBoolInExpression(SQLBoolOperatorExpression):
    """In 关键字的布尔值表达式"""

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        keyword = "NOT IN " if self.is_not else "IN"
        return f"{self.before_value.source(sql_type)} {keyword} {self.after_value.source(sql_type)}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTBoolLikeExpression(SQLBoolOperatorExpression):
    """LIKE 运算符关联表达式"""

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        keyword = "NOT LIKE" if self.is_not else "LIKE"
        return f"{self.before_value.source(sql_type)} {keyword} {self.after_value.source(sql_type)}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTBoolRlikeExpression(SQLBoolOperatorExpression):
    """RLIKE 运算符关联表达式"""

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        keyword = "NOT RLIKE" if self.is_not else "RLIKE"
        return f"{self.before_value.source(sql_type)} {keyword} {self.after_value.source(sql_type)}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTBoolExistsExpression(ASTBoolExpression):
    """Exists 运算符关联表达式"""

    after_value: ASTExpressionBase = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        keyword = "NOT EXISTS" if self.is_not else "EXISTS"
        return f"{keyword} {self.after_value.source(sql_type)}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTBoolBetweenExpression(ASTBoolExpression):
    """BETWEEN 关联表达式"""

    before_value: ASTExpressionBase = dataclasses.field(kw_only=True)
    from_value: ASTExpressionBase = dataclasses.field(kw_only=True)
    to_value: ASTExpressionBase = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        if_not_str = "NOT " if self.is_not else ""
        return (f"{self.before_value.source(sql_type)} {if_not_str}"
                f"BETWEEN {self.from_value.source(sql_type)} AND {self.to_value.source(sql_type)}")


# ---------------------------------------- 数组下标表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTArrayIndexExpression(ASTExpressionBase):
    """数组下标表达式"""

    array_expression: ASTExpressionBase = dataclasses.field(kw_only=True)
    idx: int = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        if sql_type != SQLType.HIVE:
            raise UnSupportDataSourceError(f"数组下标不支持SQL类型:{sql_type}")
        return f"{self.array_expression.source(sql_type)}"


# ---------------------------------------- 窗口表达式 ----------------------------------------


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


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTWindowExpression(ASTExpressionBase):
    """窗口表达式"""

    window_function: Union[ASTNormalFunctionExpression, ASTArrayIndexExpression] = dataclasses.field(kw_only=True)
    partition_by: Optional[ASTExpressionBase] = dataclasses.field(kw_only=True)
    order_by: Optional[ASTExpressionBase] = dataclasses.field(kw_only=True)
    row_expression: Optional[ASTWindowRow] = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        result = f"{self.window_function.source(sql_type)} OVER ("
        parenthesis = []
        if self.partition_by is not None:
            parenthesis.append(f"PARTITION BY {self.partition_by.source(sql_type)}")
        if self.order_by is not None:
            parenthesis.append(f"ORDER BY {self.order_by.source(sql_type)}")
        if self.row_expression is not None:
            parenthesis.append(self.row_expression.source(sql_type))
        result += " ".join(parenthesis) + ")"
        return result


# ---------------------------------------- 通配符表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTWildcardExpression(ASTExpressionBase):
    """通配符表达式"""

    table_name: Optional[str] = dataclasses.field(kw_only=True, default=None)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.table_name}.*" if self.table_name is not None else "*"


# ---------------------------------------- 条件表达式 ----------------------------------------

ConditionElement = Union["ASTConditionExpression", ASTBoolExpression, ASTLogicalOperator]  # 条件表达式元素类型


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTConditionExpression(ASTExpressionBase):
    """条件表达式"""

    elements: Tuple[ConditionElement, ...] = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return " ".join(f"({element.source(sql_type)})"
                        if isinstance(element, ASTConditionExpression) else element.source(sql_type)
                        for element in self.elements)


# ---------------------------------------- CASE 表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTCaseExpression(ASTExpressionBase):
    """第 1 种格式的 CASE 表达式

    CASE
        WHEN {条件表达式} THEN {一般表达式}
        ELSE {一般表达式}
    END
    """

    cases: Tuple[Tuple[ASTConditionExpression, ASTExpressionBase], ...] = dataclasses.field(kw_only=True)
    else_value: Optional[ASTExpressionBase] = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        result = ["CASE"]
        for when, then in self.cases:
            result.append(f"WHEN {when.source(sql_type)} THEN {then.source(sql_type)}")
        if self.else_value is not None:
            result.append(f"ELSE {self.else_value.source(sql_type)}")
        result.append("END")
        return " ".join(result)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTCaseValueExpression(ASTExpressionBase):
    """第 2 种格式的 CASE 表达式

    CASE {一般表达式}
        WHEN {一般表达式} THEN {一般表达式}
        ELSE {一般表达式}
    END
    """

    case_value: ASTExpressionBase = dataclasses.field(kw_only=True)
    cases: Tuple[Tuple[ASTExpressionBase, ASTExpressionBase], ...] = dataclasses.field(kw_only=True)
    else_value: Optional[ASTExpressionBase] = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        result = ["CASE", self.case_value.source(sql_type)]
        for when, then in self.cases:
            result.append(f"    WHEN {when.source(sql_type)} THEN {then.source(sql_type)}")
        if self.else_value is not None:
            result.append(f"    ELSE {self.else_value.source(sql_type)}")
        result.append("END")
        return "\n".join(result)


# ---------------------------------------- 计算表达式 ----------------------------------------

@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTComputeExpression(ASTExpressionBase):
    """计算表达式"""

    elements: Tuple[Union[ASTExpressionBase, ASTComputeOperator], ...] = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return " ".join(element.source(sql_type) for element in self.elements)


# ---------------------------------------- 子查询表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTSubQueryExpression(ASTExpressionBase):
    """子查询表达式"""

    select_statement: "ASTSelectStatement" = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return f"({self.select_statement.source(sql_type)})"


# ---------------------------------------- 别名表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTAlisaExpression(ASTBase):
    """别名表达式"""

    name: str = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return f"AS {self.name}"


# ---------------------------------------- 关联表达式 ----------------------------------------


class ASTJoinExpression(ASTBase, abc.ABC):
    """关联表达式"""


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTJoinOnExpression(ASTJoinExpression):
    """ON 关联表达式"""

    condition: ASTConditionExpression = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return f"ON {self.condition.source(sql_type)}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTJoinUsingExpression(ASTJoinExpression):
    """USING 关联表达式"""

    using_function: ASTFunctionExpression = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.using_function.source(sql_type)}"


# ---------------------------------------- 表表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTTableExpression(ASTBase):
    """表表达式"""

    table: Union[ASTTableNameExpression, ASTSubQueryExpression] = dataclasses.field(kw_only=True)
    alias: Optional[ASTAlisaExpression] = dataclasses.field(kw_only=True, default=None)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        if self.alias is not None:
            return f"{self.table.source(sql_type)} {self.alias.source(sql_type)}"
        return f"{self.table.source(sql_type)}"


# ---------------------------------------- 列表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTColumnExpression(ASTBase):
    """列表达式"""

    column_value: ASTExpressionBase = dataclasses.field(kw_only=True)
    alias: Optional[ASTAlisaExpression] = dataclasses.field(kw_only=True, default=None)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        if self.alias is not None:
            return f"{self.column_value.source(sql_type)} {self.alias.source(sql_type)}"
        return f"{self.column_value.source(sql_type)}"


# ---------------------------------------- SELECT 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTSelectClause(ASTBase):
    """SELECT 子句"""

    distinct: bool = dataclasses.field(kw_only=True)
    columns: Tuple[ASTColumnExpression, ...] = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        result = ["SELECT"]
        if self.distinct is True:
            result.append("DISTINCT")
        result.append(", ".join(column.source(sql_type) for column in self.columns))
        return " ".join(result)


# ---------------------------------------- FROM 子句 ----------------------------------------

@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTFromClause(ASTBase):
    """FROM 子句"""

    tables: Tuple[ASTTableExpression, ...] = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return "FROM " + ", ".join(table.source(sql_type) for table in self.tables)


# ---------------------------------------- LATERAL VIEW 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTLateralViewClause(ASTBase):
    """LATERAL VIEW 子句"""

    function: ASTFunctionExpression = dataclasses.field(kw_only=True)
    view_name: str = dataclasses.field(kw_only=True)
    alias: ASTAlisaExpression = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return f"LATERAL VIEW {self.function.source(sql_type)} {self.view_name} {self.alias.source(sql_type)}"


# ---------------------------------------- JOIN 子句 ----------------------------------------

@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTJoinClause(ASTBase):
    """JOIN 子句"""

    join_type: ASTJoinType = dataclasses.field(kw_only=True)
    table: ASTTableExpression = dataclasses.field(kw_only=True)
    join_rule: Optional[ASTJoinExpression] = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        if self.join_rule is not None:
            return (f"{self.join_type.source(sql_type)} {self.table.source(sql_type)} "
                    f"{self.join_rule.source(sql_type)}")
        return f"{self.join_type.source(sql_type)} {self.table.source(sql_type)}"


# ---------------------------------------- WHERE 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTWhereClause(ASTBase):
    """WHERE 子句"""

    condition: ASTConditionExpression = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return f"WHERE {self.condition.source(sql_type)}"


# ---------------------------------------- GROUP BY 子句 ----------------------------------------

class ASTGroupByClause(ASTBase, abc.ABC):
    """GROUP BY 子句"""


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTNormalGroupByClause(ASTGroupByClause):
    """普通 GROUP BY 子句"""

    columns: Tuple[ASTExpressionBase, ...] = dataclasses.field(kw_only=True)
    with_rollup: bool = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        if self.with_rollup:
            return "GROUP BY " + ", ".join(column.source(sql_type) for column in self.columns) + " WITH ROLLUP"
        return "GROUP BY " + ", ".join(column.source(sql_type) for column in self.columns)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTGroupingSetsGroupByClause(ASTGroupByClause):
    """使用 GROUPING SETS 语法的 GROUP BY 子句"""

    grouping_list: Tuple[Tuple[ASTExpressionBase, ...], ...] = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        grouping_str_list = []
        for grouping in self.grouping_list:
            if len(grouping) > 1:
                grouping_str_list.append("(" + ", ".join(column.source(sql_type) for column in grouping) + ")")
            else:
                grouping_str_list.append(grouping[0].source(sql_type))
        return "GROUP BY GROUPING SETS (" + ", ".join(grouping_str_list) + ")"


# ---------------------------------------- HAVING 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTHavingClause(ASTBase):
    """HAVING 子句"""

    condition: ASTConditionExpression = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return f"HAVING {self.condition.source(sql_type)}"


# ---------------------------------------- ORDER BY 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTOrderByClause(ASTBase):
    """ORDER BY 子句"""

    columns: Tuple[Tuple[ASTExpressionBase, ASTOrderType], ...] = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        result = []
        for column, order_type in self.columns:
            if order_type.source(sql_type) == "ASC":
                result.append(f"{column.source(sql_type)}")
            else:
                result.append(f"{column.source(sql_type)} DESC")
        return "ORDER BY " + ", ".join(result)


# ---------------------------------------- LIMIT 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTLimitClause(ASTBase):
    """LIMIT 子句"""

    limit: int = dataclasses.field(kw_only=True)
    offset: int = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        return f"LIMIT {self.offset}, {self.limit}"


# ---------------------------------------- WITH 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTWithClause(ASTBase):
    """WITH 子句"""

    tables: Tuple[Tuple[str, "ASTSelectStatement"], ...] = dataclasses.field(kw_only=True)

    @staticmethod
    def empty():
        """空 WITH 子句"""
        return ASTWithClause(tables=tuple())

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        if not self.tables:
            return ""
        table_str = ", \n".join(f"{table_name}({table_statement.source(sql_type)})"
                                for table_name, table_statement in self.tables)
        return f"WITH {table_str}"

    def get_with_table_name_set(self) -> Set[str]:
        """获取 WITH 中临时表的名称"""
        return set(table[0] for table in self.tables)

    def is_empty(self):
        """返回 WITH 语句是否为空"""
        return len(self.tables) == 0


# ---------------------------------------- SELECT 语句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTSelectStatement(ASTStatementBase, abc.ABC):
    """SELECT 语句"""

    with_clause: Optional[ASTWithClause] = dataclasses.field(kw_only=True, default=None)

    @abc.abstractmethod
    def set_with_clauses(self, with_clause: Optional[ASTWithClause]) -> "ASTSelectStatement":
        """设置 WITH 语句"""


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTSingleSelectStatement(ASTSelectStatement):
    # pylint: disable=R0902 忽略对象属性过多的问题
    """单个 SELECT 表达式"""

    with_clause: Optional[ASTWithClause] = dataclasses.field(kw_only=True)
    select_clause: ASTSelectClause = dataclasses.field(kw_only=True)
    from_clause: Optional[ASTFromClause] = dataclasses.field(kw_only=True)
    lateral_view_clauses: Tuple[ASTLateralViewClause, ...] = dataclasses.field(kw_only=True)
    join_clauses: Tuple[ASTJoinClause, ...] = dataclasses.field(kw_only=True)
    where_clause: Optional[ASTWhereClause] = dataclasses.field(kw_only=True)
    group_by_clause: Optional[ASTGroupByClause] = dataclasses.field(kw_only=True)
    having_clause: Optional[ASTHavingClause] = dataclasses.field(kw_only=True)
    order_by_clause: Optional[ASTOrderByClause] = dataclasses.field(kw_only=True)
    limit_clause: Optional[ASTLimitClause] = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        with_clause_str = self.with_clause.source(sql_type) + "\n" if not self.with_clause.is_empty() else ""
        result = [self.select_clause.source(sql_type)]
        for clause in [self.from_clause, *self.lateral_view_clauses, *self.join_clauses, self.where_clause,
                       self.group_by_clause, self.having_clause, self.order_by_clause, self.limit_clause]:
            if clause is not None:
                result.append(clause.source(sql_type))
        return with_clause_str + "\n".join(result)

    def set_with_clauses(self, with_clause: Optional[ASTWithClause]) -> ASTSelectStatement:
        params = self.get_params_dict()
        params["with_clause"] = with_clause
        return ASTSingleSelectStatement(**params)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTUnionSelectStatement(ASTSelectStatement):
    """复合查询语句，使用 UNION、EXCEPT、INTERSECT 进行组合"""

    elements: Tuple[Union[ASTUnionType, ASTSingleSelectStatement], ...] = dataclasses.field(kw_only=True)

    def source(self, sql_type: SQLType = SQLType.DEFAULT) -> str:
        """返回语法节点的 SQL 源码"""
        with_clause_str = self.with_clause.source(sql_type) + "\n" if not self.with_clause.is_empty() else ""
        return with_clause_str + "\n".join(element.source(sql_type) for element in self.elements)

    def set_with_clauses(self, with_clause: Optional[ASTWithClause]) -> ASTSelectStatement:
        params = self.get_params_dict()
        params["with_clause"] = with_clause
        return ASTUnionSelectStatement(**params)
