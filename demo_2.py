"""
解析 MySQL 建表语句
"""

from metasequoia_sql import SQLParser
from metasequoia_sql.analyzer.toolkit.current_level_column_analyzer import CurrentGroupByClauseUsedQuoteColumn

if __name__ == "__main__":
    # statement = SQLParser.parse_select_statement(SBT_CH02_33)
    statement = SQLParser.parse_select_statement("SELECT a, b FROM c GROUP BY 1, 2")
    print(CurrentGroupByClauseUsedQuoteColumn.handle(statement))

