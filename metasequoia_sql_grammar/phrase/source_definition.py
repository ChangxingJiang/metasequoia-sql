"""
复制源定义（source definition）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "SOURCE_DEF_LIST",
    "SOURCE_DEF",
    "SOURCE_FILE_DEF",
    "ASSIGN_GTIDS_TYPE",
]

# 复制源定义的列表
SOURCE_DEF_LIST = ms_parser.create_group(
    name="source_def_list",
    rules=[
        ms_parser.create_rule(
            symbols=["source_def_list", TType.OPERATOR_COMMA, "source_def"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["source_def"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 复制源定义
SOURCE_DEF = ms_parser.create_group(
    name="source_def",
    rules=[
        # MASTER_HOST/SOURCE_HOST = TEXT_STRING_sys_nonewline
        ms_parser.create_rule(
            symbols=["keyword_master_host_or_source_host", TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.SourceHostDefinition(x[2].get_str_value())
        ),
        # NETWORK_NAMESPACE = TEXT_STRING_sys_nonewline
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NETWORK_NAMESPACE, TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.NetworkNamespaceDefinition(x[2].get_str_value())
        ),
        # MASTER_BIND/SOURCE_BIND = TEXT_STRING_sys_nonewline
        ms_parser.create_rule(
            symbols=["keyword_master_bind_or_source_bind", TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.SourceBindDefinition(x[2].get_str_value())
        ),
        # MASTER_USER/SOURCE_USER = TEXT_STRING_sys_nonewline
        ms_parser.create_rule(
            symbols=["keyword_master_user_or_source_user", TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.SourceUserDefinition(x[2].get_str_value())
        ),
        # MASTER_PASSWORD/SOURCE_PASSWORD = TEXT_STRING_sys_nonewline
        ms_parser.create_rule(
            symbols=["keyword_master_password_or_source_password", TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.SourcePasswordDefinition(x[2].get_str_value())
        ),
        # MASTER_PORT/SOURCE_PORT = ulong_num
        ms_parser.create_rule(
            symbols=["keyword_master_port_or_source_port", TType.OPERATOR_EQ, "num_literal_or_hex"],
            action=lambda x: ast.SourcePortDefinition(x[2].value)
        ),
        # MASTER_CONNECT_RETRY/SOURCE_CONNECT_RETRY = ulong_num
        ms_parser.create_rule(
            symbols=["keyword_master_connect_retry_or_source_connect_retry", TType.OPERATOR_EQ, "num_literal_or_hex"],
            action=lambda x: ast.SourceConnectRetryDefinition(x[2].value)
        ),
        # MASTER_RETRY_COUNT/SOURCE_RETRY_COUNT = ulong_num
        ms_parser.create_rule(
            symbols=["keyword_master_retry_count_or_source_retry_count", TType.OPERATOR_EQ, "num_literal_or_hex"],
            action=lambda x: ast.SourceRetryCountDefinition(x[2].value)
        ),
        # MASTER_DELAY/SOURCE_DELAY = ulong_num
        ms_parser.create_rule(
            symbols=["keyword_master_delay_or_source_delay", TType.OPERATOR_EQ, "num_literal_or_hex"],
            action=lambda x: ast.SourceDelayDefinition(x[2].value)
        ),
        # MASTER_SSL/SOURCE_SSL = ulong_num
        ms_parser.create_rule(
            symbols=["keyword_master_ssl_or_source_ssl", TType.OPERATOR_EQ, "num_literal_or_hex"],
            action=lambda x: ast.SourceSslDefinition(x[2].value)
        ),
        # MASTER_SSL_CA/SOURCE_SSL_CA = TEXT_STRING_sys_nonewline
        ms_parser.create_rule(
            symbols=["keyword_master_ssl_ca_or_source_ssl_ca", TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.SourceSslCaDefinition(x[2].get_str_value())
        ),
        # MASTER_SSL_CAPATH/SOURCE_SSL_CAPATH = TEXT_STRING_sys_nonewline
        ms_parser.create_rule(
            symbols=["keyword_master_ssl_capath_or_source_ssl_capath", TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.SourceSslCapathDefinition(x[2].get_str_value())
        ),
        # MASTER_TLS_VERSION/SOURCE_TLS_VERSION = TEXT_STRING_sys_nonewline
        ms_parser.create_rule(
            symbols=["keyword_master_tls_version_or_source_tls_version", TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.SourceTlsVersionDefinition(x[2].get_str_value())
        ),
        # MASTER_TLS_CIPHERSUITES/SOURCE_TLS_CIPHERSUITES = source_tls_ciphersuites_def
        ms_parser.create_rule(
            symbols=["keyword_master_tls_ciphersuites_or_source_tls_ciphersuites", TType.OPERATOR_EQ,
                     "text_literal_sys_or_null"],
            action=lambda x: ast.SourceTlsCiphersuitesDefinition(x[2])
        ),
        # MASTER_SSL_CERT/SOURCE_SSL_CERT = TEXT_STRING_sys_nonewline
        ms_parser.create_rule(
            symbols=["keyword_master_ssl_cert_or_source_ssl_cert", TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.SourceSslCertDefinition(x[2].get_str_value())
        ),
        # MASTER_SSL_CIPHER/SOURCE_SSL_CIPHER = TEXT_STRING_sys_nonewline
        ms_parser.create_rule(
            symbols=["keyword_master_ssl_cipher_or_source_ssl_cipher", TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.SourceSslCipherDefinition(x[2].get_str_value())
        ),
        # MASTER_SSL_KEY/SOURCE_SSL_KEY = TEXT_STRING_sys_nonewline
        ms_parser.create_rule(
            symbols=["keyword_master_ssl_key_or_source_ssl_key", TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.SourceSslKeyDefinition(x[2].get_str_value())
        ),
        # MASTER_SSL_VERIFY_SERVER_CERT/SOURCE_SSL_VERIFY_SERVER_CERT = ulong_num
        ms_parser.create_rule(
            symbols=["keyword_master_ssl_verify_server_cert_or_source_ssl_verify_server_cert", TType.OPERATOR_EQ,
                     "num_literal_or_hex"],
            action=lambda x: ast.SourceSslVerifyServerCertDefinition(x[2].value)
        ),
        # MASTER_SSL_CRL/SOURCE_SSL_CRL = TEXT_STRING_sys_nonewline
        ms_parser.create_rule(
            symbols=["keyword_master_ssl_crl_or_source_ssl_crl", TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.SourceSslCrlDefinition(x[2].get_str_value())
        ),
        # MASTER_SSL_CRLPATH/SOURCE_SSL_CRLPATH = TEXT_STRING_sys_nonewline
        ms_parser.create_rule(
            symbols=["keyword_master_ssl_crlpath_or_source_ssl_crlpath", TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.SourceSslCrlpathDefinition(x[2].get_str_value())
        ),
        # MASTER_PUBLIC_KEY_PATH/SOURCE_PUBLIC_KEY_PATH = TEXT_STRING_sys_nonewline
        ms_parser.create_rule(
            symbols=["keyword_master_public_key_or_source_public_key", TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.SourcePublicKeyDefinition(x[2].get_str_value())
        ),
        # GET_MASTER_PUBLIC_KEY/GET_SOURCE_PUBLIC_KEY = ulong_num
        ms_parser.create_rule(
            symbols=["keyword_master_get_source_public_key_or_source_get_source_public_key", TType.OPERATOR_EQ,
                     "num_literal_or_hex"],
            action=lambda x: ast.SourceGetSourcePublicKeyDefinition(x[2].value)
        ),
        # MASTER_HEARTBEAT_PERIOD/SOURCE_HEARTBEAT_PERIOD = NUM_literal
        ms_parser.create_rule(
            symbols=["keyword_master_heartbeat_period_or_source_heartbeat_period", TType.OPERATOR_EQ, "num_literal"],
            action=lambda x: ast.SourceHeartbeatPeriodDefinition(x[2])
        ),
        # IGNORE_SERVER_IDS = '(' ignore_server_id_list ')'
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IGNORE_SERVER_IDS, TType.OPERATOR_EQ, TType.OPERATOR_LPAREN,
                     "opt_num_literal_or_hex_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.IgnoreServerIdsDefinition(x[3])
        ),
        # MASTER_COMPRESSION_ALGORITHMS/SOURCE_COMPRESSION_ALGORITHMS = TEXT_STRING_sys
        ms_parser.create_rule(
            symbols=["keyword_master_compression_algorithm_or_source_compression_algorithm", TType.OPERATOR_EQ,
                     "text_literal_sys"],
            action=lambda x: ast.SourceCompressionAlgorithmDefinition(x[2].get_str_value())
        ),
        # MASTER_ZSTD_COMPRESSION_LEVEL/SOURCE_ZSTD_COMPRESSION_LEVEL = ulong_num
        ms_parser.create_rule(
            symbols=["keyword_master_zstd_compression_level_or_source_zstd_compression_level", TType.OPERATOR_EQ,
                     "num_literal_or_hex"],
            action=lambda x: ast.SourceZstdCompressionLevelDefinition(x[2].value)
        ),
        # MASTER_AUTO_POSITION/SOURCE_AUTO_POSITION = ulong_num
        ms_parser.create_rule(
            symbols=["keyword_master_auto_position_or_source_auto_position", TType.OPERATOR_EQ, "num_literal_or_hex"],
            action=lambda x: ast.SourceAutoPositionDefinition(x[2].value)
        ),
        # PRIVILEGE_CHECKS_USER = privilege_check_def
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PRIVILEGE_CHECKS_USER, TType.OPERATOR_EQ, "explicit_user_name_or_null"],
            action=lambda x: ast.PrivilegeCheckDefinition(x[2])
        ),
        # REQUIRE_ROW_FORMAT = ulong_num
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REQUIRE_ROW_FORMAT, TType.OPERATOR_EQ, "num_literal_or_hex"],
            action=lambda x: ast.RequireRowFormatDefinition(x[2].value)
        ),
        # REQUIRE_TABLE_PRIMARY_KEY_CHECK = table_primary_key_check_def
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REQUIRE_TABLE_PRIMARY_KEY_CHECK, TType.OPERATOR_EQ, "table_primary_key_check_type"],
            action=lambda x: ast.RequireTablePrimaryKeyCheckDefinition(x[2])
        ),
        # SOURCE_CONNECTION_AUTO_FAILOVER = real_ulong_num
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SOURCE_CONNECTION_AUTO_FAILOVER, TType.OPERATOR_EQ, "int_literal_or_hex"],
            action=lambda x: ast.SourceConnectionAutoFailoverDefinition(x[2].value)
        ),
        # ASSIGN_GTIDS_TO_ANONYMOUS_TRANSACTIONS = assign_gtids_to_anonymous_transactions_def
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ASSIGN_GTIDS_TO_ANONYMOUS_TRANSACTIONS, TType.OPERATOR_EQ, "assign_gtids_type"],
            action=lambda x: ast.AssignGtidsToAnonymousTransactionsDefinition(x[2])
        ),
        # GTID_ONLY = real_ulong_num
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GTID_ONLY, TType.OPERATOR_EQ, "int_literal_or_hex"],
            action=lambda x: ast.GtidOnlyDefinition(x[2].value)
        ),
        # source_file_def
        ms_parser.create_rule(
            symbols=["source_file_def"]
        )
    ]
)

# 源文件定义
SOURCE_FILE_DEF = ms_parser.create_group(
    name="source_file_def",
    rules=[
        # MASTER_LOG_FILE/SOURCE_LOG_FILE = TEXT_STRING_sys_nonewline
        ms_parser.create_rule(
            symbols=["keyword_master_log_file_or_source_log_file", TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.SourceLogFileDefinition(x[2].get_str_value())
        ),
        # MASTER_LOG_POS/SOURCE_LOG_POS = ulonglong_num
        ms_parser.create_rule(
            symbols=["keyword_master_log_pos_or_source_log_pos", TType.OPERATOR_EQ, "int_literal_or_hex"],
            action=lambda x: ast.SourceLogPosDefinition(x[2].value)
        ),
        # RELAY_LOG_FILE = TEXT_STRING_sys_nonewline
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RELAY_LOG_FILE, TType.OPERATOR_EQ, "text_literal_sys"],
            action=lambda x: ast.RelayLogFileDefinition(x[2].get_str_value())
        ),
        # RELAY_LOG_POS = ulong_num
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RELAY_LOG_POS, TType.OPERATOR_EQ, "num_literal_or_hex"],
            action=lambda x: ast.RelayLogPosDefinition(x[2].value)
        )
    ]
)

# 分配 GTIDs 给匿名事务定义
ASSIGN_GTIDS_TYPE = ms_parser.create_group(
    name="assign_gtids_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_OFF],
            action=lambda _: ast.AssignGidsDefinition(
                assign_type=ast.EnumAssignGtidsType.OFF,
                uuid=None
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LOCAL],
            action=lambda _: ast.AssignGidsDefinition(
                assign_type=ast.EnumAssignGtidsType.LOCAL,
                uuid=None
            )
        ),
        ms_parser.create_rule(
            symbols=["text_literal"],
            action=lambda x: ast.AssignGidsDefinition(
                assign_type=ast.EnumAssignGtidsType.UUID,
                uuid=x[0].get_str_value()
            )
        )
    ]
)
