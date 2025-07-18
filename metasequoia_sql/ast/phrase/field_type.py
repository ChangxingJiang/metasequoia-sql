"""
字段类型相关节点
"""

from decimal import Decimal
from enum import IntEnum, IntFlag, auto
from typing import List, Optional

from metasequoia_sql.ast.base import Expression, Node
from metasequoia_sql.ast.basic.charset_name import Charset
from metasequoia_sql.ast.basic.literal import DecimalLiteral

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

    __slots__ = ["_option_1", "_option_2"]

    def __init__(self,
                 option_1: Optional[Decimal] = None,
                 option_2: Optional[Decimal] = None):
        self._option_1 = option_1  # 第 1 个参数
        self._option_2 = option_2  # 第 2 个参数

    @property
    def option_1(self) -> Optional[Decimal]:
        """获取第一个参数。
        
        Returns
        -------
        Optional[Decimal]
            第一个参数
        """
        return self._option_1

    @property
    def option_2(self) -> Optional[Decimal]:
        """获取第二个参数。
        
        Returns
        -------
        Optional[Decimal]
            第二个参数
        """
        return self._option_2

    def as_param_list(self) -> List[Expression]:
        """将参数转换为表达式列表。
        
        Returns
        -------
        List[Expression]
            表达式列表
        """
        param_list = []
        if self._option_1 is not None:
            param_list.append(DecimalLiteral(self._option_1))
        if self._option_2 is not None:
            param_list.append(DecimalLiteral(self._option_2))
        return param_list


class CastTypeEnum(IntEnum):
    """转化的字段类型的枚举类型"""

    DEFAULT = auto()  # 默认值（未指定）
    BINARY = auto()  # BINARY
    CHAR = auto()  # CHAR
    NCHAR = auto()  # NCHAR
    SIGNED = auto()  # SIGNED
    SIGNED_INT = auto()  # SIGNED INT
    UNSIGNED = auto()  # UNSIGNED
    UNSIGNED_INT = auto()  # UNSIGNED INT
    DATE = auto()  # DATE
    YEAR = auto()  # YEAR
    TIME = auto()  # TIME
    DATETIME = auto()  # DATETIME
    DECIMAL = auto()  # DECIMAL
    JSON = auto()  # JSON
    REAL = auto()  # REAL
    DOUBLE = auto()  # DOUBLE
    DOUBLE_PRECISION = auto()  # DOUBLE PRECISION
    FLOAT = auto()  # FLOAT
    POINT = auto()  # POINT
    LINESTRING = auto()  # LINESTRING
    POLYGON = auto()  # POLYGON
    MULTIPOINT = auto()  # MULTIPOINT
    MULTILINESTRING = auto()  # MULTILINESTRING
    MULTIPOLYGON = auto()  # MULTIPOLYGON
    GEOMETRYCOLLECTION = auto()  # GEOMETRYCOLLECTION


class CastType(Node):
    """转化的字段类型"""

    __slots__ = ["_field_type", "_type_params", "_charset"]

    def __init__(self,
                 field_type: CastTypeEnum,
                 params: Optional[FieldTypeParams] = None,
                 charset: Optional[Charset] = None):
        self._field_type = field_type
        self._type_params = params if params is not None else FieldTypeParams()
        self._charset = charset

    @staticmethod
    def default() -> "CastType":
        """
        创建默认的转换类型

        Returns
        -------
        CastType
            默认的转换类型实例
        """
        return CastType(field_type=CastTypeEnum.DEFAULT)

    @property
    def field_type(self) -> CastTypeEnum:
        """获取字段类型。
        
        Returns
        -------
        CastTypeEnum
            字段类型
        """
        return self._field_type

    @property
    def params(self) -> FieldTypeParams:
        """获取类型参数。
        
        Returns
        -------
        FieldTypeParams
            类型参数
        """
        return self._type_params

    @property
    def charset(self) -> Optional[Charset]:
        """获取字符集。
        
        Returns
        -------
        Optional[Charset]
            字符集
        """
        return self._charset


class FieldOption(IntFlag):
    """字段选项的枚举值"""

    NONE = 0
    SIGNED = auto()
    UNSIGNED = auto()
    ZEROFILL = auto()


class FieldTypeEnum(IntEnum):
    """DDL 语句中的字段类型的枚举类型"""

    INT = auto()  # INT
    TINYINT = auto()  # TINYINT
    SMALLINT = auto()  # SMALLINT
    MEDIUMINT = auto()  # MEDIUMINT
    BIGINT = auto()  # BIGINT
    REAL = auto()  # REAL
    DOUBLE = auto()  # DOUBLE
    DOUBLE_PRECISION = auto()  # DOUBLE PRECISION
    FLOAT = auto()  # FLOAT
    DECIMAL = auto()  # DECIMAL
    NUMERIC = auto()  # NUMERIC
    FIXED = auto()  # FIXED
    BIT = auto()  # BIT
    BOOL = auto()  # BOOL
    BOOLEAN = auto()  # BOOLEAN
    CHAR = auto()  # CHAR
    NCHAR = auto()  # NCHAR
    NCHAR_BINARY = auto()  # NCHAR BINARY
    BINARY = auto()  # BINARY
    VARCHAR = auto()  # VARCHAR
    NVARCHAR = auto()  # NVARCHAR
    NVARCHAR_BINARY = auto()  # NVARCHAR BINARY
    VARBINARY = auto()  # VARBINARY
    YEAR = auto()  # YEAR
    DATE = auto()  # DATE
    TIME = auto()  # TIME
    TIMESTAMP = auto()  # TIMESTAMP
    DATETIME = auto()  # DATETIME
    TINYBLOB = auto()  # TINYBLOB
    BLOB = auto()  # BLOB
    MEDIUMBLOB = auto()  # MEDIUMBLOB
    LONGBLOB = auto()  # LONGBLOB
    GEOMETRY = auto()  # GEOMETRY
    GEOMETRYCOLLECTION = auto()  # GEOMETRYCOLLECTION
    POINT = auto()  # POINT
    MULTIPOINT = auto()  # MULTIPOINT
    LINESTRING = auto()  # LINESTRING
    MULTILINESTRING = auto()  # MULTILINESTRING
    POLYGON = auto()  # POLYGON
    MULTIPOLYGON = auto()  # MULTIPOLYGON
    LONG_VARBINARY = auto()  # LONG VARBINARY
    LONG_VARCHAR = auto()  # LONG VARCHAR
    TINYTEXT = auto()  # TINYTEXT
    TEXT = auto()  # TEXT
    MEDIUMTEXT = auto()  # MEDIUMTEXT
    LONGTEXT = auto()  # LONGTEXT
    ENUM = auto()  # ENUM
    SET = auto()  # SET
    LONG = auto()  # LONG
    SERIAL = auto()  # SERIAL
    JSON = auto()


class FieldType(Node):
    """DDL 语句中的字段类型"""

    __slots__ = ["_field_type", "_params", "_options", "_enum_value_list", "_charset"]

    def __init__(self,
                 field_type: FieldTypeEnum,
                 params: Optional[FieldTypeParams] = None,
                 options: Optional[FieldOption] = None,
                 enum_value_list: Optional[List[str]] = None,
                 charset: Optional[Charset] = None):
        # pylint: disable=R0913,R0917
        """
        初始化字段类型。

        Parameters
        ----------
        field_type : FieldTypeEnum
            字段类型
        params : Optional[FieldTypeParams], optional
            类型参数
        options : Optional[FieldOption], optional
            字段选项
        enum_value_list : Optional[List[str]], optional
            枚举值列表
        charset : Optional[Charset], optional
            字符集
        """
        self._field_type = field_type
        self._params = params
        self._options = options
        self._enum_value_list = enum_value_list
        self._charset = charset

    @property
    def field_type(self) -> FieldTypeEnum:
        """获取字段类型。
        
        Returns
        -------
        FieldTypeEnum
            字段类型
        """
        return self._field_type

    @property
    def params(self) -> Optional[FieldTypeParams]:
        """获取类型参数。
        
        Returns
        -------
        Optional[FieldTypeParams]
            类型参数
        """
        return self._params

    @property
    def options(self) -> Optional[FieldOption]:
        """获取字段选项。
        
        Returns
        -------
        Optional[FieldOption]
            字段选项
        """
        return self._options

    @property
    def enum_value_list(self) -> Optional[List[str]]:
        """获取枚举值列表。
        
        Returns
        -------
        Optional[List[str]]
            枚举值列表
        """
        return self._enum_value_list

    @property
    def charset(self) -> Optional[Charset]:
        """获取字符集。
        
        Returns
        -------
        Optional[Charset]
            字符集
        """
        return self._charset
