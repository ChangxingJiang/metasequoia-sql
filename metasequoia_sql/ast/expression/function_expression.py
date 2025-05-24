"""
普通函数表达式（function expression）
"""

from decimal import Decimal
from enum import IntEnum
from typing import List, Optional, TYPE_CHECKING, Union

from metasequoia_sql.ast.base import Expression

if TYPE_CHECKING:
    from metasequoia_sql.ast.basic.charset_name import Charset
    from metasequoia_sql.ast.phrase.field_type import CastType
    from metasequoia_sql.ast.phrase.json_table_option import JsonOnEmptyOnError
    from metasequoia_sql.ast.basic import TimeUnitEnum
    from metasequoia_sql.ast.phrase.time_interval import TimeInterval

    FunctionParam = Union[Expression, TimeInterval, TimeUnitEnum, "DateTimeType"]

__all__ = [
    "FunctionExpression",
    "FunctionChar",
    "FunctionJsonValue",
    "TrimTypeEnum",
    "FunctionTrim",
    "FunctionExtract",
    "DateTimeTypeEnum",
    "FunctionGetFormat",
    "FunctionPosition",
    "FunctionSubstring",
    "FunctionWeightString",
    "FunctionCast",
    "FunctionCastAtTimeZone",
    "FunctionConvert",
    "FunctionConvertCharset",
]


class FunctionExpression(Expression):
    """通用函数表达式

    function_name ( ... )
    schema_name . function_name ( ... )
    """

    __slots__ = ["_schema_name", "_function_name", "_param_list"]

    def __init__(self, function_name: str, param_list: List["FunctionParam"], schema_name: Optional[str] = None):
        self._schema_name = schema_name
        self._function_name = function_name
        self._param_list = param_list

    @staticmethod
    def create_by_1_param(function_name: str, param_1: "FunctionParam") -> "FunctionExpression":
        return FunctionExpression(function_name=function_name, param_list=[param_1])

    @staticmethod
    def create_by_2_param(function_name: str, param_1: "FunctionParam",
                          param_2: "FunctionParam") -> "FunctionExpression":
        return FunctionExpression(function_name=function_name, param_list=[param_1, param_2])

    @property
    def function_name(self) -> str:
        return self._function_name

    @property
    def param_list(self) -> List["FunctionParam"]:
        return self._param_list


class FunctionChar(FunctionExpression):
    """CHAR 函数"""

    __slots__ = ["_charset_name"]

    def __init__(self, function_name: str, param_list: List[Expression], charset_name: Optional["Charset"]):
        super().__init__(function_name, param_list)
        self._charset_name = charset_name

    @staticmethod
    def create(param_list: List[Expression], charset_name: Optional["Charset"]) -> "FunctionChar":
        return FunctionChar(function_name="char", param_list=param_list, charset_name=charset_name)

    @property
    def charset_name(self) -> Optional["Charset"]:
        return self._charset_name


class FunctionJsonValue(FunctionExpression):
    """JSON_VALUE 函数"""

    __slots__ = ["_returning_type", "_json_on_empty_on_error"]

    def __init__(self, function_name: str, param_list: List[Expression], returning_type: "CastType",
                 json_on_empty_on_error: "JsonOnEmptyOnError"):
        super().__init__(function_name, param_list)
        self._returning_type = returning_type
        self._json_on_empty_on_error = json_on_empty_on_error

    @staticmethod
    def create(param_list: List[Expression],
               returning_type: "CastType",
               json_on_empty_on_error: "JsonOnEmptyOnError"
               ) -> "FunctionJsonValue":
        return FunctionJsonValue(
            function_name="json_value",
            param_list=param_list,
            returning_type=returning_type,
            json_on_empty_on_error=json_on_empty_on_error
        )

    @property
    def returning_type(self) -> "CastType":
        return self._returning_type

    @property
    def json_on_empty_on_error(self) -> "JsonOnEmptyOnError":
        return self._json_on_empty_on_error


class TrimTypeEnum(IntEnum):
    """TRIM 函数的参数类型"""

    DEFAULT = 1  # trim ( expr ) 或 trim ( expr FROM expr )
    LEADING = 2  # trim ( LEADING expr FROM expr ) 或 trim ( LEADING FROM expr )
    TRAILING = 3  # trim ( TRAILING expr FROM expr ) 或 trim ( TRAILING FROM expr )
    BOTH = 4  # trim ( BOTH expr FROM expr ) 或 trim ( BOTH FROM expr )


class FunctionTrim(FunctionExpression):
    """TRIM 函数"""

    __slots__ = ["_trim_type"]

    def __init__(self, function_name: str, param_list: List[Expression], trim_type: TrimTypeEnum):
        super().__init__(function_name, param_list)
        self._trim_type = trim_type

    @staticmethod
    def create_as_default(chars_to_remove: Optional[Expression], source_string: Expression) -> "FunctionTrim":
        return FunctionTrim(function_name="trim", param_list=[chars_to_remove, source_string],
                            trim_type=TrimTypeEnum.DEFAULT)

    @staticmethod
    def create_as_leading(chars_to_remove: Optional[Expression], source_string: Expression) -> "FunctionTrim":
        return FunctionTrim(function_name="trim", param_list=[chars_to_remove, source_string],
                            trim_type=TrimTypeEnum.LEADING)

    @staticmethod
    def create_as_trailing(chars_to_remove: Optional[Expression], source_string: Expression) -> "FunctionTrim":
        return FunctionTrim(function_name="trim", param_list=[chars_to_remove, source_string],
                            trim_type=TrimTypeEnum.TRAILING)

    @staticmethod
    def create_as_both(chars_to_remove: Optional[Expression], source_string: Expression) -> "FunctionTrim":
        return FunctionTrim(function_name="trim", param_list=[chars_to_remove, source_string],
                            trim_type=TrimTypeEnum.BOTH)

    @property
    def trim_type(self) -> TrimTypeEnum:
        return self._trim_type

    @property
    def chars_to_remove(self) -> Optional[Expression]:
        return self.param_list[0]

    @property
    def source_string(self) -> Expression:
        return self.param_list[1]


class FunctionExtract(FunctionExpression):
    """EXTRACT 函数"""

    __slots__ = ["_time_unit"]

    def __init__(self, function_name: str, param_list: List[Expression], time_unit: "TimeUnitEnum"):
        super().__init__(function_name, param_list)
        self._time_unit = time_unit

    @staticmethod
    def create(time_unit: "TimeUnitEnum", source_expression: Expression) -> "FunctionExtract":
        return FunctionExtract(function_name="extract", param_list=[source_expression], time_unit=time_unit)

    @property
    def time_unit(self) -> "TimeUnitEnum":
        return self._time_unit

    @property
    def source_expression(self) -> Expression:
        return self.param_list[0]


class DateTimeTypeEnum(IntEnum):
    """时间类型（`DATE`、`TIME` 或者 `DATETIME`）"""

    DATE = 1  # DATE
    TIME = 2  # TIME
    TIMESTAMP = 3  # TIMESTAMP
    DATETIME = 4  # DATETIME


class FunctionGetFormat(FunctionExpression):
    """GET_FORMAT 函数"""

    @staticmethod
    def create(date_time_type: DateTimeTypeEnum, format_type: Expression) -> "FunctionGetFormat":
        return FunctionGetFormat(function_name="get_format", param_list=[date_time_type, format_type])

    @property
    def date_time_type(self) -> DateTimeTypeEnum:
        return self.param_list[0]

    @property
    def format_type(self) -> Expression:
        return self.param_list[1]


class FunctionPosition(FunctionExpression):
    """POSITION 函数：

    POSITION ( sub_string IN string )
    """

    @staticmethod
    def create(sub_string: Expression, string: Expression) -> "FunctionPosition":
        return FunctionPosition(function_name="position", param_list=[sub_string, string])

    @property
    def sub_string(self) -> Expression:
        return self.param_list[0]

    @property
    def string(self) -> Expression:
        return self.param_list[1]


class FunctionSubstring(FunctionExpression):
    """SUBSTRING 函数：

    SUBSTRING ( string , pos , length )
    SUBSTRING ( string , pos )
    SUBSTRING ( string FROM pos FOR length )
    SUBSTRING ( string FROM pos )
    """

    @staticmethod
    def create(string: Expression, pos: Expression, length: Optional[Expression]) -> "FunctionSubstring":
        return FunctionSubstring(function_name="substring", param_list=[string, pos, length])

    @property
    def string(self) -> Expression:
        return self.param_list[0]

    @property
    def pos(self) -> Expression:
        return self.param_list[1]

    @property
    def length(self) -> Optional[Expression]:
        return self.param_list[2]


class FunctionWeightString(FunctionExpression):
    """WEIGHT_STRING 函数"""

    __slots__ = ["_binary_flag"]

    def __init__(self, function_name: str, param_list: List["FunctionParam"], binary_flag: bool):
        super().__init__(function_name, param_list)
        self._binary_flag = binary_flag

    @staticmethod
    def create(param1: Expression,
               param2: Optional[Expression],
               param3: Optional[Expression],
               param4: Optional[Expression],
               binary_flag: bool) -> "FunctionWeightString":
        return FunctionWeightString(
            function_name="weight_string",
            param_list=[param1, param2, param3, param4],
            binary_flag=binary_flag
        )

    @property
    def param1(self) -> Expression:
        return self.param_list[0]

    @property
    def param2(self) -> Optional[Expression]:
        return self.param_list[1]

    @property
    def param3(self) -> Optional[Expression]:
        return self.param_list[2]

    @property
    def param4(self) -> Optional[Expression]:
        return self.param_list[3]

    @property
    def binary_flag(self) -> bool:
        return self._binary_flag


class FunctionCast(Expression):
    """CAST 函数的第一种形式

    CAST ( expression AS cast_type opt_array_cast )
    CAST ( expression AT LOCAL AS cast_type opt_array_cast )
    """

    __slots__ = ["_expression", "_cast_type", "_at_local", "_is_array_cast"]

    def __init__(self, expression: Expression, cast_type: "CastType", at_local: bool, is_array_cast: bool):
        self._expression = expression
        self._cast_type = cast_type
        self._at_local = at_local
        self._is_array_cast = is_array_cast

    @property
    def expression(self) -> Expression:
        return self._expression

    @property
    def cast_type(self) -> "CastType":
        return self._cast_type

    @property
    def at_local(self) -> bool:
        return self._at_local

    @property
    def is_array_cast(self) -> bool:
        return self._is_array_cast


class FunctionCastAtTimeZone(Expression):
    """CAST 函数的第二种形式

    CAST ( expression AT TIME ZONE [INTERVAL] time_zone AS DATETIME precision )
    """

    __slots__ = ["_expression", "_is_interval", "_time_zone", "_precision"]

    def __init__(self, expression: Expression, is_interval: bool, time_zone: str, precision: Decimal):
        self._expression = expression
        self._is_interval = is_interval
        self._time_zone = time_zone
        self._precision = precision

    @property
    def expression(self) -> Expression:
        return self._expression

    @property
    def is_interval(self) -> bool:
        return self._is_interval

    @property
    def time_zone(self) -> str:
        return self._time_zone

    @property
    def precision(self) -> Decimal:
        return self._precision


class FunctionConvert(Expression):
    """CONVERT 函数的第一种形式

    CONVERT ( expression , cast_type )
    """

    __slots__ = ["_expression", "_cast_type"]

    def __init__(self, expression: Expression, cast_type: "CastType"):
        self._expression = expression
        self._cast_type = cast_type

    @property
    def expression(self) -> Expression:
        return self._expression

    @property
    def cast_type(self) -> "CastType":
        return self._cast_type


class FunctionConvertCharset(Expression):
    """CONVERT 函数的第二种形式

    CONVERT ( expression USING charset_name )
    """

    __slots__ = ["_expression", "_charset"]

    def __init__(self, expression: Expression, charset: "Charset"):
        self._expression = expression
        self._charset = charset

    @property
    def expression(self) -> Expression:
        return self._expression

    @property
    def charset_name(self) -> "Charset":
        return self._charset
