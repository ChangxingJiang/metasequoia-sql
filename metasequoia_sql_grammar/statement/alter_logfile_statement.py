"""
ALTER LOGFILE GROUP 语句（alter logfile statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ALTER_LOGFILE_STATEMENT",
    "OPT_ALTER_LOGFILE_GROUP_OPTION_LIST",
    "ALTER_LOGFILE_GROUP_OPTION_LIST",
    "ALTER_LOGFILE_GROUP_OPTION",
]

# `ALTER LOGFILE` 语句
ALTER_LOGFILE_STATEMENT = ms_parser.create_group(
    name="alter_logfile_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALTER, TType.KEYWORD_LOGFILE, TType.KEYWORD_GROUP, "ident",
                     TType.KEYWORD_ADD, "undofile", "opt_alter_logfile_group_option_list"],
            action=lambda x: ast.AlterLogfileStatement(
                group_name=x[3].get_str_value(),
                undofile=x[5],
                option_list=x[6]
            )
        )
    ]
)

# 可选的 `ALTER LOGFILE` 语句选项的列表
OPT_ALTER_LOGFILE_GROUP_OPTION_LIST = ms_parser.create_group(
    name="opt_alter_logfile_group_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["alter_logfile_group_option_list"]
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)

# `ALTER LOGFILE` 语句选项的列表
ALTER_LOGFILE_GROUP_OPTION_LIST = ms_parser.create_group(
    name="alter_logfile_group_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["alter_logfile_group_option_list", "opt_comma", "alter_logfile_group_option"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["alter_logfile_group_option"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# `ALTER LOGFILE` 语句的选项
ALTER_LOGFILE_GROUP_OPTION = ms_parser.create_group(
    name="alter_logfile_group_option",
    rules=[
        ms_parser.create_rule(
            symbols=["ddl_option_initial_size"]
        ),
        ms_parser.create_rule(
            symbols=["ddl_option_storage_engine"]
        ),
        ms_parser.create_rule(
            symbols=["ddl_option_wait"]
        )
    ]
)
