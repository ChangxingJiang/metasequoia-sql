import abc
from typing import Optional, List, Tuple, Union

from metasequoia_sql.objects.common import SQLBase


# ------------------------------ 元素层级 ------------------------------


class SQLPlus(SQLBase):
    """加法运算符"""

    @property
    def source(self) -> str:
        return "+"


class SQLSubtract(SQLBase):
    """减法运算符"""

    @property
    def source(self) -> str:
        return "-"


class SQLMultiple(SQLBase):
    """乘法运算符"""

    @property
    def source(self) -> str:
        return "*"


class SQLDivide(SQLBase):
    """除法运算符"""

    @property
    def source(self) -> str:
        return "/"


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


# ------------------------------ 表达式层级 ------------------------------


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
        params_str = ", ".join([str(param) for param in self._params])
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
                 elements: List[Union[SQLGeneralExpression, SQLPlus, SQLSubtract, SQLMultiple, SQLDivide]]):
        self._elements = elements

    @property
    def elements(self) -> List[Union[SQLGeneralExpression, SQLPlus, SQLSubtract, SQLMultiple, SQLDivide]]:
        return self._elements

    @property
    def source(self) -> str:
        return " ".join([str(element) for element in self.elements])


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
