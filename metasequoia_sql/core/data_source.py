"""
【枚举类】数据源类型（即 SQL 语句类型）
"""

import enum

__all__ = ["DataSource"]


class DataSource(enum.Enum):
    """数据源类型（即 SQL 语句类型）"""
    MYSQL = "MYSQL"
    HIVE = "HIVE"
