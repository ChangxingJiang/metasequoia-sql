from metasequoia_sql import *
from scripts.demo_sql.sql_basic_tutorial import *

statement = parse_select_statement(SBT_CH05_10_SQLSERVER)
print(statement.source)
