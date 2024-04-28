"""
表数据血缘分析器

类名：`TableLineageAnalyzer`

构造方法：提供一个建表语句获取器。

提供的核心方法：
- 添加临时表：输入 `WITH` 生成的临时表名，以及对应的表数据血缘容器（`TableDataLineageContainer`）
- 进入子查询层级：进入某一个子查询时执行，创建新的中间表命名空间
- 添加中间表（到当前命名空间）：输入子查询生成的中间表名（别名），以及对应的表数据血缘容器（`TableDataLineageContainer`）
- 离开子查询层级：退出某一个子查询时执行，关闭当前子查询的命名空间，并回退到上一层命名空间
- 获取表数据血缘容器（`get_table`）：输入表名或表别名，返回表对应的 **表血缘分析器**。
  1. 在当前子查询层级的命名空间中搜索
  2. 若搜索不到，则在更上一层的命名空间中查找（相关子查询）
  3. 若在上层命名空间中都搜索不到，则在临时表中搜索
  4. 若在临时表中也搜索不到，则使用建表语句获取器获取建表语句，并根据建表语句构造表数据血缘容器
  5. 若均无法获取，则抛出异常
- 查询引用字段的上游源字段（`get_source_column`）：输入 **引用字段对象**，返回上游表的 **源字段对象** 的列表
  - 如果引用字段对象有所属表名，且不是通配符，则调用 `get_table` 方法获取表数据血缘对象，然后调用表数据血缘对象的 `get_source_column_list` 方法
  - 如果引用字段对象有所属表名，且为通配符，则调用 `get_table` 方法获取表数据血缘对象，然后调用表数据血缘对象的 `get_all_source_column_lists` 方法
  - 如果引用字段对象没有所属表名，且不是通配符，则遍历当前层所有上游表，逐个使用 `has_column` 查询是否存在字段，如果存在；如果存在超过 2 个，则抛出异常；如果存在 1个，则然后调用表数据血缘对象的 `get_source_column_list` 方法
  - 如果引用字段对象没有所属表名，且为通配符，则遍历当前层所有上游表，逐个调用表数据血缘对象的 `get_all_source_column_lists` 方法
"""

from typing import Dict, List

from metasequoia_sql.analyzer.data_linage.table_lineage import TableLineage
from metasequoia_sql.analyzer.tool import CreateTableStatementGetter
from metasequoia_sql.analyzer.data_linage.node import StandardTable

__all__ = ["TableLineageManager"]


class TableLineageManager:
    """表数据血缘管理器"""

    def __init__(self, create_table_statement_getter: CreateTableStatementGetter):
        self._with_table: Dict[str, TableLineage] = {}  # WITH 语句生成的临时表
        self._sub_query_stack: List[Dict[str, TableLineage]] = [{}]  # 子查询生成的临时表
        self._create_table_statement_getter = create_table_statement_getter  # 建表语句查询器

    def add_with_table(self, table_name: str, table_lineage: TableLineage):
        """添加一个临时表"""
        self._with_table[table_name] = table_lineage

    def enter_sub_query(self):
        """进入子查询层级"""
        self._sub_query_stack.append({})

    def add_sub_query_table(self, table_name: str, table_lineage: TableLineage):
        """添加一个子查询的临时表"""
        self._sub_query_stack[-1][table_name] = table_lineage

    def exit_sub_query(self):
        """退出子查询层级"""
        self._sub_query_stack.pop()

    def get_table_lineage(self, table: StandardTable):
        """获取表数据血缘对象 TODO 增加对相关子查询的支持"""
        if table.table_name in self._sub_query_stack[-1]:
            return self._sub_query_stack[-1][table.table_name]
        if table.table_name in self._with_table:
            return self._with_table[table.table_name]
        create_table_statement = self._create_table_statement_getter.get_statement(table.source())
        # TODO
        # select_column_to_source_column_hash = SelectColumnFromCreateTableStatement.handle(
        #             create_table_statement)
