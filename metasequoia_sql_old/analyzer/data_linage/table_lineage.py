"""
数据血缘分析器

描述一个表的数据血缘，这个表可以是 `WITH` 语句生成的临时表，子查询的中间表或 `SELECT` 语句返回的表结果。

这个对象是固定的，一旦构造完成后，仅允许查询，不允许修改。

该对象存储如下信息：

- 表中的所有字段（有序）
- 表中每个字段对应的源数据字段

该对象支持如下查询方法：

- 查询是否包含字段名（`has_column`）：如果包含该字段名则返回 True，否则返回 False（不支持通配符）
- 返回字段名的标准字段对象（`get_standard_column`）：返回指定字段名的标准字段对象（不支持通配符）
- 返回字段名的上游源字段对象的列表（`get_source_column_list`）：返回指定字段名的源字段对象的列表（不支持通配符）
- 返回所有标准字段对象的列表（`get_all_standard_columns`）：返回所有标准字段对象的有序列表（通配符场景）
- 返回所有上游源字段对象的列表的列表（`get_all_source_column_lists`）：返回所有上游源字段对象的列表的有序列表（通配符场景）
"""

from typing import List, Tuple

from metasequoia_sql_old.analyzer import node
from metasequoia_sql_old.core import ASTCreateTableStatement

__all__ = ["SelectTableLineage", "InsertTableLineage"]


class SelectTableLineage:
    """SELECT 语句表数据血缘对象"""

    def __init__(self, data_lineage: List[Tuple[node.StandardColumn, List[node.SourceColumn]]]):
        self._column_name_list = []  # 字段名的有序列表
        self._column_name_to_standard_column_hash = {}  # 字段名到标准字段对象的哈希映射
        self._column_name_to_source_column_list_hash = {}  # 字段名到源字段对象列表的哈希映射
        self._column_idx_to_source_column_list_hash = {}  # 字段序号到源字段对象列表的哈希映射
        self._standard_table_set = set()  # 使用的上游表列表
        for standard_column, source_column_list in data_lineage:
            self._column_name_list.append(standard_column.column_name)
            self._column_name_to_standard_column_hash[standard_column.column_name] = standard_column
            self._column_name_to_source_column_list_hash[standard_column.column_name] = source_column_list
            self._column_idx_to_source_column_list_hash[standard_column.column_idx] = source_column_list
            for source_column in source_column_list:
                self._standard_table_set.add(node.StandardTable(schema_name=source_column.schema_name,
                                                                table_name=source_column.table_name))

    @staticmethod
    def by_create_table_statement(ast: ASTCreateTableStatement):
        """使用 CREATE TABLE 表达式对象实例化"""
        data_lineage = []
        schema_name = ast.table_name.schema_name if ast.table_name.schema_name is not None else ""
        table_name = ast.table_name.table_name
        for column_idx, column_expression in enumerate(ast.columns):
            column_name = column_expression.column_name
            select_column = node.StandardColumn(column_idx=column_idx, column_name=column_name)
            source_column = node.SourceColumn(schema_name=schema_name, table_name=table_name, column_name=column_name)
            data_lineage.append((select_column, [source_column]))
        return SelectTableLineage(data_lineage)

    def has_column(self, column_name: str) -> bool:
        """查询是否包含字段名：如果包含该字段名则返回 True，否则返回 False（支持通配符）"""
        return column_name in self._column_name_list or column_name == "*"

    def get_all_standard_columns(self) -> List[node.StandardColumn]:
        """返回所有标准字段对象的有序列表（通配符场景）"""
        return [self._column_name_to_standard_column_hash[column_name]
                for column_name in self._column_name_list]

    def get_source_column_list_by_idx(self, column_idx: int) -> List[node.SourceColumn]:
        """返回指定字段名的源字段对象的列表"""
        return self._column_idx_to_source_column_list_hash[column_idx]

    def get_source_column_list_by_name(self, column_name: str) -> List[node.SourceColumn]:
        """返回指定字段名的源字段对象的列表（支持通配符）"""
        if column_name != "*":
            return self._column_name_to_source_column_list_hash[column_name]
        all_source_column_list = []
        for source_column_list in self._column_name_to_source_column_list_hash.values():
            all_source_column_list.extend(source_column_list)
        return all_source_column_list

    def get_standard_table_list(self) -> List[node.StandardTable]:
        """获取上游表的列表"""
        return list(self._standard_table_set)

    def all_columns(self) -> List[Tuple[node.StandardColumn, List[node.SourceColumn]]]:
        """获取所有字段的标准字段对象和源字段对象列表的元组的列表"""
        data_lineage = []
        for column_name in self._column_name_list:
            data_lineage.append((self._column_name_to_standard_column_hash.get(column_name),
                                 self._column_name_to_source_column_list_hash.get(column_name)))
        return data_lineage


class InsertTableLineage:
    """INSERT 语句表数据血缘对象"""

    def __init__(self, data_lineage: List[Tuple[node.SourceColumn, List[node.SourceColumn]]]):
        self._down_column_name_list = []  # 下游表字段名的有序列表
        self._column_name_to_source_column_list_hash = {}  # 字段名到上游表源字段的映射
        for down_column, up_column_list in data_lineage:
            self._down_column_name_list.append(down_column)
            self._column_name_to_source_column_list_hash[down_column.column_name] = up_column_list

    def get_up_column_list(self, column_name: str):
        """根据下游表字段名查询上游源字段"""
        return self._column_name_to_source_column_list_hash[column_name]

    def get_all_down_columns(self):
        """获取所有下游表字段"""
        return self._down_column_name_list

    def all_columns(self) -> List[Tuple[node.SourceColumn, List[node.SourceColumn]]]:
        """获取所有字段的下游表字段对象和上游表源字段对象列表的元组的列表"""
        data_lineage = []
        for down_column in self._down_column_name_list:
            data_lineage.append((down_column, self._column_name_to_source_column_list_hash[down_column.column_name]))
        return data_lineage
