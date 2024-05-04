"""
解析 MySQL 建表语句
"""

from metasequoia_sql import SQLParser
from scripts.demo_sql.sql_basic_tutorial import SBT_CH03_28
from metasequoia_sql.analyzer.toolkit.current_level_column_analyzer import CurrentGroupByClauseUsedQuoteColumn

if __name__ == "__main__":
    statement = SQLParser.parse_select_statement(SBT_CH03_28)
    # statement = SQLParser.parse_select_statement("SELECT a, b FROM c GROUP BY 1, 2")
    # print(CurrentGroupByClauseUsedQuoteColumn.handle(statement))

