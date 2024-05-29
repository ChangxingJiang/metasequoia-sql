"""
语法解析 Demo
"""

from metasequoia_sql import SQLParser

statement = SQLParser.parse_select_statement("SELECT column1, '2' FROM table_1")
print(statement)
