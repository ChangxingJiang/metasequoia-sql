import abc
import enum
from typing import Optional, List, Tuple, Union

from metasequoia_sql.objects.common import SQLBase


# ------------------------------ 元素层级 ------------------------------


class SQLJoinType(enum.Enum):
    """SQL 关联类型"""
    JOIN = "JOIN"  # 内连接
    INNER_JOIN = "INNER JOIN"  # 内连接
    LEFT_JOIN = "LEFT JOIN"  # 左外连接
    LEFT_OUTER_JOIN = "LEFT OUTER JOIN"  # 左外连接
    RIGHT_JOIN = "RIGHT JOIN"  # 右外连接
    RIGHT_OUTER_JOIN = "RIGHT OUTER JOIN"  # 右外连接
    FULL_JOIN = "FULL JOIN"  # 全外连接
    FULL_OUTER_JOIN = "FULL OUTER JOIN"  # 全外连接
    CROSS_JOIN = "CROSS JOIN"  # 交叉连接


class SQLComputeOperator(SQLBase, abc.ABC):
    """计算运算符"""


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


# ------------------------------ 表达式层级（一般表达式） ------------------------------


class SQLGeneralExpression(SQLBase, abc.ABC):
    """一般表达式"""


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
        if self._table is not None:
            return f"{self._table}.{self._column}"
        else:
            return f"{self._column}"


class SQLFunctionExpression(SQLGeneralExpression):
    """函数表达式"""

    def __init__(self,
                 function_name: str,
                 params: List[SQLGeneralExpression]):
        self._function_name = function_name
        self._params = params

    @property
    def function_name(self) -> str:
        return self._function_name

    @property
    def params(self) -> List[SQLGeneralExpression]:
        return self._params

    @property
    def source(self) -> str:
        params_str = ", ".join(str(param) for param in self._params)
        return f"{self._function_name}({params_str})"


class SQLCaseExpression(SQLGeneralExpression):
    """CASE 表达式"""

    def __init__(self,
                 cases: List[Tuple[SQLGeneralExpression, SQLGeneralExpression]],
                 else_value: SQLGeneralExpression):
        self._cases = cases
        self._else_value = else_value

    @property
    def cases(self) -> List[Tuple[SQLGeneralExpression, SQLGeneralExpression]]:
        return self._cases

    @property
    def else_value(self) -> SQLGeneralExpression:
        return self._else_value

    @property
    def source(self) -> str:
        result = ["CASE"]
        for when, then in self.cases:
            result.append(f"    WHEN {when} THEN {then}")
        result.append(f"    ELSE {self.else_value}")
        result.append("END")
        return "\n".join(result)


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
        result = f"{self.window_function} OVER ("
        if self.partition_by is not None:
            result += f"PARTITION BY {self.partition_by}"
        if self.order_by is not None:
            result += f"ORDER BY {self.order_by}"
        result += ")"
        return result


class SQLComputeSentence(SQLGeneralExpression):
    """计算表达式"""

    def __init__(self,
                 elements: List[Union[SQLGeneralExpression, SQLComputeOperator]]):
        self._elements = elements

    @property
    def elements(self) -> List[Union[SQLGeneralExpression, SQLComputeOperator]]:
        return self._elements

    @property
    def source(self) -> str:
        return " ".join(str(element) for element in self.elements)


class SQLLiteralExpression(SQLGeneralExpression):
    """字面值表达式"""

    def __init__(self,
                 literal: SQLLiteral):
        self._literal = literal

    @property
    def literal(self) -> SQLLiteral:
        return self._literal

    @property
    def source(self) -> str:
        return self.literal.source


# ------------------------------ 表达式层级（专有表达式） ------------------------------


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


class SQLBoolExpression(SQLBase, abc.ABC):
    """布尔值表达式"""


class SQLBoolCompareExpression(SQLBoolExpression):
    """比较运算符关联表达式"""

    def __init__(self,
                 operator: SQLCompareOperator,
                 before: SQLGeneralExpression,
                 after: SQLGeneralExpression):
        self._operator = operator
        self._before = before
        self._after = after

    @property
    def operator(self) -> SQLCompareOperator:
        return self._operator

    @property
    def before(self) -> SQLGeneralExpression:
        return self._before

    @property
    def after(self) -> SQLGeneralExpression:
        return self._after

    @property
    def source(self) -> str:
        return f"{self.before} {self.operator} {self.after}"


class SQLBoolBetweenExpression(SQLBoolExpression):
    """BETWEEN 关联表达式"""

    def __init__(self, from_value: SQLGeneralExpression, to_value: SQLGeneralExpression):
        self._from_value = from_value
        self._to_value = to_value

    @property
    def from_value(self) -> SQLGeneralExpression:
        return self._from_value

    @property
    def to_value(self) -> SQLGeneralExpression:
        return self._to_value

    @property
    def source(self) -> str:
        return f"BETWEEN {self.from_value} TO {self.to_value}"


class SQLAlisaExpression(SQLBase):
    """别名表达式"""

    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def source(self) -> str:
        return f"{self.name}"


class SQLConditionExpression(SQLBase):
    """条件表达式"""

    def __init__(self,
                 elements: List[Union["SQLConditionExpression", SQLBoolExpression, SQLLogicalOperator]]):
        self._elements = elements

    @property
    def elements(self) -> List[Union["SQLConditionExpression", SQLBoolExpression, SQLLogicalOperator]]:
        return self._elements

    @property
    def source(self) -> "":
        return " ".join(
            f"({element})" if isinstance(element, SQLConditionExpression) else f"{element}"
            for element in self._elements
        )


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
        return f"ON {self._condition}"


class SQLJoinUsingExpression(SQLJoinExpression):
    """USING 关联表达式"""

    def __init__(self, using_function: SQLFunctionExpression):
        self._using_function = using_function

    @property
    def using_function(self) -> SQLFunctionExpression:
        return self._using_function

    @property
    def source(self) -> str:
        return f"{self.using_function}"


class SQLWildcardExpression(SQLBase):
    """通配符表达式"""

    @property
    def source(self) -> str:
        return "*"


class SQLTableExpression(SQLBase):
    """表表达式"""

    def __init__(self,
                 table: SQLGeneralExpression,
                 alias: Optional[SQLAlisaExpression]):
        self._table = table
        self._alias = alias

    @property
    def table(self) -> SQLGeneralExpression:
        return self._table

    @property
    def alias(self) -> Optional[SQLAlisaExpression]:
        return self._alias

    @property
    def source(self) -> str:
        if self.alias is not None:
            return f"{self.table} AS {self.table}"
        else:
            return f"{self.table}"


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
            return f"{self.column} AS {self.column}"
        else:
            return f"{self.column}"


# ------------------------------ 子句层级 ------------------------------


class SQLSelectClause(SQLBase):
    """SELECT 子句"""

    def __init__(self,
                 distinct: bool,
                 columns: List[Union[SQLColumnExpression, SQLWildcardExpression]]):
        self._distinct = distinct
        self._columns = columns

    @property
    def distinct(self) -> bool:
        return self._distinct

    @property
    def columns(self) -> List[Union[SQLColumnExpression, SQLWildcardExpression]]:
        return self._columns

    @property
    def source(self) -> str:
        result = ["SELECT"]
        if self.distinct is True:
            result.append("DISTINCT")
        result.append(",\n".join(str(column) for column in self.columns))
        return " ".join(result)


class SQLFromClause(SQLBase):
    """FROM 子句"""

    def __init__(self, tables: List[SQLTableExpression]):
        self._tables = tables

    @property
    def tables(self) -> List[SQLTableExpression]:
        return self._tables

    @property
    def source(self) -> str:
        return "FROM " + ", ".join(str(table) for table in self.tables)


class SQLJoinClause(SQLBase):
    """JOIN 子句"""

    def __init__(self,
                 join_type: SQLJoinType,
                 table: SQLTableExpression,
                 join_rule: SQLJoinExpression):
        self._join_type = join_type
        self._table = table
        self._join_rule = join_rule

    @property
    def join_type(self) -> SQLJoinType:
        return self._join_type

    @property
    def table(self) -> SQLTableExpression:
        return self._table

    @property
    def join_rule(self) -> SQLJoinExpression:
        return self._join_rule

    @property
    def source(self) -> str:
        return f"{self.join_type.value} {self.table} {self.join_rule}"


class SQLWhereClause(SQLBase):
    """WHERE 子句"""

    def __init__(self, condition: SQLConditionExpression):
        self._condition = condition

    @property
    def condition(self) -> SQLConditionExpression:
        return self._condition

    @property
    def source(self) -> str:
        return f"WHERE {self._condition}"


class SQLGroupByClause(SQLBase):
    """GROUP BY 子句"""

    def __init__(self, columns: List[SQLGeneralExpression]):
        self._columns = columns

    @property
    def columns(self) -> List[SQLGeneralExpression]:
        return self._columns

    @property
    def source(self) -> str:
        return "GROUP BY " + ", ".join(str(column) for column in self.columns)


class SQLHavingClause(SQLBase):
    """HAVING 子句"""

    def __init__(self, condition: SQLConditionExpression):
        self._condition = condition

    @property
    def condition(self) -> SQLConditionExpression:
        return self._condition

    @property
    def source(self) -> str:
        return f"HAVING {self.condition}"


class SQLOrderByClause(SQLBase):
    """ORDER BY 子句"""

    def __init__(self, columns: List[SQLGeneralExpression]):
        self._columns = columns

    @property
    def columns(self) -> List[SQLGeneralExpression]:
        return self._columns

    @property
    def source(self) -> str:
        return "ORDER BY " + ", ".join(str(column) for column in self.columns)


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


# ------------------------------ 语句层级 ------------------------------

class SQLSelectStatement(SQLBase):
    def __init__(self,
                 select_clause: SQLSelectClause,
                 from_clause: Optional[SQLFromClause] = None,
                 join_clause: Optional[SQLJoinClause] = None,
                 where_clause: Optional[SQLWhereClause] = None,
                 group_by_clause: Optional[SQLGroupByClause] = None,
                 having_clause: Optional[SQLHavingClause] = None,
                 order_by_clause: Optional[SQLOrderByClause] = None,
                 limit_clause: Optional[SQLLimitClause] = None
                 ):
        self._select_clause = select_clause
        self._from_clause = from_clause
        self._join_clause = join_clause
        self._where_clause = where_clause
        self._group_by_clause = group_by_clause
        self._having_clause = having_clause
        self._order_by_clause = order_by_clause
        self._limit_clause = limit_clause

    @property
    def select_clause(self) -> SQLSelectClause:
        return self._select_clause

    @property
    def from_clause(self) -> SQLFromClause:
        return self._from_clause

    @property
    def join_clause(self) -> SQLJoinClause:
        return self._join_clause

    @property
    def where_clause(self) -> SQLWhereClause:
        return self._where_clause

    @property
    def group_by_clause(self) -> SQLGroupByClause:
        return self._group_by_clause

    @property
    def having_clause(self) -> SQLHavingClause:
        return self._having_clause

    @property
    def order_by_clause(self) -> SQLOrderByClause:
        return self._order_by_clause

    @property
    def limit_clause(self) -> SQLLimitClause:
        return self._limit_clause

    @property
    def source(self) -> str:
        result = [str(self.select_clause)]
        for clause in [self.from_clause, self.join_clause, self.where_clause, self.group_by_clause, self.having_clause,
                       self.order_by_clause, self.limit_clause]:
            if clause is not None:
                result.append(str(clause))
        return "\n".join(result)
