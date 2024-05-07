"""
解析 MySQL 建表语句
"""

from metasequoia_sql import SQLParser
from scripts.demo_sql.sql_basic_tutorial import SBT_CH08_18
from metasequoia_sql import *
from metasequoia_sql.analyzer import *
from metasequoia_sql.analyzer.node import StandardColumn
from metasequoia_sql.common import ordered_distinct
from scripts.demo_sql.sql_basic_tutorial import *

if __name__ == "__main__":
    statement = SQLParser.parse_select_statement(SBT_CH08_18)
    print(statement)
    print(CurrentUsedQuoteColumn.handle(statement))
    print(CurrentGroupByClauseUsedQuoteColumn.handle(statement))
