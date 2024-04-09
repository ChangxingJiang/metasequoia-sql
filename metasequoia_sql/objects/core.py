"""
TODO 统一 SQLBase 的抽象方法：增加 get_used_column_list 和 get_used_table_list
TODO 不返回 CURRENT_DATE、CURRENT_TIME、CURRENT_TIMESTAMP 作为字段
TODO 增加 scanner 未解析完成的发现机制

参考文档：https://www.alibabacloud.com/help/zh/maxcompute/user-guide/insert-or-update-data-into-a-table-or-a-static-partition?spm=a2c63.p38356.0.0.637d7109wr3nC3
"""

import abc
import enum
from typing import Optional, List, Tuple, Union, Dict

from metasequoia_sql.common.basic import ordered_distinct
from metasequoia_sql.errors import SqlParseError


class SQLEnumJoinType(enum.Enum):
    """关联类型"""
    JOIN = "JOIN"  # 内连接
    INNER_JOIN = "INNER JOIN"  # 内连接
    LEFT_JOIN = "LEFT JOIN"  # 左外连接
    LEFT_OUTER_JOIN = "LEFT OUTER JOIN"  # 左外连接
    RIGHT_JOIN = "RIGHT JOIN"  # 右外连接
    RIGHT_OUTER_JOIN = "RIGHT OUTER JOIN"  # 右外连接
    FULL_JOIN = "FULL JOIN"  # 全外连接
    FULL_OUTER_JOIN = "FULL OUTER JOIN"  # 全外连接
    CROSS_JOIN = "CROSS JOIN"  # 交叉连接


class SQLEnumOrderType(enum.Enum):
    """排序类型"""
    ASC = "ASC"  # 升序
    DESC = "DESC"  # 降序


class SQLEnumCastDataType(enum.Enum):
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


class SQLEnumUnionType(enum.Enum):
    """关联类型"""
    UNION_ALL = ["UNION", "ALL"]
    UNION = ["UNION"]
    EXCEPT = ["EXCEPT"]
    INTERSECT = ["INTERSECT"]
    MINUS = ["MINUS"]


class SQLInsertType(enum.Enum):
    """插入类型"""
    INSERT_INTO = ["INSERT", "INTO"]
    INSERT_OVERWRITE = ["INSERT", "OVERWRITE"]


class SQLBase(abc.ABC):
    @property
    @abc.abstractmethod
    def source(self) -> str:
        """返回 SQL 源码"""

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} source={self.source}>"


# ------------------------------ 元素层级 ------------------------------


class SQLComputeOperator(SQLBase, abc.ABC):
    """计算运算符"""

    @staticmethod
    def get_used_column_list() -> List[str]:
        """获取使用的字段列表"""
        return []


class SQLPlus(SQLComputeOperator):
    """加法运算符"""

    @property
    def source(self) -> str:
        return "+"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class SQLSubtract(SQLComputeOperator):
    """减法运算符"""

    @property
    def source(self) -> str:
        return "-"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class SQLMultiple(SQLComputeOperator):
    """乘法运算符"""

    @property
    def source(self) -> str:
        return "*"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class SQLDivide(SQLComputeOperator):
    """除法运算符"""

    @property
    def source(self) -> str:
        return "/"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class SQLConcat(SQLComputeOperator):
    """字符串拼接运算符（仅 Oracle、DB2、PostgreSQL 中适用）"""

    @property
    def source(self) -> str:
        return "||"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class SQLCompareOperator(SQLBase, abc.ABC):
    """比较运算符"""


class SQLEqualTo(SQLCompareOperator):
    """等于运算符"""

    @property
    def source(self) -> str:
        return "="

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class SQLNotEqualTo(SQLCompareOperator):
    """不等于运算符：包含 != 和 <> 两种类型"""

    @property
    def source(self) -> str:
        return "!="

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class SQLIs(SQLCompareOperator):
    """不等于运算符：包含 != 和 <> 两种类型"""

    @property
    def source(self) -> str:
        return "IS"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class SQLLessThan(SQLCompareOperator):
    """小于运算符"""

    @property
    def source(self) -> str:
        return "<"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class SQLLessThanOrEqual(SQLCompareOperator):
    """小于等于运算符"""

    @property
    def source(self) -> str:
        return "<="

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class SQLGreaterThan(SQLCompareOperator):
    """大于运算符"""

    @property
    def source(self) -> str:
        return ">"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class SQLGreaterThanOrEqual(SQLCompareOperator):
    """大于等于运算符"""

    @property
    def source(self) -> str:
        return ">="

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class SQLLiteral(SQLBase, abc.ABC):
    """字面值"""

    @property
    @abc.abstractmethod
    def value(self):
        """获取字面值"""


class SQLLiteralInteger(SQLLiteral):
    """整数字面值"""

    def __init__(self, value: int):
        self._value = value

    @property
    def value(self) -> int:
        return self._value

    @property
    def source(self) -> str:
        return f"{self._value}"


class SQLLiteralFloat(SQLLiteral):
    """浮点数字面值"""

    def __init__(self, value: float):
        self._value = value

    @property
    def value(self) -> float:
        return self._value

    @property
    def source(self) -> str:
        return f"{self._value}"


class SQLLiteralString(SQLLiteral):
    """字符串字面值"""

    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    @property
    def source(self) -> str:
        return f"'{self._value}'"


class SQLLiteralHex(SQLLiteral):
    """十六进制字面值"""

    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    @property
    def source(self) -> str:
        return f"x'{self._value}'"


class SQLLiteralBit(SQLLiteral):
    """位值字面值"""

    def __init__(self, value: str):
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    @property
    def source(self) -> str:
        return f"b'{self._value}'"


class SQLLiteralBool(SQLLiteral):
    """布尔值字面值"""

    def __init__(self, value: bool):
        self._value = value

    @property
    def value(self) -> bool:
        return self._value

    @property
    def source(self) -> str:
        return "TRUE" if self._value is True else "FALSE"


class SQLLiteralNull(SQLLiteral):
    """空值字面值"""

    @property
    def value(self) -> None:
        return None

    @property
    def source(self) -> str:
        return "NULL"


class SQLLogicalOperator(SQLBase, abc.ABC):
    """逻辑运算符"""

    @staticmethod
    def get_used_column_list() -> List[str]:
        """获取使用的字段列表"""
        return []


class SQLAndOperator(SQLLogicalOperator):
    """逻辑 AND 运算符"""

    @property
    def source(self) -> str:
        return "AND"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class SQLOrOperator(SQLLogicalOperator):
    """逻辑 OR 运算符"""

    @property
    def source(self) -> str:
        return "OR"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class SQLNotOperator(SQLLogicalOperator):
    """逻辑 NOT 运算符"""

    @property
    def source(self) -> str:
        return "OR"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


class SQLUnionKeyword(SQLBase):
    """复合查询关键字"""

    def __init__(self, union_type: SQLEnumUnionType):
        self._union_type = union_type

    @property
    def union_type(self) -> SQLEnumUnionType:
        return self._union_type

    @property
    def source(self) -> str:
        return " ".join(self._union_type.value)


# ------------------------------ 表达式层级（一般表达式） ------------------------------


class SQLGeneralExpression(SQLBase, abc.ABC):
    """一般表达式"""

    @abc.abstractmethod
    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""


class SQLColumnNameExpression(SQLGeneralExpression):
    """列名表达式"""

    def __init__(self,
                 table: Optional[str],
                 column: str):
        self._table = table
        self._column = column

    @property
    def table(self) -> Optional[str]:
        return self._table

    @property
    def column(self) -> str:
        return self._column

    @property
    def source(self) -> str:
        if self.table is not None:
            return f"{self.table}.{self.column}"
        else:
            return f"{self.column}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return [self.source]


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
        return self._schema_name

    @property
    def function_name(self) -> str:
        return self._function_name

    @property
    def function_params(self) -> List[SQLGeneralExpression]:
        return self._function_params

    @property
    def source(self) -> str:
        return f"{self._get_function_str()}({self._get_param_str()})"

    def _get_param_str(self) -> str:
        return ", ".join(param.source for param in self.function_params)

    def _get_function_str(self) -> str:
        if self.schema_name is not None:
            return f"{self.schema_name}.{self.function_name}"
        else:
            return f"{self.function_name}"

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
        return self._is_distinct

    @property
    def source(self) -> str:
        is_distinct = "DISTINCT " if self.is_distinct is True else ""
        return f"{self._get_function_str()}({is_distinct}{self._get_param_str()})"


class SQLCastFunctionExpression(SQLFunctionExpression):
    """Cast 函数表达式"""

    def __init__(self,
                 column_expression: SQLGeneralExpression,
                 cast_type: "SQLCastDataType"):
        super().__init__(None, "CAST", [])
        self._column_expression = column_expression
        self._cast_type = cast_type

    @property
    def function_params(self) -> List[SQLGeneralExpression]:
        # TODO 修改父类继承关系
        raise SqlParseError("SQLCastFunctionExpression.function_params() 方法不允许调用")

    @property
    def column_expression(self) -> SQLGeneralExpression:
        return self._column_expression

    @property
    def cast_type(self) -> "SQLCastDataType":
        return self._cast_type

    @property
    def source(self) -> str:
        return f"{self._get_function_str()}({self.column_expression.source} AS {self.cast_type.source})"

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
        return self._extract_name

    @property
    def column_expression(self) -> SQLGeneralExpression:
        return self._column_expression

    @property
    def source(self) -> str:
        return f"{self._get_function_str()}({self.extract_name.source} FROM {self.column_expression.source})"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.column_expression.get_used_column_list()


class SQLCaseExpression(SQLGeneralExpression):
    """第 1 种格式的 CASE 表达式

    CASE
        WHEN {条件表达式} THEN {一般表达式}
        ELSE {一般表达式}
    END
    """

    def __init__(self,
                 cases: List[Tuple["SQLConditionExpression", SQLGeneralExpression]],
                 else_value: Optional[SQLGeneralExpression]):
        self._cases = cases
        self._else_value = else_value

    @property
    def cases(self) -> List[Tuple["SQLConditionExpression", SQLGeneralExpression]]:
        return self._cases

    @property
    def else_value(self) -> Optional[SQLGeneralExpression]:
        return self._else_value

    @property
    def source(self) -> str:
        result = ["CASE"]
        for when, then in self.cases:
            result.append(f"    WHEN {when.source} THEN {then.source}")
        if self.else_value is not None:
            result.append(f"    ELSE {self.else_value.source}")
        result.append("END")
        return "\n".join(result)

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
        return self._case_value

    @property
    def cases(self) -> List[Tuple[SQLGeneralExpression, SQLGeneralExpression]]:
        return self._cases

    @property
    def else_value(self) -> Optional[SQLGeneralExpression]:
        return self._else_value

    @property
    def source(self) -> str:
        result = ["CASE", self.case_value.source]
        for when, then in self.cases:
            result.append(f"    WHEN {when.source} THEN {then.source}")
        if self.else_value is not None:
            result.append(f"    ELSE {self.else_value.source}")
        result.append("END")
        return "\n".join(result)

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        result = self.case_value.get_used_column_list()
        for when, _ in self.cases:
            result.extend(when.get_used_column_list())
        return result


class SQLWindowExpression(SQLGeneralExpression):
    """窗口表达式"""

    def __init__(self,
                 window_function: SQLFunctionExpression,
                 partition_by: Optional[SQLGeneralExpression],
                 order_by: Optional[SQLGeneralExpression]):
        self._window_function = window_function
        self._partition_by = partition_by
        self._order_by = order_by

    @property
    def window_function(self) -> SQLFunctionExpression:
        return self._window_function

    @property
    def partition_by(self) -> Optional[SQLGeneralExpression]:
        return self._partition_by

    @property
    def order_by(self) -> Optional[SQLGeneralExpression]:
        return self._order_by

    @property
    def source(self) -> str:
        result = f"{self.window_function.source} OVER ("
        if self.partition_by is not None:
            result += f"PARTITION BY {self.partition_by.source}"
        if self.order_by is not None:
            result += f"ORDER BY {self.order_by.source}"
        result += ")"
        return result

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        result = []
        if self.partition_by is not None:
            result.extend(self.partition_by.get_used_column_list())
        if self.order_by is not None:
            result.extend(self.order_by.get_used_column_list())
        return result


class SQLComputeExpression(SQLGeneralExpression):
    """计算表达式"""

    def __init__(self,
                 elements: List[Union[SQLGeneralExpression, SQLComputeOperator]]):
        self._elements = elements

    @property
    def elements(self) -> List[Union[SQLGeneralExpression, SQLComputeOperator]]:
        return self._elements

    @property
    def source(self) -> str:
        return " ".join(element.source for element in self.elements)

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        result = []
        for element in self.elements:
            result.extend(element.get_used_column_list())
        return result


class SQLLiteralExpression(SQLGeneralExpression):
    """字面值表达式"""

    def __init__(self, literal: SQLLiteral):
        self._literal = literal

    def as_int(self) -> int:
        return int(self.literal.value)

    @property
    def literal(self) -> SQLLiteral:
        return self._literal

    @property
    def source(self) -> str:
        return self.literal.source

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return []


class SQLSubQueryExpression(SQLGeneralExpression):
    """子查询表达式"""

    def __init__(self, select_statement: "SQLSelectStatement"):
        self._select_statement = select_statement

    @property
    def select_statement(self) -> "SQLSelectStatement":
        return self._select_statement

    @property
    def source(self) -> str:
        return f"({self.select_statement.source})"

    def get_used_column_list(self) -> List[str]:
        return self.select_statement.get_select_used_column_list()

    def get_used_table_list(self) -> List[str]:
        return self.select_statement.get_used_table_list()


class SQLWildcardExpression(SQLGeneralExpression):
    """通配符表达式"""

    def __init__(self, schema: Optional[str]):
        self._schema = schema

    @property
    def schema(self) -> Optional[str]:
        return self._schema

    @property
    def source(self) -> str:
        if self.schema is not None:
            return f"{self.schema}.*"
        else:
            return "*"

    def get_used_column_list(self) -> List[str]:
        """获取语句结果中使用的字段"""
        return [self.source]


class SQLValueExpression(SQLGeneralExpression):
    """值表达式"""

    def __init__(self, values: List[SQLGeneralExpression]):
        self._values = values

    @property
    def values(self) -> List[SQLGeneralExpression]:
        return self._values

    @property
    def source(self) -> str:
        values_str = ", ".join(value.source for value in self.values)
        return f"({values_str})"

    def get_used_column_list(self) -> List[str]:
        return []


# ------------------------------ 表达式层级（专有表达式） ------------------------------


class SQLCastDataType(SQLBase):
    def __init__(self, signed: bool, data_type: SQLEnumCastDataType, params: Optional[List[SQLGeneralExpression]]):
        self._signed = signed
        self._data_type = data_type
        self._params = params

    @property
    def signed(self) -> bool:
        return self._signed

    @property
    def data_type(self) -> SQLEnumCastDataType:
        return self._data_type

    @property
    def params(self) -> Optional[List[SQLGeneralExpression]]:
        return self._params

    @property
    def source(self) -> str:
        result = []
        if self.signed is True:
            result.append("SIGNED")
        result.append(self.data_type.value)
        if self.params is not None:
            param_str = ", ".join(param.source for param in self.params)
            result.append(f"({param_str})")
        return " ".join(result)


class SQLTableNameExpression(SQLBase):
    """表名表达式"""

    def __init__(self, schema: Optional[str], table: str):
        self._schema = schema
        self._table = table

    @property
    def schema(self) -> Optional[str]:
        return self._schema

    @property
    def table(self) -> str:
        return self._table

    @property
    def source(self) -> str:
        if self.schema is not None:
            return f"{self.schema}.{self.table}"
        else:
            return f"{self.table}"

    def get_used_table_list(self) -> List[str]:
        return [self.source]


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
        return self._operator

    @property
    def before_value(self) -> SQLGeneralExpression:
        return self._before_value

    @property
    def after_value(self) -> SQLGeneralExpression:
        return self._after_value

    @property
    def source(self) -> str:
        return f"{self.before_value.source} {self.operator.source} {self.after_value.source}"

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
        return self._is_not

    @property
    def before_value(self) -> SQLGeneralExpression:
        return self._before_value

    @property
    def after_value(self) -> SQLGeneralExpression:
        return self._after_value

    @property
    def source(self) -> str:
        if self.is_not:
            return f"{self.before_value.source} IS NOT {self.after_value.source}"
        else:
            return f"{self.before_value.source} IS {self.after_value.source}"

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
        return self._is_not

    @property
    def before_value(self) -> SQLGeneralExpression:
        return self._before_value

    @property
    def after_value(self) -> SQLGeneralExpression:
        return self._after_value

    @property
    def source(self) -> str:
        if self.is_not:
            return f"{self.before_value.source} NOT IN {self.after_value.source}"
        else:
            return f"{self.before_value.source} IN {self.after_value.source}"

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
        return self._is_not

    @property
    def before_value(self) -> SQLGeneralExpression:
        return self._before_value

    @property
    def after_value(self) -> SQLGeneralExpression:
        return self._after_value

    @property
    def source(self) -> str:
        if self.is_not:
            return f"{self.before_value.source} NOT LIKE {self.after_value.source}"
        else:
            return f"{self.before_value.source} LIKE {self.after_value.source}"

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
        return self._is_not

    @property
    def after_value(self) -> SQLGeneralExpression:
        return self._after_value

    @property
    def source(self) -> str:
        if self.is_not:
            return f"NOT EXISTS {self.after_value.source}"
        else:
            return f"EXISTS {self.after_value.source}"

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
        return self._before_value

    @property
    def from_value(self) -> SQLGeneralExpression:
        return self._from_value

    @property
    def to_value(self) -> SQLGeneralExpression:
        return self._to_value

    @property
    def source(self) -> str:
        return f"{self.before_value.source} BETWEEN {self.from_value.source} TO {self.to_value.source}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        return self.before_value.get_used_column_list()


class SQLAlisaExpression(SQLBase):
    """别名表达式"""

    def __init__(self, alias_name: str):
        self._alias_name = alias_name

    @property
    def alias_name(self) -> str:
        return self._alias_name

    @property
    def source(self) -> str:
        return f"AS {self.alias_name}"


class SQLConditionExpression(SQLGeneralExpression):
    """条件表达式"""

    def __init__(self,
                 elements: List[Union["SQLConditionExpression", SQLBoolExpression, SQLLogicalOperator]]):
        self._elements = elements

    @property
    def elements(self) -> List[Union["SQLConditionExpression", SQLBoolExpression, SQLLogicalOperator]]:
        return self._elements

    @property
    def source(self) -> "":
        return " ".join(f"({element.source})" if isinstance(element, SQLConditionExpression) else element.source
                        for element in self._elements)

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段列表"""
        result = []
        for element in self.elements:
            result.extend(element.get_used_column_list())
        return result


class SQLJoinExpression(SQLBase, abc.ABC):
    """关联表达式"""


class SQLJoinOnExpression(SQLJoinExpression):
    """ON 关联表达式"""

    def __init__(self, condition: SQLConditionExpression):
        self._condition = condition

    @property
    def condition(self) -> SQLConditionExpression:
        return self._condition

    @property
    def source(self) -> str:
        return f"ON {self._condition.source}"


class SQLJoinUsingExpression(SQLJoinExpression):
    """USING 关联表达式"""

    def __init__(self, using_function: SQLFunctionExpression):
        self._using_function = using_function

    @property
    def using_function(self) -> SQLFunctionExpression:
        return self._using_function

    @property
    def source(self) -> str:
        return f"{self.using_function.source}"


class SQLTableExpression(SQLBase):
    """表表达式"""

    def __init__(self,
                 table: Union[SQLTableNameExpression, SQLSubQueryExpression],
                 alias: Optional[SQLAlisaExpression]):
        self._table = table
        self._alias = alias

    @property
    def table(self) -> Union[SQLTableNameExpression, SQLSubQueryExpression]:
        return self._table

    @property
    def alias(self) -> Optional[SQLAlisaExpression]:
        return self._alias

    @property
    def source(self) -> str:
        if self.alias is not None:
            return f"{self.table.source} {self.alias.source}"
        else:
            return f"{self.table.source}"

    def get_used_table_list(self) -> List[str]:
        return self.table.get_used_table_list()


class SQLColumnExpression(SQLBase):
    """列表达式"""

    def __init__(self,
                 column: SQLGeneralExpression,
                 alias: Optional[SQLAlisaExpression]):
        self._column = column
        self._alias = alias

    @property
    def column(self) -> SQLGeneralExpression:
        return self._column

    @property
    def alias(self) -> Optional[SQLAlisaExpression]:
        return self._alias

    @property
    def source(self) -> str:
        if self.alias is not None:
            return f"{self.column.source} {self.alias.source}"
        else:
            return f"{self.column.source}"

    def get_alias_name(self) -> Optional[str]:
        """获取别名名称"""
        if self.alias is not None:
            return self.alias.alias_name
        return None

    def get_used_column_list(self) -> List[str]:
        """获取语句结果中使用的字段"""
        return self.column.get_used_column_list()


class SQLEqualExpression(SQLBase):
    """等式表达式"""

    def __init__(self, before_value: SQLGeneralExpression, after_value: SQLGeneralExpression):
        self._before_value = before_value
        self._after_value = after_value

    @property
    def before_value(self) -> SQLGeneralExpression:
        return self._before_value

    @property
    def after_value(self) -> SQLGeneralExpression:
        return self._after_value

    @property
    def source(self) -> str:
        return f"{self.before_value.source} = {self.after_value.source}"


class SQLPartitionExpression(SQLBase):
    """分区表达式：PARTITION (<partition_expression>)"""

    def __init__(self, partition_list: List[SQLEqualExpression]):
        self._partition_list = partition_list

    @property
    def partition_list(self) -> List[SQLEqualExpression]:
        return self._partition_list

    @property
    def source(self) -> str:
        partition_list_str = ", ".join(partition.source for partition in self.partition_list)
        return f"PARTITION ({partition_list_str})"


# ------------------------------ 子句层级 ------------------------------


class SQLSelectClause(SQLBase):
    """SELECT 子句"""

    def __init__(self, distinct: bool, columns: List[SQLColumnExpression]):
        self._distinct = distinct
        self._columns = columns

    @property
    def distinct(self) -> bool:
        return self._distinct

    @property
    def columns(self) -> List[SQLColumnExpression]:
        return self._columns

    @property
    def source(self) -> str:
        result = ["SELECT"]
        if self.distinct is True:
            result.append("DISTINCT")
        result.append(",\n".join(column.source for column in self.columns))
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
        result = {}
        for idx, column in enumerate(self.columns):
            result[idx + 1] = column.get_used_column_list()  # 列编号从 1 开始
        return result


class SQLFromClause(SQLBase):
    """FROM 子句"""

    def __init__(self, tables: List[SQLTableExpression]):
        self._tables = tables

    @property
    def tables(self) -> List[SQLTableExpression]:
        return self._tables

    @property
    def source(self) -> str:
        return "FROM " + ", ".join(table.source for table in self.tables)

    def get_used_table_list(self) -> List[str]:
        """获取语句中查询的表名的列表"""
        result = []
        for table in self.tables:
            result.extend(table.get_used_table_list())
        return result


class SQLJoinClause(SQLBase):
    """JOIN 子句"""

    def __init__(self,
                 join_type: SQLEnumJoinType,
                 table: SQLTableExpression,
                 join_rule: Optional[SQLJoinExpression]):
        self._join_type = join_type
        self._table = table
        self._join_rule = join_rule

    @property
    def join_type(self) -> SQLEnumJoinType:
        return self._join_type

    @property
    def table(self) -> SQLTableExpression:
        return self._table

    @property
    def join_rule(self) -> Optional[SQLJoinExpression]:
        return self._join_rule

    @property
    def source(self) -> str:
        if self.join_rule is not None:
            return f"{self.join_type.value} {self.table.source} {self.join_rule.source}"
        else:
            return f"{self.join_type.value} {self.table.source}"

    def get_used_table_list(self) -> List[str]:
        return self.table.get_used_table_list()


class SQLWhereClause(SQLBase):
    """WHERE 子句"""

    def __init__(self, condition: SQLConditionExpression):
        self._condition = condition

    @property
    def condition(self) -> SQLConditionExpression:
        return self._condition

    @property
    def source(self) -> str:
        return f"WHERE {self.condition.source}"

    def get_used_column_list(self) -> List[str]:
        """获取使用的字段名列表"""
        return self.condition.get_used_column_list()


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
        return self._columns

    @property
    def with_rollup(self) -> bool:
        return self._with_rollup

    @property
    def source(self) -> str:
        if self.with_rollup:
            return "GROUP BY " + ", ".join(column.source for column in self.columns) + " WITH ROLLUP"
        else:
            return "GROUP BY " + ", ".join(column.source for column in self.columns)

    def get_used_column_list(self) -> List[Union[str, int]]:
        """返回字段名和列编号"""
        result = []
        for column in self.columns:
            if isinstance(column, SQLLiteralExpression):
                result.append(column.literal.value)  # 列编号
            else:
                result.extend(column.get_used_column_list())
        return result


class SQLGroupingSetsGroupByClause(SQLGroupByClause):
    """使用 GROUPING SETS 语法的 GROUP BY 子句"""

    def __init__(self, grouping_list: List[List[SQLGeneralExpression]]):
        self._grouping_list = grouping_list

    @property
    def grouping_list(self) -> List[List[SQLGeneralExpression]]:
        return self._grouping_list

    @property
    def source(self) -> str:
        grouping_str_list = []
        for grouping in self.grouping_list:
            if len(grouping) > 1:
                grouping_str_list.append("(" + ", ".join(column.source for column in grouping) + ")")
            else:
                grouping_str_list.append(grouping[0].source)
        return "GROUP BY GROUPING SETS (" + ", ".join(grouping_str_list) + ")"

    def get_used_column_list(self) -> List[Union[str, int]]:
        """返回字段名和列编号"""
        result = []
        for grouping in self.grouping_list:
            for column in grouping:
                if isinstance(column, SQLLiteralExpression):
                    result.append(column.literal.value)  # 列编号
                else:
                    result.extend(column.get_used_column_list())
        return result


class SQLHavingClause(SQLBase):
    """HAVING 子句"""

    def __init__(self, condition: SQLConditionExpression):
        self._condition = condition

    @property
    def condition(self) -> SQLConditionExpression:
        return self._condition

    @property
    def source(self) -> str:
        return f"HAVING {self.condition.source}"

    def get_used_column_list(self) -> List[str]:
        return self.condition.get_used_column_list()


class SQLOrderByClause(SQLBase):
    """ORDER BY 子句"""

    def __init__(self, columns: List[Tuple[SQLGeneralExpression, SQLEnumOrderType]]):
        self._columns = columns

    @property
    def columns(self) -> List[Tuple[SQLGeneralExpression, SQLEnumOrderType]]:
        return self._columns

    @property
    def source(self) -> str:
        result = []
        for column, order_type in self.columns:
            if order_type == SQLEnumOrderType.ASC:
                result.append(f"{column.source}")
            else:
                result.append(f"{column.source} DESC")
        return "ORDER BY " + ", ".join(result)

    def get_used_column_list(self) -> List[Union[str, int]]:
        """返回字段名和列编号"""
        result = []
        for column, order_type in self.columns:
            if isinstance(column, SQLLiteralExpression):
                result.append(column.literal.value)  # 列编号
            else:
                result.extend(column.get_used_column_list())
        return result


class SQLLimitClause(SQLBase):
    """LIMIT 子句"""

    def __init__(self, limit: int, offset: int):
        self._limit = limit
        self._offset = offset

    @property
    def limit(self) -> int:
        return self._limit

    @property
    def offset(self) -> int:
        return self._offset

    @property
    def source(self) -> str:
        return f"LIMIT {self.offset}, {self.limit}"


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
        return self._tables

    @property
    def source(self) -> str:
        if len(self.tables) > 0:
            table_str = ", \n".join(f"{table_name}({table_statement.source})"
                                    for table_name, table_statement in self.tables)
            return f"WITH {table_str}"
        else:
            return ""

    def is_empty(self):
        return len(self.tables) == 0


# ------------------------------ 语句层级 ------------------------------


class SQLStatement(SQLBase, abc.ABC):
    """表达式的抽象基类"""

    def __init__(self, with_clause: Optional[SQLWithClause]):
        self._with_clause = with_clause

    @property
    def with_clause(self) -> Optional[SQLWithClause]:
        return self._with_clause


class SQLSelectStatement(SQLStatement, abc.ABC):
    """SELECT 表达式"""

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
                 join_clauses: List[SQLJoinClause] = None,
                 where_clause: Optional[SQLWhereClause] = None,
                 group_by_clause: Optional[SQLGroupByClause] = None,
                 having_clause: Optional[SQLHavingClause] = None,
                 order_by_clause: Optional[SQLOrderByClause] = None,
                 limit_clause: Optional[SQLLimitClause] = None):
        super().__init__(with_clause)
        self._select_clause = select_clause
        self._from_clause = from_clause
        self._join_clauses = join_clauses
        self._where_clause = where_clause
        self._group_by_clause = group_by_clause
        self._having_clause = having_clause
        self._order_by_clause = order_by_clause
        self._limit_clause = limit_clause

    @property
    def select_clause(self) -> SQLSelectClause:
        return self._select_clause

    @property
    def from_clause(self) -> Optional[SQLFromClause]:
        return self._from_clause

    @property
    def join_clauses(self) -> List[SQLJoinClause]:
        return self._join_clauses

    @property
    def where_clause(self) -> Optional[SQLWhereClause]:
        return self._where_clause

    @property
    def group_by_clause(self) -> Optional[SQLGroupByClause]:
        return self._group_by_clause

    @property
    def having_clause(self) -> Optional[SQLHavingClause]:
        return self._having_clause

    @property
    def order_by_clause(self) -> Optional[SQLOrderByClause]:
        return self._order_by_clause

    @property
    def limit_clause(self) -> Optional[SQLLimitClause]:
        return self._limit_clause

    @property
    def source(self) -> str:
        with_clause_str = self.with_clause.source + "\n" if not self.with_clause.is_empty() else ""
        result = [self.select_clause.source]
        for clause in [self.from_clause, *self.join_clauses, self.where_clause, self.group_by_clause,
                       self.having_clause,
                       self.order_by_clause, self.limit_clause]:
            if clause is not None:
                result.append(clause.source)
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
        for join_clause in self.join_clauses:
            result.extend(join_clause.get_used_table_list())
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
    """复合查询语句，使用 UNION、EXCEPT、INTERSECT 进行组合

    TODO 移除表达式中直接引用枚举类的行为，外面必须套一层表达式
    """

    def __init__(self,
                 with_clause: Optional[SQLWithClause],
                 elements: List[Union[SQLUnionKeyword, SQLSingleSelectStatement]]):
        super().__init__(with_clause)
        self._elements = elements

    @property
    def elements(self) -> List[Union[SQLUnionKeyword, SQLSingleSelectStatement]]:
        return self._elements

    @property
    def source(self) -> str:
        with_clause_str = self.with_clause.source + "\n" if not self.with_clause.is_empty() else ""
        return with_clause_str + "\n".join(element.source for element in self.elements)

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
        result = []
        for element in self.elements:
            if isinstance(element, SQLSingleSelectStatement):
                result.extend(element.get_order_by_used_column_list())
        return ordered_distinct(result)


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
                 has_table_keyword: bool,
                 table_name: SQLTableNameExpression,
                 partition: Optional[SQLPartitionExpression],
                 columns: Optional[List[SQLColumnNameExpression]]):
        super().__init__(with_clause)
        self._insert_type = insert_type
        self._has_table_keyword = has_table_keyword
        self._table_name = table_name
        self._partition = partition
        self._columns = columns

    @property
    def insert_type(self) -> SQLInsertType:
        return self._insert_type

    @property
    def has_table_keyword(self) -> bool:
        return self._has_table_keyword

    @property
    def table_name(self) -> SQLTableNameExpression:
        return self._table_name

    @property
    def partition(self) -> SQLPartitionExpression:
        return self._partition

    @property
    def columns(self) -> Optional[List[SQLColumnExpression]]:
        return self._columns

    def _insert_str(self) -> str:
        """INSERT语句的前半部分"""
        insert_type_str = " ".join(self.insert_type.value)
        table_keyword_str = "TABLE " if self.has_table_keyword else ""
        partition_str = self.partition.source + " " if self.partition is not None else ""
        if self.columns is not None:
            columns_str = "(" + ", ".join(column.source for column in self.columns) + ") "
        else:
            columns_str = ""
        return f"{insert_type_str} {table_keyword_str}{self.table_name.source} {partition_str}{columns_str}"


class SQLInsertValuesStatement(SQLInsertStatement):
    """INSERT ... VALUES ... 语句"""

    def __init__(self,
                 with_clause: Optional[SQLWithClause],
                 insert_type: SQLInsertType,
                 has_table_keyword: bool,
                 table_name: SQLTableNameExpression,
                 partition: Optional[SQLPartitionExpression],
                 columns: Optional[List[SQLColumnNameExpression]],
                 values: List[SQLValueExpression]):
        super().__init__(with_clause, insert_type, has_table_keyword, table_name, partition, columns)
        self._values = values

    @property
    def values(self) -> List[SQLValueExpression]:
        return self._values

    @property
    def source(self) -> str:
        values_str = ", ".join(value.source for value in self.values)
        return f"{self._insert_str()}VALUES {values_str}"


class SQLInsertSelectStatement(SQLInsertStatement):
    """INSERT ... SELECT ... 语句"""

    def __init__(self,
                 with_clause: Optional[SQLWithClause],
                 insert_type: SQLInsertType,
                 has_table_keyword: bool,
                 table_name: SQLTableNameExpression,
                 partition: Optional[SQLPartitionExpression],
                 columns: Optional[List[SQLColumnNameExpression]],
                 select_statement: SQLSelectStatement):
        super().__init__(with_clause, insert_type, has_table_keyword, table_name, partition, columns)
        self._select_statement = select_statement

    @property
    def select_statement(self) -> SQLSelectStatement:
        return self._select_statement

    @property
    def source(self) -> str:
        return f"{self._insert_str()} {self.select_statement.source}"


# ---------- 仅在部分 SQL 语言中使用的节点 ----------

class SQLMod(SQLComputeOperator):
    """取模运算符（仅 SQL Server 中适用）"""

    @property
    def source(self) -> str:
        return "%"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"


# ---------- DDL 中使用的节点 ----------

class DDLColumnTypeExpression(SQLBase):
    """字段类型表达式"""

    def __init__(self, name: str, params: List[SQLGeneralExpression]):
        self._name = name  # 函数名称
        self._params = params  # 函数参数

    @property
    def name(self) -> str:
        return self._name

    @property
    def params(self) -> List[SQLGeneralExpression]:
        return self._params

    @property
    def source(self) -> str:
        if len(self.params) > 0:
            type_params = "(" + ", ".join([param.source for param in self.params]) + ")"
            return f"{self.name}{type_params}"
        else:
            return self.name


class DDLForeignKeyExpression(SQLBase):
    """外键表达式"""

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

    @property
    def source(self) -> str:
        slave_columns_str = ", ".join([f"{column}" for column in self.slave_columns])
        master_columns_str = ", ".join([f"{column}" for column in self.master_columns])
        return (f"CONSTRAINT {self.constraint_name} FOREIGN KEY({slave_columns_str}) "
                f"REFERENCES {self.master_table_name}({master_columns_str})")


class DDLIndexExpression(SQLBase, abc.ABC):
    """声明索引表达式"""

    def __init__(self, name: Optional[str], columns: List[str]):
        self._name = name
        self._columns = columns

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def columns(self) -> List[str]:
        return self._columns


class DDLPrimaryIndexExpression(DDLIndexExpression):
    """主键索引声明表达式"""

    def __init__(self, columns: List[str]):
        super().__init__(None, columns)

    @property
    def source(self) -> str:
        columns_str = ", ".join([f"{column}" for column in self.columns])
        return f"PRIMARY KEY ({columns_str})" if self.columns is not None else ""


class DDLUniqueIndexExpression(DDLIndexExpression):
    @property
    def source(self) -> str:
        columns_str = ", ".join([f"{column}" for column in self.columns])
        return f"UNIQUE KEY {self.name} ({columns_str})"


class DDLNormalIndexExpression(DDLIndexExpression):
    @property
    def source(self) -> str:
        columns_str = ", ".join([f"{column}" for column in self.columns])
        return f"KEY {self.name} ({columns_str})"


class DDLFulltextIndexExpression(DDLIndexExpression):
    @property
    def source(self) -> str:
        columns_str = ", ".join([f"{column}" for column in self.columns])
        return f"FULLTEXT KEY {self.name} ({columns_str})"


class DDLColumnExpression(SQLBase):
    """【DDL】建表语句中的字段信息"""

    def __init__(self,
                 column_name: str,
                 column_type: DDLColumnTypeExpression,
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
        return f"`{self._column_name}`"

    @property
    def column_name_without_quote(self) -> str:
        return self._column_name

    @property
    def column_type(self) -> DDLColumnTypeExpression:
        return self._column_type

    @property
    def comment(self) -> Optional[str]:
        return self._comment

    @property
    def is_unsigned(self) -> bool:
        return self._is_unsigned

    @property
    def is_zerofill(self) -> bool:
        return self._is_zerofill

    @property
    def character_set(self) -> Optional[str]:
        return self._character_set

    @property
    def collate(self) -> Optional[str]:
        return self._collate

    @property
    def is_allow_null(self) -> bool:
        return self._is_allow_null

    @property
    def is_not_null(self) -> bool:
        return self._is_not_null

    @property
    def is_auto_increment(self) -> bool:
        return self._is_auto_increment

    @property
    def default(self) -> Optional[SQLGeneralExpression]:
        return self._default

    @property
    def on_update(self) -> Optional[SQLGeneralExpression]:
        return self._on_update

    @property
    def source(self) -> str:
        res = f"{self._column_name} {self.column_type.source}"
        if self.is_unsigned is True:
            res += " UNSIGNED"
        if self.is_zerofill is True:
            res += " ZEROFILL"
        if self.character_set is not None:
            res += f" CHARACTER SET {self.character_set}"
        if self.collate is not None:
            res += f" COLLATE {self.collate}"
        if self.is_allow_null is True:
            res += " NULL"
        if self.is_not_null is True:
            res += " NOT NULL"
        if self.is_auto_increment is True:
            res += " AUTO_INCREMENT"
        if self.default is not None:
            res += f" DEFAULT {self.default.source}"
        if self.on_update is not None:
            res += f" ON UPDATE {self.on_update.source}"
        if self.comment is not None:
            res += f" COMMENT {self.comment}"
        return res


class DDLCreateTableStatement(SQLBase):
    """【DDL】CREATE TABLE 语句"""

    def __init__(self,
                 schema_name: Optional[str] = None,
                 table_name: Optional[str] = None,
                 comment: Optional[str] = None,
                 if_not_exists: bool = False,
                 columns: Optional[List[DDLColumnExpression]] = None,
                 primary_key: Optional[DDLPrimaryIndexExpression] = None,
                 unique_key: Optional[List[DDLUniqueIndexExpression]] = None,
                 key: Optional[List[DDLNormalIndexExpression]] = None,
                 fulltext_key: Optional[List[DDLFulltextIndexExpression]] = None,
                 foreign_key: List[DDLForeignKeyExpression] = None,
                 engine: Optional[str] = None,
                 auto_increment: Optional[int] = None,
                 default_charset: Optional[str] = None,
                 collate: Optional[str] = None,
                 row_format: Optional[str] = None,
                 states_persistent: Optional[str] = None
                 ):
        self._schema_name = schema_name
        self._table_name = table_name
        self._comment = comment

    @property
    def schema_name(self):
        return self._schema_name

    def set_schema_name(self, schema_name: str):
        self._schema_name = schema_name

    @property
    def table_name(self):
        return self._table_name

    def set_table_name(self, table_name: str):
        self._table_name = table_name

    @property
    def comment(self):
        return self._comment

    def set_comment(self, comment: str):
        self._comment = comment
