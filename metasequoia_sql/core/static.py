"""
静态方法

TODO 待将 SQL 默认语法添加到文档中
"""

import enum
from typing import Set

from metasequoia_sql.core.sql_type import SQLType

__all__ = ["get_unary_operator_set", "get_not_operator_set",
           "EnumInsertType"]


class EnumInsertType(enum.Enum):
    """插入类型的枚举类"""
    INSERT_INTO = ["INSERT", "INTO"]
    INSERT_IGNORE_INTO = ["INSERT", "IGNORE", "INTO"]
    INSERT_OVERWRITE = ["INSERT", "OVERWRITE"]


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
    elif sql_type == SQLType.HIVE:
        return {"-", "+", "~"}
    return {"-", "+", "~", "!"}


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
