"""
Hive 语句相关元素对象
"""

from metasequoia_sql.objects.common import *
from metasequoia_sql.objects.core import *


class DDLColumnTypeHive(SQLColumnType):
    """【DDL】Hive 的字段类型对象"""


class DDLColumnHive(DDLColumn):
    """【DDL】Hive 建表语句或修改表结构语句中的字段信息"""


class DDLCreateTableStatementHive(DDLCreateTableStatement):
    """CREATE TABLE 表达式"""

    def __init__(self,
                 schema_name: Optional[str] = None,
                 table_name: Optional[str] = None,
                 comment: Optional[str] = None,
                 if_not_exists: bool = False,
                 columns: List[DDLColumnHive] = None,
                 partition_by: List[DDLColumnHive] = None
                 ):
        super().__init__(schema_name=schema_name, table_name=table_name, comment=comment)
        self.if_not_exists = if_not_exists
        self.columns: List[DDLColumnHive] = columns if columns is not None else []
        self.partition_by: List[DDLColumnHive] = partition_by if partition_by is not None else []

    def set_if_not_exists(self, if_not_exists: bool):
        self.if_not_exists = if_not_exists

    def append_column(self, column: DDLColumnHive):
        """添加字段"""
        self.columns.append(column)

    def change_type(self, hashmap: Dict[str, str], remove_param: bool = True):
        """更新每个字段的变量类型"""
        for column in self.columns:
            old_column_type = column.column_type.name
            new_column_type = hashmap[old_column_type.upper()]
            column.column_type._name = new_column_type
            if remove_param is True:
                column.column_type._function_params = []

    def append_partition_by_column(self, column: DDLColumnHive):
        """添加分区字段"""
        self.partition_by.append(column)

    def source(self, n_indent: int = 4) -> str:
        indentation = " " * n_indent  # 缩进字符串
        result = "CREATE TABLE"
        if self.if_not_exists is True:
            result += " IF NOT EXISTS"
        result += " "
        if self._schema_name is not None:
            result += f"`{self._schema_name}`."
        result += f"`{self._table_name}`(\n"
        columns_and_keys = []
        for column in self.columns:
            columns_and_keys.append(f"{indentation}{column.source}")
        result += ",\n".join(columns_and_keys)
        result += "\n)"
        if self._comment is not None:
            result += f" COMMENT {self._comment}"
        if len(self.partition_by) > 0:
            partition_columns = []
            for column in self.partition_by:
                partition_columns.append(column.source)
            partition_str = ", ".join(partition_columns)
            result += f" PARTITIONED BY ({partition_str})"
        return result
