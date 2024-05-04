"""
解析 MySQL 建表语句
"""

from metasequoia_sql import SQLParser
from scripts.demo_sql.sql_basic_tutorial import SBT_CH02_19

if __name__ == "__main__":
    statement = SQLParser.parse_select_statement(SBT_CH02_19)
