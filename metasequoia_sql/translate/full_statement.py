"""
包含所有数据库特性的 FullStatement，仅用于数类型转换，不支持其他使用方式
"""

from typing import Optional, List

from metasequoia_sql.errors import FullStatementCalledSource
from metasequoia_sql.objects.core import SQLGeneralExpression

__all__ = ["DDLColumnTypeFull", "DDLColumnFull", "DDLPrimaryKeyFull", "DDLUniqueKeyFull", "DDLKeyFull",
           "DDLForeignKeyFull", "DDLFulltextKeyFull", "DDLCreateTableStatementFull"]


class FullBase:
    """FullStatement 各元素的抽象基类，在调用 source 方法时抛出异常"""

    def source(self):
        raise FullStatementCalledSource()


class DDLColumnTypeFull(FullBase):
    """【DDL】MySQL 的字段类型对象"""

    def __init__(self, name: str, params: Optional[List[SQLGeneralExpression]] = None):
        self.name = name
        self.params = params


class DDLColumnFull(FullBase):
    """【DDL】建表语句或修改表结构语句中的字段信息"""

    def __init__(self,
                 column_name: str,
                 column_type: DDLColumnTypeFull,
                 comment: Optional[str] = None,
                 is_unsigned: bool = False,
                 is_zerofill: bool = False,
                 character_set: Optional[str] = None,
                 collate: Optional[str] = None,
                 is_allow_null: bool = False,
                 is_not_null: bool = False,
                 is_auto_increment: bool = False,
                 default: Optional[SQLGeneralExpression] = None,
                 on_update: Optional[SQLGeneralExpression] = None
                 ):
        self.column_name = column_name
        self.column_type = column_type
        self.is_unsigned = is_unsigned
        self.is_zerofill = is_zerofill
        self.character_set = character_set
        self.collate = collate
        self.is_allow_null = is_allow_null  # 是否显式地允许 NULL 值
        self.is_not_null = is_not_null
        self.is_auto_increment = is_auto_increment
        self.default = default
        self.on_update = on_update
        self.comment = comment


class DDLPrimaryKeyFull(FullBase):
    """【DDL】主键索引"""

    def __init__(self, column: str):
        self.column = column


class DDLUniqueKeyFull(FullBase):
    """【DDL】唯一索引"""

    def __init__(self, name: str, columns: List[str]):
        self.name = name
        self.columns = columns


class DDLKeyFull(FullBase):
    """【DDL】索引"""

    def __init__(self, name: str, columns: List[str]):
        self.name = name
        self.columns = columns


class DDLForeignKeyFull(FullBase):
    """【DDL】外键索引"""

    def __init__(self,
                 constraint_name: str,
                 slave_columns: List[str],
                 master_table_name: str,
                 master_columns: List[str]):
        self.constraint_name = constraint_name
        self.slave_columns = slave_columns
        self.master_table_name = master_table_name
        self.master_columns = master_columns


class DDLFulltextKeyFull(FullBase):
    """【DDL】"""

    def __init__(self, name: str, columns: List[str]):
        self.name: str = name
        self.columns: List[str] = columns


class DDLCreateTableStatementFull(FullBase):
    """CREATE TABLE 表达式"""

    def __init__(self,
                 schema_name: Optional[str] = None,
                 table_name: Optional[str] = None,
                 comment: Optional[str] = None,
                 if_not_exists: bool = False,
                 columns: Optional[List[DDLColumnFull]] = None,
                 primary_key: Optional[DDLPrimaryKeyFull] = None,
                 unique_key: Optional[List[DDLUniqueKeyFull]] = None,
                 key: Optional[List[DDLKeyFull]] = None,
                 fulltext_key: Optional[List[DDLFulltextKeyFull]] = None,
                 foreign_key: List[DDLForeignKeyFull] = None,
                 engine: Optional[str] = None,
                 auto_increment: Optional[int] = None,
                 default_charset: Optional[str] = None,
                 collate: Optional[str] = None,
                 row_format: Optional[str] = None,
                 states_persistent: Optional[str] = None,
                 partition_by: Optional[List[DDLColumnFull]] = None
                 ):
        self.schema_name = schema_name
        self.table_name = table_name
        self.comment = comment
        self.if_not_exists = if_not_exists
        self.columns = columns if columns is not None else []
        self.primary_key = primary_key
        self.unique_key = unique_key if unique_key is not None else []
        self.key = key if key is not None else []
        self.fulltext_key = fulltext_key if fulltext_key is not None else []
        self.foreign_key = foreign_key if foreign_key is not None else []
        self.engine = engine
        self.auto_increment = auto_increment
        self.default_charset = default_charset
        self.collate = collate
        self.row_format = row_format
        self.states_persistent = states_persistent
        self.partition_by: List[DDLColumnFull] = partition_by if partition_by is not None else []
