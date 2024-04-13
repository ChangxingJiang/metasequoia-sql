from metasequoia_sql import *
from scripts.demo.sql_basic_tutorial import *

statement = parse_select_statement(SBT_CH05_10_SQLSERVER)
print(statement.source)
