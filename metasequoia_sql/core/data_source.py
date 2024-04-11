"""
【枚举类】数据源类型（即 SQL 语句类型）
"""

import enum

__all__ = ["DataSource"]


class DataSource(enum.Enum):
    """数据源类型（即 SQL 语句类型）"""
    MYSQL = "MySQL"
    HIVE = "Hive"
    ORACLE = "Oracle"
    DB2 = "DB2"
    POSTGRE_SQL = "PostgreSQL"
    SQL_SERVER = "SQL Server"
