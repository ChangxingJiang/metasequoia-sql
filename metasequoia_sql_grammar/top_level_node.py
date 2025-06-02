"""
顶层节点（top level node）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "START_ENTRY",
    "SQL_STATEMENT_ENTRY",
    "SQL_STATEMENT",
    "OPT_END_OF_INPUT",
]

# 入口语义组 TODO 待补充其他备选规则
START_ENTRY = ms_parser.create_group(
    name="start_entry",
    rules=[
        ms_parser.create_rule(
            symbols=["sql_statement_entry"]
        )
    ]
)

# 标准 SQL 语句的入口语义组
SQL_STATEMENT_ENTRY = ms_parser.create_group(
    name="sql_statement_entry",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.SYSTEM_END_OF_INPUT],
            action=lambda _: None
        ),
        ms_parser.create_rule(
            symbols=["sql_statement", TType.OPERATOR_SEMICOLON, "opt_end_of_input"],
            action=lambda x: x[0]
        ),
        ms_parser.create_rule(
            symbols=["sql_statement", TType.SYSTEM_END_OF_INPUT],
            action=lambda x: x[0]
        )
    ]
)

# 标准 SQL 语句 TODO 待补充其他备选规则
SQL_STATEMENT = ms_parser.create_group(
    name="sql_statement",
    rules=[
        ms_parser.create_rule(
            symbols=["select_statement"]
        )
    ]
)

# 可选的输入流结束符
OPT_END_OF_INPUT = ms_parser.create_group(
    name="opt_end_of_input",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.SYSTEM_END_OF_INPUT],
            action=lambda _: None
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)
