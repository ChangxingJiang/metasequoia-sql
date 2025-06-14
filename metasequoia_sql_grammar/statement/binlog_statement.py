"""
二进制日志语句的语法规则。
"""

import metasequoia_parser as ms_parser
from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "BINLOG_STATEMENT"
]

# `BINLOG` 语句
BINLOG_STATEMENT = ms_parser.create_group(
    name="binlog_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BINLOG, "text_literal_sys"],
            action=lambda x: ast.BinlogStatement(event_string=x[1])
        )
    ]
)
