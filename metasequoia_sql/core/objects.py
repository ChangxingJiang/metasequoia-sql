# pylint: disable=C0302

"""
语法节点

因为不同语法节点之间需要相互引用，所以脚本文件不可避免地需要超过 1000 行，故忽略 pylint C0302。

TODO 统一 SQLBase 的抽象方法：增加 get_used_column_list 和 get_used_table_list
TODO 不返回 CURRENT_DATE、CURRENT_TIME、CURRENT_TIMESTAMP 作为字段
TODO 增加 scanner 未解析完成的发现机制
TODO 存在重复代码的类优化
TODO 移除 data_source 的默认值
"""

import abc
import enum
from typing import Optional, List, Tuple, Union, Dict, Set

from metasequoia_sql.common.basic import ordered_distinct
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
    "EnumCastDataType", "SQLFunctionExpression", "SQLAggregationFunctionExpression", "SQLCastDataType",
    "SQLCastFunctionExpression", "SQLExtractFunctionExpression",

    # 一般表达式：布尔值表达式
    "SQLBoolExpression", "SQLBoolCompareExpression", "SQLBoolIsExpression", "SQLBoolInExpression",
    "SQLBoolLikeExpression", "SQLBoolExistsExpression", "SQLBoolBetweenExpression",

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

    # 一般表达式：数组下标表达式
    "SQLArrayIndexExpression",

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


class SQLBase(abc.ABC):
    """所有 SQL 语句对象节点的抽象基类

    TODO 待增加 parse 和 check 两个抽象静态方法
    """

    @abc.abstractmethod
    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码

        TODO 待将 MySQL 修改为自动指定
        """

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        """
        TODO 修改 source 生成规则
        """
        return f"<{self.__class__.__name__} source={self.source(DataSource.MYSQL)}>"


# ---------------------------------------- 插入类型 ----------------------------------------


class EnumInsertType(enum.Enum):
    """插入类型的枚举类"""
    INSERT_INTO = ["INSERT", "INTO"]
    INSERT_OVERWRITE = ["INSERT", "OVERWRITE"]


class SQLInsertType(SQLBase):
    """插入类型"""

    def __init__(self, insert_type: EnumInsertType):
        self._insert_type = insert_type

    @property
    def insert_type(self) -> EnumInsertType:
        """返回插入类型的枚举类"""
        return self._insert_type

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


class SQLJoinType(SQLBase):
    """关联类型"""

    def __init__(self, join_type: EnumJoinType):
        self._join_type = join_type

    @property
    def join_type(self) -> EnumJoinType:
        """返回关联类型的枚举类"""
        return self._join_type

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return " ".join(self.join_type.value)


# ---------------------------------------- 排序类型 ----------------------------------------


class EnumOrderType(enum.Enum):
    """排序类型的枚举类"""
    ASC = "ASC"  # 升序
    DESC = "DESC"  # 降序


class SQLOrderType(SQLBase):
    """排序类型"""

    def __init__(self, order_type: EnumOrderType):
        self._order_type = order_type

    @property
    def order_type(self) -> EnumOrderType:
        """返回排序类型的枚举类"""
        return self._order_type

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


class SQLUnionType(SQLBase):
    """组合类型"""

    def __init__(self, union_type: EnumUnionType):
        self._union_type = union_type

    @property
    def union_type(self) -> EnumUnionType:
        """返回组合类型的枚举类"""
        return self._union_type

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


class SQLCompareOperator(SQLBase):
    """比较运算符"""

    def __init__(self, compare_operator: EnumCompareOperator):
        self._compare_operator = compare_operator

    @property
    def compare_operator(self) -> EnumCompareOperator:
        """返回比较运算符的枚举类"""
        return self._compare_operator

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return self.compare_operator.value

    @staticmethod
    def get_used_column_list() -> List[str]:
        """获取使用的字段列表"""
        return []


# ---------------------------------------- 计算运算符 ----------------------------------------


class EnumComputeOperator(enum.Enum):
    """计算运算符的枚举类"""
    PLUS = "+"  # 加法运算符
    SUBTRACT = "-"  # 减法运算符
    MULTIPLE = "*"  # 乘法运算符
    DIVIDE = "/"  # 除法运算符
    MOD = "%"  # 取模运算符
    CONCAT = "||"  # 字符串拼接运算符（仅 Oracle、DB2、PostgreSQL 中适用）


class SQLComputeOperator(SQLBase):
    """计算运算符"""

    def __init__(self, compute_operator: EnumComputeOperator):
        self._compute_operator = compute_operator

    @property
    def compute_operator(self) -> EnumComputeOperator:
        """返回计算运算符的枚举类"""
        return self._compute_operator

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        if self.compute_operator == EnumComputeOperator.MOD and data_source != DataSource.SQL_SERVER:
            raise UnSupportDataSourceError(f"{data_source} 不支持使用 % 运算符")
        if (self.compute_operator == EnumComputeOperator.CONCAT
                and data_source not in {DataSource.ORACLE, DataSource.DB2, DataSource.POSTGRE_SQL}):
            raise UnSupportDataSourceError(f"{data_source} 不支持使用 || 运算符")
        return self.compute_operator.value

    @staticmethod
    def get_used_column_list() -> List[str]:
        """获取使用的字段列表"""
        return []


# ---------------------------------------- 逻辑运算符 ----------------------------------------


class EnumLogicalOperator(enum.Enum):
    """逻辑运算符的枚举类"""
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


class SQLLogicalOperator(SQLBase):
    """逻辑运算符"""

    def __init__(self, logical_operator: EnumLogicalOperator):
        self._logical_operator = logical_operator

    @property
    def logical_operator(self) -> EnumLogicalOperator:
        """返回逻辑运算符的枚举类"""
        return self._logical_operator

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return self.logical_operator.value

    @staticmethod
    def get_used_column_list() -> List[str]:
        """获取使用的字段列表"""
        return []


# ---------------------------------------- 一般表达式的抽象基类 ----------------------------------------


class SQLGeneralExpression(SQLBase, abc.ABC):
    """一般表达式的抽象基类

    TODO 待移除所有方法
    """

    @abc.abstractmethod
    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""

    @abc.abstractmethod
    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""


# ---------------------------------------- 字面值表达式 ----------------------------------------


class SQLLiteralExpression(SQLGeneralExpression, abc.ABC):
    """字面值表达式"""

    def as_int(self) -> Optional[int]:
        """将字面值作为整形返回"""
        return None

    def as_string(self) -> str:
        """将字面值作为字符串返回"""
        return self.source()

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return []


class SQLLiteralIntegerExpression(SQLLiteralExpression):
    """整数字面值"""

    def __init__(self, value: int):
        self._value = value

    @property
    def value(self) -> int:
        """返回整型的字面值"""
        return self._value

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.value}"

    def as_int(self) -> int:
        return self.value

    def as_string(self) -> str:
        return f"{self.value}"


class SQLLiteralFloatExpression(SQLLiteralExpression):
    """浮点数字面值"""

    def __init__(self, value: float):
        self._value = value

    @property
    def value(self) -> float:
        """返回浮点型的字面值"""
        return self._value

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.value}"

    def as_string(self) -> str:
        return f"{self.value}"


class SQLLiteralStringExpression(SQLLiteralExpression):
    """字符串字面值"""

    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        """返回字符串类型的字面值"""
        return self._value

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return f"'{self.value}'"

    def as_int(self) -> Optional[int]:
        if self.value.isdigit():
            return int(self.value)
        return None

    def as_string(self) -> Optional[str]:
        return self.value


class SQLLiteralHexExpression(SQLLiteralExpression):
    """十六进制字面值"""

    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        """返回字符串类型的十六进制字面值"""
        return self._value

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return f"x'{self._value}'"

    def as_string(self) -> str:
        return f"{self._value}"


class SQLLiteralBitExpression(SQLLiteralExpression):
    """位值字面值"""

    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        """返回字符串类型的位置字面值"""
        return self._value

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return f"b'{self._value}'"

    def as_string(self) -> str:
        return f"{self._value}"


class SQLLiteralBoolExpression(SQLLiteralExpression):
    """布尔值字面值"""

    def __init__(self, value: bool):
        self._value = value

    @property
    def value(self) -> bool:
        """返回布尔值类型的字面值"""
        return self._value

    def as_int(self) -> int:
        return 1 if self.value is True else 0

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return "TRUE" if self._value is True else "FALSE"


class SQLLiteralNullExpression(SQLLiteralExpression):
    """空值字面值"""

    @property
    def value(self) -> None:
        """返回空值字面值"""
        return None

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return "NULL"


# ---------------------------------------- 列名表达式 ----------------------------------------


class SQLColumnNameExpression(SQLGeneralExpression):
    """列名表达式"""

    def __init__(self, table: Optional[str], column: str):
        self._table = table
        self._column = column

    @property
    def table(self) -> Optional[str]:
        """返回表名"""
        return self._table

    @property
    def column(self) -> str:
        """返回列名"""
        return self._column

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.table}.{self.column}" if self.table is not None else f"{self.column}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return [self.source()]


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


class SQLFunctionExpression(SQLGeneralExpression):
    """函数表达式"""

    def __init__(self,
                 schema_name: Optional[str],
                 function_name: str,
                 function_params: List[SQLGeneralExpression]):
        self._schema_name = schema_name
        self._function_name = function_name
        self._function_params = function_params

    @property
    def schema_name(self) -> Optional[str]:
        """返回模式名称"""
        return self._schema_name

    @property
    def function_name(self) -> str:
        """返回函数名称"""
        return self._function_name

    @property
    def function_params(self) -> List[SQLGeneralExpression]:
        """返回函数参数的列表"""
        return self._function_params

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self._get_function_str()}({self._get_param_str(data_source)})"

    def _get_param_str(self, data_source: DataSource = DataSource.MYSQL) -> str:
        return ", ".join(param.source(data_source) for param in self.function_params)

    def _get_function_str(self) -> str:
        return f"{self.schema_name}.{self.function_name}" if self.schema_name is not None else f"{self.function_name}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        result = []
        for param in self.function_params:
            result.extend(param.get_used_column_list())
        return result


class SQLAggregationFunctionExpression(SQLFunctionExpression):
    """聚合函数表达式"""

    def __init__(self,
                 function_name: str,
                 function_params: List[SQLGeneralExpression],
                 is_distinct: bool):
        super().__init__(None, function_name, function_params)
        self._is_distinct = is_distinct

    @property
    def is_distinct(self) -> bool:
        """返回是否包含 DISTINCT 参数"""
        return self._is_distinct

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        is_distinct = "DISTINCT " if self.is_distinct is True else ""
        return f"{self._get_function_str()}({is_distinct}{self._get_param_str(data_source)})"


class SQLCastDataType(SQLBase):
    """CAST 语句中的数据类型"""

    def __init__(self, signed: bool, data_type: EnumCastDataType, params: Optional[List[SQLGeneralExpression]]):
        self._signed = signed
        self._data_type = data_type
        self._params = params

    @property
    def signed(self) -> bool:
        """返回是否包含 SIGNED 关键字"""
        return self._signed

    @property
    def data_type(self) -> EnumCastDataType:
        """返回转换的类型"""
        return self._data_type

    @property
    def params(self) -> Optional[List[SQLGeneralExpression]]:
        """返回类型的参数列表"""
        return self._params

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        result = []
        if self.signed is True:
            result.append("SIGNED")
        result.append(self.data_type.value)
        if self.params is not None:
            param_str = ", ".join(param.source() for param in self.params)
            result.append(f"({param_str})")
        return " ".join(result)


class SQLCastFunctionExpression(SQLFunctionExpression):
    """Cast 函数表达式"""

    def __init__(self,
                 column_expression: SQLGeneralExpression,
                 cast_type: SQLCastDataType):
        super().__init__(None, "CAST", [])
        self._column_expression = column_expression
        self._cast_type = cast_type

    @property
    def function_params(self) -> List[SQLGeneralExpression]:
        # TODO 修改父类继承关系
        raise SqlParseError("SQLCastFunctionExpression.function_params() 方法不允许调用")

    @property
    def column_expression(self) -> SQLGeneralExpression:
        """返回 CASE 表达式中要转换的列表达式"""
        return self._column_expression

    @property
    def cast_type(self) -> SQLCastDataType:
        """返回 CAST 参数中要转换的函数类型"""
        return self._cast_type

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self._get_function_str()}({self.column_expression.source()} AS {self.cast_type.source()})"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.column_expression.get_used_column_list()


class SQLExtractFunctionExpression(SQLFunctionExpression):
    """Extract 函数表达式"""

    def __init__(self,
                 extract_name: SQLGeneralExpression,
                 column_expression: SQLGeneralExpression):
        super().__init__(None, "EXTRACT", [])
        self._extract_name = extract_name
        self._column_expression = column_expression

    @property
    def function_params(self) -> List[SQLGeneralExpression]:
        # TODO 修改父类继承关系
        raise SqlParseError("SQLCastFunctionExpression.function_params() 方法不允许调用")

    @property
    def extract_name(self) -> SQLGeneralExpression:
        """返回 FROM 关键字之前的提取名称"""
        return self._extract_name

    @property
    def column_expression(self) -> SQLGeneralExpression:
        """返回 FROM 关键字之后的一般表达式"""
        return self._column_expression

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self._get_function_str()}({self.extract_name.source()} FROM {self.column_expression.source()})"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.column_expression.get_used_column_list()


# ---------------------------------------- 布尔值表达式 ----------------------------------------


class SQLBoolExpression(SQLBase, abc.ABC):
    """布尔值表达式

    TODO 整理子类继承关系
    """

    @abc.abstractmethod
    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""


class SQLBoolCompareExpression(SQLBoolExpression):
    """比较运算符关联表达式"""

    def __init__(self,
                 operator: SQLCompareOperator,
                 before_value: SQLGeneralExpression,
                 after_value: SQLGeneralExpression):
        self._operator = operator
        self._before_value = before_value
        self._after_value = after_value

    @property
    def operator(self) -> SQLCompareOperator:
        """返回比较运算符"""
        return self._operator

    @property
    def before_value(self) -> SQLGeneralExpression:
        """返回比较运算符之前的表达式"""
        return self._before_value

    @property
    def after_value(self) -> SQLGeneralExpression:
        """返回比较运算符之后的表达式"""
        return self._after_value

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return (f"{self.before_value.source(data_source)}"
                f" {self.operator.source(data_source)} "
                f"{self.after_value.source(data_source)}")

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.before_value.get_used_column_list() + self.after_value.get_used_column_list()


class SQLBoolIsExpression(SQLBoolExpression):
    """IS运算符布尔值表达式"""

    def __init__(self,
                 is_not: bool,
                 before_value: SQLGeneralExpression,
                 after_value: SQLGeneralExpression):
        self._is_not = is_not
        self._before_value = before_value
        self._after_value = after_value

    @property
    def is_not(self) -> bool:
        """返回是否包含 NOT 关键字"""
        return self._is_not

    @property
    def before_value(self) -> SQLGeneralExpression:
        """返回 IS 关键字之前表达式"""
        return self._before_value

    @property
    def after_value(self) -> SQLGeneralExpression:
        """返回 IS 关键字之后表达式"""
        return self._after_value

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        keyword = "IS NOT" if self.is_not else "IS"
        return f"{self.before_value.source()} {keyword} {self.after_value.source()}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.before_value.get_used_column_list() + self.after_value.get_used_column_list()


class SQLBoolInExpression(SQLBoolExpression):
    """In 关键字的布尔值表达式"""

    def __init__(self,
                 is_not: bool,
                 before_value: SQLGeneralExpression,
                 after_value: SQLGeneralExpression):
        self._is_not = is_not
        self._before_value = before_value
        self._after_value = after_value

    @property
    def is_not(self) -> bool:
        """返回是否包含 NOT 关键字"""
        return self._is_not

    @property
    def before_value(self) -> SQLGeneralExpression:
        """返回 IN 关键字之前的表达式"""
        return self._before_value

    @property
    def after_value(self) -> SQLGeneralExpression:
        """返回 IN 关键字之后的表达式"""
        return self._after_value

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        keyword = "NOT IN " if self.is_not else "IN"
        return f"{self.before_value.source()} {keyword} {self.after_value.source()}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.before_value.get_used_column_list() + self.after_value.get_used_column_list()


class SQLBoolLikeExpression(SQLBoolExpression):
    """LIKE 运算符关联表达式"""

    def __init__(self,
                 is_not: bool,
                 before_value: SQLGeneralExpression,
                 after_value: SQLGeneralExpression):
        self._is_not = is_not
        self._before_value = before_value
        self._after_value = after_value

    @property
    def is_not(self) -> bool:
        """返回是否包含 NOT 关键字"""
        return self._is_not

    @property
    def before_value(self) -> SQLGeneralExpression:
        """返回 LIKE 关键字之前的表达式"""
        return self._before_value

    @property
    def after_value(self) -> SQLGeneralExpression:
        """返回 LIKE 关键字之后的表达式"""
        return self._after_value

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        keyword = "NOT LIKE" if self.is_not else "LIKE"
        return f"{self.before_value.source()} {keyword} {self.after_value.source()}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.before_value.get_used_column_list() + self.after_value.get_used_column_list()


class SQLBoolExistsExpression(SQLBoolExpression):
    """Exists 运算符关联表达式"""

    def __init__(self,
                 is_not: bool,
                 after_value: SQLGeneralExpression):
        self._is_not = is_not
        self._after_value = after_value

    @property
    def is_not(self) -> bool:
        """返回是否包含 NOT 关键字"""
        return self._is_not

    @property
    def after_value(self) -> SQLGeneralExpression:
        """返回 EXISTS 关键字之后的表达式"""
        return self._after_value

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        keyword = "NOT EXISTS" if self.is_not else "EXISTS"
        return f"{keyword} {self.after_value.source()}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.after_value.get_used_column_list()


class SQLBoolBetweenExpression(SQLBoolExpression):
    """BETWEEN 关联表达式"""

    def __init__(self,
                 before_value: SQLGeneralExpression,
                 from_value: SQLGeneralExpression,
                 to_value: SQLGeneralExpression):
        self._before_value = before_value
        self._from_value = from_value
        self._to_value = to_value

    @property
    def before_value(self) -> SQLGeneralExpression:
        """返回 BETWEEN 关键字之前的表达式"""
        return self._before_value

    @property
    def from_value(self) -> SQLGeneralExpression:
        """返回 BETWEEN 关键字之后，AND 关键字之前的表达式"""
        return self._from_value

    @property
    def to_value(self) -> SQLGeneralExpression:
        """返回 AND 关键字之后的表达式"""
        return self._to_value

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.before_value.source()} BETWEEN {self.from_value.source()} AND {self.to_value.source()}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.before_value.get_used_column_list()


# ---------------------------------------- 窗口表达式 ----------------------------------------


class SQLWindowExpression(SQLGeneralExpression):
    """窗口表达式"""

    def __init__(self,
                 window_function: Union[SQLFunctionExpression, "SQLArrayIndexExpression"],
                 partition_by: Optional[SQLGeneralExpression],
                 order_by: Optional[SQLGeneralExpression]):
        self._window_function = window_function
        self._partition_by = partition_by
        self._order_by = order_by

    @property
    def window_function(self) -> Union[SQLFunctionExpression, "SQLArrayIndexExpression"]:
        """返回窗口函数"""
        return self._window_function

    @property
    def partition_by(self) -> Optional[SQLGeneralExpression]:
        """返回 PARTITION BY 关键字之后的表达式"""
        return self._partition_by

    @property
    def order_by(self) -> Optional[SQLGeneralExpression]:
        """返回 ORDER BY　关键字之后的表达式"""
        return self._order_by

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        result = f"{self.window_function.source()} OVER ("
        parenthesis = []
        if self.partition_by is not None:
            parenthesis.append(f"PARTITION BY {self.partition_by.source()}")
        if self.order_by is not None:
            parenthesis.append(f"ORDER BY {self.order_by.source()}")
        result += " ".join(parenthesis) + ")"
        return result

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        result = []
        if self.partition_by is not None:
            result.extend(self.partition_by.get_used_column_list())
        if self.order_by is not None:
            result.extend(self.order_by.get_used_column_list())
        return result


# ---------------------------------------- 通配符表达式 ----------------------------------------


class SQLWildcardExpression(SQLGeneralExpression):
    """通配符表达式"""

    def __init__(self, schema: Optional[str]):
        self._schema = schema

    @property
    def schema(self) -> Optional[str]:
        """返回模式名称"""
        return self._schema

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.schema}.*" if self.schema is not None else "*"

    def get_used_column_list(self) -> List[str]:
        """获取语句结果中使用的字段"""
        return [self.source()]


# ---------------------------------------- 条件表达式 ----------------------------------------

class SQLConditionExpression(SQLGeneralExpression):
    """条件表达式"""

    def __init__(self,
                 elements: List[Union["SQLConditionExpression", SQLBoolExpression, SQLLogicalOperator]]):
        self._elements = elements

    @property
    def elements(self) -> List[Union["SQLConditionExpression", SQLBoolExpression, SQLLogicalOperator]]:
        """返回条件表达式中的元素"""
        return self._elements

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return " ".join(f"({element.source(data_source)})"
                        if isinstance(element, SQLConditionExpression) else element.source(data_source)
                        for element in self._elements)

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        result = []
        for element in self.elements:
            result.extend(element.get_used_column_list())
        return result


# ---------------------------------------- CASE 表达式 ----------------------------------------


class SQLCaseExpression(SQLGeneralExpression):
    """第 1 种格式的 CASE 表达式

    CASE
        WHEN {条件表达式} THEN {一般表达式}
        ELSE {一般表达式}
    END
    """

    def __init__(self,
                 cases: List[Tuple[SQLConditionExpression, SQLGeneralExpression]],
                 else_value: Optional[SQLGeneralExpression]):
        self._cases = cases
        self._else_value = else_value

    @property
    def cases(self) -> List[Tuple[SQLConditionExpression, SQLGeneralExpression]]:
        """返回 WHEN 关键字之后的条件表达式与 THEN 关键字之后的一般表达式的元组的列表"""
        return self._cases

    @property
    def else_value(self) -> Optional[SQLGeneralExpression]:
        """返回 ELSE 关键字之后的表达式"""
        return self._else_value

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
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
        result = []
        for when, _ in self.cases:
            result.extend(when.get_used_column_list())
        return result


class SQLCaseValueExpression(SQLGeneralExpression):
    """第 2 种格式的 CASE 表达式

    CASE {一般表达式}
        WHEN {一般表达式} THEN {一般表达式}
        ELSE {一般表达式}
    END
    """

    def __init__(self,
                 case_value: SQLGeneralExpression,
                 cases: List[Tuple[SQLGeneralExpression, SQLGeneralExpression]],
                 else_value: Optional[SQLGeneralExpression]):
        self._case_value = case_value
        self._cases = cases
        self._else_value = else_value

    @property
    def case_value(self) -> SQLGeneralExpression:
        """返回 CASE 关键字之后的表达式"""
        return self._case_value

    @property
    def cases(self) -> List[Tuple[SQLGeneralExpression, SQLGeneralExpression]]:
        """返回 WHEN 关键字之后的一般表达式与 THEN 关键字之后的一般表达式的元组的列表"""
        return self._cases

    @property
    def else_value(self) -> Optional[SQLGeneralExpression]:
        """返回 ELSE 关键字之后的表达式"""
        return self._else_value

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        result = ["CASE", self.case_value.source()]
        for when, then in self.cases:
            result.append(f"    WHEN {when.source(data_source)} THEN {then.source(data_source)}")
        if self.else_value is not None:
            result.append(f"    ELSE {self.else_value.source(data_source)}")
        result.append("END")
        return "\n".join(result)

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        result = self.case_value.get_used_column_list()
        for when, _ in self.cases:
            result.extend(when.get_used_column_list())
        return result


# ---------------------------------------- 计算表达式 ----------------------------------------

class SQLComputeExpression(SQLGeneralExpression):
    """计算表达式"""

    def __init__(self,
                 elements: List[Union[SQLGeneralExpression, SQLComputeOperator]]):
        self._elements = elements

    @property
    def elements(self) -> List[Union[SQLGeneralExpression, SQLComputeOperator]]:
        """返回计算表达式中的元素的列表"""
        return self._elements

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return " ".join(element.source(data_source) for element in self.elements)

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        result = []
        for element in self.elements:
            result.extend(element.get_used_column_list())
        return result


# ---------------------------------------- 值表达式 ----------------------------------------


class SQLValueExpression(SQLGeneralExpression):
    """INSERT INTO 表达式中，VALUES 里的表达式"""

    def __init__(self, values: List[SQLGeneralExpression]):
        self._values = values

    @property
    def values(self) -> List[SQLGeneralExpression]:
        """值的列表"""
        return self._values

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        values_str = ", ".join(value.source() for value in self.values)
        return f"({values_str})"

    def get_used_column_list(self) -> List[str]:
        """返回使用的字段列表"""
        return []


# ---------------------------------------- 子查询表达式 ----------------------------------------


class SQLSubQueryExpression(SQLGeneralExpression):
    """子查询表达式"""

    def __init__(self, select_statement: "SQLSelectStatement"):
        self._select_statement = select_statement

    @property
    def select_statement(self) -> "SQLSelectStatement":
        """返回查询语句"""
        return self._select_statement

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return f"({self.select_statement.source()})"

    def get_used_column_list(self) -> List[str]:
        """返回使用的字段列表"""
        return self.select_statement.get_select_used_column_list()

    def get_used_table_list(self) -> List[str]:
        """返回使用的表列表"""
        return self.select_statement.get_used_table_list()


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

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        if data_source != DataSource.HIVE:
            raise UnSupportDataSourceError(f"数组下标不支持SQL类型:{data_source}")
        return f"{self.array_expression.source(data_source)}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.array_expression.get_used_column_list()

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return self.array_expression.get_used_column_list()  # TODO 待修复


# ---------------------------------------- 表名表达式 ----------------------------------------


class SQLTableNameExpression(SQLBase):
    """表名表达式"""

    def __init__(self, schema: Optional[str], table: str):
        self._schema = schema
        self._table = table

    @property
    def schema(self) -> Optional[str]:
        """返回模式名称"""
        return self._schema

    @property
    def table(self) -> str:
        """返回表名"""
        return self._table

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.schema}.{self.table}" if self.schema is not None else f"{self.table}"

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return [self.source()]


# ---------------------------------------- 别名表达式 ----------------------------------------


class SQLAlisaExpression(SQLBase):
    """别名表达式"""

    def __init__(self, alias_name: str):
        self._alias_name = alias_name

    @property
    def alias_name(self) -> str:
        """返回别名"""
        return self._alias_name

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return f"AS {self.alias_name}"


# ---------------------------------------- 关联表达式 ----------------------------------------


class SQLJoinExpression(SQLBase, abc.ABC):
    """关联表达式"""

    @abc.abstractmethod
    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码  TODO 待移除"""


class SQLJoinOnExpression(SQLJoinExpression):
    """ON 关联表达式"""

    def __init__(self, condition: SQLConditionExpression):
        self._condition = condition

    @property
    def condition(self) -> SQLConditionExpression:
        """返回条件表达式"""
        return self._condition

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return f"ON {self._condition.source()}"


class SQLJoinUsingExpression(SQLJoinExpression):
    """USING 关联表达式"""

    def __init__(self, using_function: SQLFunctionExpression):
        self._using_function = using_function

    @property
    def using_function(self) -> SQLFunctionExpression:
        """返回 USING 函数"""
        return self._using_function

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.using_function.source()}"


# ---------------------------------------- 字段类型表达式 ----------------------------------------

class SQLColumnTypeExpression(SQLBase):
    """字段类型表达式"""

    def __init__(self, name: str, params: List[SQLGeneralExpression]):
        self._name = name
        self._params = params

    @property
    def name(self) -> str:
        """返回函数名称"""
        return self._name

    @property
    def params(self) -> List[SQLGeneralExpression]:
        """返回函数参数的列表"""
        return self._params

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        if len(self.params) == 0 or data_source == DataSource.HIVE:
            return self.name
        type_params = "(" + ", ".join([param.source() for param in self.params]) + ")"
        return f"{self.name}{type_params}"


# ---------------------------------------- 表表达式 ----------------------------------------


class SQLTableExpression(SQLBase):
    """表表达式"""

    def __init__(self,
                 table: Union[SQLTableNameExpression, SQLSubQueryExpression],
                 alias: Optional[SQLAlisaExpression]):
        self._table = table
        self._alias = alias

    @property
    def table(self) -> Union[SQLTableNameExpression, SQLSubQueryExpression]:
        """返回表名表达式或子查询表达式"""
        return self._table

    @property
    def alias(self) -> Optional[SQLAlisaExpression]:
        """返回别名表达式"""
        return self._alias

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        if self.alias is not None:
            return f"{self.table.source()} {self.alias.source()}"
        return f"{self.table.source()}"

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return self.table.get_used_table_list()


# ---------------------------------------- 列表达式 ----------------------------------------


class SQLColumnExpression(SQLBase):
    """列表达式"""

    def __init__(self,
                 column: SQLGeneralExpression,
                 alias: Optional[SQLAlisaExpression]):
        self._column = column
        self._alias = alias

    @property
    def column(self) -> SQLGeneralExpression:
        """返回列值的一般表达式"""
        return self._column

    @property
    def alias(self) -> Optional[SQLAlisaExpression]:
        """返回别名表达式"""
        return self._alias

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        if self.alias is not None:
            return f"{self.column.source(data_source)} {self.alias.source()}"
        return f"{self.column.source(data_source)}"

    def get_alias_name(self) -> Optional[str]:
        """获取别名名称"""
        if self.alias is not None:
            return self.alias.alias_name
        return None

    def get_used_column_list(self) -> List[str]:
        """获取语句结果中使用的字段"""
        return self.column.get_used_column_list()


# ---------------------------------------- 等式表达式 ----------------------------------------


class SQLEqualExpression(SQLBase):
    """等式表达式"""

    def __init__(self, before_value: SQLGeneralExpression, after_value: SQLGeneralExpression):
        self._before_value = before_value
        self._after_value = after_value

    @property
    def before_value(self) -> SQLGeneralExpression:
        """返回等号之前的表达式"""
        return self._before_value

    @property
    def after_value(self) -> SQLGeneralExpression:
        """返回等号之后的表达式"""
        return self._after_value

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return f"{self.before_value.source()} = {self.after_value.source()}"


# ---------------------------------------- 分区表达式 ----------------------------------------


class SQLPartitionExpression(SQLBase):
    """分区表达式：PARTITION (<partition_expression>)"""

    def __init__(self, partition_list: List[SQLEqualExpression]):
        self._partition_list = partition_list

    @property
    def partition_list(self) -> List[SQLEqualExpression]:
        """返回分区语句的列表"""
        return self._partition_list

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        partition_list_str = ", ".join(partition.source() for partition in self.partition_list)
        return f"PARTITION ({partition_list_str})"


# ---------------------------------------- 声明外键表达式 ----------------------------------------


class SQLForeignKeyExpression(SQLBase):
    """声明外键表达式"""

    def __init__(self, constraint_name: str, slave_columns: List[str], master_table_name: str,
                 master_columns: List[str]):
        """

        Parameters
        ----------
        constraint_name : str
            外键约束名称
        slave_columns : List[str]
            从表的字段
        master_table_name : str
            主表名称
        master_columns : List[str]
            主表的字段名
        """
        self.constraint_name = constraint_name
        self.slave_columns = slave_columns
        self.master_table_name = master_table_name
        self.master_columns = master_columns

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        slave_columns_str = ", ".join([f"{column}" for column in self.slave_columns])
        master_columns_str = ", ".join([f"{column}" for column in self.master_columns])
        return (f"CONSTRAINT {self.constraint_name} FOREIGN KEY({slave_columns_str}) "
                f"REFERENCES {self.master_table_name}({master_columns_str})")


# ---------------------------------------- 声明索引表达式 ----------------------------------------


class SQLIndexExpression(SQLBase, abc.ABC):
    """声明索引表达式"""

    def __init__(self, name: Optional[str], columns: List[str]):
        self._name = name
        self._columns = columns

    @property
    def name(self) -> Optional[str]:
        """返回索引名称"""
        return self._name

    @property
    def columns(self) -> List[str]:
        """返回索引的字段列表"""
        return self._columns


class SQLPrimaryIndexExpression(SQLIndexExpression):
    """主键索引声明表达式"""

    def __init__(self, columns: List[str]):
        super().__init__(None, columns)

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        columns_str = ", ".join([f"{column}" for column in self.columns])
        return f"PRIMARY KEY ({columns_str})" if self.columns is not None else ""


class SQLUniqueIndexExpression(SQLIndexExpression):
    """唯一键索引声明表达式"""

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        columns_str = ", ".join([f"{column}" for column in self.columns])
        return f"UNIQUE KEY {self.name} ({columns_str})"


class SQLNormalIndexExpression(SQLIndexExpression):
    """普通索引声明表达式"""

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        columns_str = ", ".join([f"{column}" for column in self.columns])
        return f"KEY {self.name} ({columns_str})"


class SQLFulltextIndexExpression(SQLIndexExpression):
    """全文本索引声明表达式"""

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        columns_str = ", ".join([f"{column}" for column in self.columns])
        return f"FULLTEXT KEY {self.name} ({columns_str})"


# ---------------------------------------- 声明字段表达式 ----------------------------------------


class SQLDefineColumnExpression(SQLBase):
    """声明字段表达式"""

    def __init__(self,
                 column_name: str,
                 column_type: SQLColumnTypeExpression,
                 comment: Optional[str] = None,
                 is_unsigned: bool = False,
                 is_zerofill: bool = False,
                 character_set: Optional[str] = None,
                 collate: Optional[str] = None,
                 is_allow_null: bool = False,
                 is_not_null: bool = False,
                 is_auto_increment: bool = False,
                 default: Optional[SQLGeneralExpression] = None,
                 on_update: Optional[SQLGeneralExpression] = None
                 ):
        self._column_name = column_name.strip("`")
        self._column_type = column_type
        self._comment = comment
        self._is_unsigned = is_unsigned
        self._is_zerofill = is_zerofill
        self._character_set = character_set
        self._collate = collate
        self._is_allow_null = is_allow_null  # 是否显式地允许 NULL 值
        self._is_not_null = is_not_null
        self._is_auto_increment = is_auto_increment
        self._default = default
        self._on_update = on_update

    @property
    def column_name(self) -> str:
        """返回列名"""
        return f"`{self._column_name}`"

    @property
    def column_name_without_quote(self) -> str:
        """返回没有被引号框柱的列名"""
        return self._column_name

    @property
    def column_type(self) -> SQLColumnTypeExpression:
        """返回列的类型"""
        return self._column_type

    @property
    def comment(self) -> Optional[str]:
        """返回列的注释"""
        return self._comment

    @property
    def is_unsigned(self) -> bool:
        """返回是否包含 UNSIGHED 关键字"""
        return self._is_unsigned

    @property
    def is_zerofill(self) -> bool:
        """返回是否包含 ZEROFILL 关键字"""
        return self._is_zerofill

    @property
    def character_set(self) -> Optional[str]:
        """返回是否包含 CHARSET SET 关键字"""
        return self._character_set

    @property
    def collate(self) -> Optional[str]:
        """返回是否包含 COLLATE 关键字"""
        return self._collate

    @property
    def is_allow_null(self) -> bool:
        """返回是否包含 NULL 关键字"""
        return self._is_allow_null

    @property
    def is_not_null(self) -> bool:
        """返回是否包含 NOT NULL 关键字"""
        return self._is_not_null

    @property
    def is_auto_increment(self) -> bool:
        """返回是否包含 AUTO_INCREMENT 关键字"""
        return self._is_auto_increment

    @property
    def default(self) -> Optional[SQLGeneralExpression]:
        """返回是否包含 DEFAULT 关键字"""
        return self._default

    @property
    def on_update(self) -> Optional[SQLGeneralExpression]:
        """返回是否包含 ON UPDATE 关键字"""
        return self._on_update

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        res = f"{self._column_name} {self.column_type.source(data_source)}"
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
            res += f" DEFAULT {self.default.source()}"
        if self.on_update is not None and data_source == DataSource.MYSQL:
            res += f" ON UPDATE {self.on_update.source()}"
        if self.comment is not None:
            res += f" COMMENT {self.comment}"
        return res


# ---------------------------------------- 配置名称和配置值表达式 ----------------------------------------


class SQLConfigNameExpression(SQLBase):
    """配置名称表达式"""

    def __init__(self, config_name: str):
        self._config_name = config_name

    @property
    def config_name(self) -> str:
        """返回配置名称"""
        return self._config_name

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return self.config_name


class SQLConfigValueExpression(SQLBase):
    """配置值表达式"""

    def __init__(self, config_value: str):
        self._config_value = config_value

    @property
    def config_value(self) -> str:
        """返回配置值"""
        return self._config_value

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return self.config_value


# ---------------------------------------- SELECT 子句 ----------------------------------------


class SQLSelectClause(SQLBase):
    """SELECT 子句"""

    def __init__(self, distinct: bool, columns: List[SQLColumnExpression]):
        self._distinct = distinct
        self._columns = columns

    @property
    def distinct(self) -> bool:
        """返回是否包含 DISTINCT 关键字"""
        return self._distinct

    @property
    def columns(self) -> List[SQLColumnExpression]:
        """返回 SELECT 中获取的列表达式的列表"""
        return self._columns

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        result = ["SELECT"]
        if self.distinct is True:
            result.append("DISTINCT")
        result.append(", ".join(column.source(data_source) for column in self.columns))
        return " ".join(result)

    def get_used_column_list(self) -> List[str]:
        """获取语句结果中使用的字段的列表"""
        result = []
        for column in self.columns:
            result.extend(column.get_used_column_list())
        return result

    def get_alias_to_used_column_hash(self) -> Dict[str, List[str]]:
        """获取字段别名对应的原始字段的列表"""
        result = {}
        for column in self.columns:
            result[column.get_alias_name()] = column.get_used_column_list()
        return result

    def get_index_to_used_column_hash(self) -> Dict[int, List[str]]:
        """获取字段序号对应的原始字段列表的映射表"""
        result = {}
        for idx, column in enumerate(self.columns):
            result[idx + 1] = column.get_used_column_list()  # 列编号从 1 开始
        return result


# ---------------------------------------- FROM 子句 ----------------------------------------

class SQLFromClause(SQLBase):
    """FROM 子句"""

    def __init__(self, tables: List[SQLTableExpression]):
        self._tables = tables

    @property
    def tables(self) -> List[SQLTableExpression]:
        """返回 FROM 中获取的表表达式的列表"""
        return self._tables

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return "FROM " + ", ".join(table.source() for table in self.tables)

    def get_used_table_list(self) -> List[str]:
        """获取语句中查询的表名的列表"""
        result = []
        for table in self.tables:
            result.extend(table.get_used_table_list())
        return result


# ---------------------------------------- LATERAL VIEW 子句 ----------------------------------------


class SQLLateralViewClause(SQLBase):
    """LATERAL VIEW 子句"""

    def __init__(self, function: SQLFunctionExpression, view_name: str, alias: SQLAlisaExpression):
        self._function = function
        self._view_name = view_name
        self._alias = alias

    @property
    def function(self) -> SQLFunctionExpression:
        """返回行专列的函数表达式"""
        return self._function

    @property
    def view_name(self) -> str:
        """返回视图的名称"""
        return self._view_name

    @property
    def alias(self) -> SQLAlisaExpression:
        """返回新生成的列的别名"""
        return self._alias

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"LATERAL VIEW {self.function.source(data_source)} {self.view_name} {self.alias.source(data_source)}"

    def get_used_column_list(self) -> List[str]:
        """返回使用的字段列表"""
        return self.function.get_used_column_list()


# ---------------------------------------- JOIN 子句 ----------------------------------------

class SQLJoinClause(SQLBase):
    """JOIN 子句"""

    def __init__(self,
                 join_type: SQLJoinType,
                 table: SQLTableExpression,
                 join_rule: Optional[SQLJoinExpression]):
        self._join_type = join_type
        self._table = table
        self._join_rule = join_rule

    @property
    def join_type(self) -> SQLJoinType:
        """返回关联类型"""
        return self._join_type

    @property
    def table(self) -> SQLTableExpression:
        """返回关联的表表达式"""
        return self._table

    @property
    def join_rule(self) -> Optional[SQLJoinExpression]:
        """返回关联规则的关联表达式"""
        return self._join_rule

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        if self.join_rule is not None:
            return f"{self.join_type.source(data_source)} {self.table.source()} {self.join_rule.source()}"
        return f"{self.join_type.source(data_source)} {self.table.source()}"

    def get_used_table_list(self) -> List[str]:
        """获取使用的表列表"""
        return self.table.get_used_table_list()


# ---------------------------------------- WHERE 子句 ----------------------------------------


class SQLWhereClause(SQLBase):
    """WHERE 子句"""

    def __init__(self, condition: SQLConditionExpression):
        self._condition = condition

    @property
    def condition(self) -> SQLConditionExpression:
        """返回 WHERE 子句中的条件表达式"""
        return self._condition

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return f"WHERE {self.condition.source()}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段名列表"""
        return self.condition.get_used_column_list()


# ---------------------------------------- GROUP BY 子句 ----------------------------------------

class SQLGroupByClause(SQLBase, abc.ABC):
    """GROUP BY 子句"""

    @abc.abstractmethod
    def get_used_column_list(self) -> List[Union[str, int]]:
        """返回字段名和列编号"""


class SQLNormalGroupByClause(SQLGroupByClause):
    """普通 GROUP BY 子句"""

    def __init__(self, columns: List[SQLGeneralExpression], with_rollup: bool):
        self._columns = columns
        self._with_rollup = with_rollup

    @property
    def columns(self) -> List[SQLGeneralExpression]:
        """返回 GROUP BY 中的列的一般表达式的列表"""
        return self._columns

    @property
    def with_rollup(self) -> bool:
        """返回是否包含 WITH ROLLUP 关键字"""
        return self._with_rollup

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        if self.with_rollup:
            return "GROUP BY " + ", ".join(column.source() for column in self.columns) + " WITH ROLLUP"
        return "GROUP BY " + ", ".join(column.source() for column in self.columns)

    def get_used_column_list(self) -> List[Union[str, int]]:
        """返回字段名和列编号"""
        result = []
        for column in self.columns:
            if isinstance(column, SQLLiteralExpression):
                result.append(column.as_int())  # 列编号
            else:
                result.extend(column.get_used_column_list())
        return result


class SQLGroupingSetsGroupByClause(SQLGroupByClause):
    """使用 GROUPING SETS 语法的 GROUP BY 子句"""

    def __init__(self, grouping_list: List[List[SQLGeneralExpression]]):
        self._grouping_list = grouping_list

    @property
    def grouping_list(self) -> List[List[SQLGeneralExpression]]:
        """返回 GROUPING SETS 中的各个组的列表"""
        return self._grouping_list

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        grouping_str_list = []
        for grouping in self.grouping_list:
            if len(grouping) > 1:
                grouping_str_list.append("(" + ", ".join(column.source() for column in grouping) + ")")
            else:
                grouping_str_list.append(grouping[0].source())
        return "GROUP BY GROUPING SETS (" + ", ".join(grouping_str_list) + ")"

    def get_used_column_list(self) -> List[Union[str, int]]:
        """返回字段名和列编号"""
        result = []
        for grouping in self.grouping_list:
            for column in grouping:
                if isinstance(column, SQLLiteralExpression):
                    result.append(column.as_int())  # 列编号
                else:
                    result.extend(column.get_used_column_list())
        return result


# ---------------------------------------- HAVING 子句 ----------------------------------------


class SQLHavingClause(SQLBase):
    """HAVING 子句"""

    def __init__(self, condition: SQLConditionExpression):
        self._condition = condition

    @property
    def condition(self) -> SQLConditionExpression:
        """返回 HAVING 中的条件表达式"""
        return self._condition

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return f"HAVING {self.condition.source()}"

    def get_used_column_list(self) -> List[str]:
        """返回使用的字段列表"""
        return self.condition.get_used_column_list()


# ---------------------------------------- ORDER BY 子句 ----------------------------------------


class SQLOrderByClause(SQLBase):
    """ORDER BY 子句"""

    def __init__(self, columns: List[Tuple[SQLGeneralExpression, SQLOrderType]]):
        self._columns = columns

    @property
    def columns(self) -> List[Tuple[SQLGeneralExpression, SQLOrderType]]:
        """返回 ORDER BY　子句中的列的一般表达式和排序类型的元组的列表"""
        return self._columns

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        result = []
        for column, order_type in self.columns:
            if order_type.source(data_source) == "ASC":
                result.append(f"{column.source(data_source)}")
            else:
                result.append(f"{column.source(data_source)} DESC")
        return "ORDER BY " + ", ".join(result)

    def get_used_column_list(self) -> List[Union[str, int]]:
        """返回字段名和列编号"""
        result = []
        for column, _ in self.columns:
            if isinstance(column, SQLLiteralExpression):
                result.append(column.as_int())  # 列编号
            else:
                result.extend(column.get_used_column_list())
        return result


# ---------------------------------------- LIMIT 子句 ----------------------------------------


class SQLLimitClause(SQLBase):
    """LIMIT 子句"""

    def __init__(self, limit: int, offset: int):
        self._limit = limit
        self._offset = offset

    @property
    def limit(self) -> int:
        """返回开始的位置"""
        return self._limit

    @property
    def offset(self) -> int:
        """返回检索的行数"""
        return self._offset

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        return f"LIMIT {self.offset}, {self.limit}"


# ---------------------------------------- WITH 子句 ----------------------------------------


class SQLWithClause(SQLBase):
    """WITH 子句"""

    def __init__(self, tables: List[Tuple[str, "SQLSelectStatement"]]):
        self._tables = tables

    @staticmethod
    def empty():
        """空 WITH 子句"""
        return SQLWithClause(tables=[])

    @property
    def tables(self) -> List[Tuple[str, "SQLSelectStatement"]]:
        """返回 WITH 中的表名与表的 SELECT 表达式的元组的列表"""
        return self._tables

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        if not self.tables:
            return ""
        table_str = ", \n".join(f"{table_name}({table_statement.source()})"
                                for table_name, table_statement in self.tables)
        return f"WITH {table_str}"

    def get_with_table_name_set(self) -> Set[str]:
        """获取 WITH 中临时表的名称"""
        return set(table[0] for table in self.tables)

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


class SQLStatement(SQLBase, abc.ABC):
    """语句的抽象基类"""

    def __init__(self, with_clause: Optional[SQLWithClause]):
        self._with_clause = with_clause

    @property
    def with_clause(self) -> Optional[SQLWithClause]:
        """返回语句的 WITH 子句"""
        return self._with_clause


# ---------------------------------------- SELECT 语句 ----------------------------------------


class SQLSelectStatement(SQLStatement, abc.ABC):
    """SELECT 语句"""

    @abc.abstractmethod
    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码  TODO 待移除"""

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


class SQLSingleSelectStatement(SQLSelectStatement):
    """单个 SELECT 表达式"""

    def __init__(self,
                 with_clause: Optional[SQLWithClause],
                 select_clause: SQLSelectClause,
                 from_clause: Optional[SQLFromClause] = None,
                 lateral_view_clauses: Optional[List[SQLLateralViewClause]] = None,
                 join_clauses: Optional[List[SQLJoinClause]] = None,
                 where_clause: Optional[SQLWhereClause] = None,
                 group_by_clause: Optional[SQLGroupByClause] = None,
                 having_clause: Optional[SQLHavingClause] = None,
                 order_by_clause: Optional[SQLOrderByClause] = None,
                 limit_clause: Optional[SQLLimitClause] = None):
        super().__init__(with_clause)
        if lateral_view_clauses is None:
            lateral_view_clauses = []
        if join_clauses is None:
            join_clauses = []
        self._select_clause = select_clause
        self._from_clause = from_clause
        self._lateral_view_clauses = lateral_view_clauses
        self._join_clauses = join_clauses
        self._where_clause = where_clause
        self._group_by_clause = group_by_clause
        self._having_clause = having_clause
        self._order_by_clause = order_by_clause
        self._limit_clause = limit_clause

    @property
    def select_clause(self) -> SQLSelectClause:
        """返回 SELECT 子句"""
        return self._select_clause

    @property
    def from_clause(self) -> Optional[SQLFromClause]:
        """返回 FROM 子句"""
        return self._from_clause

    @property
    def lateral_view_clauses(self) -> List[SQLLateralViewClause]:
        """返回 LATERAL VIEW 子句"""
        return self._lateral_view_clauses

    @property
    def join_clauses(self) -> List[SQLJoinClause]:
        """返回 JOIN 子句"""
        return self._join_clauses

    @property
    def where_clause(self) -> Optional[SQLWhereClause]:
        """返回 WHERE 子句"""
        return self._where_clause

    @property
    def group_by_clause(self) -> Optional[SQLGroupByClause]:
        """返回 GROUP BY 子句"""
        return self._group_by_clause

    @property
    def having_clause(self) -> Optional[SQLHavingClause]:
        """返回 HAVING 子句"""
        return self._having_clause

    @property
    def order_by_clause(self) -> Optional[SQLOrderByClause]:
        """返回 ORDER BY 子句"""
        return self._order_by_clause

    @property
    def limit_clause(self) -> Optional[SQLLimitClause]:
        """返回 LIMIT 子句"""
        return self._limit_clause

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        with_clause_str = self.with_clause.source() + "\n" if not self.with_clause.is_empty() else ""
        result = [self.select_clause.source(data_source)]
        for clause in [self.from_clause, *self.lateral_view_clauses, *self.join_clauses, self.where_clause,
                       self.group_by_clause, self.having_clause, self.order_by_clause, self.limit_clause]:
            if clause is not None:
                result.append(clause.source())
        return with_clause_str + "\n".join(result)

    def get_alias_to_used_column_hash(self) -> Dict[str, List[str]]:
        """获取字段别名对应的原始字段列表的映射表"""
        return self.select_clause.get_alias_to_used_column_hash()

    def get_index_to_used_column_hash(self) -> Dict[int, List[str]]:
        """获取字段序号对应的原始字段列表的映射表"""
        return self.select_clause.get_index_to_used_column_hash()

    def get_from_used_table_list(self) -> List[str]:
        """获取 FROM 语句中使用的表名的列表"""
        if self.from_clause is None:
            return []
        result = self.from_clause.get_used_table_list()
        return ordered_distinct(result)

    def get_join_used_table_list(self) -> List[str]:
        """获取 JOIN 语句中使用的表名的列表"""
        result = []
        for join_clause in self.join_clauses:
            result.extend(join_clause.get_used_table_list())
        return result

    def get_select_used_column_list(self) -> List[str]:
        """获取 SELECT 语句结果中使用的字段的列表"""
        return ordered_distinct(self.select_clause.get_used_column_list())

    def get_where_used_column_list(self) -> List[str]:
        """获取在 WHERE 条件中使用的字段名的列表"""
        if self.where_clause is None:
            return []
        return ordered_distinct(self.where_clause.get_used_column_list())

    def get_group_by_used_column_list(self) -> List[str]:
        """获取在 GROUP BY 中使用的字段名的列表"""
        if self.group_by_clause is None:
            return []
        return self._get_source_column_list(self.group_by_clause.get_used_column_list())

    def get_having_used_column_list(self) -> List[str]:
        """获取在 HAVING 中使用的字段名的列表"""
        if self.having_clause is None:
            return []
        return self._get_source_column_list(self.having_clause.get_used_column_list())

    def get_order_by_used_column_list(self) -> List[str]:
        """获取在 ORDER BY 中使用的字段名的列表"""
        if self.order_by_clause is None:
            return []
        return self._get_source_column_list(self.order_by_clause.get_used_column_list())

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


class SQLUnionSelectStatement(SQLSelectStatement):
    """复合查询语句，使用 UNION、EXCEPT、INTERSECT 进行组合"""

    def __init__(self,
                 with_clause: Optional[SQLWithClause],
                 elements: List[Union[SQLUnionType, SQLSingleSelectStatement]]):
        super().__init__(with_clause)
        self._elements = elements

    @property
    def elements(self) -> List[Union[SQLUnionType, SQLSingleSelectStatement]]:
        """返回包含组合关键字的表达式的列表"""
        return self._elements

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        with_clause_str = self.with_clause.source() + "\n" if not self.with_clause.is_empty() else ""
        return with_clause_str + "\n".join(element.source(data_source) for element in self.elements)

    def get_from_used_table_list(self) -> List[str]:
        """获取 FROM 语句中使用的表名的列表"""
        result = []
        for element in self.elements:
            if isinstance(element, SQLSingleSelectStatement):
                result.extend(element.get_from_used_table_list())
        return ordered_distinct(result)

    def get_join_used_table_list(self) -> List[str]:
        """获取 JOIN 语句中使用的表名的列表"""
        result = []
        for element in self.elements:
            if isinstance(element, SQLSingleSelectStatement):
                result.extend(element.get_join_used_table_list())
        return ordered_distinct(result)

    def get_select_used_column_list(self) -> List[str]:
        """获取 SELECT 语句结果中使用的字段的列表"""
        result = []
        for element in self.elements:
            if isinstance(element, SQLSingleSelectStatement):
                result.extend(element.get_select_used_column_list())
        return ordered_distinct(result)

    def get_where_used_column_list(self) -> List[str]:
        """获取在 WHERE 条件中使用的字段名的列表"""
        result = []
        for element in self.elements:
            if isinstance(element, SQLSingleSelectStatement):
                result.extend(element.get_where_used_column_list())
        return ordered_distinct(result)

    def get_group_by_used_column_list(self) -> List[str]:
        """获取在 GROUP BY 中使用的字段名的列表"""
        result = []
        for element in self.elements:
            if isinstance(element, SQLSingleSelectStatement):
                result.extend(element.get_group_by_used_column_list())
        return ordered_distinct(result)

    def get_having_used_column_list(self) -> List[str]:
        """获取在 HAVING 中使用的字段名的列表"""
        result = []
        for element in self.elements:
            if isinstance(element, SQLSingleSelectStatement):
                result.extend(element.get_having_used_column_list())
        return ordered_distinct(result)

    def get_order_by_used_column_list(self) -> List[str]:
        """返回在 ORDER BY 子句中使用的字段名的列表"""
        result = []
        for element in self.elements:
            if isinstance(element, SQLSingleSelectStatement):
                result.extend(element.get_order_by_used_column_list())
        return ordered_distinct(result)


# ---------------------------------------- INSERT 语句 ----------------------------------------


class SQLInsertStatement(SQLStatement, abc.ABC):
    """INSERT 表达式

    两个子类包含 VALUES 和 SELECT 两种方式

    INSERT {INTO|OVERWRITE} [TABLE] <table_name_expression> [PARTITION (<partition_expression>)]
    [(<colum_name_expression [,<column_name_expression> ...]>)]
    {VALUES <value_expression> [,<value_expression> ...] | <select_statement>}
    """

    def __init__(self,
                 with_clause: Optional[SQLWithClause],
                 insert_type: SQLInsertType,
                 table_name: SQLTableNameExpression,
                 partition: Optional[SQLPartitionExpression],
                 columns: Optional[List[SQLColumnNameExpression]]):
        super().__init__(with_clause)
        self._insert_type = insert_type
        self._table_name = table_name
        self._partition = partition
        self._columns = columns

    @property
    def insert_type(self) -> SQLInsertType:
        """返回插入类型"""
        return self._insert_type

    @property
    def table_name(self) -> SQLTableNameExpression:
        """返回插入的表名"""
        return self._table_name

    @property
    def partition(self) -> SQLPartitionExpression:
        """返回插入的分区"""
        return self._partition

    @property
    def columns(self) -> Optional[List[SQLColumnExpression]]:
        """返回插入的列列表"""
        return self._columns

    def _insert_str(self, data_source: DataSource) -> str:
        insert_type_str = self.insert_type.source(data_source)
        table_keyword_str = "TABLE " if data_source == DataSource.HIVE else ""
        partition_str = self.partition.source() + " " if self.partition is not None else ""
        if self.columns is not None:
            columns_str = "(" + ", ".join(column.source() for column in self.columns) + ") "
        else:
            columns_str = ""
        return f"{insert_type_str} {table_keyword_str}{self.table_name.source()} {partition_str}{columns_str}"

    @abc.abstractmethod
    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""

    @abc.abstractmethod
    def get_used_table_list(self) -> List[str]:
        """获取使用的表的列表"""


class SQLInsertValuesStatement(SQLInsertStatement):
    """INSERT ... VALUES ... 语句"""

    def __init__(self,
                 with_clause: Optional[SQLWithClause],
                 insert_type: SQLInsertType,
                 table_name: SQLTableNameExpression,
                 partition: Optional[SQLPartitionExpression],
                 columns: Optional[List[SQLColumnNameExpression]],
                 values: List[SQLValueExpression]):
        super().__init__(with_clause, insert_type, table_name, partition, columns)
        self._values = values

    @property
    def values(self) -> List[SQLValueExpression]:
        """返回插入的值表达式的列表"""
        return self._values

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
        """返回语法节点的 SQL 源码"""
        values_str = ", ".join(value.source() for value in self.values)
        return f"{self._insert_str(data_source)}VALUES {values_str}"

    def get_used_table_list(self) -> List[str]:
        """获取使用的表的列表"""
        return []

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return []


class SQLInsertSelectStatement(SQLInsertStatement):
    """INSERT ... SELECT ... 语句"""

    def __init__(self,
                 with_clause: Optional[SQLWithClause],
                 insert_type: SQLInsertType,
                 table_name: SQLTableNameExpression,
                 partition: Optional[SQLPartitionExpression],
                 columns: Optional[List[SQLColumnNameExpression]],
                 select_statement: SQLSelectStatement):
        super().__init__(with_clause, insert_type, table_name, partition, columns)
        self._select_statement = select_statement

    @property
    def select_statement(self) -> SQLSelectStatement:
        """返回插入语句中使用的 SELECT 语句"""
        return self._select_statement

    def source(self, data_source: DataSource = DataSource.MYSQL) -> str:
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


class SQLSetStatement(SQLBase):
    """SQL 语句"""

    def __init__(self, config_name: SQLConfigNameExpression, config_value: SQLConfigValueExpression):
        self._config_name = config_name
        self._config_value = config_value

    @property
    def config_name(self) -> SQLConfigNameExpression:
        """返回配置名称表达式"""
        return self._config_name

    @property
    def config_value(self) -> SQLConfigValueExpression:
        """返回配置值表达式"""
        return self._config_value

    def source(self, data_source: DataSource) -> str:
        """返回语法节点的 SQL 源码"""
        return f"SET {self.config_name.source(data_source)} = {self.config_value.source(data_source)}"


# ---------------------------------------- CREATE TABLE 语句 ----------------------------------------


class SQLTableConfigExpression(SQLBase):
    """建表语句配置信息表达式"""


class SQLCreateTableStatement(SQLBase):
    """【DDL】CREATE TABLE 语句"""

    def __init__(self,
                 table_name_expression: SQLTableNameExpression,
                 comment: Optional[str] = None,
                 if_not_exists: bool = False,
                 columns: Optional[List[SQLDefineColumnExpression]] = None,
                 primary_key: Optional[SQLPrimaryIndexExpression] = None,
                 unique_key: Optional[List[SQLUniqueIndexExpression]] = None,
                 key: Optional[List[SQLNormalIndexExpression]] = None,
                 fulltext_key: Optional[List[SQLFulltextIndexExpression]] = None,
                 foreign_key: List[SQLForeignKeyExpression] = None,
                 engine: Optional[str] = None,
                 auto_increment: Optional[int] = None,
                 default_charset: Optional[str] = None,
                 collate: Optional[str] = None,
                 row_format: Optional[str] = None,
                 states_persistent: Optional[str] = None,
                 partition_by: List[SQLDefineColumnExpression] = None
                 ):
        self._table_name_expression = table_name_expression
        self._comment = comment
        self._if_not_exists = if_not_exists
        self._columns = columns
        self._primary_key = primary_key
        self._unique_key = unique_key
        self._key = key
        self._fulltext_key = fulltext_key
        self._foreign_key = foreign_key
        self._engine = engine
        self._auto_increment = auto_increment
        self._default_charset = default_charset
        self._collate = collate
        self._row_format = row_format
        self._states_persistent = states_persistent
        self._partition_by = partition_by if partition_by is not None else []

    @property
    def table_name_expression(self):
        """返回表名表达式"""
        return self._table_name_expression

    @property
    def comment(self):
        """返回表注释"""
        return self._comment

    @property
    def if_not_exists(self) -> bool:
        """返回是否包含 IS NOT EXISTS 关键字"""
        return self._if_not_exists

    @property
    def columns(self) -> List[SQLDefineColumnExpression]:
        """返回列声明表达式"""
        return self._columns

    @property
    def primary_key(self) -> SQLPrimaryIndexExpression:
        """返回主键索引声明表达式"""
        return self._primary_key

    @property
    def unique_key(self) -> List[SQLUniqueIndexExpression]:
        """返回唯一键索引声明表达式的列表"""
        return self._unique_key

    @property
    def key(self) -> List[SQLNormalIndexExpression]:
        """返回普通索引声明表达式的列表"""
        return self._key

    @property
    def fulltext_key(self) -> List[SQLFulltextIndexExpression]:
        """返回全文本索引声明表达式的列表"""
        return self._fulltext_key

    @property
    def foreign_key(self) -> List[SQLForeignKeyExpression]:
        """返回外键"""
        return self._foreign_key

    @property
    def engine(self) -> Optional[str]:
        """返回 ENGINE 的配置值"""
        return self._engine

    @property
    def auto_increment(self) -> Optional[str]:
        """返回 AUTO INCREMENT 的配置值"""
        return self._auto_increment

    @property
    def default_charset(self) -> Optional[str]:
        """返回 DEFAULT CHARSET 的配置值"""
        return self._default_charset

    @property
    def collate(self) -> Optional[str]:
        """返回 COLLATE 的配置值"""
        return self._collate

    @property
    def row_format(self) -> Optional[str]:
        """返回 ROW FORMAT 的配置值"""
        return self._row_format

    @property
    def states_persistent(self) -> Optional[str]:
        """配置 STATES PERSISTENT 的配置值"""
        return self._states_persistent

    @property
    def partition_by(self) -> List[SQLDefineColumnExpression]:
        """返回分组字段的字段声明表达式的列表"""
        return self._partition_by

    def set_table_name(self, table_name_expression: SQLTableNameExpression):
        """设置表名"""
        self._table_name_expression = table_name_expression

    def change_type(self, hashmap: Dict[str, str], remove_param: bool = True):
        """更新每个字段的变量类型"""
        for column in self.columns:
            old_column_type = column.column_type.name
            new_column_type = hashmap[old_column_type.upper()]
            column.column_type._name = new_column_type
            if remove_param is True:
                column.column_type._function_params = []

    def append_column(self, column: SQLDefineColumnExpression):
        """添加字段"""
        self.columns.append(column)

    def append_partition_by_column(self, column: SQLDefineColumnExpression):
        """添加分区字段"""

    def source(self, data_source: DataSource = DataSource.MYSQL, n_indent: int = 4) -> str:
        """返回语法节点的 SQL 源码"""
        if data_source == DataSource.MYSQL:
            indentation = " " * n_indent  # 缩进字符串
            result = "CREATE TABLE"
            if self.if_not_exists is True:
                result += " IF NOT EXISTS"
            result += f" {self.table_name_expression.source(data_source)}(\n"
            columns_and_keys = []
            for column in self.columns:
                columns_and_keys.append(f"{indentation}{column.source()}")
            if self.primary_key is not None:
                columns_and_keys.append(f"{indentation}{self.primary_key.source()}")
            for unique_key in self.unique_key:
                columns_and_keys.append(f"{indentation}{unique_key.source()}")
            for key in self.key:
                columns_and_keys.append(f"{indentation}{key.source()}")
            for fulltext_key in self.fulltext_key:
                columns_and_keys.append(f"{indentation}{fulltext_key.source()}")
            for foreign_key in self.foreign_key:
                columns_and_keys.append(f"{indentation}{foreign_key.source()}")
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
            if self._comment is not None:
                result += f" COMMENT = {self._comment}"
            return result
        if data_source == DataSource.HIVE:
            indentation = " " * n_indent  # 缩进字符串
            result = "CREATE TABLE"
            if self.if_not_exists is True:
                result += " IF NOT EXISTS"
            result += f" {self.table_name_expression.source(data_source)}(\n"
            columns_and_keys = []
            for column in self.columns:
                columns_and_keys.append(f"{indentation}{column.source(DataSource.HIVE)}")
            result += ",\n".join(columns_and_keys)
            result += "\n)"
            if self._comment is not None:
                result += f" COMMENT {self._comment}"
            if len(self.partition_by) > 0:
                partition_columns = []
                for column in self.partition_by:
                    partition_columns.append(column.source(DataSource.HIVE))
                partition_str = ", ".join(partition_columns)
                result += f" PARTITIONED BY ({partition_str})"
            return result
        raise SqlParseError(f"暂不支持的数据类型: {data_source}")
