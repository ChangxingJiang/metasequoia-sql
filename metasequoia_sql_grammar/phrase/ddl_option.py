"""
DDL 选项（ddl option）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    # `CREATE TABLE` 选项
    "CREATE_TABLE_OPTION_LIST",
    "CREATE_TABLE_OPTION_LIST_SPACE_SEPARATED",
    "CREATE_TABLE_OPTION",

    # `CREATE DATABASE` 选项
    "OPT_CREATE_DATABASE_OPTION_LIST",
    "CREATE_DATABASE_OPTION_LIST",
    "CREATE_DATABASE_OPTION",

    # `ALTER DATABASE` 选项
    "ALTER_DATABASE_OPTION_LIST",
    "ALTER_DATABASE_OPTION",

    # `DROP TABLESPACE` 选项列表
    "OPT_DROP_TABLESPACE_OPTION_LIST",
    "DROP_TABLESPACE_OPTION_LIST",
    "DROP_TABLESPACE_OPTION",

    # `DROP UNDO TABLESPACE` 选项列表
    "OPT_DROP_UNDO_TABLESPACE_OPTION_LIST",
    "DROP_UNDO_TABLESPACE_OPTION_LIST",
    "DROP_UNDO_TABLESPACE_OPTION",

    # 基础选项
    "DDL_OPTION_STORAGE_ENGINE",
    "DDL_OPTION_WAIT",
    "DDL_OPTION_DEFAULT_CHARSET",
    "DDL_OPTION_DEFAULT_COLLATE",
    "DDL_OPTION_DEFAULT_ENCRYPTION",
    "DDL_OPTION_AUTOEXTEND_SIZE",
    "DDL_OPTION_INITIAL_SIZE",

    # 选项值
    "TERNARY_OPTION_VALUE",
]

# 逗号或空格分隔的 `CREATE TABLE` 语句中的表属性的列表
CREATE_TABLE_OPTION_LIST = ms_parser.create_group(
    name="create_table_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["create_table_option_list", "opt_comma", "create_table_option"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["create_table_option"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 空格分隔的 `CREATE TABLE` 语句中的表属性的列表
CREATE_TABLE_OPTION_LIST_SPACE_SEPARATED = ms_parser.create_group(
    name="create_table_option_list_space_separated",
    rules=[
        ms_parser.create_rule(
            symbols=["create_table_option_list_space_separated", "create_table_option"],
            action=ms_parser.template.action.LIST_APPEND_1
        ),
        ms_parser.create_rule(
            symbols=["create_table_option"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# `CREATE TABLE` 语句中的表选项
CREATE_TABLE_OPTION = ms_parser.create_group(
    name="create_table_option",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ENGINE, "opt_equal", "ident_or_text"],
            action=lambda x: ast.DdlOptionEngine(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SECONDARY_ENGINE, "opt_equal", TType.KEYWORD_NULL],
            action=lambda x: ast.DdlOptionSecondaryEngine(value=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SECONDARY_ENGINE, "opt_equal", "ident_or_text"],
            action=lambda x: ast.DdlOptionSecondaryEngine(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MAX_ROWS, "opt_equal", "num_literal"],
            action=lambda x: ast.DdlOptionMaxRows(value=x[2].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MIN_ROWS, "opt_equal", "num_literal"],
            action=lambda x: ast.DdlOptionMinRows(value=x[2].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AVG_ROW_LENGTH, "opt_equal", "num_literal"],
            action=lambda x: ast.DdlOptionAvgRowLength(value=x[2].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PASSWORD, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.DdlOptionPassword(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COMMENT, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.DdlOptionComment(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COMPRESSION, "opt_equal", "ident_or_text"],
            action=lambda x: ast.DdlOptionCompression(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ENCRYPTION, "opt_equal", "ident_or_text"],
            action=lambda x: ast.DdlOptionEncryption(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AUTO_INCREMENT, "opt_equal", "num_literal"],
            action=lambda x: ast.DdlOptionAutoIncrement(value=x[2].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PACK_KEYS, "opt_equal", "ternary_option_value"],
            action=lambda x: ast.DdlOptionPackKey(value=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STATS_AUTO_RECALC, "opt_equal", "ternary_option_value"],
            action=lambda x: ast.DdlOptionStatsAutoRecalc(value=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STATS_PERSISTENT, "opt_equal", "ternary_option_value"],
            action=lambda x: ast.DdlOptionStatsPersistent(value=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STATS_SAMPLE_PAGES, "opt_equal", "ternary_option_value"],
            action=lambda x: ast.DdlOptionStatsSamplePages(value=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHECKSUM, "opt_equal", "num_literal_or_hex"],
            action=lambda x: ast.DdlOptionChecksum(value=x[2].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TABLE_CHECKSUM, "opt_equal", "num_literal_or_hex"],
            action=lambda x: ast.DdlOptionTableChecksum(value=x[2].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DELAY_KEY_WRITE, "opt_equal", "num_literal_or_hex"],
            action=lambda x: ast.DdlOptionDelayKeyWrite(value=x[2].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ROW_FORMAT, "opt_equal", "row_format_type"],
            action=lambda x: ast.DdlOptionRowFormat(value=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UNION, "opt_equal", TType.OPERATOR_LPAREN, "opt_identifier_list",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.DdlOptionUnion(table_list=x[3])
        ),
        ms_parser.create_rule(
            symbols=["ddl_option_default_charset"]
        ),
        ms_parser.create_rule(
            symbols=["ddl_option_default_collate"]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INSERT_METHOD, "opt_equal", "merge_insert_type"],
            action=lambda x: ast.DdlOptionInsertMethod(value=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DATA, TType.KEYWORD_DIRECTORY, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.DdlOptionDataDirectory(value=x[3].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INDEX, TType.KEYWORD_DIRECTORY, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.DdlOptionIndexDirectory(value=x[3].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TABLESPACE, "opt_equal", "ident"],
            action=lambda x: ast.DdlOptionTableSpace(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STORAGE, TType.KEYWORD_DISK],
            action=lambda x: ast.DdlOptionStorage(value=ast.EnumStorageType.DISK)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STORAGE, TType.KEYWORD_MEMORY],
            action=lambda x: ast.DdlOptionStorage(value=ast.EnumStorageType.MEMORY)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CONNECTION, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.DdlOptionConnection(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_KEY_BLOCK_SIZE, "opt_equal", "num_literal"],
            action=lambda x: ast.DdlOptionKeyBlockSize(value=x[2].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_START, TType.KEYWORD_TRANSACTION],
            action=lambda _: ast.DdlOptionStartTransaction()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ENGINE_ATTRIBUTE, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.DdlOptionEngineAttribute(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SECONDARY_ENGINE_ATTRIBUTE, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.DdlOptionSecondaryEngineAttribute(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=["ddl_option_autoextend_size"]
        )
    ]
)

# 可选的 `CREATE DATABASE` 语句中的数据库选项列表
OPT_CREATE_DATABASE_OPTION_LIST = ms_parser.create_group(
    name="opt_create_database_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["create_database_option_list"]
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)

# `CREATE DATABASE` 语句中的数据库选项列表
CREATE_DATABASE_OPTION_LIST = ms_parser.create_group(
    name="create_database_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["create_database_option"],
            action=ms_parser.template.action.LIST_INIT_0
        ),
        ms_parser.create_rule(
            symbols=["create_database_option_list", "create_database_option"],
            action=ms_parser.template.action.LIST_APPEND_1
        )
    ]
)

# `CREATE DATABASE` 语句中的数据库选项
CREATE_DATABASE_OPTION = ms_parser.create_group(
    name="create_database_option",
    rules=[
        ms_parser.create_rule(
            symbols=["ddl_option_default_collate"]
        ),
        ms_parser.create_rule(
            symbols=["ddl_option_default_charset"]
        ),
        ms_parser.create_rule(
            symbols=["ddl_option_default_encryption"]
        )
    ]
)

# `ALTER DATABASE` 语句中的数据库选项列表
ALTER_DATABASE_OPTION_LIST = ms_parser.create_group(
    name="alter_database_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["alter_database_option"]
        ),
        ms_parser.create_rule(
            symbols=["alter_database_option_list", "alter_database_option"]
        )
    ]
)

# `ALTER DATABASE` 语句中的数据库选项
ALTER_DATABASE_OPTION = ms_parser.create_group(
    name="alter_database_option",
    rules=[
        ms_parser.create_rule(
            symbols=["create_database_option"]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_READ, TType.KEYWORD_ONLY, "opt_equal", "ternary_option_value"],
            action=lambda x: ast.DdlOptionReadOnly(value=x[3])
        )
    ]
)

# 可选的 `DROP TABLESPACE` 和 `DROP LOGFILE` 的选项的列表
OPT_DROP_TABLESPACE_OPTION_LIST = ms_parser.create_group(
    name="opt_drop_tablespace_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["drop_tablespace_option_list"]
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)

# `DROP TABLESPACE` 和 `DROP LOGFILE` 的选项的列表
DROP_TABLESPACE_OPTION_LIST = ms_parser.create_group(
    name="drop_tablespace_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["drop_tablespace_option_list", "opt_comma", "drop_tablespace_option"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["drop_tablespace_option"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# `DROP TABLESPACE` 和 `DROP LOGFILE` 的选项
DROP_TABLESPACE_OPTION = ms_parser.create_group(
    name="drop_tablespace_option",
    rules=[
        ms_parser.create_rule(
            symbols=["ddl_option_storage_engine"]
        ),
        ms_parser.create_rule(
            symbols=["ddl_option_wait"]
        )
    ]
)

# ALTER 选项：[STORAGE] ENGINE
DDL_OPTION_STORAGE_ENGINE = ms_parser.create_group(
    name="ddl_option_storage_engine",
    rules=[
        ms_parser.create_rule(
            symbols=["opt_keyword_storage", TType.KEYWORD_ENGINE, "opt_equal", "ident_or_text"],
            action=lambda x: ast.DdlOptionStorageEngine(value=x[3].get_str_value())
        )
    ]
)

# ALTER 选项：`WAIT` 或 `NO_WAIT`
DDL_OPTION_WAIT = ms_parser.create_group(
    name="ddl_option_wait",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WAIT],
            action=lambda _: ast.DdlOptionWait(value=True)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NO_WAIT],
            action=lambda _: ast.DdlOptionWait(value=False)
        )
    ]
)

# 可选的 `UNDO TABLESPACE` 的选项的列表
OPT_DROP_UNDO_TABLESPACE_OPTION_LIST = ms_parser.create_group(
    name="opt_drop_undo_tablespace_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["drop_undo_tablespace_option_list"]
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)

# `UNDO TABLESPACE` 的选项的列表
DROP_UNDO_TABLESPACE_OPTION_LIST = ms_parser.create_group(
    name="drop_undo_tablespace_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["drop_undo_tablespace_option_list", "opt_comma", "drop_undo_tablespace_option"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["drop_undo_tablespace_option"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# `UNDO TABLESPACE` 的选项
DROP_UNDO_TABLESPACE_OPTION = ms_parser.create_group(
    name="drop_undo_tablespace_option",
    rules=[
        ms_parser.create_rule(
            symbols=["ddl_option_storage_engine"]
        )
    ]
)

# 整数字面值、十六进制字面值或 `DEFAULT` 关键字
TERNARY_OPTION_VALUE = ms_parser.create_group(
    name="ternary_option_value",
    rules=[
        ms_parser.create_rule(
            symbols=["num_literal_or_hex"]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DEFAULT],
            action=lambda _: ast.DefaultValue()
        )
    ]
)

# 指定默认字符集的数据库选项或表选项
DDL_OPTION_DEFAULT_CHARSET = ms_parser.create_group(
    name="ddl_option_default_charset",
    rules=[
        ms_parser.create_rule(
            symbols=["opt_keyword_default", "keyword_charset", "opt_equal", "charset_name"],
            action=lambda x: ast.DdlOptionDefaultCharset(value=x[3])
        )
    ]
)

# 指定默认排序规则的数据库选项或表选项
DDL_OPTION_DEFAULT_COLLATE = ms_parser.create_group(
    name="ddl_option_default_collate",
    rules=[
        ms_parser.create_rule(
            symbols=["opt_keyword_default", TType.KEYWORD_COLLATE, "opt_equal", "charset_name"],
            action=lambda x: ast.DdlOptionDefaultCollate(value=x[3])
        )
    ]
)

# 指定默认加密的数据库选项
DDL_OPTION_DEFAULT_ENCRYPTION = ms_parser.create_group(
    name="ddl_option_default_encryption",
    rules=[
        ms_parser.create_rule(
            symbols=["opt_keyword_default", TType.KEYWORD_ENCRYPTION, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.DdlOptionDefaultEncryption(value=x[3].get_str_value())
        )
    ]
)

# 指定表空间每次自动扩展的大小属性
DDL_OPTION_AUTOEXTEND_SIZE = ms_parser.create_group(
    name="ddl_option_autoextend_size",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AUTOEXTEND_SIZE, "opt_equal", "size_number"],
            action=lambda x: ast.DdlOptionAutoextendSize(value=x[2])
        )
    ]
)

# 指定表空间初始大小的属性
DDL_OPTION_INITIAL_SIZE = ms_parser.create_group(
    name="ddl_option_initial_size",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INITIAL_SIZE, "opt_equal", "size_number"],
            action=lambda x: ast.DdlOptionInitialSize(value=x[2])
        )
    ]
)
