"""
数据血缘分析器
"""

from typing import List, Tuple

from metasequoia_sql.analyzer.data_linage import node


class TableLineageAnalyzer:
    """表数据血缘分析器"""

    def __init__(self, data_lineage: List[Tuple[node.StandardColumn, List[node.SourceColumn]]]):
        self._column_name_list = []  # 字段名的有序列表
        self._column_name_to_standard_column_hash = {}  # 字段名到标准字段对象的哈希映射
        self._column_name_to_source_column_list_hash = {}  # 字段名到源字段对象列表的哈希映射
        for standard_column, source_column_list in data_lineage:
            column_name = standard_column.column_name
            self._column_name_list.append(column_name)
            self._column_name_to_standard_column_hash[column_name] = standard_column
            self._column_name_to_source_column_list_hash[column_name] = source_column_list

    def has_column(self, column_name: str) -> bool:
        """查询是否包含字段名：如果包含该字段名则返回 True，否则返回 False（不支持通配符）"""
        return column_name in self._column_name_list

    def get_standard_column(self, column_name: str) -> node.StandardColumn:
        """返回指定字段名的标准字段对象（不支持通配符）"""
        return self._column_name_to_standard_column_hash[column_name]

    def get_source_column_list(self, column_name: str) -> List[node.SourceColumn]:
        """返回指定字段名的源字段对象的列表（不支持通配符）"""
        return self._column_name_to_source_column_list_hash[column_name]

    def get_all_standard_columns(self) -> List[node.StandardColumn]:
        """返回所有标准字段对象的有序列表（通配符场景）"""
        return [self._column_name_to_standard_column_hash[column_name]
                for column_name in self._column_name_list]

    def get_all_source_column_lists(self) -> List[List[node.SourceColumn]]:
        """返回所有上游源字段对象的列表的有序列表（通配符场景）"""
        return [self._column_name_to_source_column_list_hash[column_name]
                for column_name in self._column_name_list]
