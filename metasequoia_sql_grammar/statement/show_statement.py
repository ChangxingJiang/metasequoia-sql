"""
SHOW 语句（show statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    # SHOW 语句
    "SHOW_BINARY_LOG_STATUS_STATEMENT",
    "SHOW_BINARY_LOGS_STATEMENT",
    "SHOW_BINLOG_EVENTS_STATEMENT",
    "SHOW_CHAR_SET_STATEMENT",
    "SHOW_COLLATION_STATEMENT",
    "SHOW_COLUMNS_STATEMENT",
    "SHOW_COUNT_ERRORS_STATEMENT",
    "SHOW_COUNT_WARNINGS_STATEMENT",
    "SHOW_CREATE_DATABASE_STATEMENT",
    "SHOW_CREATE_EVENT_STATEMENT",
    "SHOW_CREATE_FUNCTION_STATEMENT",
    "SHOW_CREATE_PROCEDURE_STATEMENT",
    "SHOW_CREATE_TABLE_STATEMENT",
    "SHOW_CREATE_TRIGGER_STATEMENT",
    "SHOW_CREATE_USER_STATEMENT",
    "SHOW_CREATE_VIEW_STATEMENT",
    "SHOW_DATABASES_STATEMENT",
    "SHOW_ENGINE_LOGS_STATEMENT",
    "SHOW_ENGINE_MUTEX_STATEMENT",
    "SHOW_ENGINE_STATUS_STATEMENT",
    "SHOW_ENGINES_STATEMENT",
    "SHOW_ERRORS_STATEMENT",
    "SHOW_EVENTS_STATEMENT",
    "SHOW_FUNCTION_CODE_STATEMENT",
    "SHOW_FUNCTION_STATUS_STATEMENT",
    "SHOW_GRANTS_STATEMENT",
    "SHOW_KEYS_STATEMENT",
    "SHOW_MASTER_STATUS_STATEMENT",
    "SHOW_OPEN_TABLES_STATEMENT",
    "SHOW_PARSE_TREE_STATEMENT",
    "SHOW_PLUGINS_STATEMENT",
    "SHOW_PRIVILEGES_STATEMENT",
    "SHOW_PROCEDURE_CODE_STATEMENT",
    "SHOW_PROCEDURE_STATUS_STATEMENT",
    "SHOW_PROCESSLIST_STATEMENT",
    "SHOW_PROFILE_STATEMENT",
    "SHOW_PROFILES_STATEMENT",
    "SHOW_RELAYLOG_EVENTS_STATEMENT",
    "SHOW_REPLICA_STATUS_STATEMENT",
    "SHOW_REPLICAS_STATEMENT",
    "SHOW_STATUS_STATEMENT",
    "SHOW_TABLE_STATUS_STATEMENT",
    "SHOW_TABLES_STATEMENT",
    "SHOW_TRIGGERS_STATEMENT",
    "SHOW_WARNINGS_STATEMENT",
    "SHOW_VARIABLES_STATEMENT",

    # SHOW 语句的组成部分
    "OPT_BINLOG_IN",
    "OPT_BINLOG_FROM",
    "OPT_WILD_OR_WHERE",
    "OPT_SHOW_SCHEMA",
    "ENGINE_NAME_OR_ALL",
    "OPT_FOR_QUERY",
    "OPT_FOR_CHANNEL",
]

# `SHOW BINARY LOG STATUS` 语句
SHOW_BINARY_LOG_STATUS_STATEMENT = ms_parser.create_group(
    name="show_binary_log_status_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_BINARY, TType.KEYWORD_LOG, TType.KEYWORD_STATUS],
            action=lambda x: ast.ShowBinaryLogStatusStatement()
        )
    ]
)

# `SHOW BINARY LOGS` 语句
SHOW_BINARY_LOGS_STATEMENT = ms_parser.create_group(
    name="show_binary_logs_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, "keyword_master_or_binary", TType.KEYWORD_LOGS],
            action=lambda x: ast.ShowBinaryLogsStatement()
        )
    ]
)

# `SHOW BINLOG EVENTS` 语句
SHOW_BINLOG_EVENTS_STATEMENT = ms_parser.create_group(
    name="show_binlog_events_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_BINLOG, TType.KEYWORD_EVENTS, "opt_binlog_in", "opt_binlog_from",
                     "opt_limit_clause"],
            action=lambda x: ast.ShowBinlogEventsStatement(in_file=x[3], from_event=x[4], limit_clause=x[5])
        )
    ]
)

# `SHOW CHAR SET` 语句
SHOW_CHAR_SET_STATEMENT = ms_parser.create_group(
    name="show_char_set_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, "keyword_charset", "opt_wild_or_where"],
            action=lambda x: ast.ShowCharSetStatement(wild=x[2].wild, where=x[2].where)
        )
    ]
)

# `SHOW COLLATION` 语句
SHOW_COLLATION_STATEMENT = ms_parser.create_group(
    name="show_collation_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_COLLATION, "opt_wild_or_where"],
            action=lambda x: ast.ShowCollationStatement(wild=x[2].wild, where=x[2].where)
        )
    ]
)

# `SHOW COLUMNS` 语句
SHOW_COLUMNS_STATEMENT = ms_parser.create_group(
    name="show_columns_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_SHOW,  # 0
                "opt_show_command_type",  # 1
                TType.KEYWORD_COLUMNS,  # 2
                "keyword_from_or_in",  # 3
                "identifier",  # 4
                "opt_show_schema",  # 5
                "opt_wild_or_where"  # 6
            ],
            action=lambda x: ast.ShowColumnsStatement(
                command_type=x[1],
                table_ident=x[4],
                schema_name=x[5],
                wild=x[6].wild,
                where=x[6].where
            )
        )
    ]
)

# `SHOW COUNT ERRORS` 语句
SHOW_COUNT_ERRORS_STATEMENT = ms_parser.create_group(
    name="show_count_errors_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.WORD_COUNT, TType.OPERATOR_LPAREN, TType.OPERATOR_STAR,
                     TType.OPERATOR_RPAREN, TType.KEYWORD_ERRORS],
            action=lambda x: ast.ShowCountErrorsStatement()
        )
    ]
)

# `SHOW COUNT WARNINGS` 语句
SHOW_COUNT_WARNINGS_STATEMENT = ms_parser.create_group(
    name="show_count_warnings_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.WORD_COUNT, TType.OPERATOR_LPAREN, TType.OPERATOR_STAR,
                     TType.OPERATOR_RPAREN, TType.KEYWORD_WARNINGS],
            action=lambda x: ast.ShowCountWarningsStatement()
        )
    ]
)

# `SHOW CREATE DATABASE` 语句
SHOW_CREATE_DATABASE_STATEMENT = ms_parser.create_group(
    name="show_create_database_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_CREATE, TType.KEYWORD_DATABASE, "opt_keyword_if_not_exists",
                     "ident"],
            action=lambda x: ast.ShowCreateDatabaseStatement(if_not_exists=x[3], database_name=x[4].get_str_value())
        )
    ]
)

# `SHOW CREATE EVENT` 语句
SHOW_CREATE_EVENT_STATEMENT = ms_parser.create_group(
    name="show_create_event_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_CREATE, TType.KEYWORD_EVENT, "identifier"],
            action=lambda x: ast.ShowCreateEventStatement(event_name=x[3])
        )
    ]
)

# `SHOW CREATE FUNCTION` 语句
SHOW_CREATE_FUNCTION_STATEMENT = ms_parser.create_group(
    name="show_create_function_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_CREATE, TType.KEYWORD_FUNCTION, "identifier"],
            action=lambda x: ast.ShowCreateFunctionStatement(function_name=x[3])
        )
    ]
)

# `SHOW CREATE PROCEDURE` 语句
SHOW_CREATE_PROCEDURE_STATEMENT = ms_parser.create_group(
    name="show_create_procedure_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_CREATE, TType.KEYWORD_PROCEDURE, "identifier"],
            action=lambda x: ast.ShowCreateProcedureStatement(procedure_name=x[3])
        )
    ]
)

# `SHOW CREATE TABLE` 语句
SHOW_CREATE_TABLE_STATEMENT = ms_parser.create_group(
    name="show_create_table_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_CREATE, TType.KEYWORD_TABLE, "identifier"],
            action=lambda x: ast.ShowCreateTableStatement(table_ident=x[3])
        )
    ]
)

# `SHOW CREATE TRIGGER` 语句
SHOW_CREATE_TRIGGER_STATEMENT = ms_parser.create_group(
    name="show_create_trigger_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_CREATE, TType.KEYWORD_TRIGGER, "identifier"],
            action=lambda x: ast.ShowCreateTriggerStatement(trigger_name=x[3])
        )
    ]
)

# `SHOW CREATE USER` 语句
SHOW_CREATE_USER_STATEMENT = ms_parser.create_group(
    name="show_create_user_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_CREATE, TType.KEYWORD_USER, "user_name"],
            action=lambda x: ast.ShowCreateUserStatement(user_name=x[3])
        )
    ]
)

# `SHOW CREATE VIEW` 语句
SHOW_CREATE_VIEW_STATEMENT = ms_parser.create_group(
    name="show_create_view_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_CREATE, TType.KEYWORD_VIEW, "identifier"],
            action=lambda x: ast.ShowCreateViewStatement(view_name=x[3])
        )
    ]
)

# `SHOW DATABASES` 语句
SHOW_DATABASES_STATEMENT = ms_parser.create_group(
    name="show_databases_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_DATABASES, "opt_wild_or_where"],
            action=lambda x: ast.ShowDatabasesStatement(wild=x[2].wild, where=x[2].where)
        )
    ]
)

# `SHOW ENGINE LOGS` 语句
SHOW_ENGINE_LOGS_STATEMENT = ms_parser.create_group(
    name="show_engine_logs_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_ENGINE, "engine_name_or_all", TType.KEYWORD_LOGS],
            action=lambda x: ast.ShowEngineLogsStatement(engine_name=x[2])
        )
    ]
)

# `SHOW ENGINE MUTEX` 语句
SHOW_ENGINE_MUTEX_STATEMENT = ms_parser.create_group(
    name="show_engine_mutex_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_ENGINE, "engine_name_or_all", TType.KEYWORD_MUTEX],
            action=lambda x: ast.ShowEngineMutexStatement(engine_name=x[2])
        )
    ]
)

# `SHOW ENGINE STATUS` 语句
SHOW_ENGINE_STATUS_STATEMENT = ms_parser.create_group(
    name="show_engine_status_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_ENGINE, "engine_name_or_all", TType.KEYWORD_STATUS],
            action=lambda x: ast.ShowEngineStatusStatement(engine_name=x[2])
        )
    ]
)

# `SHOW ENGINES` 语句
SHOW_ENGINES_STATEMENT = ms_parser.create_group(
    name="show_engines_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, "opt_keyword_storage", TType.KEYWORD_ENGINES],
            action=lambda x: ast.ShowEnginesStatement()
        )
    ]
)

# `SHOW ERRORS` 语句
SHOW_ERRORS_STATEMENT = ms_parser.create_group(
    name="show_errors_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_ERRORS, "opt_limit_clause"],
            action=lambda x: ast.ShowErrorsStatement(limit_clause=x[2])
        )
    ]
)

# `SHOW EVENTS` 语句
SHOW_EVENTS_STATEMENT = ms_parser.create_group(
    name="show_events_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_EVENTS, "opt_show_schema", "opt_wild_or_where"],
            action=lambda x: ast.ShowEventsStatement(schema_name=x[2], wild=x[3].wild, where=x[3].where)
        )
    ]
)

# `SHOW FUNCTION CODE` 语句
SHOW_FUNCTION_CODE_STATEMENT = ms_parser.create_group(
    name="show_function_code_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_FUNCTION, TType.KEYWORD_CODE, "identifier"],
            action=lambda x: ast.ShowFunctionCodeStatement(function_name=x[3])
        )
    ]
)

# `SHOW FUNCTION STATUS` 语句
SHOW_FUNCTION_STATUS_STATEMENT = ms_parser.create_group(
    name="show_function_status_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_FUNCTION, TType.KEYWORD_STATUS, "opt_wild_or_where"],
            action=lambda x: ast.ShowFunctionStatusStatement(wild=x[3].wild, where=x[3].where)
        )
    ]
)

# `SHOW GRANTS` 语句
SHOW_GRANTS_STATEMENT = ms_parser.create_group(
    name="show_grants_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_GRANTS],
            action=lambda _: ast.ShowEnginesStatement()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_GRANTS, TType.KEYWORD_FOR, "user_name"],
            action=lambda x: ast.ShowGrantsStatement(for_user=x[3])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_GRANTS, TType.KEYWORD_FOR, "user_name", TType.KEYWORD_USING,
                     "user_name_list"],
            action=lambda x: ast.ShowGrantsStatement(for_user=x[3], using_user_list=x[5])
        )
    ]
)

# `SHOW KEYS` 语句
SHOW_KEYS_STATEMENT = ms_parser.create_group(
    name="show_keys_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_SHOW,  # 0
                "opt_keyword_extended",  # 1
                "keyword_keys_or_index",  # 2
                "keyword_from_or_in",  # 3
                "identifier",  # 4
                "opt_show_schema",  # 5
                "opt_where_clause"  # 6
            ],
            action=lambda x: ast.ShowKeysStatement(
                is_extended=x[1],
                table_ident=x[4],
                schema_name=x[5],
                where_clause=x[6]
            )
        )
    ]
)

# `SHOW MASTER STATUS` 语句
SHOW_MASTER_STATUS_STATEMENT = ms_parser.create_group(
    name="show_master_status_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_MASTER, TType.KEYWORD_STATUS],
            action=lambda _: ast.ShowMasterStatusStatement()
        )
    ]
)

# `SHOW OPEN TABLES` 语句
SHOW_OPEN_TABLES_STATEMENT = ms_parser.create_group(
    name="show_open_tables_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_OPEN, TType.KEYWORD_TABLES, "opt_show_schema",
                     "opt_wild_or_where"],
            action=lambda x: ast.ShowOpenTablesStatement(schema_name=x[3], wild=x[4].wild, where=x[4].where)
        )
    ]
)

# `SHOW PARSE TREE` 语句
SHOW_PARSE_TREE_STATEMENT = ms_parser.create_group(
    name="show_parse_tree_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_PARSE_TREE, "sql_statement"],
            action=lambda x: ast.ShowParseTreeStatement(statement=x[2])
        )
    ]
)

# `SHOW PLUGINS` 语句
SHOW_PLUGINS_STATEMENT = ms_parser.create_group(
    name="show_plugins_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_PLUGINS],
            action=lambda _: ast.ShowPluginsStatement()
        )
    ]
)

# `SHOW PRIVILEGES` 语句
SHOW_PRIVILEGES_STATEMENT = ms_parser.create_group(
    name="show_privileges_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_PRIVILEGES],
            action=lambda _: ast.ShowPrivilegesStatement()
        ),
    ]
)

# `SHOW PROCEDURE CODE` 语句
SHOW_PROCEDURE_CODE_STATEMENT = ms_parser.create_group(
    name="show_procedure_code_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_PROCEDURE, TType.KEYWORD_CODE, "identifier"],
            action=lambda x: ast.ShowProcedureCodeStatement(procedure_name=x[3])
        )
    ]
)

# `SHOW PROCEDURE STATUS` 语句
SHOW_PROCEDURE_STATUS_STATEMENT = ms_parser.create_group(
    name="show_procedure_status_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_PROCEDURE, TType.KEYWORD_STATUS, "opt_wild_or_where"],
            action=lambda x: ast.ShowProcedureStatusStatement(wild=x[3].wild, where=x[3].where)
        )
    ]
)

# `SHOW PROCESSLIST` 语句
SHOW_PROCESSLIST_STATEMENT = ms_parser.create_group(
    name="show_processlist_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, "opt_keyword_full", TType.KEYWORD_PROCESSLIST],
            action=lambda x: ast.ShowProcesslistStatement(is_full=x[1])
        )
    ]
)

# `SHOW PROFILE` 语句
SHOW_PROFILE_STATEMENT = ms_parser.create_group(
    name="show_profile_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_PROFILE, "opt_profile_type_list", "opt_for_query",
                     "opt_limit_clause"],
            action=lambda x: ast.ShowProfileStatement(profile_type=x[2], thread_id=x[3], limit_clause=x[4])
        )
    ]
)

# `SHOW PROFILES` 语句
SHOW_PROFILES_STATEMENT = ms_parser.create_group(
    name="show_profiles_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_PROFILES],
            action=lambda _: ast.ShowProfilesStatement()
        )
    ]
)

# `SHOW RELAYLOG EVENTS` 语句
SHOW_RELAYLOG_EVENTS_STATEMENT = ms_parser.create_group(
    name="show_relaylog_events_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_RELAYLOG, TType.KEYWORD_EVENTS, "opt_binlog_in",
                     "opt_binlog_from", "opt_limit_clause", "opt_for_channel"],
            action=lambda x: ast.ShowRelaylogEventsStatement(
                binlog_in=x[3],
                binlog_from=x[4],
                limit_clause=x[5],
                channel_name=x[6]
            )
        )
    ]
)

# `SHOW REPLICA STATUS` 语句
SHOW_REPLICA_STATUS_STATEMENT = ms_parser.create_group(
    name="show_replica_status_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, "keyword_replica_or_slave", TType.KEYWORD_STATUS, "opt_for_channel"],
            action=lambda x: ast.ShowReplicaStatusStatement(channel_name=x[3])
        )
    ]
)

# `SHOW REPLICAS` 语句
SHOW_REPLICAS_STATEMENT = ms_parser.create_group(
    name="show_replicas_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_REPLICAS, TType.KEYWORD_STATUS],
            action=lambda _: ast.ShowReplicasStatement()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_SLAVE, TType.KEYWORD_HOSTS],
            action=lambda _: ast.ShowReplicasStatement()
        )
    ]
)

# `SHOW STATUS` 语句
SHOW_STATUS_STATEMENT = ms_parser.create_group(
    name="show_status_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, "opt_variable_type", TType.KEYWORD_STATUS, "opt_wild_or_where"],
            action=lambda x: ast.ShowStatusStatement(variable_type=x[1], wild=x[3].wild, where=x[3].where)
        )
    ]
)

# `SHOW TABLE STATUS` 语句
SHOW_TABLE_STATUS_STATEMENT = ms_parser.create_group(
    name="show_table_status_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_TABLE, TType.KEYWORD_STATUS, "opt_show_schema",
                     "opt_wild_or_where"],
            action=lambda x: ast.ShowTableStatusStatement(schema_name=x[3], wild=x[4].wild, where=x[4].where)
        )
    ]
)

# `SHOW TABLES` 语句
SHOW_TABLES_STATEMENT = ms_parser.create_group(
    name="show_tables_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, "opt_show_command_type", TType.KEYWORD_TABLES, "opt_show_schema",
                     "opt_wild_or_where"],
            action=lambda x: ast.ShowTablesStatement(command_type=x[1], schema_name=x[3], wild=x[4].wild,
                                                     where=x[4].where)
        )
    ]
)

# `SHOW TRIGGERS` 语句
SHOW_TRIGGERS_STATEMENT = ms_parser.create_group(
    name="show_triggers_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, "opt_keyword_full", TType.KEYWORD_TRIGGERS, "opt_show_schema",
                     "opt_wild_or_where"],
            action=lambda x: ast.ShowTriggersStatement(is_full=x[1], schema_name=x[3], wild=x[4].wild, where=x[4].where)
        )
    ]
)

# `SHOW WARNINGS` 语句
SHOW_WARNINGS_STATEMENT = ms_parser.create_group(
    name="show_warnings_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, TType.KEYWORD_WARNINGS, "opt_limit_clause"],
            action=lambda x: ast.ShowWarningsStatement(limit_clause=x[2])
        )
    ]
)

# `SHOW VARIABLES` 语句
SHOW_VARIABLES_STATEMENT = ms_parser.create_group(
    name="show_variables_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SHOW, "opt_variable_type", TType.KEYWORD_VARIABLES, "opt_wild_or_where"],
            action=lambda x: ast.ShowVariablesStatement(variable_type=x[1], wild=x[3].wild, where=x[3].where)
        )
    ]
)

# 可选的 `IN` 关键字引导的指定文件名子句
OPT_BINLOG_IN = ms_parser.create_group(
    name="opt_binlog_in",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IN, "text_literal_sys"],
            action=lambda x: x[1].get_str_value()
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的 `FROM` 关键字引导指定位事件开始位置子句
OPT_BINLOG_FROM = ms_parser.create_group(
    name="opt_binlog_from",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FROM, "num_literal"],
            action=lambda x: x[1].value
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的通配符或 `WHERE` 子句
OPT_WILD_OR_WHERE = ms_parser.create_group(
    name="opt_wild_or_where",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LIKE, "text_literal_sys"],
            action=lambda x: ast.TempWildOrWhere(
                wild=x[1].get_str_value(),
                where=None
            )
        ),
        ms_parser.create_rule(
            symbols=["where_clause"],
            action=lambda x: ast.TempWildOrWhere(
                wild=None,
                where=x[0]
            )
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.TempWildOrWhere(
                wild=None,
                where=None
            )
        )
    ]
)

# `SHOW` 语句中可选的数据库名称
OPT_SHOW_SCHEMA = ms_parser.create_group(
    name="opt_show_schema",
    rules=[
        ms_parser.create_rule(
            symbols=["keyword_from_or_in", "ident"],
            action=lambda x: x[1].get_str_value()
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 引擎名称或 `ALL` 关键字
ENGINE_NAME_OR_ALL = ms_parser.create_group(
    name="engine_name_or_all",
    rules=[
        ms_parser.create_rule(
            symbols=["ident_or_text"],
            action=lambda x: x[0].get_str_value()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALL],
            action=ms_parser.template.action.RETURN_NULL
        )
    ]
)

# 可选的 `FOR QUERY` 引导的线程 ID
OPT_FOR_QUERY = ms_parser.create_group(
    name="opt_for_query",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FOR, TType.KEYWORD_QUERY, TType.LITERAL_INT_NUM],
            action=lambda x: int(x[2])
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的 `FOR CHANNEL` 引导的通道名
OPT_FOR_CHANNEL = ms_parser.create_group(
    name="opt_for_channel",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FOR, TType.KEYWORD_CHANNEL, "text_literal_sys"],
            action=lambda x: x[2].get_str_value()
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)
