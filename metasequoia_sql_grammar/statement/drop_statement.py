"""
DROP 语句（drop statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "DROP_DATABASE_STATEMENT",
    "DROP_EVENT_STATEMENT",
    "DROP_FUNCTION_STATEMENT",
    "DROP_INDEX_STATEMENT",
    "DROP_LOGFILE_STATEMENT",
    "DROP_PROCEDURE_STATEMENT",
    "DROP_RESOURCE_GROUP_STATEMENT",
    "DROP_ROLE_STATEMENT",
    "DROP_SERVER_STATEMENT",
    "DROP_SRS_STATEMENT",
    "DROP_TABLESPACE_STATEMENT",
    "DROP_UNDO_TABLESPACE_STATEMENT",
    "DROP_TABLE_STATEMENT",
    "DROP_TRIGGER_STATEMENT",
    "DROP_USER_STATEMENT",
    "DROP_VIEW_STATEMENT",
]

# `DROP DATABASE` 语句
DROP_DATABASE_STATEMENT = ms_parser.create_group(
    name="drop_database_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_DATABASE, "opt_keyword_if_exists", "ident"],
            action=lambda x: ast.DropDatabaseStatement(if_exists=x[2], schema_name=x[3].get_str_value())
        )
    ]
)

# `DROP EVENT` 语句
DROP_EVENT_STATEMENT = ms_parser.create_group(
    name="drop_event_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_EVENT, "opt_keyword_if_exists", "identifier"],
            action=lambda x: ast.DropEventStatement(if_exists=x[2], event_name=x[3])
        )
    ]
)

# `DROP FUNCTION` 语句
DROP_FUNCTION_STATEMENT = ms_parser.create_group(
    name="drop_function_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_FUNCTION, "opt_keyword_if_exists", "identifier"],
            action=lambda x: ast.DropFunctionStatement(if_exists=x[2], function_name=x[3])
        )
    ]
)

# `DROP INDEX` 语句
DROP_INDEX_STATEMENT = ms_parser.create_group(
    name="drop_index_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_INDEX, "ident", TType.KEYWORD_ON, "identifier",
                     "opt_alter_option_lock_and_algorithm"],
            action=lambda x: ast.DropIndexStatement(
                index_name=x[2],
                table_name=x[4],
                lock=x[5].lock,
                algorithm=x[5].algorithm,
                validation=x[5].validation
            )
        )
    ]
)

# `DROP LOGFILE` 语句
DROP_LOGFILE_STATEMENT = ms_parser.create_group(
    name="drop_logfile_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_LOGFILE, TType.KEYWORD_GROUP, "ident",
                     "opt_drop_tablespace_option_list"],
            action=lambda x: ast.DropLogfileStatement(logfile_name=x[3].get_str_value(), options=x[4])
        )
    ]
)

# `DROP PROCEDURE` 语句
DROP_PROCEDURE_STATEMENT = ms_parser.create_group(
    name="drop_procedure_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_PROCEDURE, "opt_keyword_if_exists", "identifier"],
            action=lambda x: ast.DropProcedureStatement(if_exists=x[2], procedure_name=x[3])
        )
    ]
)

# `DROP RESOURCE GROUP` 语句
DROP_RESOURCE_GROUP_STATEMENT = ms_parser.create_group(
    name="drop_resource_group_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_RESOURCE, TType.KEYWORD_GROUP, "ident",
                     "opt_keyword_force"],
            action=lambda x: ast.DropResourceGroupStatement(group_name=x[3].get_str_value(), is_force=x[4])
        )
    ]
)

# `DROP ROLE` 语句
DROP_ROLE_STATEMENT = ms_parser.create_group(
    name="drop_role_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_ROLE, "opt_keyword_if_exists", "role_name_list"],
            action=lambda x: ast.DropRoleStatement(if_exists=x[2], role_list=x[3])
        )
    ]
)

# `DROP SERVER` 语句
DROP_SERVER_STATEMENT = ms_parser.create_group(
    name="drop_server_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_SERVER, "opt_keyword_if_exists", "ident_or_text"],
            action=lambda x: ast.DropServerStatement(if_exists=x[2], server_name=x[3].get_str_value())
        )
    ]
)

# `DROP SPATIAL REFERENCE SYSTEM` 语句
DROP_SRS_STATEMENT = ms_parser.create_group(
    name="drop_srs_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_SPATIAL, TType.KEYWORD_REFERENCE, TType.KEYWORD_SYSTEM,
                     "opt_keyword_if_exists", "int_literal_or_hex"],
            action=lambda x: ast.DropSrsStatement(if_exists=x[4], srs_id=x[5].value)
        )
    ]
)

# `DROP TABLESPACE` 语句
DROP_TABLESPACE_STATEMENT = ms_parser.create_group(
    name="drop_tablespace_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_TABLESPACE, "ident", "opt_drop_tablespace_option_list"],
            action=lambda x: ast.DropTablespaceStatement(tablespace_name=x[2].get_str_value(), options=x[3])
        )
    ]
)

# `DROP UNDO TABLESPACE` 语句
DROP_UNDO_TABLESPACE_STATEMENT = ms_parser.create_group(
    name="drop_undo_tablespace_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_UNDO, TType.KEYWORD_TABLESPACE, "ident",
                     "opt_drop_undo_tablespace_option_list"],
            action=lambda x: ast.DropUndoTablespaceStatement(tablespace_name=x[3].get_str_value(), options=x[4])
        )
    ]
)

# `DROP TABLE` 语句
DROP_TABLE_STATEMENT = ms_parser.create_group(
    name="drop_table_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_DROP,  # 0
                "opt_keyword_temporary",  # 1
                "keyword_table_or_tables",  # 2
                "opt_keyword_if_exists",  # 3
                "identifier_list",  # 4
                "opt_drop_restrict"  # 5
            ],
            action=lambda x: ast.DropTableStatement(
                temporary=x[1],
                if_exists=x[3],
                table_list=x[4],
                restrict=x[5]
            )
        )
    ]
)

# `DROP TRIGGER` 语句
DROP_TRIGGER_STATEMENT = ms_parser.create_group(
    name="drop_trigger_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_TRIGGER, "opt_keyword_if_exists", "identifier"],
            action=lambda x: ast.DropTriggerStatement(if_exists=x[2], trigger_name=x[3])
        )
    ]
)

# `DROP USER` 语句
DROP_USER_STATEMENT = ms_parser.create_group(
    name="drop_user_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_USER, "opt_keyword_if_exists", "user_name_list"],
            action=lambda x: ast.DropUserStatement(if_exists=x[2], user_list=x[3])
        )
    ]
)

# `DROP VIEW` 语句
DROP_VIEW_STATEMENT = ms_parser.create_group(
    name="drop_view_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_VIEW, "opt_keyword_if_exists", "identifier_list",
                     "opt_drop_restrict"],
            action=lambda x: ast.DropViewStatement(if_exists=x[2], table_list=x[3], restrict=x[4])
        )
    ]
)
