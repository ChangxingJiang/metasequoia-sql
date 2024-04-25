# pylint: disable=C0302

"""
语法节点

因为不同语法节点之间需要相互引用，所以脚本文件不可避免地需要超过 1000 行，故忽略 pylint C0302。

在设计上，要求每个节点都是不可变节点，从而保证节点是可哈希的。同时，我们提供专门的修改方法：
- 当前，我们使用复制并返回新元素的方法，且不提供 inplace 参数
- 未来，我们为每个元素提供 .changeable() 方法，返回该元素的可变节点形式

TODO 重新实现支持 None 的 __eq__ 方法
"""

import abc
import dataclasses
import enum
from typing import Optional, Tuple, Union, Dict, Set

from metasequoia_sql.errors import SqlParseError, UnSupportDataSourceError
from metasequoia_sql.core.node.sql_type import SQLType

__all__ = [
    # ------------------------------ 抽象基类 ------------------------------
    "ASTBase",

    # ------------------------------ 基础元素（其中不引用其他元素） ------------------------------
    # 插入类型
    "EnumInsertType", "ASTInsertType",

    # 关联类型
    "EnumJoinType", "ASTJoinType",

    # 排序类型
    "EnumOrderType", "ASTOrderType",

    # 组合类型
    "EnumUnionType", "ASTUnionType",

    # 比较运算符
    "EnumCompareOperator", "ASTCompareOperator",

    # 计算运算符
    "EnumComputeOperator", "ASTComputeOperator",

    # 逻辑运算符
    "EnumLogicalOperator", "ASTLogicalOperator",

    # ------------------------------ 一般表达式 ------------------------------
    # 一般表达式的抽象基类
    "ASTGeneralExpression",

    # 一般表达式：字面值表达式
    "ASTLiteralExpression", "ASTLiteralIntegerExpression", "ASTLiteralFloatExpression", "ASTLiteralStringExpression",
    "ASTLiteralHexExpression", "ASTLiteralBitExpression", "ASTLiteralBoolExpression", "ASTLiteralNullExpression",

    # 一般表达式：列名表达式
    "ASTColumnNameExpression",

    # 一般表达式：函数表达式
    "ASTFunctionExpression", "EnumCastDataType", "ASTNormalFunctionExpression", "ASTAggregationFunctionExpression",
    "ASTCastDataType", "ASTCastFunctionExpression", "ASTExtractFunctionExpression",

    # 一般表达式：布尔值表达式
    "ASTBoolExpression", "ASTBoolCompareExpression", "ASTBoolIsExpression", "ASTBoolInExpression",
    "ASTBoolLikeExpression", "ASTBoolExistsExpression", "ASTBoolBetweenExpression",

    # 一般表达式：数组下标表达式
    "ASTArrayIndexExpression",

    # 一般表达式：窗口表达式
    "EnumWindowRowType", "ASTWindowRow", "ASTWindowRowExpression", "ASTWindowExpression",

    # 一般表达式：通配符表达式
    "ASTWildcardExpression",

    # 一般表达式：条件表达式
    "ASTConditionExpression",

    # 一般表达式：CASE 表达式
    "ASTCaseExpression", "ASTCaseValueExpression",

    # 一般表达式：计算表达式
    "ASTComputeExpression",

    # 一般表达式：值表达式
    "ASTValueExpression",

    # 一般表达式：子查询表达式
    "ASTSubQueryExpression",

    # ------------------------------ 专有表达式 ------------------------------
    # 专有表达式：表名表达式
    "ASTTableNameExpression",

    # 专有表达式：别名表达式
    "ASTAlisaExpression",

    # 专有表达式：关联表达式
    "ASTJoinExpression", "ASTJoinOnExpression", "ASTJoinUsingExpression",

    # 专有表达式：字段类型表达式
    "ASTColumnTypeExpression",

    # 专有表达式：表表达式
    "ASTTableExpression",

    # 专有表达式：列表达式
    "ASTColumnExpression",

    # 专有表达式：等式表达式
    "ASTEqualExpression",

    # 专有表达式：分区表达式
    "ASTPartitionExpression",

    # 专有表达式：声明外键表达式
    "ASTForeignKeyExpression",

    # 专有表达式：声明索引表达式
    "ASTIndexExpression", "ASTPrimaryIndexExpression", "ASTUniqueIndexExpression", "ASTNormalIndexExpression",
    "ASTFulltextIndexExpression", "ASTIndexColumn",

    # 专有表达式：声明字段表达式
    "ASTDefineColumnExpression",

    # 专有表达式：配置名称表达式和配置值表达式
    "ASTConfigNameExpression", "ASTConfigValueExpression",

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

    # INSERT 语句
    "ASTInsertStatement", "ASTInsertSelectStatement", "ASTInsertValuesStatement",

    # SET 语句
    "ASTSetStatement",

    # CREATE TABLE 语句
    "ASTCreateTableStatement",
]


# ---------------------------------------- 所有 SQL 语句对象节点的抽象基类 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTBase(abc.ABC):
    """所有 SQL 语法节点的抽象基类"""

    @abc.abstractmethod
    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} source={self.source(SQLType.DEFAULT)}>"

    def get_params_dict(self):
        """获取当前节点的所有参数（用于复制）"""
        return {field.name: getattr(self, field.name) for field in dataclasses.fields(self)}


# ---------------------------------------- 插入类型 ----------------------------------------


class EnumInsertType(enum.Enum):
    """插入类型的枚举类"""
    INSERT_INTO = ["INSERT", "INTO"]
    INSERT_OVERWRITE = ["INSERT", "OVERWRITE"]


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTInsertType(ASTBase):
    """插入类型"""

    insert_type: EnumInsertType = dataclasses.field(kw_only=True)  # 插入类型的枚举类

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return " ".join(self.insert_type.value)


# ---------------------------------------- 关联类型 ----------------------------------------


class EnumJoinType(enum.Enum):
    """关联类型的枚举类"""
    JOIN = ["JOIN"]  # 内连接
    INNER_JOIN = ["INNER", "JOIN"]  # 内连接
    LEFT_JOIN = ["LEFT", "JOIN"]  # 左外连接
    LEFT_OUTER_JOIN = ["LEFT", "OUTER", "JOIN"]  # 左外连接
    RIGHT_JOIN = ["RIGHT", "JOIN"]  # 右外连接
    RIGHT_OUTER_JOIN = ["RIGHT", "OUTER", "JOIN"]  # 右外连接
    FULL_JOIN = ["FULL", "JOIN"]  # 全外连接
    FULL_OUTER_JOIN = ["FULL", "OUTER", "JOIN"]  # 全外连接
    CROSS_JOIN = ["CROSS", "JOIN"]  # 交叉连接


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTJoinType(ASTBase):
    """关联类型"""

    join_type: EnumJoinType = dataclasses.field(kw_only=True)  # 关联类型的枚举类

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return " ".join(self.join_type.value)


# ---------------------------------------- 排序类型 ----------------------------------------


class EnumOrderType(enum.Enum):
    """排序类型的枚举类"""
    ASC = "ASC"  # 升序
    DESC = "DESC"  # 降序


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTOrderType(ASTBase):
    """排序类型"""

    order_type: EnumOrderType = dataclasses.field(kw_only=True)  # 排序类型的枚举类

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return self.order_type.value


# ---------------------------------------- 组合类型 ----------------------------------------


class EnumUnionType(enum.Enum):
    """组合类型的枚举类"""
    UNION_ALL = ["UNION", "ALL"]
    UNION = ["UNION"]
    EXCEPT = ["EXCEPT"]
    INTERSECT = ["INTERSECT"]
    MINUS = ["MINUS"]


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTUnionType(ASTBase):
    """组合类型"""

    union_type: EnumUnionType = dataclasses.field(kw_only=True)  # 组合类型的枚举类

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return " ".join(self.union_type.value)


# ---------------------------------------- 比较运算符 ----------------------------------------

class EnumCompareOperator(enum.Enum):
    """比较运算符的枚举类"""
    EQ = "="
    EQUAL_TO = "="
    NEQ = "!="
    NOT_EQUAL_TO = "!="
    LT = "<"
    LESS_THAN = "<"
    LTE = "<="
    LESS_THAN_OR_EQUAL = "<="
    GT = ">"
    GREATER_THAN = ">"
    GTE = ">="
    GREATER_THAN_OR_EQUAL = ">="


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTCompareOperator(ASTBase):
    """比较运算符"""

    compare_operator: EnumCompareOperator = dataclasses.field(kw_only=True)  # 比较运算符的枚举类

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return self.compare_operator.value


# ---------------------------------------- 计算运算符 ----------------------------------------

class EnumComputeOperator(enum.Enum):
    """计算运算符的枚举类"""
    PLUS = "+"  # 加法运算符
    SUBTRACT = "-"  # 减法运算符
    MULTIPLE = "*"  # 乘法运算符
    DIVIDE = "/"  # 除法运算符
    MOD = "%"  # 取模运算符
    CONCAT = "||"  # 字符串拼接运算符（仅 Oracle、DB2、PostgreSQL 中适用）


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTComputeOperator(ASTBase):
    """计算运算符"""

    compute_operator: EnumComputeOperator = dataclasses.field(kw_only=True)  # 计算运算符的枚举类

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        if self.compute_operator == EnumComputeOperator.MOD and data_source != SQLType.SQL_SERVER:
            raise UnSupportDataSourceError(f"{data_source} 不支持使用 % 运算符")
        if (self.compute_operator == EnumComputeOperator.CONCAT
                and data_source not in {SQLType.ORACLE, SQLType.DB2, SQLType.POSTGRE_SQL}):
            raise UnSupportDataSourceError(f"{data_source} 不支持使用 || 运算符")
        return self.compute_operator.value


# ---------------------------------------- 逻辑运算符 ----------------------------------------


class EnumLogicalOperator(enum.Enum):
    """逻辑运算符的枚举类"""
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTLogicalOperator(ASTBase):
    """逻辑运算符"""

    logical_operator: EnumLogicalOperator = dataclasses.field(kw_only=True)  # 逻辑运算符的枚举类

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return self.logical_operator.value


# ---------------------------------------- 一般表达式的抽象基类 ----------------------------------------


class ASTGeneralExpression(ASTBase, abc.ABC):
    """一般表达式的抽象基类"""


# ---------------------------------------- 字面值表达式 ----------------------------------------


class ASTLiteralExpression(ASTGeneralExpression, abc.ABC):
    """字面值表达式"""

    def as_int(self) -> Optional[int]:
        """将字面值作为整形返回"""
        return None

    def as_string(self) -> str:
        """将字面值作为字符串返回"""
        return self.source(SQLType.DEFAULT)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTLiteralIntegerExpression(ASTLiteralExpression):
    """整数字面值"""

    value: int = dataclasses.field(kw_only=True)  # 字面值

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.value}"

    def as_int(self) -> int:
        return self.value

    def as_string(self) -> str:
        return f"{self.value}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTLiteralFloatExpression(ASTLiteralExpression):
    """浮点数字面值"""

    value: float = dataclasses.field(kw_only=True)  # 字面值

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.value}"

    def as_string(self) -> str:
        return f"{self.value}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTLiteralStringExpression(ASTLiteralExpression):
    """字符串字面值"""

    value: str = dataclasses.field(kw_only=True)  # 字面值

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"'{self.value}'"

    def as_int(self) -> Optional[int]:
        if self.value.isdigit():
            return int(self.value)
        return None

    def as_string(self) -> Optional[str]:
        return self.value


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTLiteralHexExpression(ASTLiteralExpression):
    """十六进制字面值"""

    value: str = dataclasses.field(kw_only=True)  # 字面值

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"x'{self.value}'"

    def as_string(self) -> str:
        return f"{self.value}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTLiteralBitExpression(ASTLiteralExpression):
    """位值字面值"""

    value: str = dataclasses.field(kw_only=True)  # 字面值

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"b'{self.value}'"

    def as_string(self) -> str:
        return f"{self.value}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTLiteralBoolExpression(ASTLiteralExpression):
    """布尔值字面值"""

    value: bool = dataclasses.field(kw_only=True)  # 字面值

    def as_int(self) -> int:
        return 1 if self.value is True else 0

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return "TRUE" if self.value is True else "FALSE"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTLiteralNullExpression(ASTLiteralExpression):
    """空值字面值"""

    value: None = dataclasses.field(init=False, repr=False, compare=False, default=None)  # 字面值

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return "NULL"


# ---------------------------------------- 列名表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTColumnNameExpression(ASTGeneralExpression):
    """列名表达式"""

    table: Optional[str] = dataclasses.field(kw_only=True, default=None)  # 表名称
    column: str = dataclasses.field(kw_only=True)  # 字段名称

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        if self.column not in {"*", "CURRENT_DATE", "CURRENT_TIME", "CURRENT_TIMESTAMP"}:  # TODO 统一兼容通配符
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


class EnumCastDataType(enum.Enum):
    """CAST 函数的字段类型"""
    CHAR = "CHAR"
    ENUM = "ENUM"
    LONGTEXT = "LONGTEXT"
    MEDIUMTEXT = "MEDIUMTEXT"
    SET = "SET"
    TEXT = "TEXT"
    TINYTEXT = "TINYTEXT"
    VARCHAR = "VARCHAR"
    BIT = "BIT"
    BIGINT = "BIGINT"
    BOOLEAN = "BOOLEAN"
    BOOL = "BOOL"
    DECIMAL = "DECIMAL"
    DEC = "DEC"
    DOUBLE = "DOUBLE"
    INT = "INT"
    INTEGER = "INTEGER"
    MEDIUMINT = "MEDIUMINT"
    REAL = "REAL"
    SMALLINT = "SMALLINT"
    TINYINT = "TINYINT"
    DATE = "DATE"
    DATETIME = "DATETIME"
    TIMESTAMP = "TIMESTAMP"
    TIME = "TIME"
    YEAR = "YEAR"
    BOLB = "BOLB"
    MEDIUMBLOB = "MEDIUMBLOB"
    LONGBLOB = "LONGBLOB"
    TINYBLOB = "TINYBLOB"


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
class ASTCastDataType(ASTBase):
    """CAST 语句中的数据类型"""

    signed: bool = dataclasses.field(kw_only=True)  # 是否包含 SIGNED 关键字
    data_type: EnumCastDataType = dataclasses.field(kw_only=True)  # 目标转换的数据类型
    params: Optional[Tuple[ASTGeneralExpression]] = dataclasses.field(kw_only=True)  # 目标转换的数据类型的参数列表

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        result = []
        if self.signed is True:
            result.append("SIGNED")
        result.append(self.data_type.value)
        if self.params is not None:
            param_str = ", ".join(param.source(data_source) for param in self.params)
            result.append(f"({param_str})")
        return " ".join(result)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTCastFunctionExpression(ASTFunctionExpression):
    """Cast 函数表达式"""

    function_name: str = dataclasses.field(init=False, default="CAST")  # 函数名称
    column_expression: ASTGeneralExpression = dataclasses.field(kw_only=True)  # CAST 表达式中要转换的列表达式
    cast_type: ASTCastDataType = dataclasses.field(kw_only=True)  # CAST 参数中目标要转换的函数类型

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
class ASTBoolExpression(ASTBase, abc.ABC):
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

    operator: ASTCompareOperator = dataclasses.field(kw_only=True)

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


class EnumWindowRowType(enum.Enum):
    """窗口函数中的行限制的类型"""
    PRECEDING = "PRECEDING"
    CURRENT_ROW = "CURRENT ROW"
    FOLLOWING = "FOLLOWING"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTWindowRow(ASTBase):
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

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        if self.row_type == EnumWindowRowType.CURRENT_ROW:
            return "CURRENT ROW"
        row_type_str = self.row_type.value
        if self.is_unbounded is True:
            return f"UNBOUNDED {row_type_str}"
        return f"{self.row_num} {row_type_str}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTWindowRowExpression(ASTBase):
    """窗口函数中的行限制表达式

    ROWS BETWEEN {SQLWindowRow} AND {SQLWindowRow}
    """

    from_row: ASTWindowRow = dataclasses.field(kw_only=True)
    to_row: ASTWindowRow = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"ROWS BETWEEN {self.from_row.source(data_source)} AND {self.to_row.source(data_source)}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTWindowExpression(ASTGeneralExpression):
    """窗口表达式"""

    window_function: Union[ASTNormalFunctionExpression, ASTArrayIndexExpression] = dataclasses.field(kw_only=True)
    partition_by: Optional[ASTGeneralExpression] = dataclasses.field(kw_only=True)
    order_by: Optional[ASTGeneralExpression] = dataclasses.field(kw_only=True)
    row_expression: Optional[ASTWindowRowExpression] = dataclasses.field(kw_only=True)

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

@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTConditionExpression(ASTGeneralExpression):
    """条件表达式"""

    elements: Tuple[Union["ASTConditionExpression", ASTBoolExpression, ASTLogicalOperator], ...] = dataclasses.field(
        kw_only=True)

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

    elements: Tuple[Union[ASTGeneralExpression, ASTComputeOperator], ...] = dataclasses.field(kw_only=True)

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
class ASTTableNameExpression(ASTBase):
    """表名表达式"""

    schema: Optional[str] = dataclasses.field(kw_only=True, default=None)
    table: str = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"`{self.schema}.{self.table}`" if self.schema is not None else f"`{self.table}`"


# ---------------------------------------- 别名表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTAlisaExpression(ASTBase):
    """别名表达式"""

    name: str = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"AS {self.name}"


# ---------------------------------------- 关联表达式 ----------------------------------------


class ASTJoinExpression(ASTBase, abc.ABC):
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


# ---------------------------------------- 字段类型表达式 ----------------------------------------

@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTColumnTypeExpression(ASTBase):
    """字段类型表达式"""

    name: str = dataclasses.field(kw_only=True)
    params: Optional[Tuple[ASTGeneralExpression, ...]] = dataclasses.field(kw_only=True, default=None)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        if self.params is None or data_source == SQLType.HIVE:
            return self.name
        # MySQL 标准导出逗号间没有空格
        type_params = "(" + ",".join([param.source(data_source) for param in self.params]) + ")"
        return f"{self.name}{type_params}"


# ---------------------------------------- 表表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTTableExpression(ASTBase):
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
class ASTColumnExpression(ASTBase):
    """列表达式"""

    column: ASTGeneralExpression = dataclasses.field(kw_only=True)
    alias: Optional[ASTAlisaExpression] = dataclasses.field(kw_only=True, default=None)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        if self.alias is not None:
            return f"{self.column.source(data_source)} {self.alias.source(data_source)}"
        return f"{self.column.source(data_source)}"


# ---------------------------------------- 等式表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTEqualExpression(ASTBase):
    """等式表达式"""

    before_value: ASTGeneralExpression = dataclasses.field(kw_only=True)
    after_value: ASTGeneralExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.before_value.source(data_source)} = {self.after_value.source(data_source)}"


# ---------------------------------------- 分区表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTPartitionExpression(ASTBase):
    """分区表达式：PARTITION (<partition_expression>)"""

    partition_list: Tuple[ASTEqualExpression, ...] = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        partition_list_str = ", ".join(partition.source(data_source) for partition in self.partition_list)
        return f"PARTITION ({partition_list_str})"


# ---------------------------------------- 声明外键表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTForeignKeyExpression(ASTBase):
    """声明外键表达式"""

    constraint_name: str = dataclasses.field(kw_only=True)
    slave_columns: Tuple[str, ...] = dataclasses.field(kw_only=True)
    master_table_name: str = dataclasses.field(kw_only=True)
    master_columns: Tuple[str, ...] = dataclasses.field(kw_only=True)
    on_delete_cascade: bool = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        slave_columns_str = ", ".join([f"{column}" for column in self.slave_columns])
        master_columns_str = ", ".join([f"{column}" for column in self.master_columns])
        on_delete_cascade_str = " ON DELETE CASCADE" if self.on_delete_cascade else ""
        return (f"CONSTRAINT {self.constraint_name} FOREIGN KEY ({slave_columns_str}) "
                f"REFERENCES {self.master_table_name} ({master_columns_str}){on_delete_cascade_str}")


# ---------------------------------------- 声明索引表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTIndexColumn(ASTBase):
    """索引声明表达式中的字段"""

    name: str = dataclasses.field(kw_only=True)  # 字段名
    max_length: Optional[int] = dataclasses.field(kw_only=True, default=None)  # 最大长度

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        if self.max_length is None:
            return f"`{self.name}`"
        return f"`{self.name}`({self.max_length})"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTIndexExpression(ASTBase, abc.ABC):
    """声明索引表达式

    TODO 将 key_block_size 改为配置
    """

    name: Optional[str] = dataclasses.field(kw_only=True, default=None)
    columns: Tuple[ASTIndexColumn, ...] = dataclasses.field(kw_only=True)
    using: Optional[str] = dataclasses.field(kw_only=True, default=None)
    comment: Optional[str] = dataclasses.field(kw_only=True, default=None)
    key_block_size: Optional[int] = dataclasses.field(kw_only=True, default=None)


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTPrimaryIndexExpression(ASTIndexExpression):
    """主键索引声明表达式"""

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        columns_str = ",".join([f"{column.source(data_source)}" for column in self.columns])  # MySQL 标准导出逗号间没有空格
        using_str = f" USING {self.using}" if self.using is not None else ""
        comment_str = f" COMMENT {self.comment}" if self.comment is not None else ""
        config_str = f" KEY_BLOCK_SIZE={self.key_block_size}" if self.key_block_size is not None else ""
        return f"PRIMARY KEY ({columns_str}){using_str}{comment_str}{config_str}" if self.columns is not None else ""


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTUniqueIndexExpression(ASTIndexExpression):
    """唯一键索引声明表达式"""

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        columns_str = ",".join([f"{column.source(data_source)}" for column in self.columns])  # MySQL 标准导出逗号间没有空格
        using_str = f" USING {self.using}" if self.using is not None else ""
        comment_str = f" COMMENT {self.comment}" if self.comment is not None else ""
        config_str = f" KEY_BLOCK_SIZE={self.key_block_size}" if self.key_block_size is not None else ""
        return f"UNIQUE KEY {self.name} ({columns_str}){using_str}{comment_str}{config_str}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTNormalIndexExpression(ASTIndexExpression):
    """普通索引声明表达式"""

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        columns_str = ",".join([f"{column.source(data_source)}" for column in self.columns])  # MySQL 标准导出逗号间没有空格
        using_str = f" USING {self.using}" if self.using is not None else ""
        comment_str = f" COMMENT {self.comment}" if self.comment is not None else ""
        config_str = f" KEY_BLOCK_SIZE={self.key_block_size}" if self.key_block_size is not None else ""
        return f"KEY {self.name} ({columns_str}){using_str}{comment_str}{config_str}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTFulltextIndexExpression(ASTIndexExpression):
    """全文本索引声明表达式"""

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        columns_str = ",".join([f"{column.source(data_source)}" for column in self.columns])  # MySQL 标准导出逗号间没有空格
        using_str = f" USING {self.using}" if self.using is not None else ""
        comment_str = f" COMMENT {self.comment}" if self.comment is not None else ""
        config_str = f" KEY_BLOCK_SIZE={self.key_block_size}" if self.key_block_size is not None else ""
        return f"FULLTEXT KEY {self.name} ({columns_str}){using_str}{comment_str}{config_str}"


# ---------------------------------------- 声明字段表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTDefineColumnExpression(ASTBase):
    """声明字段表达式

    TODO 将各种标识添加为一个集合
    """

    column_name: str = dataclasses.field(kw_only=True)
    column_type: ASTColumnTypeExpression = dataclasses.field(kw_only=True)
    comment: Optional[str] = dataclasses.field(kw_only=True, default=None)
    is_unsigned: bool = dataclasses.field(kw_only=True, default=False)
    is_zerofill: bool = dataclasses.field(kw_only=True, default=False)
    character_set: Optional[str] = dataclasses.field(kw_only=True, default=None)
    collate: Optional[str] = dataclasses.field(kw_only=True, default=None)
    is_allow_null: bool = dataclasses.field(kw_only=True, default=False)
    is_not_null: bool = dataclasses.field(kw_only=True, default=False)
    is_auto_increment: bool = dataclasses.field(kw_only=True, default=False)
    default: Optional[ASTGeneralExpression] = dataclasses.field(kw_only=True, default=None)
    on_update: Optional[ASTGeneralExpression] = dataclasses.field(kw_only=True, default=None)

    @property
    def column_name_without_quote(self) -> str:
        """返回没有被引号框柱的列名"""
        return self.column_name

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        res = f"`{self.column_name}` {self.column_type.source(data_source)}"
        if self.is_unsigned is True and data_source == SQLType.MYSQL:
            res += " UNSIGNED"
        if self.is_zerofill is True and data_source == SQLType.MYSQL:
            res += " ZEROFILL"
        if self.character_set is not None and data_source == SQLType.MYSQL:
            res += f" CHARACTER SET {self.character_set}"
        if self.collate is not None and data_source == SQLType.MYSQL:
            res += f" COLLATE {self.collate}"
        if self.is_allow_null is True and data_source == SQLType.MYSQL:
            res += " NULL"
        if self.is_not_null is True and data_source == SQLType.MYSQL:
            res += " NOT NULL"
        if self.is_auto_increment is True and data_source == SQLType.MYSQL:
            res += " AUTO_INCREMENT"
        if self.default is not None and data_source == SQLType.MYSQL:
            res += f" DEFAULT {self.default.source(data_source)}"
        if self.on_update is not None and data_source == SQLType.MYSQL:
            res += f" ON UPDATE {self.on_update.source(data_source)}"
        if self.comment is not None:
            res += f" COMMENT {self.comment}"
        return res


# ---------------------------------------- 配置名称和配置值表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTConfigNameExpression(ASTBase):
    """配置名称表达式"""

    config_name: str = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return self.config_name


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTConfigValueExpression(ASTBase):
    """配置值表达式"""

    config_value: str = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return self.config_value


# ---------------------------------------- SELECT 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTSelectClause(ASTBase):
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
class ASTFromClause(ASTBase):
    """FROM 子句"""

    tables: Tuple[ASTTableExpression, ...] = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return "FROM " + ", ".join(table.source(data_source) for table in self.tables)


# ---------------------------------------- LATERAL VIEW 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTLateralViewClause(ASTBase):
    """LATERAL VIEW 子句"""

    function: ASTFunctionExpression = dataclasses.field(kw_only=True)
    view_name: str = dataclasses.field(kw_only=True)
    alias: ASTAlisaExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"LATERAL VIEW {self.function.source(data_source)} {self.view_name} {self.alias.source(data_source)}"


# ---------------------------------------- JOIN 子句 ----------------------------------------

@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTJoinClause(ASTBase):
    """JOIN 子句"""

    join_type: ASTJoinType = dataclasses.field(kw_only=True)
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
class ASTWhereClause(ASTBase):
    """WHERE 子句"""

    condition: ASTConditionExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"WHERE {self.condition.source(data_source)}"


# ---------------------------------------- GROUP BY 子句 ----------------------------------------

class ASTGroupByClause(ASTBase, abc.ABC):
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
class ASTHavingClause(ASTBase):
    """HAVING 子句"""

    condition: ASTConditionExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"HAVING {self.condition.source(data_source)}"


# ---------------------------------------- ORDER BY 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTOrderByClause(ASTBase):
    """ORDER BY 子句"""

    columns: Tuple[Tuple[ASTGeneralExpression, ASTOrderType], ...] = dataclasses.field(kw_only=True)

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
class ASTLimitClause(ASTBase):
    """LIMIT 子句"""

    limit: int = dataclasses.field(kw_only=True)
    offset: int = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
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
class ASTStatement(ASTBase, abc.ABC):
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
        return ASTSingleSelectStatement(
            with_clause=with_clause,
            select_clause=self.select_clause,
            from_clause=self.from_clause,
            lateral_view_clauses=self.lateral_view_clauses,
            join_clauses=self.join_clauses,
            where_clause=self.where_clause,
            group_by_clause=self.group_by_clause,
            having_clause=self.having_clause,
            order_by_clause=self.order_by_clause,
            limit_clause=self.limit_clause
        )


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTUnionSelectStatement(ASTSelectStatement):
    """复合查询语句，使用 UNION、EXCEPT、INTERSECT 进行组合"""

    elements: Tuple[Union[ASTUnionType, ASTSingleSelectStatement], ...] = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        with_clause_str = self.with_clause.source(data_source) + "\n" if not self.with_clause.is_empty() else ""
        return with_clause_str + "\n".join(element.source(data_source) for element in self.elements)

    def set_with_clauses(self, with_clause: Optional[ASTWithClause]) -> ASTSelectStatement:
        return ASTUnionSelectStatement(
            with_clause=with_clause,
            elements=self.elements
        )


# ---------------------------------------- INSERT 语句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTInsertStatement(ASTStatement, abc.ABC):
    """INSERT 表达式

    两个子类包含 VALUES 和 SELECT 两种方式

    INSERT {INTO|OVERWRITE} [TABLE] <table_name_expression> [PARTITION (<partition_expression>)]
    [(<colum_name_expression [,<column_name_expression> ...]>)]
    {VALUES <value_expression> [,<value_expression> ...] | <select_statement>}
    """

    insert_type: ASTInsertType = dataclasses.field(kw_only=True)
    table_name: ASTTableNameExpression = dataclasses.field(kw_only=True)
    partition: Optional[ASTPartitionExpression] = dataclasses.field(kw_only=True)
    columns: Optional[Tuple[ASTColumnNameExpression, ...]] = dataclasses.field(kw_only=True)

    def _insert_str(self, data_source: SQLType) -> str:
        insert_type_str = self.insert_type.source(data_source)
        table_keyword_str = "TABLE " if data_source == SQLType.HIVE else ""
        partition_str = self.partition.source(data_source) + " " if self.partition is not None else ""
        if self.columns is not None:
            columns_str = "(" + ", ".join(column.source(data_source) for column in self.columns) + ") "
        else:
            columns_str = ""
        return (f"{insert_type_str} {table_keyword_str}{self.table_name.source(data_source)} "
                f"{partition_str}{columns_str}")


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTInsertValuesStatement(ASTInsertStatement):
    """INSERT ... VALUES ... 语句"""

    values: Tuple[ASTValueExpression, ...] = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        values_str = ", ".join(value.source(data_source) for value in self.values)
        return f"{self._insert_str(data_source)}VALUES {values_str}"


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTInsertSelectStatement(ASTInsertStatement):
    """INSERT ... SELECT ... 语句"""

    select_statement: ASTSelectStatement = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self._insert_str(data_source)} {self.select_statement.source(data_source)}"


# ---------------------------------------- SET 语句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTSetStatement(ASTBase):
    """SQL 语句"""

    config_name: ASTConfigNameExpression = dataclasses.field(kw_only=True)
    config_value: ASTConfigValueExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: SQLType) -> str:
        """返回语法节点的 SQL 源码"""
        return f"SET {self.config_name.source(data_source)} = {self.config_value.source(data_source)}"


# ---------------------------------------- CREATE TABLE 语句 ----------------------------------------

@dataclasses.dataclass(slots=True, frozen=True, eq=True)
class ASTCreateTableStatement(ASTBase):
    """【DDL】CREATE TABLE 语句"""

    table_name_expression: ASTTableNameExpression = dataclasses.field(kw_only=True)
    if_not_exists: bool = dataclasses.field(kw_only=True)
    columns: Optional[Tuple[ASTDefineColumnExpression, ...]] = dataclasses.field(kw_only=True)
    primary_key: Optional[ASTPrimaryIndexExpression] = dataclasses.field(kw_only=True)
    unique_key: Optional[Tuple[ASTUniqueIndexExpression, ...]] = dataclasses.field(kw_only=True)
    key: Optional[Tuple[ASTNormalIndexExpression, ...]] = dataclasses.field(kw_only=True)
    fulltext_key: Optional[Tuple[ASTFulltextIndexExpression, ...]] = dataclasses.field(kw_only=True)
    foreign_key: Tuple[ASTForeignKeyExpression, ...] = dataclasses.field(kw_only=True)
    partitioned_by: Tuple[ASTDefineColumnExpression, ...] = dataclasses.field(kw_only=True)
    comment: Optional[str] = dataclasses.field(kw_only=True)
    engine: Optional[str] = dataclasses.field(kw_only=True)
    auto_increment: Optional[int] = dataclasses.field(kw_only=True)
    default_charset: Optional[str] = dataclasses.field(kw_only=True)
    collate: Optional[str] = dataclasses.field(kw_only=True)
    row_format: Optional[str] = dataclasses.field(kw_only=True)
    states_persistent: Optional[str] = dataclasses.field(kw_only=True)
    row_format_serde: Optional[str] = dataclasses.field(kw_only=True, default=None)  # Hive
    stored_as_inputformat: Optional[str] = dataclasses.field(kw_only=True, default=None)  # Hive
    outputformat: Optional[str] = dataclasses.field(kw_only=True, default=None)  # Hive
    location: Optional[str] = dataclasses.field(kw_only=True, default=None)  # Hive
    tblproperties: Optional[Tuple[Tuple[ASTConfigNameExpression, ASTConfigValueExpression], ...]] = dataclasses.field(
        kw_only=True, default=None)  # Hive

    def set_table_name_expression(self, table_name_expression: ASTTableNameExpression):
        table_params = self.get_params_dict()
        table_params["table_name_expression"] = table_name_expression
        return ASTCreateTableStatement(**table_params)

    def change_type(self, hashmap: Dict[str, str], remove_param: bool = True):
        """更新每个字段的变量类型"""
        table_params = self.get_params_dict()
        new_columns = []
        for old_column in self.columns:
            column_params = old_column.get_params_dict()
            column_params["column_type"] = ASTColumnTypeExpression(
                name=hashmap[old_column.column_type.name.upper()],
                params=None if remove_param else old_column.column_type.params)
            new_columns.append(ASTDefineColumnExpression(**column_params))
        table_params["columns"] = new_columns
        return ASTCreateTableStatement(**table_params)

    def append_column(self, column: ASTDefineColumnExpression):
        """添加字段"""
        table_params = self.get_params_dict()
        table_params["columns"] += (column,)
        return ASTCreateTableStatement(**table_params)

    def append_partition_by_column(self, column: ASTDefineColumnExpression):
        """添加分区字段"""
        table_params = self.get_params_dict()
        table_params["partitioned_by"] += (column,)
        return ASTCreateTableStatement(**table_params)

    def source(self, data_source: SQLType, n_indent: int = 2) -> str:
        """返回语法节点的 SQL 源码"""
        if data_source == SQLType.MYSQL:
            indentation = " " * n_indent  # 缩进字符串
            result = f"{self._title_str(data_source)} (\n"
            columns_and_keys = []
            for column in self.columns:
                columns_and_keys.append(f"{indentation}{column.source(data_source)}")
            if self.primary_key is not None:
                columns_and_keys.append(f"{indentation}{self.primary_key.source(data_source)}")
            for unique_key in self.unique_key:
                columns_and_keys.append(f"{indentation}{unique_key.source(data_source)}")
            for key in self.key:
                columns_and_keys.append(f"{indentation}{key.source(data_source)}")
            for fulltext_key in self.fulltext_key:
                columns_and_keys.append(f"{indentation}{fulltext_key.source(data_source)}")
            for foreign_key in self.foreign_key:
                columns_and_keys.append(f"{indentation}{foreign_key.source(data_source)}")
            result += ",\n".join(columns_and_keys)
            result += "\n)"
            if self.engine is not None:
                result += f" ENGINE={self.engine}"
            if self.auto_increment is not None:
                result += f" AUTO_INCREMENT={self.auto_increment}"
            if self.default_charset is not None:
                result += f" DEFAULT CHARSET={self.default_charset}"
            if self.collate is not None:
                result += f" COLLATE={self.collate}"
            if self.row_format is not None:
                result += f" ROW_FORMAT={self.row_format}"
            if self.states_persistent is not None:
                result += f" STATS_PERSISTENT={self.states_persistent}"
            if self.comment is not None:
                result += f" COMMENT={self.comment}"
            return result
        if data_source == SQLType.HIVE:
            indentation = " " * n_indent  # 缩进字符串
            result = f" {self._title_str(data_source)}(\n"
            columns_and_keys = []
            for column in self.columns:
                columns_and_keys.append(f"{indentation}{column.source(data_source)}")
            result += ",\n".join(columns_and_keys)
            result += "\n)"
            if self.comment is not None:
                result += f" COMMENT {self.comment}"
            if len(self.partitioned_by) > 0:
                partition_columns = []
                for column in self.partitioned_by:
                    partition_columns.append(column.source(data_source))
                partition_str = ", ".join(partition_columns)
                result += f" PARTITIONED BY ({partition_str})"
            if self.row_format_serde is not None:
                result += f" ROW FORMAT SERDE {self.row_format_serde}"
            if self.stored_as_inputformat is not None:
                result += f" STORED AS INPUTFORMAT {self.stored_as_inputformat}"
            if self.outputformat is not None:
                result += f" OUTPUTFORMAT {self.outputformat}"
            if self.location is not None:
                result += f" LOCATION {self.location}"
            if len(self.tblproperties) > 0:
                tblproperties_str = ", ".join([f"{config_name.source(data_source)}={config_value.source(data_source)}"
                                               for config_name, config_value in self.tblproperties])
                result += f"TBLPROPERTIES ({tblproperties_str})"
            return result
        raise SqlParseError(f"暂不支持的数据类型: {data_source}")

    def _title_str(self, data_source: SQLType) -> str:
        is_not_exists_str = " IF NOT EXISTS" if self.if_not_exists is True else ""
        return f"CREATE TABLE{is_not_exists_str} {self.table_name_expression.source(data_source)}"
