"""
应用样例：数据血缘分析
"""

from metasequoia_sql_old import *
from metasequoia_sql_old.analyzer import CreateTableStatementGetter
from metasequoia_sql_old.analyzer.data_linage.table_lineage_analyzer import TableLineageAnalyzer

table_lineage_analyzer = TableLineageAnalyzer(CreateTableStatementGetter(...))
for statement in SQLParser.parse_statements("your sql"):
    if isinstance(statement, ASTInsertSelectStatement):
        result = table_lineage_analyzer.get_insert_table_lineage(statement)
        print(result)
