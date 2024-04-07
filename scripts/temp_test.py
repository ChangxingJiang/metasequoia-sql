from metasequoia_sql.common.token_scanner import build_scanner
from metasequoia_sql.parser.common import parse_select_statement
from scripts.demo.sql_basic_tutorial import *

statement = parse_select_statement(build_scanner(SBT_CH05_10_SQLSERVER))
print(statement.source)
