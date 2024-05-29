"""
语法解析 Demo
"""

from metasequoia_sql import SQLParser

statements = SQLParser.parse_statements("SELECT column1 FROM table_1; SELECT column2 FROM table_2")
for statement in statements:
    print(statement)
