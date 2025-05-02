"""
字段类型相关节点
"""

import decimal
import enum
import typing

from metasequoia_sql_new.ast.base import Node
from metasequoia_sql_new.ast.charset import Charset

__all__ = [
    "Charset",
    "FieldTypeParams",
    "CastTypeEnum",
    "CastType",
    "FieldOption",
    "FieldTypeEnum",
    "FieldType",
]


class FieldTypeParams(Node):
    """字段类型的参数"""

    def __init__(self,
                 option_1: typing.Optional[decimal.Decimal] = None,
                 option_2: typing.Optional[decimal.Decimal] = None):
        self._option_1 = option_1  # 第 1 个参数
        self._option_2 = option_2  # 第 2 个参数

    def attr_list(self) -> typing.List[str]:
        return ["option_1", "option_2"]

    @property
    def option_1(self) -> typing.Optional[decimal.Decimal]:
        return self._option_1

    @property
    def option_2(self) -> typing.Optional[decimal.Decimal]:
        return self._option_2


class CastTypeEnum(enum.IntEnum):
    """转化的字段类型的枚举类型"""

    BINARY = enum.auto()  # BINARY
    CHAR = enum.auto()  # CHAR
    NCHAR = enum.auto()  # NCHAR
    SIGNED = enum.auto()  # SIGNED
    SIGNED_INT = enum.auto()  # SIGNED INT
    UNSIGNED = enum.auto()  # UNSIGNED
    UNSIGNED_INT = enum.auto()  # UNSIGNED INT
    DATE = enum.auto()  # DATE
    YEAR = enum.auto()  # YEAR
    TIME = enum.auto()  # TIME
    DATETIME = enum.auto()  # DATETIME
    DECIMAL = enum.auto()  # DECIMAL
    JSON = enum.auto()  # JSON
    REAL = enum.auto()  # REAL
    DOUBLE = enum.auto()  # DOUBLE
    DOUBLE_PRECISION = enum.auto()  # DOUBLE PRECISION
    FLOAT = enum.auto()  # FLOAT
    POINT = enum.auto()  # POINT
    LINESTRING = enum.auto()  # LINESTRING
    POLYGON = enum.auto()  # POLYGON
    MULTIPOINT = enum.auto()  # MULTIPOINT
    MULTILINESTRING = enum.auto()  # MULTILINESTRING
    MULTIPOLYGON = enum.auto()  # MULTIPOLYGON
    GEOMETRYCOLLECTION = enum.auto()  # GEOMETRYCOLLECTION


class CastType(Node):
    """转化的字段类型"""

    def __init__(self,
                 field_type: CastTypeEnum,
                 params: typing.Optional[FieldTypeParams] = None,
                 charset: typing.Optional[Charset] = None):
        self._field_type = field_type
        self._type_params = params if params is not None else FieldTypeParams()
        self._charset = charset

    def attr_list(self) -> typing.List[str]:
        return ["field_type", "params", "charset"]

    @property
    def field_type(self) -> CastTypeEnum:
        return self._field_type

    @property
    def params(self) -> FieldTypeParams:
        return self._type_params

    @property
    def charset(self) -> Charset:
        return self._charset


class FieldOption(enum.IntFlag):
    """字段选项的枚举值"""

    NONE = 0
    SIGNED = enum.auto()
    UNSIGNED = enum.auto()
    ZEROFILL = enum.auto()


class FieldTypeEnum(enum.IntEnum):
    """DDL 语句中的字段类型的枚举类型"""

    INT = enum.auto()  # INT
    TINYINT = enum.auto()  # TINYINT
    SMALLINT = enum.auto()  # SMALLINT
    MEDIUMINT = enum.auto()  # MEDIUMINT
    BIGINT = enum.auto()  # BIGINT
    REAL = enum.auto()  # REAL
    DOUBLE = enum.auto()  # DOUBLE
    DOUBLE_PRECISION = enum.auto()  # DOUBLE PRECISION
    FLOAT = enum.auto()  # FLOAT
    DECIMAL = enum.auto()  # DECIMAL
    NUMERIC = enum.auto()  # NUMERIC
    FIXED = enum.auto()  # FIXED
    BIT = enum.auto()  # BIT
    BOOL = enum.auto()  # BOOL
    BOOLEAN = enum.auto()  # BOOLEAN
    CHAR = enum.auto()  # CHAR
    NCHAR = enum.auto()  # NCHAR
    NCHAR_BINARY = enum.auto()  # NCHAR BINARY
    BINARY = enum.auto()  # BINARY
    VARCHAR = enum.auto()  # VARCHAR
    NVARCHAR = enum.auto()  # NVARCHAR
    NVARCHAR_BINARY = enum.auto()  # NVARCHAR BINARY
    VARBINARY = enum.auto()  # VARBINARY
    YEAR = enum.auto()  # YEAR
    DATE = enum.auto()  # DATE
    TIME = enum.auto()  # TIME
    TIMESTAMP = enum.auto()  # TIMESTAMP
    DATETIME = enum.auto()  # DATETIME
    TINYBLOB = enum.auto()  # TINYBLOB
    BLOB = enum.auto()  # BLOB
    MEDIUMBLOB = enum.auto()  # MEDIUMBLOB
    LONGBLOB = enum.auto()  # LONGBLOB
    GEOMETRY = enum.auto()  # GEOMETRY
    GEOMETRYCOLLECTION = enum.auto()  # GEOMETRYCOLLECTION
    POINT = enum.auto()  # POINT
    MULTIPOINT = enum.auto()  # MULTIPOINT
    LINESTRING = enum.auto()  # LINESTRING
    MULTILINESTRING = enum.auto()  # MULTILINESTRING
    POLYGON = enum.auto()  # POLYGON
    MULTIPOLYGON = enum.auto()  # MULTIPOLYGON
    LONG_VARBINARY = enum.auto()  # LONG VARBINARY
    LONG_VARCHAR = enum.auto()  # LONG VARCHAR
    TINYTEXT = enum.auto()  # TINYTEXT
    TEXT = enum.auto()  # TEXT
    MEDIUMTEXT = enum.auto()  # MEDIUMTEXT
    LONGTEXT = enum.auto()  # LONGTEXT
    ENUM = enum.auto()  # ENUM
    SET = enum.auto()  # SET
    LONG = enum.auto()  # LONG
    SERIAL = enum.auto()  # SERIAL
    JSON = enum.auto()


class FieldType(Node):
    """DDL 语句中的字段类型"""

    def __init__(self,
                 field_type: FieldTypeEnum,
                 params: typing.Optional[FieldTypeParams] = None,
                 options: typing.Optional[FieldOption] = None,
                 enum_value_list: typing.Optional[typing.List[str]] = None,
                 charset: typing.Optional[Charset] = None):
        self._field_type = field_type
        self._params = params
        self._options = options
        self._enum_value_list = enum_value_list
        self._charset = charset

    def attr_list(self) -> typing.List[str]:
        return ["field_type", "params", "options", "enum_value_list", "charset"]

    @property
    def field_type(self) -> FieldTypeEnum:
        return self._field_type

    @property
    def params(self) -> typing.Optional[FieldTypeParams]:
        return self._params

    @property
    def options(self) -> typing.Optional[FieldOption]:
        return self._options

    @property
    def enum_value_list(self) -> typing.Optional[typing.List[str]]:
        return self._enum_value_list

    @property
    def charset(self) -> typing.Optional[Charset]:
        return self._charset
