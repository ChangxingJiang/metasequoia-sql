"""
抽象语法树（AST）的 DQL 类节点

在设计上，要求每个节点都是不可变节点，从而保证节点是可哈希的。同时，我们提供专门的修改方法：
- 当前，我们使用复制并返回新元素的方法，且不提供 inplace 参数
- 未来，我们为每个元素提供 .changeable() 方法，返回该元素的可变节点形式

TODO 尽可能移除固定数量的元组
TODO 统一兼容通配符
"""

import abc
import dataclasses
from typing import Optional, Tuple, Union, Set

from metasequoia_sql.common.basic import is_int_literal
from metasequoia_sql.core.node import basic_node, abc_node
from metasequoia_sql.core.node.sql_type import SQLType
from metasequoia_sql.errors import SqlParseError, UnSupportDataSourceError

__all__ = [
    # ------------------------------ 一般表达式 ------------------------------
    # 一般表达式的抽象基类
    "ASTGeneralExpression",

    # 一般表达式：字面值表达式
    "ASTLiteralExpression",

    # 一般表达式：列名表达式
    "ASTColumnNameExpression",

    # 一般表达式：函数表达式
    "ASTFunctionExpression", "ASTNormalFunctionExpression", "ASTAggregationFunctionExpression",
    "ASTCastFunctionExpression", "ASTExtractFunctionExpression",

    # 一般表达式：布尔值表达式
    "ASTBoolExpression", "ASTBoolCompareExpression", "ASTBoolIsExpression", "ASTBoolInExpression",
    "ASTBoolLikeExpression", "ASTBoolExistsExpression", "ASTBoolBetweenExpression", "ASTBoolRlikeExpression",

    # 一般表达式：数组下标表达式
    "ASTArrayIndexExpression",

    # 一般表达式：窗口表达式
    "ASTWindowExpression",

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

    # 专有表达式：值表达式
    "ASTValueExpression",

    # ------------------------------ 专有表达式 ------------------------------
    # 专有表达式：表名表达式
    "ASTTableNameExpression",

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
    # 语句的抽象基类
    "ASTStatement",

    # SELECT 语句
    "ASTSelectStatement", "ASTSingleSelectStatement", "ASTUnionSelectStatement",
]


# ---------------------------------------- 一般表达式的抽象基类 ----------------------------------------


class ASTGeneralExpression(abc_node.ASTBase, abc.ABC):
    """一般表达式的抽象基类"""


# ---------------------------------------- 字面值表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTLiteralExpression(ASTGeneralExpression):
    """字面值表达式"""

    value: str = dataclasses.field(kw_only=True)  # 字面值

    def source(self, data_source: SQLType) -> str:
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


# ---------------------------------------- 列名表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTColumnNameExpression(ASTGeneralExpression):
    """列名表达式"""

    table: Optional[str] = dataclasses.field(kw_only=True, default=None)  # 表名称
    column: str = dataclasses.field(kw_only=True)  # 字段名称

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        if self.column not in {"*", "CURRENT_DATE", "CURRENT_TIME", "CURRENT_TIMESTAMP"}:
            result = f"`{self.table}`.`{self.column}`" if self.table is not None else f"`{self.column}`"
        else:
            result = f"`{self.table}`.{self.column}" if self.table is not None else f"{self.column}"
        if data_source == SQLType.DB2:
            # 兼容 DB2 的 CURRENT DATE、CURRENT TIME、CURRENT TIMESTAMP 语法
            result = result.replace("CURRENT_DATE", "CURRENT DATE")
            result = result.replace("CURRENT_TIME", "CURRENT TIME")
            result = result.replace("CURRENT_TIMESTAMP", "CURRENT TIMESTAMP")
        return result


# ---------------------------------------- 函数表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTFunctionExpression(ASTGeneralExpression, abc.ABC):
    """函数表达式的抽象基类"""

    schema_name: Optional[str] = dataclasses.field(kw_only=True, default=None)  # 模式名称
    function_name: str = dataclasses.field(kw_only=True)  # 函数名称

    def _get_function_str(self) -> str:
        return f"`{self.schema_name}`.{self.function_name}" if self.schema_name is not None else f"{self.function_name}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTNormalFunctionExpression(ASTFunctionExpression):
    """包含一般参数的函数表达式"""

    function_params: Tuple[ASTGeneralExpression] = dataclasses.field(kw_only=True)  # 函数表达式的参数

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self._get_function_str()}({self._get_param_str(data_source)})"

    def _get_param_str(self, data_source: SQLType) -> str:
        return ", ".join(param.source(data_source) for param in self.function_params)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTAggregationFunctionExpression(ASTNormalFunctionExpression):
    """聚合函数表达式"""

    is_distinct: bool = dataclasses.field(kw_only=True)  # 是否包含 DISTINCT 关键字

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        is_distinct = "DISTINCT " if self.is_distinct is True else ""
        return f"{self._get_function_str()}({is_distinct}{self._get_param_str(data_source)})"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTCastFunctionExpression(ASTFunctionExpression):
    """Cast 函数表达式"""

    function_name: str = dataclasses.field(init=False, default="CAST")  # 函数名称
    column_expression: ASTGeneralExpression = dataclasses.field(kw_only=True)  # CAST 表达式中要转换的列表达式
    cast_type: basic_node.ASTCastDataType = dataclasses.field(kw_only=True)  # CAST 参数中目标要转换的函数类型

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return (f"{self._get_function_str()}"
                f"({self.column_expression.source(data_source)} AS {self.cast_type.source(data_source)})")


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTExtractFunctionExpression(ASTFunctionExpression):
    """Extract 函数表达式"""

    function_name: str = dataclasses.field(init=False, default="EXTRACT")  # 函数名称
    extract_name: ASTGeneralExpression = dataclasses.field(kw_only=True)  # FROM 关键字之前的提取名称
    column_expression: ASTGeneralExpression = dataclasses.field(kw_only=True)  # FROM 关键字之后的一般表达式

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return (f"{self._get_function_str()}({self.extract_name.source(data_source)} "
                f"FROM {self.column_expression.source(data_source)})")


# ---------------------------------------- 布尔值表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTBoolExpression(abc_node.ASTBase, abc.ABC):
    """布尔值表达式"""

    is_not: bool = dataclasses.field(kw_only=True)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class SQLBoolOperatorExpression(ASTBoolExpression, abc.ABC):
    """通过运算符或关键字比较运算符前后两个表达式的布尔值表达式"""

    before_value: ASTGeneralExpression = dataclasses.field(kw_only=True)
    after_value: ASTGeneralExpression = dataclasses.field(kw_only=True)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTBoolCompareExpression(SQLBoolOperatorExpression):
    """比较运算符布尔值表达式"""

    operator: basic_node.ASTCompareOperator = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        is_not_str = "NOT " if self.is_not else ""
        return (f"{is_not_str}{self.before_value.source(data_source)} {self.operator.source(data_source)} "
                f"{self.after_value.source(data_source)}")


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTBoolIsExpression(SQLBoolOperatorExpression):
    """IS运算符布尔值表达式"""

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        keyword = "IS NOT" if self.is_not else "IS"
        return f"{self.before_value.source(data_source)} {keyword} {self.after_value.source(data_source)}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTBoolInExpression(SQLBoolOperatorExpression):
    """In 关键字的布尔值表达式"""

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        keyword = "NOT IN " if self.is_not else "IN"
        return f"{self.before_value.source(data_source)} {keyword} {self.after_value.source(data_source)}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTBoolLikeExpression(SQLBoolOperatorExpression):
    """LIKE 运算符关联表达式"""

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        keyword = "NOT LIKE" if self.is_not else "LIKE"
        return f"{self.before_value.source(data_source)} {keyword} {self.after_value.source(data_source)}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTBoolRlikeExpression(SQLBoolOperatorExpression):
    """RLIKE 运算符关联表达式"""

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        keyword = "NOT RLIKE" if self.is_not else "RLIKE"
        return f"{self.before_value.source(data_source)} {keyword} {self.after_value.source(data_source)}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTBoolExistsExpression(ASTBoolExpression):
    """Exists 运算符关联表达式"""

    after_value: ASTGeneralExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        keyword = "NOT EXISTS" if self.is_not else "EXISTS"
        return f"{keyword} {self.after_value.source(data_source)}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTBoolBetweenExpression(ASTBoolExpression):
    """BETWEEN 关联表达式"""

    before_value: ASTGeneralExpression = dataclasses.field(kw_only=True)
    from_value: ASTGeneralExpression = dataclasses.field(kw_only=True)
    to_value: ASTGeneralExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        if_not_str = "NOT " if self.is_not else ""
        return (f"{self.before_value.source(data_source)} {if_not_str}"
                f"BETWEEN {self.from_value.source(data_source)} AND {self.to_value.source(data_source)}")


# ---------------------------------------- 数组下标表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTArrayIndexExpression(ASTGeneralExpression):
    """数组下标表达式"""

    array_expression: ASTGeneralExpression = dataclasses.field(kw_only=True)
    idx: int = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        if data_source != SQLType.HIVE:
            raise UnSupportDataSourceError(f"数组下标不支持SQL类型:{data_source}")
        return f"{self.array_expression.source(data_source)}"


# ---------------------------------------- 窗口表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTWindowExpression(ASTGeneralExpression):
    """窗口表达式"""

    window_function: Union[ASTNormalFunctionExpression, ASTArrayIndexExpression] = dataclasses.field(kw_only=True)
    partition_by: Optional[ASTGeneralExpression] = dataclasses.field(kw_only=True)
    order_by: Optional[ASTGeneralExpression] = dataclasses.field(kw_only=True)
    row_expression: Optional[basic_node.ASTWindowRowExpression] = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        result = f"{self.window_function.source(data_source)} OVER ("
        parenthesis = []
        if self.partition_by is not None:
            parenthesis.append(f"PARTITION BY {self.partition_by.source(data_source)}")
        if self.order_by is not None:
            parenthesis.append(f"ORDER BY {self.order_by.source(data_source)}")
        if self.row_expression is not None:
            parenthesis.append(self.row_expression.source(data_source))
        result += " ".join(parenthesis) + ")"
        return result


# ---------------------------------------- 通配符表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTWildcardExpression(ASTGeneralExpression):
    """通配符表达式"""

    schema: Optional[str] = dataclasses.field(kw_only=True, default=None)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.schema}.*" if self.schema is not None else "*"


# ---------------------------------------- 条件表达式 ----------------------------------------

ConditionElement = Union["ASTConditionExpression", ASTBoolExpression, basic_node.ASTLogicalOperator]  # 条件表达式元素类型


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTConditionExpression(ASTGeneralExpression):
    """条件表达式"""

    elements: Tuple[ConditionElement, ...] = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return " ".join(f"({element.source(data_source)})"
                        if isinstance(element, ASTConditionExpression) else element.source(data_source)
                        for element in self.elements)


# ---------------------------------------- CASE 表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTCaseExpression(ASTGeneralExpression):
    """第 1 种格式的 CASE 表达式

    CASE
        WHEN {条件表达式} THEN {一般表达式}
        ELSE {一般表达式}
    END
    """

    cases: Tuple[Tuple[ASTConditionExpression, ASTGeneralExpression], ...] = dataclasses.field(kw_only=True)
    else_value: Optional[ASTGeneralExpression] = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        result = ["CASE"]
        for when, then in self.cases:
            result.append(f"WHEN {when.source(data_source)} THEN {then.source(data_source)}")
        if self.else_value is not None:
            result.append(f"ELSE {self.else_value.source(data_source)}")
        result.append("END")
        return " ".join(result)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTCaseValueExpression(ASTGeneralExpression):
    """第 2 种格式的 CASE 表达式

    CASE {一般表达式}
        WHEN {一般表达式} THEN {一般表达式}
        ELSE {一般表达式}
    END
    """

    case_value: ASTGeneralExpression = dataclasses.field(kw_only=True)
    cases: Tuple[Tuple[ASTGeneralExpression, ASTGeneralExpression], ...] = dataclasses.field(kw_only=True)
    else_value: Optional[ASTGeneralExpression] = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        result = ["CASE", self.case_value.source(data_source)]
        for when, then in self.cases:
            result.append(f"    WHEN {when.source(data_source)} THEN {then.source(data_source)}")
        if self.else_value is not None:
            result.append(f"    ELSE {self.else_value.source(data_source)}")
        result.append("END")
        return "\n".join(result)


# ---------------------------------------- 计算表达式 ----------------------------------------

@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTComputeExpression(ASTGeneralExpression):
    """计算表达式"""

    elements: Tuple[Union[ASTGeneralExpression, basic_node.ASTComputeOperator], ...] = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return " ".join(element.source(data_source) for element in self.elements)


# ---------------------------------------- 值表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTValueExpression(ASTGeneralExpression):
    """INSERT INTO 表达式中，VALUES 里的表达式"""

    values: Tuple[ASTGeneralExpression, ...] = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        values_str = ", ".join(value.source(data_source) for value in self.values)
        return f"({values_str})"


# ---------------------------------------- 子查询表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTSubQueryExpression(ASTGeneralExpression):
    """子查询表达式"""

    select_statement: "ASTSelectStatement" = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"({self.select_statement.source(data_source)})"


# ---------------------------------------- 表名表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTTableNameExpression(abc_node.ASTBase):
    """表名表达式"""

    schema: Optional[str] = dataclasses.field(kw_only=True, default=None)
    table: str = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"`{self.schema}.{self.table}`" if self.schema is not None else f"`{self.table}`"


# ---------------------------------------- 别名表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTAlisaExpression(abc_node.ASTBase):
    """别名表达式"""

    name: str = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"AS {self.name}"


# ---------------------------------------- 关联表达式 ----------------------------------------


class ASTJoinExpression(abc_node.ASTBase, abc.ABC):
    """关联表达式"""


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTJoinOnExpression(ASTJoinExpression):
    """ON 关联表达式"""

    condition: ASTConditionExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"ON {self.condition.source(data_source)}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTJoinUsingExpression(ASTJoinExpression):
    """USING 关联表达式"""

    using_function: ASTFunctionExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.using_function.source(data_source)}"


# ---------------------------------------- 表表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTTableExpression(abc_node.ASTBase):
    """表表达式"""

    table: Union[ASTTableNameExpression, ASTSubQueryExpression] = dataclasses.field(kw_only=True)
    alias: Optional[ASTAlisaExpression] = dataclasses.field(kw_only=True, default=None)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        if self.alias is not None:
            return f"{self.table.source(data_source)} {self.alias.source(data_source)}"
        return f"{self.table.source(data_source)}"


# ---------------------------------------- 列表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTColumnExpression(abc_node.ASTBase):
    """列表达式"""

    column: ASTGeneralExpression = dataclasses.field(kw_only=True)
    alias: Optional[ASTAlisaExpression] = dataclasses.field(kw_only=True, default=None)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        if self.alias is not None:
            return f"{self.column.source(data_source)} {self.alias.source(data_source)}"
        return f"{self.column.source(data_source)}"


# ---------------------------------------- SELECT 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTSelectClause(abc_node.ASTBase):
    """SELECT 子句"""

    distinct: bool = dataclasses.field(kw_only=True)
    columns: Tuple[ASTColumnExpression, ...] = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        result = ["SELECT"]
        if self.distinct is True:
            result.append("DISTINCT")
        result.append(", ".join(column.source(data_source) for column in self.columns))
        return " ".join(result)


# ---------------------------------------- FROM 子句 ----------------------------------------

@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTFromClause(abc_node.ASTBase):
    """FROM 子句"""

    tables: Tuple[ASTTableExpression, ...] = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return "FROM " + ", ".join(table.source(data_source) for table in self.tables)


# ---------------------------------------- LATERAL VIEW 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTLateralViewClause(abc_node.ASTBase):
    """LATERAL VIEW 子句"""

    function: ASTFunctionExpression = dataclasses.field(kw_only=True)
    view_name: str = dataclasses.field(kw_only=True)
    alias: ASTAlisaExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"LATERAL VIEW {self.function.source(data_source)} {self.view_name} {self.alias.source(data_source)}"


# ---------------------------------------- JOIN 子句 ----------------------------------------

@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTJoinClause(abc_node.ASTBase):
    """JOIN 子句"""

    join_type: basic_node.ASTJoinType = dataclasses.field(kw_only=True)
    table: ASTTableExpression = dataclasses.field(kw_only=True)
    join_rule: Optional[ASTJoinExpression] = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        if self.join_rule is not None:
            return (f"{self.join_type.source(data_source)} {self.table.source(data_source)} "
                    f"{self.join_rule.source(data_source)}")
        return f"{self.join_type.source(data_source)} {self.table.source(data_source)}"


# ---------------------------------------- WHERE 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTWhereClause(abc_node.ASTBase):
    """WHERE 子句"""

    condition: ASTConditionExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"WHERE {self.condition.source(data_source)}"


# ---------------------------------------- GROUP BY 子句 ----------------------------------------

class ASTGroupByClause(abc_node.ASTBase, abc.ABC):
    """GROUP BY 子句"""


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTNormalGroupByClause(ASTGroupByClause):
    """普通 GROUP BY 子句"""

    columns: Tuple[ASTGeneralExpression, ...] = dataclasses.field(kw_only=True)
    with_rollup: bool = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        if self.with_rollup:
            return "GROUP BY " + ", ".join(column.source(data_source) for column in self.columns) + " WITH ROLLUP"
        return "GROUP BY " + ", ".join(column.source(data_source) for column in self.columns)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTGroupingSetsGroupByClause(ASTGroupByClause):
    """使用 GROUPING SETS 语法的 GROUP BY 子句"""

    grouping_list: Tuple[Tuple[ASTGeneralExpression, ...], ...] = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        grouping_str_list = []
        for grouping in self.grouping_list:
            if len(grouping) > 1:
                grouping_str_list.append("(" + ", ".join(column.source(data_source) for column in grouping) + ")")
            else:
                grouping_str_list.append(grouping[0].source(data_source))
        return "GROUP BY GROUPING SETS (" + ", ".join(grouping_str_list) + ")"


# ---------------------------------------- HAVING 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTHavingClause(abc_node.ASTBase):
    """HAVING 子句"""

    condition: ASTConditionExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"HAVING {self.condition.source(data_source)}"


# ---------------------------------------- ORDER BY 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTOrderByClause(abc_node.ASTBase):
    """ORDER BY 子句"""

    columns: Tuple[Tuple[ASTGeneralExpression, basic_node.ASTOrderType], ...] = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        result = []
        for column, order_type in self.columns:
            if order_type.source(data_source) == "ASC":
                result.append(f"{column.source(data_source)}")
            else:
                result.append(f"{column.source(data_source)} DESC")
        return "ORDER BY " + ", ".join(result)


# ---------------------------------------- LIMIT 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTLimitClause(abc_node.ASTBase):
    """LIMIT 子句"""

    limit: int = dataclasses.field(kw_only=True)
    offset: int = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"LIMIT {self.offset}, {self.limit}"


# ---------------------------------------- WITH 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTWithClause(abc_node.ASTBase):
    """WITH 子句"""

    tables: Tuple[Tuple[str, "ASTSelectStatement"], ...] = dataclasses.field(kw_only=True)

    @staticmethod
    def empty():
        """空 WITH 子句"""
        return ASTWithClause(tables=tuple())

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        if not self.tables:
            return ""
        table_str = ", \n".join(f"{table_name}({table_statement.source(data_source)})"
                                for table_name, table_statement in self.tables)
        return f"WITH {table_str}"

    def get_with_table_name_set(self) -> Set[str]:
        """获取 WITH 中临时表的名称"""
        return set(table[0] for table in self.tables)

    def is_empty(self):
        """返回 WITH 语句是否为空"""
        return len(self.tables) == 0


# ---------------------------------------- 语句的抽象基类 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTStatement(abc_node.ASTBase, abc.ABC):
    """语句的抽象基类"""

    with_clause: Optional[ASTWithClause] = dataclasses.field(kw_only=True, default=None)


# ---------------------------------------- SELECT 语句 ----------------------------------------


class ASTSelectStatement(ASTStatement, abc.ABC):
    """SELECT 语句"""

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

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        with_clause_str = self.with_clause.source(data_source) + "\n" if not self.with_clause.is_empty() else ""
        result = [self.select_clause.source(data_source)]
        for clause in [self.from_clause, *self.lateral_view_clauses, *self.join_clauses, self.where_clause,
                       self.group_by_clause, self.having_clause, self.order_by_clause, self.limit_clause]:
            if clause is not None:
                result.append(clause.source(data_source))
        return with_clause_str + "\n".join(result)

    def set_with_clauses(self, with_clause: Optional[ASTWithClause]) -> ASTSelectStatement:
        params = self.get_params_dict()
        params["with_clause"] = with_clause
        return ASTSingleSelectStatement(**params)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTUnionSelectStatement(ASTSelectStatement):
    """复合查询语句，使用 UNION、EXCEPT、INTERSECT 进行组合"""

    elements: Tuple[Union[basic_node.ASTUnionType, ASTSingleSelectStatement], ...] = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        with_clause_str = self.with_clause.source(data_source) + "\n" if not self.with_clause.is_empty() else ""
        return with_clause_str + "\n".join(element.source(data_source) for element in self.elements)

    def set_with_clauses(self, with_clause: Optional[ASTWithClause]) -> ASTSelectStatement:
        params = self.get_params_dict()
        params["with_clause"] = with_clause
        return ASTUnionSelectStatement(**params)
