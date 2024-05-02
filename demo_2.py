"""
解析 MySQL 建表语句
"""

from metasequoia_sql import SQLParser
from scripts.demo_sql.sql_basic_tutorial import *

if __name__ == "__main__":
    # statement = SQLParser.parse_select_statement(SBT_CH02_06)
    SQLParser.check_literal_expression("x'3f' WHERE")

    SQLParser.check_literal_expression("1 WHERE")
    SQLParser.check_literal_expression("2.5 WHERE")
    SQLParser.check_literal_expression("'a' WHERE")
    SQLParser.check_literal_expression("x'3f' WHERE")
    SQLParser.check_literal_expression("TRUE WHERE")
    SQLParser.check_literal_expression("true WHERE")
    SQLParser.check_literal_expression("False WHERE")
    SQLParser.check_literal_expression("b'1' WHERE")
    SQLParser.check_literal_expression("null WHERE")
    SQLParser.check_literal_expression("NULL WHERE")
    SQLParser.check_literal_expression("cnt WHERE")
    SQLParser.check_literal_expression("table_name.column_name WHERE")