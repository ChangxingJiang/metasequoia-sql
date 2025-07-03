"""
CREATE TABLESPACE 语句（create tablespace statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CREATE_TABLESPACE_STATEMENT",
    "OPT_TS_DATAFILE_NAME",
    "OPT_LOGFILE_GROUP_NAME",
]

# `CREATE TABLESPACE` 语句
CREATE_TABLESPACE_STATEMENT = ms_parser.create_group(
    name="create_tablespace_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CREATE, TType.KEYWORD_TABLESPACE, "ident", "opt_ts_datafile_name",
                     "opt_logfile_group_name", "opt_create_tablespace_option_list"],
            action=lambda x: ast.CreateTablespaceStatement(
                tablespace_name=x[2].get_str_value(),
                datafile=x[3],
                logfile_group_name=x[4],
                options=x[5]
            )
        )
    ]
)

# 可选的表空间数据文件名称
OPT_TS_DATAFILE_NAME = ms_parser.create_group(
    name="opt_ts_datafile_name",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ADD, "datafile"],
            action=lambda x: x[1]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: None
        )
    ]
)

# 可选的日志文件组名称
OPT_LOGFILE_GROUP_NAME = ms_parser.create_group(
    name="opt_logfile_group_name",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_USE, TType.KEYWORD_LOGFILE, TType.KEYWORD_GROUP, "ident"],
            action=lambda x: x[3].get_str_value()
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: None
        )
    ]
)
