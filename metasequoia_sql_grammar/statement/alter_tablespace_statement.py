# pylint: disable=R0801

"""
ALTER TABLESPACE 语句（alter tablespace statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ALTER_TABLESPACE_STATEMENT",
    "OPT_ALTER_TABLESPACE_OPTION_LIST",
    "ALTER_TABLESPACE_OPTION_LIST",
    "ALTER_TABLESPACE_OPTION",
]

# `ALTER TABLESPACE` 语句
ALTER_TABLESPACE_STATEMENT = ms_parser.create_group(
    name="alter_tablespace_statement",
    rules=[
        # ALTER TABLESPACE name ADD DATAFILE 'path' [options]
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALTER, TType.KEYWORD_TABLESPACE, "ident", TType.KEYWORD_ADD, "datafile",
                     "opt_alter_tablespace_option_list"],
            action=lambda x: ast.AlterTablespaceStatement(
                tablespace_name=x[2],
                action_type=ast.EnumAlterTablespaceActionType.ADD,
                datafile=x[4],
                option_list=x[5]
            )
        ),
        # ALTER TABLESPACE name DROP DATAFILE 'path' [options]
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALTER, TType.KEYWORD_TABLESPACE, "ident", TType.KEYWORD_DROP, "datafile",
                     "opt_alter_tablespace_option_list"],
            action=lambda x: ast.AlterTablespaceStatement(
                tablespace_name=x[2],
                action_type=ast.EnumAlterTablespaceActionType.DROP,
                datafile=x[4],
                option_list=x[5]
            )
        ),
        # ALTER TABLESPACE name RENAME TO new_name
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALTER, TType.KEYWORD_TABLESPACE, "ident", TType.KEYWORD_RENAME, TType.KEYWORD_TO,
                     "ident"],
            action=lambda x: ast.AlterTablespaceStatement(
                tablespace_name=x[2],
                action_type=ast.EnumAlterTablespaceActionType.RENAME,
                target_name=x[5]
            )
        ),
        # ALTER TABLESPACE name alter_tablespace_option_list
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALTER, TType.KEYWORD_TABLESPACE, "ident", "alter_tablespace_option_list"],
            action=lambda x: ast.AlterTablespaceStatement(
                tablespace_name=x[2],
                action_type=ast.EnumAlterTablespaceActionType.ALTER,
                option_list=x[3]
            )
        )
    ]
)

# 可选的 `ALTER TABLESPACE` 选项的列表
OPT_ALTER_TABLESPACE_OPTION_LIST = ms_parser.create_group(
    name="opt_alter_tablespace_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["alter_tablespace_option_list"],
            action=lambda x: x[0]
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)

# `ALTER TABLESPACE` 的选项的列表
ALTER_TABLESPACE_OPTION_LIST = ms_parser.create_group(
    name="alter_tablespace_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["alter_tablespace_option"],
            action=lambda x: [x[0]]
        ),
        ms_parser.create_rule(
            symbols=["alter_tablespace_option_list", "opt_comma", "alter_tablespace_option"],
            action=lambda x: x[0] + [x[2]]
        )
    ]
)

# `ALTER TABLESPACE` 的选项
ALTER_TABLESPACE_OPTION = ms_parser.create_group(
    name="alter_tablespace_option",
    rules=[
        ms_parser.create_rule(
            symbols=["ddl_option_initial_size"]
        ),
        ms_parser.create_rule(
            symbols=["ddl_option_autoextend_size"]
        ),
        ms_parser.create_rule(
            symbols=["ddl_option_max_size"]
        ),
        ms_parser.create_rule(
            symbols=["ddl_option_storage_engine"]
        ),
        ms_parser.create_rule(
            symbols=["ddl_option_wait"]
        ),
        ms_parser.create_rule(
            symbols=["ddl_option_tablespace_encryption"]
        ),
        ms_parser.create_rule(
            symbols=["ddl_option_tablespace_engine_attribute"]
        )
    ]
)
