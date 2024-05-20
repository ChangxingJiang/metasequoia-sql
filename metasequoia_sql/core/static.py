"""
静态方法

针对 MySQL 和 Hive 在 ! 计算优先级的冲突，在默认场景（SQLType.DEFAULT）中，我们使用 MySQL 中 ! 的优先级。
"""

import enum
from typing import Set

from metasequoia_sql.core.sql_type import SQLType

__all__ = [
    # SQL 的各种类型的枚举类
    "EnumInsertType",  # 插入类型的枚举类
    "EnumJoinType",  # 关联类型的枚举类
    "EnumOrderType",  # 排序类型的枚举类
    "EnumUnionType",  # 组合类型的枚举类
    "EnumWindowRowType",  # 窗口函数中的行限制的类型
    "EnumCastDataType",  # CAST 函数的字段类型

    # 一元运算符
    "get_unary_operator_set",  # 获取一元运算符的集合

    # 计算运算符
    "EnumComputeOperator",  # 计算运算符的枚举类
    "COMPUTE_OPERATOR_HASH",  # 计算运算符字符串到枚举类的映射关系
    "COMPUTE_OPERATOR_SET",  # 计算运算符字符串的集合

    # 比较运算符
    "EnumCompareOperator",  # 比较运算符的枚举类
    "COMPARE_OPERATOR_HASH",  # 比较运算符字符串到枚举类的映射关系
    "COMPARE_OPERATOR_SET",  # 比较运算符字符串的集合

    # 逻辑运算符
    "EnumLogicalOperator",  # 逻辑运算符的枚举类
    "get_not_operator_set",  # 获取逻辑否运算符的集合
]


# ---------------------------------------- 插入类型 ----------------------------------------


class EnumInsertType(enum.Enum):
    """插入类型的枚举类"""
    INSERT_INTO = ["INSERT", "INTO"]
    INSERT_IGNORE_INTO = ["INSERT", "IGNORE", "INTO"]
    INSERT_OVERWRITE = ["INSERT", "OVERWRITE"]


# ---------------------------------------- 关联类型 ----------------------------------------


class EnumJoinType(enum.Enum):
    """关联类型的枚举类"""
    JOIN = ["JOIN"]  # 内连接
    INNER_JOIN = ["INNER", "JOIN"]  # 内连接
    LEFT_JOIN = ["LEFT", "JOIN"]  # 左外连接
    LEFT_OUTER_JOIN = ["LEFT", "OUTER", "JOIN"]  # 左外连接
    LEFT_SEMI_JOIN = ["LEFT", "SEMI", "JOIN"]  # 左半连接
    RIGHT_JOIN = ["RIGHT", "JOIN"]  # 右外连接
    RIGHT_OUTER_JOIN = ["RIGHT", "OUTER", "JOIN"]  # 右外连接
    RIGHT_SEMI_JOIN = ["RIGHT", "SEMI", "JOIN"]  # 右半连接
    FULL_JOIN = ["FULL", "JOIN"]  # 全外连接
    FULL_OUTER_JOIN = ["FULL", "OUTER", "JOIN"]  # 全外连接
    CROSS_JOIN = ["CROSS", "JOIN"]  # 交叉连接


# ---------------------------------------- 排序类型 ----------------------------------------


class EnumOrderType(enum.Enum):
    """排序类型的枚举类"""
    ASC = ["ASC"]  # 升序
    DESC = ["DESC"]  # 降序


# ---------------------------------------- 组合类型 ----------------------------------------


class EnumUnionType(enum.Enum):
    """组合类型的枚举类"""
    UNION_ALL = ["UNION", "ALL"]
    UNION = ["UNION"]
    EXCEPT = ["EXCEPT"]
    INTERSECT = ["INTERSECT"]
    MINUS = ["MINUS"]


# ---------------------------------------- CAST 函数的字段类型 ----------------------------------------


class EnumCastDataType(enum.Enum):
    """CAST 函数的字段类型"""
    # MySQL 类型
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

    # Hive 类型
    STRING = "STRING"


# ---------------------------------------- 窗口函数中的行限制的类型 ----------------------------------------


class EnumWindowRowType(enum.Enum):
    """窗口函数中的行限制的类型"""
    PRECEDING = "PRECEDING"
    CURRENT_ROW = "CURRENT ROW"
    FOLLOWING = "FOLLOWING"


# ---------------------------------------- 计算运算符 ----------------------------------------


class EnumComputeOperator(enum.Enum):
    """计算运算符的枚举类"""
    PLUS = ["+"]  # 加法运算符
    SUBTRACT = ["-"]  # 减法运算符
    MULTIPLE = ["*"]  # 乘法运算符
    DIVIDE = ["/"]  # 除法运算符
    DIVIDE_2 = ["DIV"]  # 除法运算符
    MOD = ["%"]  # 取模运算符
    MOD_2 = ["MOD"]  # 取模运算符
    BITWISE_AND = ["&"]  # 按位与
    BITWISE_OR = ["|"]  # 按位或
    BITWISE_XOR = ["^"]  # 按位异或
    BITWISE_INVERSION = ["~"]  # 按位取反
    LOGICAL_INVERSION = ["!"]  # 逻辑取反
    SHIFT_LEFT = ["<<"]  # 左移位
    SHIRT_RIGHT = [">>"]  # 右移位


# 计算运算符字符串到枚举类的映射关系
COMPUTE_OPERATOR_HASH = {
    "+": EnumComputeOperator.PLUS,
    "-": EnumComputeOperator.SUBTRACT,
    "*": EnumComputeOperator.MULTIPLE,
    "/": EnumComputeOperator.DIVIDE,
    "DIV": EnumComputeOperator.DIVIDE,
    "%": EnumComputeOperator.MOD,
    "MOD": EnumComputeOperator.MOD,
    "&": EnumComputeOperator.BITWISE_AND,
    "|": EnumComputeOperator.BITWISE_OR,
    "^": EnumComputeOperator.BITWISE_XOR,
    "~": EnumComputeOperator.BITWISE_INVERSION,
    "!": EnumComputeOperator.LOGICAL_INVERSION,
    "<<": EnumComputeOperator.SHIFT_LEFT,
    ">>": EnumComputeOperator.SHIRT_RIGHT
}

# 计算运算符字符串的集合
COMPUTE_OPERATOR_SET = set(COMPUTE_OPERATOR_HASH)


# ---------------------------------------- 比较运算符 ----------------------------------------


class EnumCompareOperator(enum.Enum):
    """比较运算符的枚举类

    包含简写名称和完整名称两种，但都映射到相同的枚举值
    """
    EQ = ["="]
    EQUAL_TO = ["="]
    NEQ = ["!="]
    NOT_EQUAL_TO = ["!="]
    LT = ["<"]
    LESS_THAN = ["<"]
    LTE = ["<="]
    LESS_THAN_OR_EQUAL = ["<="]
    GT = [">"]
    GREATER_THAN = [">"]
    GTE = [">="]
    GREATER_THAN_OR_EQUAL = [">="]
    SAME_EQUAL = ["<=>"]


# 比较运算符字符串到枚举类的映射关系
COMPARE_OPERATOR_HASH = {
    "=": EnumCompareOperator.EQUAL_TO,
    "!=": EnumCompareOperator.NOT_EQUAL_TO,
    "<>": EnumCompareOperator.NOT_EQUAL_TO,
    "<": EnumCompareOperator.LESS_THAN,
    "<=": EnumCompareOperator.LESS_THAN_OR_EQUAL,
    ">": EnumCompareOperator.GREATER_THAN,
    ">=": EnumCompareOperator.GREATER_THAN_OR_EQUAL,
    "<=>": EnumCompareOperator.SAME_EQUAL
}

# 比较运算符字符串的集合
COMPARE_OPERATOR_SET = set(COMPARE_OPERATOR_HASH)


# ---------------------------------------- 逻辑运算符 ----------------------------------------


class EnumLogicalOperator(enum.Enum):
    """逻辑运算符的枚举类"""
    LOGICAL_AND = ["AND"]
    LOGICAL_OR = ["OR"]
    LOGICAL_XOR = ["XOR"]
    LOGICAL_NOT = ["NOT"]


# 逻辑运算符字符串到枚举类的映射关系
LOGICAL_OPERATOR_HASH = {
    "AND": EnumLogicalOperator.LOGICAL_AND,
    "&&": EnumLogicalOperator.LOGICAL_AND,
    "OR": EnumLogicalOperator.LOGICAL_AND,
    "||": EnumLogicalOperator.LOGICAL_AND,
    "XOR": EnumLogicalOperator.LOGICAL_XOR,
    "NOT": EnumLogicalOperator.LOGICAL_NOT,
}


# ---------------------------------------- 一元运算符 ----------------------------------------


def get_unary_operator_set(sql_type: SQLType):
    """获取 sql_type 类型的一元运算符集合

    Parameters
    ----------
    sql_type : SQLType
        SQL 语言类型

    Returns
    -------
    Set[str]
        指定 SQL 语言类型支持的一元运算符的集合
    """
    if sql_type == SQLType.MYSQL:
        return {"-", "+", "~", "!"}
    if sql_type == SQLType.HIVE:
        return {"-", "+", "~"}
    return {"-", "+", "~", "!"}


# ---------------------------------------- 逻辑否运算符 ----------------------------------------


def get_not_operator_set(sql_type: SQLType) -> Set[str]:
    """获取 sql_type 类型的 NOT 含义运算符的集合

    Parameters
    ----------
    sql_type : SQLType
        SQL 语言类型

    Returns
    -------
    Set[str]
        指定 SQL 语言类型支持的 NOT 含义运算符的集合
    """
    if sql_type == SQLType.HIVE:
        return {"NOT", "!"}
    return {"NOT"}
