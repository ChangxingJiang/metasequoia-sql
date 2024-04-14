# pylint: disable=C0302

"""
语法节点

因为不同语法节点之间需要相互引用，所以脚本文件不可避免地需要超过 1000 行，故忽略 pylint C0302。

TODO 不将 CURRENT_DATE、CURRENT_TIME、CURRENT_TIMESTAMP 作为字段返回
TODO 增加 scanner 未解析完成的发现机制
"""

import abc
import dataclasses
import enum
from typing import Optional, List, Tuple, Union, Dict, Set

from metasequoia_sql.common.basic import ordered_distinct, chain_list
from metasequoia_sql.errors import SqlParseError, UnSupportDataSourceError

__all__ = [
    # ------------------------------ SQL 数据源类型 ------------------------------
    "DataSource",

    # ------------------------------ 基础元素（其中不引用其他元素） ------------------------------
    # 插入类型
    "EnumInsertType", "SQLInsertType",

    # 关联类型
    "EnumJoinType", "SQLJoinType",

    # 排序类型
    "EnumOrderType", "SQLOrderType",

    # 组合类型
    "EnumUnionType", "SQLUnionType",

    # 比较运算符
    "EnumCompareOperator", "SQLCompareOperator",

    # 计算运算符
    "EnumComputeOperator", "SQLComputeOperator",

    # 逻辑运算符
    "EnumLogicalOperator", "SQLLogicalOperator",

    # ------------------------------ 一般表达式 ------------------------------
    # 一般表达式的抽象基类
    "SQLGeneralExpression",

    # 一般表达式：字面值表达式
    "SQLLiteralExpression", "SQLLiteralIntegerExpression", "SQLLiteralFloatExpression", "SQLLiteralStringExpression",
    "SQLLiteralHexExpression", "SQLLiteralBitExpression", "SQLLiteralBoolExpression", "SQLLiteralNullExpression",

    # 一般表达式：列名表达式
    "SQLColumnNameExpression",

    # 一般表达式：函数表达式
    "SQLFunctionExpression", "EnumCastDataType", "SQLNormalFunctionExpression", "SQLAggregationFunctionExpression",
    "SQLCastDataType", "SQLCastFunctionExpression", "SQLExtractFunctionExpression",

    # 一般表达式：布尔值表达式
    "SQLBoolExpression", "SQLBoolCompareExpression", "SQLBoolIsExpression", "SQLBoolInExpression",
    "SQLBoolLikeExpression", "SQLBoolExistsExpression", "SQLBoolBetweenExpression",

    # 一般表达式：数组下标表达式
    "SQLArrayIndexExpression",

    # 一般表达式：窗口表达式
    "SQLWindowExpression",

    # 一般表达式：通配符表达式
    "SQLWildcardExpression",

    # 一般表达式：条件表达式
    "SQLConditionExpression",

    # 一般表达式：CASE 表达式
    "SQLCaseExpression", "SQLCaseValueExpression",

    # 一般表达式：计算表达式
    "SQLComputeExpression",

    # 一般表达式：值表达式
    "SQLValueExpression",

    # 一般表达式：子查询表达式
    "SQLSubQueryExpression",

    # ------------------------------ 专有表达式 ------------------------------
    # 专有表达式：表名表达式
    "SQLTableNameExpression",

    # 专有表达式：别名表达式
    "SQLAlisaExpression",

    # 专有表达式：关联表达式
    "SQLJoinExpression", "SQLJoinOnExpression", "SQLJoinUsingExpression",

    # 专有表达式：字段类型表达式
    "SQLColumnTypeExpression",

    # 专有表达式：表表达式
    "SQLTableExpression",

    # 专有表达式：列表达式
    "SQLColumnExpression",

    # 专有表达式：等式表达式
    "SQLEqualExpression",

    # 专有表达式：分区表达式
    "SQLPartitionExpression",

    # 专有表达式：声明外键表达式
    "SQLForeignKeyExpression",

    # 专有表达式：声明索引表达式
    "SQLIndexExpression", "SQLPrimaryIndexExpression", "SQLUniqueIndexExpression", "SQLNormalIndexExpression",
    "SQLFulltextIndexExpression",

    # 专有表达式：声明字段表达式
    "SQLDefineColumnExpression",

    # 专有表达式：配置名称表达式和配置值表达式
    "SQLConfigNameExpression", "SQLConfigValueExpression",

    # ------------------------------ 子句节点 ------------------------------
    # 子句节点：SELECT 子句
    "SQLSelectClause",

    # 子句节点：FROM 子句
    "SQLFromClause",

    # 子句节点：LATERAL VIEW 子句
    "SQLLateralViewClause",

    # 子句节点；JOIN 子句
    "SQLJoinClause",

    # 子句节点：WHERE 子句
    "SQLWhereClause",

    # 子句节点：GROUP BY 子句
    "SQLGroupByClause", "SQLNormalGroupByClause", "SQLGroupingSetsGroupByClause",

    # 子句节点：HAVING 子句
    "SQLHavingClause",

    # 子句节点：ORDER BY 子句
    "SQLOrderByClause",

    # 子句节点：LIMIT 子句
    "SQLLimitClause",

    # 子句节点：WITH 子句
    "SQLWithClause",

    # ------------------------------ 语句节点 ------------------------------
    # 语句的抽象基类
    "SQLStatement",

    # SELECT 语句
    "SQLSelectStatement", "SQLSingleSelectStatement", "SQLUnionSelectStatement",

    # INSERT 语句
    "SQLInsertStatement", "SQLInsertSelectStatement", "SQLInsertValuesStatement",

    # SET 语句
    "SQLSetStatement",

    # CREATE TABLE 语句
    "SQLCreateTableStatement",
]


# ---------------------------------------- 所有 SQL 语句对象节点的抽象基类 ----------------------------------------


class DataSource(enum.Enum):
    """数据源类型（即 SQL 语句类型）"""
    MYSQL = "MySQL"
    HIVE = "Hive"
    ORACLE = "Oracle"
    DB2 = "DB2"
    POSTGRE_SQL = "PostgreSQL"
    SQL_SERVER = "SQL Server"
    DEFAULT = "DEFAULT"


class SQLBase(abc.ABC):
    """所有 SQL 语法节点的抽象基类"""

    @abc.abstractmethod
    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""

    @abc.abstractmethod
    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""

    @abc.abstractmethod
    def get_used_table_list(self) -> List[str]:
        """获取使用的表的列表"""

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} source={self.source(DataSource.DEFAULT)}>"


class SQLBaseAlone(SQLBase, abc.ABC):
    """不使用字段、表的 SQL 固定值语法节点的抽象基类"""

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return []

    def get_used_table_list(self) -> List[str]:
        """获取使用的表的列表"""
        return []


# ---------------------------------------- 插入类型 ----------------------------------------


class EnumInsertType(enum.Enum):
    """插入类型的枚举类"""
    INSERT_INTO = ["INSERT", "INTO"]
    INSERT_OVERWRITE = ["INSERT", "OVERWRITE"]


@dataclasses.dataclass(slots=True, frozen=True)
class SQLInsertType(SQLBaseAlone):
    """插入类型"""

    insert_type: EnumInsertType = dataclasses.field(kw_only=True)  # 插入类型的枚举类

    def source(self, data_source: DataSource) -> str:
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


@dataclasses.dataclass(slots=True, frozen=True)
class SQLJoinType(SQLBaseAlone):
    """关联类型"""

    join_type: EnumJoinType = dataclasses.field(kw_only=True)  # 关联类型的枚举类

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return " ".join(self.join_type.value)


# ---------------------------------------- 排序类型 ----------------------------------------


class EnumOrderType(enum.Enum):
    """排序类型的枚举类"""
    ASC = "ASC"  # 升序
    DESC = "DESC"  # 降序


@dataclasses.dataclass(slots=True, frozen=True)
class SQLOrderType(SQLBaseAlone):
    """排序类型"""

    order_type: EnumOrderType = dataclasses.field(kw_only=True)  # 排序类型的枚举类

    def source(self, data_source: DataSource) -> str:
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


@dataclasses.dataclass(slots=True, frozen=True)
class SQLUnionType(SQLBaseAlone):
    """组合类型"""

    union_type: EnumUnionType = dataclasses.field(kw_only=True)  # 组合类型的枚举类

    def source(self, data_source: DataSource) -> str:
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


@dataclasses.dataclass(slots=True, frozen=True)
class SQLCompareOperator(SQLBaseAlone):
    """比较运算符"""

    compare_operator: EnumCompareOperator = dataclasses.field(kw_only=True)  # 比较运算符的枚举类

    def source(self, data_source: DataSource) -> str:
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


@dataclasses.dataclass(slots=True, frozen=True)
class SQLComputeOperator(SQLBaseAlone):
    """计算运算符"""

    compute_operator: EnumComputeOperator = dataclasses.field(kw_only=True)  # 计算运算符的枚举类

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        if self.compute_operator == EnumComputeOperator.MOD and data_source != DataSource.SQL_SERVER:
            raise UnSupportDataSourceError(f"{data_source} 不支持使用 % 运算符")
        if (self.compute_operator == EnumComputeOperator.CONCAT
                and data_source not in {DataSource.ORACLE, DataSource.DB2, DataSource.POSTGRE_SQL}):
            raise UnSupportDataSourceError(f"{data_source} 不支持使用 || 运算符")
        return self.compute_operator.value


# ---------------------------------------- 逻辑运算符 ----------------------------------------


class EnumLogicalOperator(enum.Enum):
    """逻辑运算符的枚举类"""
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


@dataclasses.dataclass(slots=True, frozen=True)
class SQLLogicalOperator(SQLBaseAlone):
    """逻辑运算符"""

    logical_operator: EnumLogicalOperator = dataclasses.field(kw_only=True)  # 逻辑运算符的枚举类

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return self.logical_operator.value


# ---------------------------------------- 一般表达式的抽象基类 ----------------------------------------


class SQLGeneralExpression(SQLBase, abc.ABC):
    """一般表达式的抽象基类"""


# ---------------------------------------- 字面值表达式 ----------------------------------------


class SQLLiteralExpression(SQLBaseAlone, SQLGeneralExpression, abc.ABC):
    """字面值表达式"""

    def as_int(self) -> Optional[int]:
        """将字面值作为整形返回"""
        return None

    def as_string(self) -> str:
        """将字面值作为字符串返回"""
        return self.source(DataSource.DEFAULT)

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return []


@dataclasses.dataclass(slots=True, frozen=True)
class SQLLiteralIntegerExpression(SQLLiteralExpression):
    """整数字面值"""

    value: int = dataclasses.field(kw_only=True)  # 字面值

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.value}"

    def as_int(self) -> int:
        return self.value

    def as_string(self) -> str:
        return f"{self.value}"


@dataclasses.dataclass(slots=True, frozen=True)
class SQLLiteralFloatExpression(SQLLiteralExpression):
    """浮点数字面值"""

    value: float = dataclasses.field(kw_only=True)  # 字面值

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.value}"

    def as_string(self) -> str:
        return f"{self.value}"


@dataclasses.dataclass(slots=True, frozen=True)
class SQLLiteralStringExpression(SQLLiteralExpression):
    """字符串字面值"""

    value: str = dataclasses.field(kw_only=True)  # 字面值

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"'{self.value}'"

    def as_int(self) -> Optional[int]:
        if self.value.isdigit():
            return int(self.value)
        return None

    def as_string(self) -> Optional[str]:
        return self.value


@dataclasses.dataclass(slots=True, frozen=True)
class SQLLiteralHexExpression(SQLLiteralExpression):
    """十六进制字面值"""

    value: str = dataclasses.field(kw_only=True)  # 字面值

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"x'{self.value}'"

    def as_string(self) -> str:
        return f"{self.value}"


@dataclasses.dataclass(slots=True, frozen=True)
class SQLLiteralBitExpression(SQLLiteralExpression):
    """位值字面值"""

    value: str = dataclasses.field(kw_only=True)  # 字面值

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"b'{self.value}'"

    def as_string(self) -> str:
        return f"{self.value}"


@dataclasses.dataclass(slots=True, frozen=True)
class SQLLiteralBoolExpression(SQLLiteralExpression):
    """布尔值字面值"""

    value: bool = dataclasses.field(kw_only=True)  # 字面值

    def as_int(self) -> int:
        return 1 if self.value is True else 0

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return "TRUE" if self.value is True else "FALSE"


@dataclasses.dataclass(slots=True, frozen=True)
class SQLLiteralNullExpression(SQLLiteralExpression):
    """空值字面值"""

    value: None = dataclasses.field(init=False, repr=False, compare=False, default=None)  # 字面值

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return "NULL"


# ---------------------------------------- 列名表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLColumnNameExpression(SQLGeneralExpression):
    """列名表达式"""

    table: Optional[str] = dataclasses.field(kw_only=True, default=None)  # 表名称
    column: str = dataclasses.field(kw_only=True)  # 字段名称

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.table}.{self.column}" if self.table is not None else f"{self.column}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return [self.source(DataSource.DEFAULT)]

    def get_used_table_list(self) -> List[str]:
        """获取使用的表名列表"""
        return []


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


@dataclasses.dataclass(slots=True, frozen=True)
class SQLFunctionExpression(SQLGeneralExpression, abc.ABC):
    """函数表达式的抽象基类"""

    schema_name: Optional[str] = dataclasses.field(kw_only=True, default=None)  # 模式名称
    function_name: str = dataclasses.field(kw_only=True)  # 函数名称

    def _get_function_str(self) -> str:
        return f"{self.schema_name}.{self.function_name}" if self.schema_name is not None else f"{self.function_name}"


@dataclasses.dataclass(slots=True, frozen=True)
class SQLNormalFunctionExpression(SQLFunctionExpression):
    """包含一般参数的函数表达式"""

    function_params: List[SQLGeneralExpression] = dataclasses.field(kw_only=True)  # 函数表达式的参数

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self._get_function_str()}({self._get_param_str(data_source)})"

    def _get_param_str(self, data_source: DataSource) -> str:
        return ", ".join(param.source(data_source) for param in self.function_params)

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return chain_list(param.get_used_column_list() for param in self.function_params)

    def get_used_table_list(self) -> List[str]:
        """获取使用的表名列表"""
        return chain_list(param.get_used_table_list() for param in self.function_params)


@dataclasses.dataclass(slots=True, frozen=True)
class SQLAggregationFunctionExpression(SQLNormalFunctionExpression):
    """聚合函数表达式"""

    is_distinct: bool = dataclasses.field(kw_only=True)  # 是否包含 DISTINCT 关键字

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        is_distinct = "DISTINCT " if self.is_distinct is True else ""
        return f"{self._get_function_str()}({is_distinct}{self._get_param_str(data_source)})"


@dataclasses.dataclass(slots=True, frozen=True)
class SQLCastDataType(SQLBaseAlone):
    """CAST 语句中的数据类型"""

    signed: bool = dataclasses.field(kw_only=True)  # 是否包含 SIGNED 关键字
    data_type: EnumCastDataType = dataclasses.field(kw_only=True)  # 目标转换的数据类型
    params: Optional[List[SQLGeneralExpression]] = dataclasses.field(kw_only=True)  # 目标转换的数据类型的参数列表

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        result = []
        if self.signed is True:
            result.append("SIGNED")
        result.append(self.data_type.value)
        if self.params is not None:
            param_str = ", ".join(param.source(data_source) for param in self.params)
            result.append(f"({param_str})")
        return " ".join(result)


@dataclasses.dataclass(slots=True, frozen=True)
class SQLCastFunctionExpression(SQLFunctionExpression):
    """Cast 函数表达式"""

    function_name: str = dataclasses.field(init=False, default="CAST")  # 函数名称
    column_expression: SQLGeneralExpression = dataclasses.field(kw_only=True)  # CAST 表达式中要转换的列表达式
    cast_type: SQLCastDataType = dataclasses.field(kw_only=True)  # CAST 参数中目标要转换的函数类型

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return (f"{self._get_function_str()}"
                f"({self.column_expression.source(data_source)} AS {self.cast_type.source(data_source)})")

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.column_expression.get_used_column_list()

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return self.column_expression.get_used_table_list()


@dataclasses.dataclass(slots=True, frozen=True)
class SQLExtractFunctionExpression(SQLFunctionExpression):
    """Extract 函数表达式"""

    function_name: str = dataclasses.field(init=False, default="EXTRACT")  # 函数名称
    extract_name: SQLGeneralExpression = dataclasses.field(kw_only=True)  # FROM 关键字之前的提取名称
    column_expression: SQLGeneralExpression = dataclasses.field(kw_only=True)  # FROM 关键字之后的一般表达式

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return (f"{self._get_function_str()}({self.extract_name.source(data_source)} "
                f"FROM {self.column_expression.source(data_source)})")

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.column_expression.get_used_column_list()

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return self.column_expression.get_used_table_list()


# ---------------------------------------- 布尔值表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLBoolExpression(SQLBase, abc.ABC):
    """布尔值表达式"""

    is_not: bool = dataclasses.field(kw_only=True)


@dataclasses.dataclass(slots=True, frozen=True)
class SQLBoolOperatorExpression(SQLBoolExpression, abc.ABC):
    """通过运算符或关键字比较运算符前后两个表达式的布尔值表达式"""

    before_value: SQLGeneralExpression = dataclasses.field(kw_only=True)
    after_value: SQLGeneralExpression = dataclasses.field(kw_only=True)

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.before_value.get_used_column_list() + self.after_value.get_used_column_list()

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return self.before_value.get_used_table_list() + self.after_value.get_used_table_list()


@dataclasses.dataclass(slots=True, frozen=True)
class SQLBoolCompareExpression(SQLBoolOperatorExpression):
    """比较运算符布尔值表达式"""

    operator: SQLCompareOperator = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        is_not_str = "NOT " if self.is_not else ""
        return (f"{is_not_str}{self.before_value.source(data_source)} {self.operator.source(data_source)} "
                f"{self.after_value.source(data_source)}")


@dataclasses.dataclass(slots=True, frozen=True)
class SQLBoolIsExpression(SQLBoolOperatorExpression):
    """IS运算符布尔值表达式"""

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        keyword = "IS NOT" if self.is_not else "IS"
        return f"{self.before_value.source(data_source)} {keyword} {self.after_value.source(data_source)}"


@dataclasses.dataclass(slots=True, frozen=True)
class SQLBoolInExpression(SQLBoolOperatorExpression):
    """In 关键字的布尔值表达式"""

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        keyword = "NOT IN " if self.is_not else "IN"
        return f"{self.before_value.source(data_source)} {keyword} {self.after_value.source(data_source)}"


@dataclasses.dataclass(slots=True, frozen=True)
class SQLBoolLikeExpression(SQLBoolOperatorExpression):
    """LIKE 运算符关联表达式"""

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        keyword = "NOT LIKE" if self.is_not else "LIKE"
        return f"{self.before_value.source(data_source)} {keyword} {self.after_value.source(data_source)}"


@dataclasses.dataclass(slots=True, frozen=True)
class SQLBoolExistsExpression(SQLBoolExpression):
    """Exists 运算符关联表达式"""

    after_value: SQLGeneralExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        keyword = "NOT EXISTS" if self.is_not else "EXISTS"
        return f"{keyword} {self.after_value.source(data_source)}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.after_value.get_used_column_list()

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return self.after_value.get_used_table_list()


@dataclasses.dataclass(slots=True, frozen=True)
class SQLBoolBetweenExpression(SQLBoolExpression):
    """BETWEEN 关联表达式"""

    before_value: SQLGeneralExpression = dataclasses.field(kw_only=True)
    from_value: SQLGeneralExpression = dataclasses.field(kw_only=True)
    to_value: SQLGeneralExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        if_not_str = "NOT " if self.is_not else ""
        return (f"{self.before_value.source(data_source)} {if_not_str}"
                f"BETWEEN {self.from_value.source(data_source)} AND {self.to_value.source(data_source)}")

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return (self.before_value.get_used_column_list() + self.from_value.get_used_column_list()
                + self.to_value.get_used_column_list())

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return (self.before_value.get_used_table_list() + self.from_value.get_used_table_list()
                + self.to_value.get_used_table_list())


# ---------------------------------------- 数组下标表达式 ----------------------------------------


class SQLArrayIndexExpression(SQLGeneralExpression):
    """数组下标表达式"""

    def __init__(self, array_expression: SQLGeneralExpression, idx: int):
        self._array_expression = array_expression
        self._idx = idx

    @property
    def array_expression(self) -> SQLGeneralExpression:
        """返回数组的一般表达式"""
        return self._array_expression

    @property
    def idx(self) -> int:
        """返回下标"""
        return self._idx

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        if data_source != DataSource.HIVE:
            raise UnSupportDataSourceError(f"数组下标不支持SQL类型:{data_source}")
        return f"{self.array_expression.source(data_source)}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.array_expression.get_used_column_list()

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return self.array_expression.get_used_column_list()


# ---------------------------------------- 窗口表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLWindowExpression(SQLGeneralExpression):
    """窗口表达式"""

    window_function: Union[SQLNormalFunctionExpression, SQLArrayIndexExpression] = dataclasses.field(kw_only=True)
    partition_by: Optional[SQLGeneralExpression] = dataclasses.field(kw_only=True)
    order_by: Optional[SQLGeneralExpression] = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        result = f"{self.window_function.source(data_source)} OVER ("
        parenthesis = []
        if self.partition_by is not None:
            parenthesis.append(f"PARTITION BY {self.partition_by.source(data_source)}")
        if self.order_by is not None:
            parenthesis.append(f"ORDER BY {self.order_by.source(data_source)}")
        result += " ".join(parenthesis) + ")"
        return result

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        result = []
        result.extend(self.partition_by.get_used_column_list() if self.partition_by is not None else [])
        result.extend(self.order_by.get_used_column_list() if self.order_by is not None else [])
        return result

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        result = []
        result.extend(self.partition_by.get_used_table_list() if self.partition_by is not None else [])
        result.extend(self.order_by.get_used_table_list() if self.order_by is not None else [])
        return result


# ---------------------------------------- 通配符表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLWildcardExpression(SQLGeneralExpression):
    """通配符表达式"""

    schema: Optional[str] = dataclasses.field(kw_only=True, default=None)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.schema}.*" if self.schema is not None else "*"

    def get_used_column_list(self) -> List[str]:
        """获取语句结果中使用的字段"""
        return [self.source(DataSource.DEFAULT)]

    def get_used_table_list(self) -> List[str]:
        """获取语句结果中使用的字段"""
        return []


# ---------------------------------------- 条件表达式 ----------------------------------------

@dataclasses.dataclass(slots=True, frozen=True)
class SQLConditionExpression(SQLGeneralExpression):
    """条件表达式"""

    elements: List[Union["SQLConditionExpression", SQLBoolExpression, SQLLogicalOperator]] = dataclasses.field(
        kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return " ".join(f"({element.source(data_source)})"
                        if isinstance(element, SQLConditionExpression) else element.source(data_source)
                        for element in self.elements)

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return chain_list(element.get_used_column_list() for element in self.elements)

    def get_used_table_list(self) -> List[str]:
        """获取使用的字段列表"""
        return chain_list(element.get_used_table_list() for element in self.elements)


# ---------------------------------------- CASE 表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLCaseExpression(SQLGeneralExpression):
    """第 1 种格式的 CASE 表达式

    CASE
        WHEN {条件表达式} THEN {一般表达式}
        ELSE {一般表达式}
    END
    """

    cases: List[Tuple[SQLConditionExpression, SQLGeneralExpression]] = dataclasses.field(kw_only=True)
    else_value: Optional[SQLGeneralExpression] = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        result = ["CASE"]
        for when, then in self.cases:
            result.append(f"WHEN {when.source(data_source)} THEN {then.source(data_source)}")
        if self.else_value is not None:
            result.append(f"ELSE {self.else_value.source(data_source)}")
        result.append("END")
        return " ".join(result)

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return chain_list(when.get_used_column_list() for when, _ in self.cases)

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return chain_list(when.get_used_table_list() for when, _ in self.cases)


@dataclasses.dataclass(slots=True, frozen=True)
class SQLCaseValueExpression(SQLGeneralExpression):
    """第 2 种格式的 CASE 表达式

    CASE {一般表达式}
        WHEN {一般表达式} THEN {一般表达式}
        ELSE {一般表达式}
    END
    """

    case_value: SQLGeneralExpression = dataclasses.field(kw_only=True)
    cases: List[Tuple[SQLGeneralExpression, SQLGeneralExpression]] = dataclasses.field(kw_only=True)
    else_value: Optional[SQLGeneralExpression] = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        result = ["CASE", self.case_value.source(data_source)]
        for when, then in self.cases:
            result.append(f"    WHEN {when.source(data_source)} THEN {then.source(data_source)}")
        if self.else_value is not None:
            result.append(f"    ELSE {self.else_value.source(data_source)}")
        result.append("END")
        return "\n".join(result)

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return (self.case_value.get_used_column_list()
                + chain_list(when.get_used_column_list() for when, _ in self.cases))

    def get_used_table_list(self) -> List[str]:
        """获取使用的字段列表"""
        return (self.case_value.get_used_table_list()
                + chain_list(when.get_used_table_list() for when, _ in self.cases))


# ---------------------------------------- 计算表达式 ----------------------------------------

@dataclasses.dataclass(slots=True, frozen=True)
class SQLComputeExpression(SQLGeneralExpression):
    """计算表达式"""

    elements: List[Union[SQLGeneralExpression, SQLComputeOperator]] = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return " ".join(element.source(data_source) for element in self.elements)

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return chain_list(element.get_used_column_list() for element in self.elements)

    def get_used_table_list(self) -> List[str]:
        """获取使用的字段列表"""
        return chain_list(element.get_used_table_list() for element in self.elements)


# ---------------------------------------- 值表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLValueExpression(SQLBaseAlone, SQLGeneralExpression):
    """INSERT INTO 表达式中，VALUES 里的表达式"""

    values: List[SQLGeneralExpression] = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        values_str = ", ".join(value.source(data_source) for value in self.values)
        return f"({values_str})"


# ---------------------------------------- 子查询表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLSubQueryExpression(SQLGeneralExpression):
    """子查询表达式"""

    select_statement: "SQLSelectStatement" = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"({self.select_statement.source(data_source)})"

    def get_used_column_list(self) -> List[str]:
        """返回使用的字段列表"""
        return self.select_statement.get_used_column_list()

    def get_used_table_list(self) -> List[str]:
        """返回使用的表列表"""
        return self.select_statement.get_used_table_list()


# ---------------------------------------- 表名表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLTableNameExpression(SQLBase):
    """表名表达式"""

    schema: Optional[str] = dataclasses.field(kw_only=True, default=None)
    table: str = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.schema}.{self.table}" if self.schema is not None else f"{self.table}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return []

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return [self.source(DataSource.DEFAULT)]


# ---------------------------------------- 别名表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLAlisaExpression(SQLBaseAlone):
    """别名表达式"""

    name: str = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"AS {self.name}"


# ---------------------------------------- 关联表达式 ----------------------------------------


class SQLJoinExpression(SQLBase, abc.ABC):
    """关联表达式"""


@dataclasses.dataclass(slots=True, frozen=True)
class SQLJoinOnExpression(SQLJoinExpression):
    """ON 关联表达式"""

    condition: SQLConditionExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"ON {self.condition.source(data_source)}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.condition.get_used_column_list()

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return self.condition.get_used_table_list()


@dataclasses.dataclass(slots=True, frozen=True)
class SQLJoinUsingExpression(SQLJoinExpression):
    """USING 关联表达式"""

    using_function: SQLFunctionExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.using_function.source(data_source)}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.using_function.get_used_column_list()

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return self.using_function.get_used_table_list()


# ---------------------------------------- 字段类型表达式 ----------------------------------------

@dataclasses.dataclass(slots=True, frozen=True)
class SQLColumnTypeExpression(SQLBaseAlone):
    """字段类型表达式"""

    name: str = dataclasses.field(kw_only=True)
    params: Optional[List[SQLGeneralExpression]] = dataclasses.field(kw_only=True, default=None)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        if self.params is None or data_source == DataSource.HIVE:
            return self.name
        type_params = "(" + ", ".join([param.source(data_source) for param in self.params]) + ")"
        return f"{self.name}{type_params}"


# ---------------------------------------- 表表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLTableExpression(SQLBase):
    """表表达式"""

    table: Union[SQLTableNameExpression, SQLSubQueryExpression] = dataclasses.field(kw_only=True)
    alias: Optional[SQLAlisaExpression] = dataclasses.field(kw_only=True, default=None)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        if self.alias is not None:
            return f"{self.table.source(data_source)} {self.alias.source(data_source)}"
        return f"{self.table.source(data_source)}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return []

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return self.table.get_used_table_list()


# ---------------------------------------- 列表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLColumnExpression(SQLBase):
    """列表达式"""

    column: SQLGeneralExpression = dataclasses.field(kw_only=True)
    alias: Optional[SQLAlisaExpression] = dataclasses.field(kw_only=True, default=None)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        if self.alias is not None:
            return f"{self.column.source(data_source)} {self.alias.source(data_source)}"
        return f"{self.column.source(data_source)}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.column.get_used_column_list()

    def get_used_table_list(self) -> List[str]:
        """返回使用的表列表"""
        return []


# ---------------------------------------- 等式表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLEqualExpression(SQLBase):
    """等式表达式"""

    before_value: SQLGeneralExpression = dataclasses.field(kw_only=True)
    after_value: SQLGeneralExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.before_value.source(data_source)} = {self.after_value.source(data_source)}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.before_value.get_used_column_list() + self.after_value.get_used_column_list()

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return self.before_value.get_used_table_list() + self.after_value.get_used_table_list()


# ---------------------------------------- 分区表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLPartitionExpression(SQLBase):
    """分区表达式：PARTITION (<partition_expression>)"""

    partition_list: List[SQLEqualExpression] = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        partition_list_str = ", ".join(partition.source(data_source) for partition in self.partition_list)
        return f"PARTITION ({partition_list_str})"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return chain_list(partition.get_used_column_list() for partition in self.partition_list)

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return chain_list(partition.get_used_table_list() for partition in self.partition_list)


# ---------------------------------------- 声明外键表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLForeignKeyExpression(SQLBaseAlone):
    """声明外键表达式"""

    constraint_name: str = dataclasses.field(kw_only=True)
    slave_columns: List[str] = dataclasses.field(kw_only=True)
    master_table_name: str = dataclasses.field(kw_only=True)
    master_columns: List[str] = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        slave_columns_str = ", ".join([f"{column}" for column in self.slave_columns])
        master_columns_str = ", ".join([f"{column}" for column in self.master_columns])
        return (f"CONSTRAINT {self.constraint_name} FOREIGN KEY({slave_columns_str}) "
                f"REFERENCES {self.master_table_name}({master_columns_str})")


# ---------------------------------------- 声明索引表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLIndexExpression(SQLBaseAlone, abc.ABC):
    """声明索引表达式"""

    name: Optional[str] = dataclasses.field(kw_only=True, default=None)
    columns: List[str] = dataclasses.field(kw_only=True)


@dataclasses.dataclass(slots=True, frozen=True)
class SQLPrimaryIndexExpression(SQLIndexExpression):
    """主键索引声明表达式"""

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        columns_str = ", ".join([f"{column}" for column in self.columns])
        return f"PRIMARY KEY ({columns_str})" if self.columns is not None else ""


@dataclasses.dataclass(slots=True, frozen=True)
class SQLUniqueIndexExpression(SQLIndexExpression):
    """唯一键索引声明表达式"""

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        columns_str = ", ".join([f"{column}" for column in self.columns])
        return f"UNIQUE KEY {self.name} ({columns_str})"


@dataclasses.dataclass(slots=True, frozen=True)
class SQLNormalIndexExpression(SQLIndexExpression):
    """普通索引声明表达式"""

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        columns_str = ", ".join([f"{column}" for column in self.columns])
        return f"KEY {self.name} ({columns_str})"


@dataclasses.dataclass(slots=True, frozen=True)
class SQLFulltextIndexExpression(SQLIndexExpression):
    """全文本索引声明表达式"""

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        columns_str = ", ".join([f"{column}" for column in self.columns])
        return f"FULLTEXT KEY {self.name} ({columns_str})"


# ---------------------------------------- 声明字段表达式 ----------------------------------------


@dataclasses.dataclass(slots=True)
class SQLDefineColumnExpression(SQLBaseAlone):
    """声明字段表达式"""

    column_name: str = dataclasses.field(kw_only=True)
    column_type: SQLColumnTypeExpression = dataclasses.field(kw_only=True)
    comment: Optional[str] = dataclasses.field(kw_only=True, default=None)
    is_unsigned: bool = dataclasses.field(kw_only=True, default=False)
    is_zerofill: bool = dataclasses.field(kw_only=True, default=False)
    character_set: Optional[str] = dataclasses.field(kw_only=True, default=None)
    collate: Optional[str] = dataclasses.field(kw_only=True, default=None)
    is_allow_null: bool = dataclasses.field(kw_only=True, default=False)
    is_not_null: bool = dataclasses.field(kw_only=True, default=False)
    is_auto_increment: bool = dataclasses.field(kw_only=True, default=False)
    default: Optional[SQLGeneralExpression] = dataclasses.field(kw_only=True, default=None)
    on_update: Optional[SQLGeneralExpression] = dataclasses.field(kw_only=True, default=None)

    @property
    def column_name_without_quote(self) -> str:
        """返回没有被引号框柱的列名"""
        return self.column_name

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        res = f"{self.column_name} {self.column_type.source(data_source)}"
        if self.is_unsigned is True and data_source == DataSource.MYSQL:
            res += " UNSIGNED"
        if self.is_zerofill is True and data_source == DataSource.MYSQL:
            res += " ZEROFILL"
        if self.character_set is not None and data_source == DataSource.MYSQL:
            res += f" CHARACTER SET {self.character_set}"
        if self.collate is not None and data_source == DataSource.MYSQL:
            res += f" COLLATE {self.collate}"
        if self.is_allow_null is True and data_source == DataSource.MYSQL:
            res += " NULL"
        if self.is_not_null is True and data_source == DataSource.MYSQL:
            res += " NOT NULL"
        if self.is_auto_increment is True and data_source == DataSource.MYSQL:
            res += " AUTO_INCREMENT"
        if self.default is not None and data_source == DataSource.MYSQL:
            res += f" DEFAULT {self.default.source(data_source)}"
        if self.on_update is not None and data_source == DataSource.MYSQL:
            res += f" ON UPDATE {self.on_update.source(data_source)}"
        if self.comment is not None:
            res += f" COMMENT {self.comment}"
        return res


# ---------------------------------------- 配置名称和配置值表达式 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLConfigNameExpression(SQLBaseAlone):
    """配置名称表达式"""

    config_name: str = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return self.config_name


@dataclasses.dataclass(slots=True, frozen=True)
class SQLConfigValueExpression(SQLBaseAlone):
    """配置值表达式"""

    config_value: str = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return self.config_value


# ---------------------------------------- SELECT 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLSelectClause(SQLBase):
    """SELECT 子句"""

    distinct: bool = dataclasses.field(kw_only=True)
    columns: List[SQLColumnExpression] = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        result = ["SELECT"]
        if self.distinct is True:
            result.append("DISTINCT")
        result.append(", ".join(column.source(data_source) for column in self.columns))
        return " ".join(result)

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return chain_list(column.get_used_column_list() for column in self.columns)

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return []

    def get_alias_to_used_column_hash(self) -> Dict[str, List[str]]:
        """获取字段别名对应的原始字段的列表"""
        return {column.alias.name: column.get_used_column_list()
                for column in self.columns if column.alias is not None}

    def get_index_to_used_column_hash(self) -> Dict[int, List[str]]:
        """获取字段序号对应的原始字段列表的映射表"""
        return {idx + 1: column.get_used_column_list() for idx, column in enumerate(self.columns)}  # 列编号从 1 开始


# ---------------------------------------- FROM 子句 ----------------------------------------

@dataclasses.dataclass(slots=True, frozen=True)
class SQLFromClause(SQLBase):
    """FROM 子句"""

    tables: List[SQLTableExpression] = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return "FROM " + ", ".join(table.source(data_source) for table in self.tables)

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return []

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return chain_list(table.get_used_table_list() for table in self.tables)


# ---------------------------------------- LATERAL VIEW 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLLateralViewClause(SQLBase):
    """LATERAL VIEW 子句"""

    function: SQLFunctionExpression = dataclasses.field(kw_only=True)
    view_name: str = dataclasses.field(kw_only=True)
    alias: SQLAlisaExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"LATERAL VIEW {self.function.source(data_source)} {self.view_name} {self.alias.source(data_source)}"

    def get_used_column_list(self) -> List[str]:
        """返回使用的字段列表"""
        return self.function.get_used_column_list()

    def get_used_table_list(self) -> List[str]:
        """返回使用的表列表"""
        return []


# ---------------------------------------- JOIN 子句 ----------------------------------------

@dataclasses.dataclass(slots=True, frozen=True)
class SQLJoinClause(SQLBase):
    """JOIN 子句"""

    join_type: SQLJoinType = dataclasses.field(kw_only=True)
    table: SQLTableExpression = dataclasses.field(kw_only=True)
    join_rule: Optional[SQLJoinExpression] = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        if self.join_rule is not None:
            return (f"{self.join_type.source(data_source)} {self.table.source(data_source)} "
                    f"{self.join_rule.source(data_source)}")
        return f"{self.join_type.source(data_source)} {self.table.source(data_source)}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.join_rule.get_used_column_list()

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return self.table.get_used_table_list()


# ---------------------------------------- WHERE 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLWhereClause(SQLBase):
    """WHERE 子句"""

    condition: SQLConditionExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"WHERE {self.condition.source(data_source)}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.condition.get_used_column_list()

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return []


# ---------------------------------------- GROUP BY 子句 ----------------------------------------

class SQLGroupByClause(SQLBase, abc.ABC):
    """GROUP BY 子句"""


@dataclasses.dataclass(slots=True, frozen=True)
class SQLNormalGroupByClause(SQLGroupByClause):
    """普通 GROUP BY 子句"""

    columns: List[SQLGeneralExpression] = dataclasses.field(kw_only=True)
    with_rollup: bool = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        if self.with_rollup:
            return "GROUP BY " + ", ".join(column.source(data_source) for column in self.columns) + " WITH ROLLUP"
        return "GROUP BY " + ", ".join(column.source(data_source) for column in self.columns)

    def get_used_column_list(self) -> List[Union[str, int]]:
        """返回使用的字段列表（和字段序号）"""
        result = []
        for column in self.columns:
            if isinstance(column, SQLLiteralExpression):
                result.append(column.as_int())  # 列编号
            else:
                result.extend(column.get_used_column_list())
        return result

    def get_used_table_list(self) -> List[str]:
        """返回使用的表列表"""
        return []


@dataclasses.dataclass(slots=True, frozen=True)
class SQLGroupingSetsGroupByClause(SQLGroupByClause):
    """使用 GROUPING SETS 语法的 GROUP BY 子句"""

    grouping_list: List[List[SQLGeneralExpression]] = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        grouping_str_list = []
        for grouping in self.grouping_list:
            if len(grouping) > 1:
                grouping_str_list.append("(" + ", ".join(column.source(data_source) for column in grouping) + ")")
            else:
                grouping_str_list.append(grouping[0].source(data_source))
        return "GROUP BY GROUPING SETS (" + ", ".join(grouping_str_list) + ")"

    def get_used_column_list(self) -> List[Union[str, int]]:
        """返回使用的字段列表（和字段序号）"""
        result = []
        for grouping in self.grouping_list:
            for column in grouping:
                if isinstance(column, SQLLiteralExpression):
                    result.append(column.as_int())  # 列编号
                else:
                    result.extend(column.get_used_column_list())
        return result

    def get_used_table_list(self) -> List[str]:
        """返回使用的表列表"""
        return []


# ---------------------------------------- HAVING 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLHavingClause(SQLBase):
    """HAVING 子句"""

    condition: SQLConditionExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"HAVING {self.condition.source(data_source)}"

    def get_used_column_list(self) -> List[str]:
        """返回使用的字段列表"""
        return self.condition.get_used_column_list()

    def get_used_table_list(self) -> List[str]:
        """返回使用的表列表"""
        return self.condition.get_used_table_list()


# ---------------------------------------- ORDER BY 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLOrderByClause(SQLBase):
    """ORDER BY 子句"""

    columns: List[Tuple[SQLGeneralExpression, SQLOrderType]] = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        result = []
        for column, order_type in self.columns:
            if order_type.source(data_source) == "ASC":
                result.append(f"{column.source(data_source)}")
            else:
                result.append(f"{column.source(data_source)} DESC")
        return "ORDER BY " + ", ".join(result)

    def get_used_column_list(self) -> List[Union[str, int]]:
        """返回使用的字段列表（和字段序号）"""
        result = []
        for column, _ in self.columns:
            if isinstance(column, SQLLiteralExpression):
                result.append(column.as_int())  # 列编号
            else:
                result.extend(column.get_used_column_list())
        return result

    def get_used_table_list(self) -> List[str]:
        """返回使用的表列表"""
        return []


# ---------------------------------------- LIMIT 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLLimitClause(SQLBaseAlone):
    """LIMIT 子句"""

    limit: int = dataclasses.field(kw_only=True)
    offset: int = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"LIMIT {self.offset}, {self.limit}"


# ---------------------------------------- WITH 子句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLWithClause(SQLBase):
    """WITH 子句"""

    tables: List[Tuple[str, "SQLSelectStatement"]] = dataclasses.field(kw_only=True)

    @staticmethod
    def empty():
        """空 WITH 子句"""
        return SQLWithClause(tables=[])

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        if not self.tables:
            return ""
        table_str = ", \n".join(f"{table_name}({table_statement.source(data_source)})"
                                for table_name, table_statement in self.tables)
        return f"WITH {table_str}"

    def get_with_table_name_set(self) -> Set[str]:
        """获取 WITH 中临时表的名称"""
        return set(table[0] for table in self.tables)

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return chain_list(select_statement.get_used_column_list() for _, select_statement in self.tables)

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        with_table_name_set = self.get_with_table_name_set()
        result = []
        for _, select_statement in self.tables:
            result.extend([table_name for table_name in select_statement.get_used_table_list()
                           if table_name not in with_table_name_set])
        return ordered_distinct(result)

    def is_empty(self):
        """返回 WITH 语句是否为空"""
        return len(self.tables) == 0


# ---------------------------------------- 语句的抽象基类 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLStatement(SQLBase, abc.ABC):
    """语句的抽象基类"""

    with_clause: Optional[SQLWithClause] = dataclasses.field(kw_only=True, default=None)


# ---------------------------------------- SELECT 语句 ----------------------------------------


class SQLSelectStatement(SQLStatement, abc.ABC):
    """SELECT 语句"""

    @abc.abstractmethod
    def get_from_used_table_list(self) -> List[str]:
        """获取 FROM 语句中使用的表名的列表"""

    @abc.abstractmethod
    def get_join_used_table_list(self) -> List[str]:
        """获取 JOIN 语句中使用的表名的列表"""

    @abc.abstractmethod
    def get_select_used_column_list(self) -> List[str]:
        """获取 SELECT 语句结果中使用的字段的列表"""

    @abc.abstractmethod
    def get_where_used_column_list(self) -> List[str]:
        """获取在 WHERE 条件中使用的字段名的列表"""

    @abc.abstractmethod
    def get_group_by_used_column_list(self) -> List[str]:
        """获取在 GROUP BY 中使用的字段名的列表"""

    @abc.abstractmethod
    def get_having_used_column_list(self) -> List[str]:
        """获取在 HAVING 中使用的字段名的列表"""

    @abc.abstractmethod
    def get_order_by_used_column_list(self) -> List[str]:
        """获取在 ORDER BY 中使用的字段名的列表"""

    def get_used_table_list(self) -> List[str]:
        """获取使用的表的列表"""
        return ordered_distinct(self.get_from_used_table_list() + self.get_join_used_table_list())

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return ordered_distinct(self.get_select_used_column_list() + self.get_where_used_column_list() +
                                self.get_group_by_used_column_list() + self.get_having_used_column_list() +
                                self.get_order_by_used_column_list())


@dataclasses.dataclass(slots=True, frozen=True)
class SQLSingleSelectStatement(SQLSelectStatement):
    """单个 SELECT 表达式"""

    with_clause: Optional[SQLWithClause] = dataclasses.field(kw_only=True)
    select_clause: SQLSelectClause = dataclasses.field(kw_only=True)
    from_clause: Optional[SQLFromClause] = dataclasses.field(kw_only=True)
    lateral_view_clauses: List[SQLLateralViewClause] = dataclasses.field(kw_only=True)
    join_clauses: List[SQLJoinClause] = dataclasses.field(kw_only=True)
    where_clause: Optional[SQLWhereClause] = dataclasses.field(kw_only=True)
    group_by_clause: Optional[SQLGroupByClause] = dataclasses.field(kw_only=True)
    having_clause: Optional[SQLHavingClause] = dataclasses.field(kw_only=True)
    order_by_clause: Optional[SQLOrderByClause] = dataclasses.field(kw_only=True)
    limit_clause: Optional[SQLLimitClause] = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        with_clause_str = self.with_clause.source(data_source) + "\n" if not self.with_clause.is_empty() else ""
        result = [self.select_clause.source(data_source)]
        for clause in [self.from_clause, *self.lateral_view_clauses, *self.join_clauses, self.where_clause,
                       self.group_by_clause, self.having_clause, self.order_by_clause, self.limit_clause]:
            if clause is not None:
                result.append(clause.source(data_source))
        return with_clause_str + "\n".join(result)

    def get_alias_to_used_column_hash(self) -> Dict[str, List[str]]:
        """获取字段别名对应的原始字段列表的映射表"""
        return self.select_clause.get_alias_to_used_column_hash()

    def get_index_to_used_column_hash(self) -> Dict[int, List[str]]:
        """获取字段序号对应的原始字段列表的映射表"""
        return self.select_clause.get_index_to_used_column_hash()

    def get_from_used_table_list(self) -> List[str]:
        """获取 FROM 语句中使用的表名的列表"""
        return ordered_distinct(self.from_clause.get_used_table_list()) if self.from_clause is not None else []

    def get_join_used_table_list(self) -> List[str]:
        """获取 JOIN 语句中使用的表名的列表"""
        return chain_list(join_clause.get_used_table_list() for join_clause in self.join_clauses)

    def get_select_used_column_list(self) -> List[str]:
        """获取 SELECT 语句结果中使用的字段的列表"""
        return ordered_distinct(self.select_clause.get_used_column_list())

    def get_where_used_column_list(self) -> List[str]:
        """获取在 WHERE 条件中使用的字段名的列表"""
        return ordered_distinct(self.where_clause.get_used_column_list()) if self.where_clause is not None else []

    def get_group_by_used_column_list(self) -> List[str]:
        """获取在 GROUP BY 中使用的字段名的列表"""
        return (self._get_source_column_list(self.group_by_clause.get_used_column_list())
                if self.group_by_clause is not None else [])

    def get_having_used_column_list(self) -> List[str]:
        """获取在 HAVING 中使用的字段名的列表"""
        return (self._get_source_column_list(self.having_clause.get_used_column_list())
                if self.having_clause is not None else [])

    def get_order_by_used_column_list(self) -> List[str]:
        """获取在 ORDER BY 中使用的字段名的列表"""
        return (self._get_source_column_list(self.order_by_clause.get_used_column_list())
                if self.order_by_clause is not None else [])

    def _get_source_column_list(self, column_list: List[Union[str, int]]) -> List[str]:
        """根据别名获取原始表的字段名"""
        alias_to_used_column_hash = self.get_alias_to_used_column_hash()
        index_to_used_column_hash = self.get_index_to_used_column_hash()
        result = []
        for column in column_list:
            if column in alias_to_used_column_hash:
                result.extend(alias_to_used_column_hash[column])  # 列名
            elif column in index_to_used_column_hash:
                result.extend(index_to_used_column_hash[column])  # 列编号
            else:
                result.append(column)
        return ordered_distinct(result)


@dataclasses.dataclass(slots=True, frozen=True)
class SQLUnionSelectStatement(SQLSelectStatement):
    """复合查询语句，使用 UNION、EXCEPT、INTERSECT 进行组合"""

    elements: List[Union[SQLUnionType, SQLSingleSelectStatement]] = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        with_clause_str = self.with_clause.source(data_source) + "\n" if not self.with_clause.is_empty() else ""
        return with_clause_str + "\n".join(element.source(data_source) for element in self.elements)

    def get_from_used_table_list(self) -> List[str]:
        """获取 FROM 语句中使用的表名的列表"""
        return ordered_distinct(chain_list([element.get_from_used_table_list()
                                            for element in self.elements
                                            if isinstance(element, SQLSingleSelectStatement)]))

    def get_join_used_table_list(self) -> List[str]:
        """获取 JOIN 语句中使用的表名的列表"""
        return ordered_distinct(chain_list([element.get_join_used_table_list()
                                            for element in self.elements
                                            if isinstance(element, SQLSingleSelectStatement)]))

    def get_select_used_column_list(self) -> List[str]:
        """获取 SELECT 语句结果中使用的字段的列表"""
        return ordered_distinct(chain_list([element.get_select_used_column_list()
                                            for element in self.elements
                                            if isinstance(element, SQLSingleSelectStatement)]))

    def get_where_used_column_list(self) -> List[str]:
        """获取在 WHERE 条件中使用的字段名的列表"""
        return ordered_distinct(chain_list([element.get_where_used_column_list()
                                            for element in self.elements
                                            if isinstance(element, SQLSingleSelectStatement)]))

    def get_group_by_used_column_list(self) -> List[str]:
        """获取在 GROUP BY 中使用的字段名的列表"""
        return ordered_distinct(chain_list([element.get_group_by_used_column_list()
                                            for element in self.elements
                                            if isinstance(element, SQLSingleSelectStatement)]))

    def get_having_used_column_list(self) -> List[str]:
        """获取在 HAVING 中使用的字段名的列表"""
        return ordered_distinct(chain_list([element.get_having_used_column_list()
                                            for element in self.elements
                                            if isinstance(element, SQLSingleSelectStatement)]))

    def get_order_by_used_column_list(self) -> List[str]:
        """返回在 ORDER BY 子句中使用的字段名的列表"""
        return ordered_distinct(chain_list([element.get_order_by_used_column_list()
                                            for element in self.elements
                                            if isinstance(element, SQLSingleSelectStatement)]))


# ---------------------------------------- INSERT 语句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLInsertStatement(SQLStatement, abc.ABC):
    """INSERT 表达式

    两个子类包含 VALUES 和 SELECT 两种方式

    INSERT {INTO|OVERWRITE} [TABLE] <table_name_expression> [PARTITION (<partition_expression>)]
    [(<colum_name_expression [,<column_name_expression> ...]>)]
    {VALUES <value_expression> [,<value_expression> ...] | <select_statement>}
    """

    insert_type: SQLInsertType = dataclasses.field(kw_only=True)
    table_name: SQLTableNameExpression = dataclasses.field(kw_only=True)
    partition: Optional[SQLPartitionExpression] = dataclasses.field(kw_only=True)
    columns: Optional[List[SQLColumnNameExpression]] = dataclasses.field(kw_only=True)

    def _insert_str(self, data_source: DataSource) -> str:
        insert_type_str = self.insert_type.source(data_source)
        table_keyword_str = "TABLE " if data_source == DataSource.HIVE else ""
        partition_str = self.partition.source(data_source) + " " if self.partition is not None else ""
        if self.columns is not None:
            columns_str = "(" + ", ".join(column.source(data_source) for column in self.columns) + ") "
        else:
            columns_str = ""
        return (f"{insert_type_str} {table_keyword_str}{self.table_name.source(data_source)} "
                f"{partition_str}{columns_str}")


@dataclasses.dataclass(slots=True, frozen=True)
class SQLInsertValuesStatement(SQLInsertStatement):
    """INSERT ... VALUES ... 语句"""

    values: List[SQLValueExpression] = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        values_str = ", ".join(value.source(data_source) for value in self.values)
        return f"{self._insert_str(data_source)}VALUES {values_str}"

    def get_used_table_list(self) -> List[str]:
        """获取使用的表的列表"""
        return []

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return []


@dataclasses.dataclass(slots=True, frozen=True)
class SQLInsertSelectStatement(SQLInsertStatement):
    """INSERT ... SELECT ... 语句"""

    select_statement: SQLSelectStatement = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self._insert_str(data_source)} {self.select_statement.source(data_source)}"

    def get_used_table_list(self) -> List[str]:
        """获取使用的表的列表"""
        with_table_name_set = self.with_clause.get_with_table_name_set()
        result = self.with_clause.get_used_table_list()
        for table_name in self.select_statement.get_used_table_list():
            if table_name not in with_table_name_set:
                result.append(table_name)
        return ordered_distinct(result)

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.select_statement.get_used_column_list()


# ---------------------------------------- SET 语句 ----------------------------------------


@dataclasses.dataclass(slots=True, frozen=True)
class SQLSetStatement(SQLBaseAlone):
    """SQL 语句"""

    config_name: SQLConfigNameExpression = dataclasses.field(kw_only=True)
    config_value: SQLConfigValueExpression = dataclasses.field(kw_only=True)

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"SET {self.config_name.source(data_source)} = {self.config_value.source(data_source)}"


# ---------------------------------------- CREATE TABLE 语句 ----------------------------------------


# class SQLTableConfigExpression(SQLBaseAlone):
#     """建表语句配置信息表达式"""


@dataclasses.dataclass(slots=True)
class SQLCreateTableStatement(SQLBaseAlone):
    """【DDL】CREATE TABLE 语句"""

    table_name_expression: SQLTableNameExpression = dataclasses.field(kw_only=True)
    comment: Optional[str] = dataclasses.field(kw_only=True)
    if_not_exists: bool = dataclasses.field(kw_only=True)
    columns: Optional[List[SQLDefineColumnExpression]] = dataclasses.field(kw_only=True)
    primary_key: Optional[SQLPrimaryIndexExpression] = dataclasses.field(kw_only=True)
    unique_key: Optional[List[SQLUniqueIndexExpression]] = dataclasses.field(kw_only=True)
    key: Optional[List[SQLNormalIndexExpression]] = dataclasses.field(kw_only=True)
    fulltext_key: Optional[List[SQLFulltextIndexExpression]] = dataclasses.field(kw_only=True)
    foreign_key: List[SQLForeignKeyExpression] = dataclasses.field(kw_only=True)
    engine: Optional[str] = dataclasses.field(kw_only=True)
    auto_increment: Optional[int] = dataclasses.field(kw_only=True)
    default_charset: Optional[str] = dataclasses.field(kw_only=True)
    collate: Optional[str] = dataclasses.field(kw_only=True)
    row_format: Optional[str] = dataclasses.field(kw_only=True)
    states_persistent: Optional[str] = dataclasses.field(kw_only=True)
    partition_by: List[SQLDefineColumnExpression] = dataclasses.field(kw_only=True)

    def change_type(self, hashmap: Dict[str, str], remove_param: bool = True):
        """更新每个字段的变量类型"""
        for column in self.columns:
            old_column_type = column.column_type
            column.column_type = SQLColumnTypeExpression(name=hashmap[old_column_type.name.upper()],
                                                         params=None if remove_param else old_column_type.params)

    def append_column(self, column: SQLDefineColumnExpression):
        """添加字段"""
        self.columns.append(column)

    def append_partition_by_column(self, column: SQLDefineColumnExpression):
        """添加分区字段"""
        self.partition_by.append(column)

    def source(self, data_source: DataSource, n_indent: int = 4) -> str:
        """返回语法节点的 SQL 源码"""
        if data_source == DataSource.MYSQL:
            indentation = " " * n_indent  # 缩进字符串
            result = f" {self._title_str(data_source)}(\n"
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
                result += f" ENGINE = {self.engine}"
            if self.auto_increment is not None:
                result += f" AUTO_INCREMENT = {self.auto_increment}"
            if self.default_charset is not None:
                result += f" DEFAULT CHARSET = {self.default_charset}"
            if self.collate is not None:
                result += f" COLLATE = {self.collate}"
            if self.states_persistent is not None:
                result += f" STATS_PERSISTENT = {self.states_persistent}"
            if self.comment is not None:
                result += f" COMMENT = {self.comment}"
            return result
        if data_source == DataSource.HIVE:
            indentation = " " * n_indent  # 缩进字符串
            result = f" {self._title_str(data_source)}(\n"
            columns_and_keys = []
            for column in self.columns:
                columns_and_keys.append(f"{indentation}{column.source(data_source)}")
            result += ",\n".join(columns_and_keys)
            result += "\n)"
            if self.comment is not None:
                result += f" COMMENT {self.comment}"
            if len(self.partition_by) > 0:
                partition_columns = []
                for column in self.partition_by:
                    partition_columns.append(column.source(data_source))
                partition_str = ", ".join(partition_columns)
                result += f" PARTITIONED BY ({partition_str})"
            return result
        raise SqlParseError(f"暂不支持的数据类型: {data_source}")

    def _title_str(self, data_source: DataSource) -> str:
        is_not_exists_str = " IF NOT EXISTS" if self.if_not_exists is True else ""
        return f"CREATE TABLE{is_not_exists_str} {self.table_name_expression.source(data_source)}"
