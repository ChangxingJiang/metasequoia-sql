"""
语法解析 Demo
"""

from metasequoia_sql_old import SQLParser

expression = SQLParser.parse_logical_and_level_expression("(`column1` > 2) AND (`column2` > 1)")
print(expression)
