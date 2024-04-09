"""
Hive 语句相关元素对象
"""

from metasequoia_sql.objects.core import *


class DDLCreateTableStatementHive(DDLCreateTableStatement):
    """CREATE TABLE 表达式"""

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
