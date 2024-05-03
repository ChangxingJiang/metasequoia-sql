"""
SQL 语句类型
"""

import enum

__all__ = ["SQLType"]


class SQLType(enum.Enum):
    """SQL 语句类型"""
    MYSQL = "MySQL"
    HIVE = "Hive"
    ORACLE = "Oracle"
    DB2 = "DB2"
    POSTGRE_SQL = "PostgreSQL"
    SQL_SERVER = "SQL Server"
    DEFAULT = "DEFAULT"
