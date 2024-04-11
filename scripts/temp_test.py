from metasequoia_sql import *
from scripts.demo.sql_basic_tutorial import *

statement = parse_select_statement(build_token_scanner(SBT_CH05_10_SQLSERVER))
print(statement.source)
