"""
MyBatis 插件 Demo
"""

from metasequoia_sql_old.plugins.mybaitis import SQLParserMyBatis

statements = SQLParserMyBatis.parse_statements("SELECT column_1 FROM Shohin "
                                               "WHERE #{column_2} > 500 "
                                               "GROUP BY #{column_3}")
for statement in statements:
    print(statement)
