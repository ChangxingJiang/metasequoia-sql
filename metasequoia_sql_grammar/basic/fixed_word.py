# pylint: disable=C0302,R0801

"""
固定的词语组合
"""

import metasequoia_parser as ms_parser

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    # 可选的关键字
    "OPT_KEYWORD_IF_NOT_EXISTS",
    "OPT_KEYWORD_IF_EXISTS",
    "OPT_KEYWORD_NO_WRITE_TO_BINLOG",
    "OPT_KEYWORD_VALUE",
    "OPT_KEYWORD_PRIVILEGES",
    "OPT_KEYWORD_WITH_ADMIN_OPTION",
    "OPT_KEYWORD_IGNORE_UNKNOWN_USER",
    "OPT_KEYWORD_GRANT_OPTION",
    "OPT_KEYWORD_CONVERT_XID",
    "OPT_KEYWORD_ONE_PHASE",
    "OPT_KEYWORD_COLUMN",
    "OPT_KEYWORD_ON_REPLACE",
    "OPT_KEYWORD_AND",
    "OPT_KEYWORD_RETAIN_CURRENT_PASSWORD",
    "OPT_KEYWORD_DISCARD_OLD_PASSWORD",
    "OPT_KEYWORD_IGNORE_LEAVES",

    # 多种备选的关键字
    "KEYWORD_BEGIN_OR_START",
    "KEYWORD_NEXT_FROM_OR_FROM",
    "KEYWORD_DEALLOCATE_OR_DROP",
    "KEYWORD_DESCRIBE_OR_EXPLAIN",
    "KEYWORD_TABLE_OR_TABLES",
    "KEYWORD_MASTER_OR_BINARY",
    "KEYWORD_FROM_OR_IN",
    "KEYWORD_KEYS_OR_INDEX",
    "KEYWORD_REPLICA_OR_SLAVE",
    "KEYWORD_MASTER_OR_BINARY_LOGS_AND_GTIDS",
    "KEYWORD_CHARSET",
    "KEYWORD_NCHAR",
    "KEYWORD_VARCHAR",
    "KEYWORD_NVARCHAR",
    "KEYWORD_VISIBLE_OR_INVISIBLE",

    # 复制源相关的关键字组合
    "KEYWORD_MASTER_AUTO_POSITION_OR_SOURCE_AUTO_POSITION",
    "KEYWORD_MASTER_HOST_OR_SOURCE_HOST",
    "KEYWORD_MASTER_BIND_OR_SOURCE_BIND",
    "KEYWORD_MASTER_USER_OR_SOURCE_USER",
    "KEYWORD_MASTER_PASSWORD_OR_SOURCE_PASSWORD",
    "KEYWORD_MASTER_PORT_OR_SOURCE_PORT",
    "KEYWORD_MASTER_CONNECT_RETRY_OR_SOURCE_CONNECT_RETRY",
    "KEYWORD_MASTER_RETRY_COUNT_OR_SOURCE_RETRY_COUNT",
    "KEYWORD_MASTER_DELAY_OR_SOURCE_DELAY",
    "KEYWORD_MASTER_SSL_OR_SOURCE_SSL",
    "KEYWORD_MASTER_SSL_CA_OR_SOURCE_SSL_CA",
    "KEYWORD_MASTER_SSL_CAPATH_OR_SOURCE_SSL_CAPATH",
    "KEYWORD_MASTER_SSL_CIPHER_OR_SOURCE_SSL_CIPHER",
    "KEYWORD_MASTER_SSL_CRL_OR_SOURCE_SSL_CRL",
    "KEYWORD_MASTER_SSL_CRLPATH_OR_SOURCE_SSL_CRLPATH",
    "KEYWORD_MASTER_SSL_KEY_OR_SOURCE_SSL_KEY",
    "KEYWORD_MASTER_SSL_VERIFY_SERVER_CERT_OR_SOURCE_SSL_VERIFY_SERVER_CERT",
    "KEYWORD_MASTER_TLS_VERSION_OR_SOURCE_TLS_VERSION",
    "KEYWORD_MASTER_TLS_CIPHERSUITES_OR_SOURCE_TLS_CIPHERSUITES",
    "KEYWORD_MASTER_SSL_CERT_OR_SOURCE_SSL_CERT",
    "KEYWORD_MASTER_PUBLIC_KEY_PATH_OR_SOURCE_PUBLIC_KEY_PATH",
    "KEYWORD_GET_MASTER_PUBLIC_KEY_OR_GET_SOURCE_PUBLIC_KEY",
    "KEYWORD_MASTER_HEARTBEAT_PERIOD_OR_SOURCE_HEARTBEAT_PERIOD",
    "KEYWORD_MASTER_COMPRESSION_ALGORITHM_OR_SOURCE_COMPRESSION_ALGORITHM",
    "KEYWORD_MASTER_ZSTD_COMPRESSION_LEVEL_OR_SOURCE_ZSTD_COMPRESSION_LEVEL",
    "KEYWORD_MASTER_LOG_FILE_OR_SOURCE_LOG_FILE",
    "KEYWORD_MASTER_LOG_POS_OR_SOURCE_LOG_POS",

    # 可选的运算符
    "OPT_BRACES",
    "OPT_COMMA",
    "OPT_EQUAL",
    "EQUAL",
    "OPT_TO_OR_EQ_OR_AS",

    # LOAD 语句相关的固定词语组合
    "OPT_KEYWORD_LOCAL",
    "OPT_KEYWORD_IN_PRIMARY_KEY_ORDER",
    "KEYWORD_LINES_OR_ROWS",
]

# `DESCRIBE` 关键字或 `EXPLAIN` 关键字
KEYWORD_DESCRIBE_OR_EXPLAIN = ms_parser.create_group(
    name="keyword_describe_or_explain",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DESCRIBE],
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DESC],
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXPLAIN],
        )
    ]
)

# `TABLE` 关键字或 `TABLES` 关键字
KEYWORD_TABLE_OR_TABLES = ms_parser.create_group(
    name="keyword_table_or_tables",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TABLE],
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TABLES],
        )
    ]
)

# `MASTER` 关键字或 `BINARY` 关键字
KEYWORD_MASTER_OR_BINARY = ms_parser.create_group(
    name="keyword_master_or_binary",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER],
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BINARY],
        )
    ]
)

# `FROM` 关键字或 `IN` 关键字
KEYWORD_FROM_OR_IN = ms_parser.create_group(
    name="keyword_from_or_in",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FROM],
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IN],
        )
    ]
)

# `KEYS`、`INDEX` 或 `INDEXES` 关键字
KEYWORD_KEYS_OR_INDEX = ms_parser.create_group(
    name="keyword_keys_or_index",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_KEYS]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INDEX]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INDEXES]
        )
    ]
)

# `REPLICA` 或 `SLAVE` 关键字
KEYWORD_REPLICA_OR_SLAVE = ms_parser.create_group(
    name="keyword_replica_or_slave",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REPLICA]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SLAVE]
        )
    ]
)

# 可选的 `IF NOT EXISTS` 关键字
OPT_KEYWORD_IF_NOT_EXISTS = ms_parser.create_group(
    name="opt_keyword_if_not_exists",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IF, TType.KEYWORD_NOT, TType.KEYWORD_EXISTS],
            action=ms_parser.template.action.RETURN_TRUE
        ),
        ms_parser.create_rule(
            symbols=[],
            action=ms_parser.template.action.RETURN_FALSE
        )
    ]
)

# 可选的 `IF EXISTS` 关键字
OPT_KEYWORD_IF_EXISTS = ms_parser.create_group(
    name="opt_keyword_if_exists",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IF, TType.KEYWORD_EXISTS],
            action=ms_parser.template.action.RETURN_TRUE
        ),
        ms_parser.create_rule(
            symbols=[],
            action=ms_parser.template.action.RETURN_FALSE
        )
    ]
)

# 可选的 `NO_WRITE_TO_BINLOG` 关键字或 `LOCAL` 关键字
OPT_KEYWORD_NO_WRITE_TO_BINLOG = ms_parser.create_group(
    name="opt_keyword_no_write_to_binlog",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NO_WRITE_TO_BINLOG],
            action=ms_parser.template.action.RETURN_TRUE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOCAL],
            action=ms_parser.template.action.RETURN_TRUE
        ),
        ms_parser.create_rule(
            symbols=[],
            action=ms_parser.template.action.RETURN_FALSE
        )
    ]
)

# 可选的 `VALUE` 关键字
OPT_KEYWORD_VALUE = ms_parser.create_group(
    name="opt_keyword_value",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_VALUE]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的 `CONVERT XID` 关键字组合
OPT_KEYWORD_CONVERT_XID = ms_parser.create_group(
    name="opt_keyword_convert_xid",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: False
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CONVERT, TType.KEYWORD_XID],
            action=lambda x: True
        )
    ]
)

# 可选的 `ONE PHASE` 关键字组合
OPT_KEYWORD_ONE_PHASE = ms_parser.create_group(
    name="opt_keyword_one_phase",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: False
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ONE, TType.KEYWORD_PHASE],
            action=lambda x: True
        )
    ]
)

# 可选的 `ON REPLACE` 关键字组合
OPT_KEYWORD_ON_REPLACE = ms_parser.create_group(
    name="opt_keyword_on_replace",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ON, TType.KEYWORD_REPLACE],
            action=ms_parser.template.action.RETURN_TRUE
        ),
        ms_parser.create_rule(
            symbols=[],
            action=ms_parser.template.action.RETURN_FALSE
        )
    ]
)

# 可选的 `AND` 关键字
OPT_KEYWORD_AND = ms_parser.create_group(
    name="opt_keyword_and",
    rules=[
        ms_parser.template.rule.EMPTY_RETURN_NULL,
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AND],
            action=lambda _: None
        )
    ]
)

# `DEALLOCATE` 关键字或 `DROP` 关键字
KEYWORD_DEALLOCATE_OR_DROP = ms_parser.create_group(
    name="keyword_deallocate_or_drop",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DEALLOCATE]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP]
        )
    ]
)

# `MASTER` 关键字或 `BINARY LOGS AND GTIDS` 关键字组合
KEYWORD_MASTER_OR_BINARY_LOGS_AND_GTIDS = ms_parser.create_group(
    name="keyword_master_or_binary_logs_and_gtids",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BINARY, TType.KEYWORD_LOGS, TType.KEYWORD_AND, TType.KEYWORD_GTIDS]
        )
    ]
)

# 可选的 `PRIVILEGES` 关键字
OPT_KEYWORD_PRIVILEGES = ms_parser.create_group(
    name="opt_keyword_privileges",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PRIVILEGES]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的 `WITH ADMIN OPTION` 关键字组合
OPT_KEYWORD_WITH_ADMIN_OPTION = ms_parser.create_group(
    name="opt_keyword_with_admin_option",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: False
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITH, TType.KEYWORD_ADMIN, TType.KEYWORD_OPTION],
            action=lambda x: True
        )
    ]
)

# 可选的 `IGNORE UNKNOWN USER` 关键字组合
OPT_KEYWORD_IGNORE_UNKNOWN_USER = ms_parser.create_group(
    name="opt_keyword_ignore_unknown_user",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: False
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IGNORE, TType.KEYWORD_UNKNOWN, TType.KEYWORD_USER],
            action=lambda x: True
        )
    ]
)

# 可选的 `WITH GRANT OPTION` 关键字组合（合并 grant_options 和 opt_grant_option）
OPT_KEYWORD_GRANT_OPTION = ms_parser.create_group(
    name="opt_keyword_grant_option",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: False
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITH, TType.KEYWORD_GRANT, TType.KEYWORD_OPTION],
            action=lambda x: True
        )
    ]
)

# 可选的 `COLUMN` 关键字
OPT_KEYWORD_COLUMN = ms_parser.create_group(
    name="opt_keyword_column",
    rules=[
        ms_parser.create_rule(
            symbols=[]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COLUMN]
        )
    ]
)

# `BEGIN` 关键字或 `START` 关键字
KEYWORD_BEGIN_OR_START = ms_parser.create_group(
    name="keyword_begin_or_start",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BEGIN]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_START]
        )
    ]
)

# 可选的 `NEXT FROM` 或 `FROM` 关键字，用于 FETCH 语法中的噪声词
KEYWORD_NEXT_FROM_OR_FROM = ms_parser.create_group(
    name="keyword_next_from_or_from",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NEXT, TType.KEYWORD_FROM]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FROM]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的空括号
OPT_BRACES = ms_parser.create_group(
    name="opt_braces",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, TType.OPERATOR_RPAREN]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的逗号
OPT_COMMA = ms_parser.create_group(
    name="opt_comma",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_COMMA]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# `CHARSET` 关键字或 `CHAR SET` 关键字
KEYWORD_CHARSET = ms_parser.create_group(
    name="keyword_charset",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHAR, TType.KEYWORD_SET],
            action=lambda _: None
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHARSET],
            action=lambda _: None
        )
    ]
)

# `NCHAR` 关键字或 `NATIONAL CHAR` 关键字（兼容的 `NCHAR` 类型名称）
KEYWORD_NCHAR = ms_parser.create_group(
    name="keyword_nchar",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NCHAR],
            action=lambda _: None
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NATIONAL, TType.KEYWORD_CHAR],
            action=lambda _: None
        )
    ]
)

# `CHAR VARYING` 关键字或 `VARCHAR` 关键字（兼容的 `VARCHAR` 类型名称）
KEYWORD_VARCHAR = ms_parser.create_group(
    name="keyword_varchar",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_VARCHAR],
            action=lambda _: None
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHAR, TType.KEYWORD_VARYING],
            action=lambda _: None
        )
    ]
)

# `NVARCHAR` 关键字、`NATIONAL VARCHAR` 关键字、`NCHAR VARCHAR` 关键字、`NATIONAL CHAR VARYING` 关键字或 `NCHAR VARYING` 关键字
# （兼容的 `NVARCHAR` 类型名称）
KEYWORD_NVARCHAR = ms_parser.create_group(
    name="keyword_nvarchar",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NVARCHAR],
            action=lambda _: None
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NATIONAL, TType.KEYWORD_VARCHAR],
            action=lambda _: None
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NCHAR, TType.KEYWORD_VARCHAR],
            action=lambda _: None
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NATIONAL, TType.KEYWORD_CHAR, TType.KEYWORD_VARYING],
            action=lambda _: None
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NCHAR, TType.KEYWORD_VARYING],
            action=lambda _: None
        )
    ]
)

# `VISIBLE` 关键字或 `INVISIBLE` 关键字
KEYWORD_VISIBLE_OR_INVISIBLE = ms_parser.create_group(
    name="keyword_visible_or_invisible",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_VISIBLE],
            action=lambda _: True
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INVISIBLE],
            action=lambda _: False
        )
    ]
)

# `MASTER_LOG_FILE` 关键字或 `SOURCE_LOG_FILE` 关键字
KEYWORD_MASTER_LOG_FILE_OR_SOURCE_LOG_FILE = ms_parser.create_group(
    name="keyword_master_log_file_or_source_log_file",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_LOG_FILE]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_LOG_FILE]
        )
    ]
)

# `MASTER_LOG_POS` 关键字或 `SOURCE_LOG_POS` 关键字
KEYWORD_MASTER_LOG_POS_OR_SOURCE_LOG_POS = ms_parser.create_group(
    name="keyword_master_log_pos_or_source_log_pos",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_LOG_POS]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_LOG_POS]
        )
    ]
)

# 可选的 `=` 运算符或 `:=` 运算符
OPT_EQUAL = ms_parser.create_group(
    name="opt_equal",
    rules=[
        ms_parser.create_rule(
            symbols=["equal"]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# `=` 运算符或 `:=` 运算符
EQUAL = ms_parser.create_group(
    name="equal",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_EQ]
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_COLON_EQ]
        )
    ]
)

# `TO` 关键字、`=` 运算符或 `AS` 关键字
OPT_TO_OR_EQ_OR_AS = ms_parser.create_group(
    name="opt_to_or_eq_or_as",
    rules=[
        ms_parser.create_rule(
            symbols=[]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TO]
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_EQ]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AS]
        )
    ]
)

# 可选的 `LOCAL` 关键字
OPT_KEYWORD_LOCAL = ms_parser.create_group(
    name="opt_keyword_local",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: False
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOCAL],
            action=lambda _: True
        )
    ]
)

# 可选的 `IN PRIMARY KEY ORDER` 关键字组合
OPT_KEYWORD_IN_PRIMARY_KEY_ORDER = ms_parser.create_group(
    name="opt_keyword_in_primary_key_order",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: False
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IN, TType.KEYWORD_PRIMARY, TType.KEYWORD_KEY, TType.KEYWORD_ORDER],
            action=lambda _: True
        )
    ]
)

# `LINES` 关键字或 `ROWS` 关键字
KEYWORD_LINES_OR_ROWS = ms_parser.create_group(
    name="keyword_lines_or_rows",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LINES]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ROWS]
        )
    ]
)

# `MASTER_AUTO_POSITION` 关键字或 `SOURCE_AUTO_POSITION` 关键字
KEYWORD_MASTER_AUTO_POSITION_OR_SOURCE_AUTO_POSITION = ms_parser.create_group(
    name="keyword_master_auto_position_or_source_auto_position",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_AUTO_POSITION]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_AUTO_POSITION]
        )
    ]
)

# `MASTER_HOST` 关键字或 `SOURCE_HOST` 关键字
KEYWORD_MASTER_HOST_OR_SOURCE_HOST = ms_parser.create_group(
    name="keyword_master_host_or_source_host",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_HOST]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_HOST]
        )
    ]
)

# `MASTER_BIND` 关键字或 `SOURCE_BIND` 关键字
KEYWORD_MASTER_BIND_OR_SOURCE_BIND = ms_parser.create_group(
    name="keyword_master_bind_or_source_bind",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_BIND]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_BIND]
        )
    ]
)

# `MASTER_USER` 关键字或 `SOURCE_USER` 关键字
KEYWORD_MASTER_USER_OR_SOURCE_USER = ms_parser.create_group(
    name="keyword_master_user_or_source_user",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_USER]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_USER]
        )
    ]
)

# `MASTER_PASSWORD` 关键字或 `SOURCE_PASSWORD` 关键字
KEYWORD_MASTER_PASSWORD_OR_SOURCE_PASSWORD = ms_parser.create_group(
    name="keyword_master_password_or_source_password",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_PASSWORD]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_PASSWORD]
        )
    ]
)

# `MASTER_PORT` 关键字或 `SOURCE_PORT` 关键字
KEYWORD_MASTER_PORT_OR_SOURCE_PORT = ms_parser.create_group(
    name="keyword_master_port_or_source_port",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_PORT]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_PORT]
        )
    ]
)

# `MASTER_CONNECT_RETRY` 关键字或 `SOURCE_CONNECT_RETRY` 关键字
KEYWORD_MASTER_CONNECT_RETRY_OR_SOURCE_CONNECT_RETRY = ms_parser.create_group(
    name="keyword_master_connect_retry_or_source_connect_retry",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_CONNECT_RETRY]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_CONNECT_RETRY]
        )
    ]
)

# `MASTER_RETRY_COUNT` 关键字或 `SOURCE_RETRY_COUNT` 关键字
KEYWORD_MASTER_RETRY_COUNT_OR_SOURCE_RETRY_COUNT = ms_parser.create_group(
    name="keyword_master_retry_count_or_source_retry_count",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_RETRY_COUNT]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_RETRY_COUNT]
        )
    ]
)

# `MASTER_DELAY` 关键字或 `SOURCE_DELAY` 关键字
KEYWORD_MASTER_DELAY_OR_SOURCE_DELAY = ms_parser.create_group(
    name="keyword_master_delay_or_source_delay",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_DELAY]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_DELAY]
        )
    ]
)

# `MASTER_SSL` 关键字或 `SOURCE_SSL` 关键字
KEYWORD_MASTER_SSL_OR_SOURCE_SSL = ms_parser.create_group(
    name="keyword_master_ssl_or_source_ssl",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_SSL]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_SSL]
        )
    ]
)

# `MASTER_SSL_CA` 关键字或 `SOURCE_SSL_CA` 关键字
KEYWORD_MASTER_SSL_CA_OR_SOURCE_SSL_CA = ms_parser.create_group(
    name="keyword_master_ssl_ca_or_source_ssl_ca",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_SSL_CA]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_SSL_CA]
        )
    ]
)

# `MASTER_SSL_CAPATH` 关键字或 `SOURCE_SSL_CAPATH` 关键字
KEYWORD_MASTER_SSL_CAPATH_OR_SOURCE_SSL_CAPATH = ms_parser.create_group(
    name="keyword_master_ssl_capath_or_source_ssl_capath",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_SSL_CAPATH]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_SSL_CAPATH]
        )
    ]
)

# `MASTER_SSL_CIPHER` 关键字或 `SOURCE_SSL_CIPHER` 关键字
KEYWORD_MASTER_SSL_CIPHER_OR_SOURCE_SSL_CIPHER = ms_parser.create_group(
    name="keyword_master_ssl_cipher_or_source_ssl_cipher",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_SSL_CIPHER]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_SSL_CIPHER]
        )
    ]
)

# `MASTER_SSL_CRL` 关键字或 `SOURCE_SSL_CRL` 关键字
KEYWORD_MASTER_SSL_CRL_OR_SOURCE_SSL_CRL = ms_parser.create_group(
    name="keyword_master_ssl_crl_or_source_ssl_crl",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_SSL_CRL]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_SSL_CRL]
        )
    ]
)

# `MASTER_SSL_CRLPATH` 关键字或 `SOURCE_SSL_CRLPATH` 关键字
KEYWORD_MASTER_SSL_CRLPATH_OR_SOURCE_SSL_CRLPATH = ms_parser.create_group(
    name="keyword_master_ssl_crlpath_or_source_ssl_crlpath",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_SSL_CRLPATH]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_SSL_CRLPATH]
        )
    ]
)

# `MASTER_SSL_KEY` 关键字或 `SOURCE_SSL_KEY` 关键字
KEYWORD_MASTER_SSL_KEY_OR_SOURCE_SSL_KEY = ms_parser.create_group(
    name="keyword_master_ssl_key_or_source_ssl_key",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_SSL_KEY]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_SSL_KEY]
        )
    ]
)

# `MASTER_SSL_VERIFY_SERVER_CERT` 关键字或 `SOURCE_SSL_VERIFY_SERVER_CERT` 关键字
KEYWORD_MASTER_SSL_VERIFY_SERVER_CERT_OR_SOURCE_SSL_VERIFY_SERVER_CERT = ms_parser.create_group(
    name="keyword_master_ssl_verify_server_cert_or_source_ssl_verify_server_cert",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_SSL_VERIFY_SERVER_CERT]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_SSL_VERIFY_SERVER_CERT]
        )
    ]
)

# `MASTER_TLS_VERSION` 关键字或 `SOURCE_TLS_VERSION` 关键字
KEYWORD_MASTER_TLS_VERSION_OR_SOURCE_TLS_VERSION = ms_parser.create_group(
    name="keyword_master_tls_version_or_source_tls_version",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_TLS_VERSION]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_TLS_VERSION]
        )
    ]
)

# `MASTER_TLS_CIPHERSUITES` 关键字或 `SOURCE_TLS_CIPHERSUITES` 关键字
KEYWORD_MASTER_TLS_CIPHERSUITES_OR_SOURCE_TLS_CIPHERSUITES = ms_parser.create_group(
    name="keyword_master_tls_ciphersuites_or_source_tls_ciphersuites",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_TLS_CIPHERSUITES]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_TLS_CIPHERSUITES]
        )
    ]
)

# `MASTER_SSL_CERT` 关键字或 `SOURCE_SSL_CERT` 关键字
KEYWORD_MASTER_SSL_CERT_OR_SOURCE_SSL_CERT = ms_parser.create_group(
    name="keyword_master_ssl_cert_or_source_ssl_cert",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_SSL_CERT]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_SSL_CERT]
        )
    ]
)

# `MASTER_PUBLIC_KEY_PATH` 关键字或 `SOURCE_PUBLIC_KEY_PATH` 关键字
KEYWORD_MASTER_PUBLIC_KEY_PATH_OR_SOURCE_PUBLIC_KEY_PATH = ms_parser.create_group(
    name="keyword_master_public_key_path_or_source_public_key_path",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_PUBLIC_KEY_PATH]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_PUBLIC_KEY_PATH]
        )
    ]
)

# `GET_MASTER_PUBLIC_KEY` 关键字或 `GET_SOURCE_PUBLIC_KEY` 关键字
KEYWORD_GET_MASTER_PUBLIC_KEY_OR_GET_SOURCE_PUBLIC_KEY = ms_parser.create_group(
    name="keyword_get_master_public_key_or_get_source_public_key",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GET_MASTER_PUBLIC_KEY]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GET_SOURCE_PUBLIC_KEY]
        )
    ]
)

# `MASTER_HEARTBEAT_PERIOD` 关键字或 `SOURCE_HEARTBEAT_PERIOD` 关键字
KEYWORD_MASTER_HEARTBEAT_PERIOD_OR_SOURCE_HEARTBEAT_PERIOD = ms_parser.create_group(
    name="keyword_master_heartbeat_period_or_source_heartbeat_period",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_HEARTBEAT_PERIOD]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_HEARTBEAT_PERIOD]
        )
    ]
)

# `MASTER_COMPRESSION_ALGORITHM` 关键字或 `SOURCE_COMPRESSION_ALGORITHM` 关键字
KEYWORD_MASTER_COMPRESSION_ALGORITHM_OR_SOURCE_COMPRESSION_ALGORITHM = ms_parser.create_group(
    name="keyword_master_compression_algorithm_or_source_compression_algorithm",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_COMPRESSION_ALGORITHM]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_COMPRESSION_ALGORITHM]
        )
    ]
)

# `MASTER_ZSTD_COMPRESSION_LEVEL` 关键字或 `SOURCE_ZSTD_COMPRESSION_LEVEL` 关键字
KEYWORD_MASTER_ZSTD_COMPRESSION_LEVEL_OR_SOURCE_ZSTD_COMPRESSION_LEVEL = ms_parser.create_group(
    name="keyword_master_zstd_compression_level_or_source_zstd_compression_level",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MASTER_ZSTD_COMPRESSION_LEVEL]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_ZSTD_COMPRESSION_LEVEL]
        )
    ]
)

# 可选的 `RETAIN CURRENT PASSWORD` 关键字组合
OPT_KEYWORD_RETAIN_CURRENT_PASSWORD = ms_parser.create_group(
    name="opt_keyword_retain_current_password",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RETAIN, TType.KEYWORD_CURRENT, TType.KEYWORD_PASSWORD],
            action=ms_parser.template.action.RETURN_TRUE
        ),
        ms_parser.create_rule(
            symbols=[],
            action=ms_parser.template.action.RETURN_FALSE
        )
    ]
)

# 可选的 `DISCARD OLD PASSWORD` 关键字组合
OPT_KEYWORD_DISCARD_OLD_PASSWORD = ms_parser.create_group(
    name="opt_keyword_discard_old_password",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DISCARD, TType.KEYWORD_OLD, TType.KEYWORD_PASSWORD],
            action=ms_parser.template.action.RETURN_TRUE
        ),
        ms_parser.create_rule(
            symbols=[],
            action=ms_parser.template.action.RETURN_FALSE
        )
    ]
)

# 可选的 `IGNORE LEAVES` 关键字组合
OPT_KEYWORD_IGNORE_LEAVES = ms_parser.create_group(
    name="opt_keyword_ignore_leaves",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IGNORE, TType.KEYWORD_LEAVES],
            action=ms_parser.template.action.RETURN_TRUE
        ),
        ms_parser.create_rule(
            symbols=[],
            action=ms_parser.template.action.RETURN_FALSE
        )
    ]
)
