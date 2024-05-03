"""
解析 MySQL 建表语句
"""

from metasequoia_sql import SQLParser, SQLType
from scripts.demo_sql.sql_basic_tutorial import *
import dataclasses

if __name__ == "__main__":
    # statement = SQLParser.parse_select_statement(SBT_CH02_33)
    test = SQLParser.parse_compare_operator("= 3")
    print(type(test))
    print(dataclasses.fields(test))