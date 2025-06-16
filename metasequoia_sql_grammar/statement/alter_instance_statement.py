"""
ALTER INSTANCE 语句（alter instance statement）
"""

import metasequoia_parser as ms_parser
from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ALTER_INSTANCE_STATEMENT",
    "ALTER_INSTANCE_ACTION",
]

# `ALTER INSTANCE` 语句
ALTER_INSTANCE_STATEMENT = ms_parser.create_group(
    name="alter_instance_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALTER, TType.KEYWORD_INSTANCE, "alter_instance_action"],
            action=lambda x: ast.AlterInstanceStatement(action=x[2])
        )
    ]
)

# `ALTER INSTANCE` 操作
ALTER_INSTANCE_ACTION = ms_parser.create_group(
    name="alter_instance_action",
    rules=[
        # ROTATE INNODB/BINLOG MASTER KEY
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ROTATE, "ident_or_text", TType.KEYWORD_MASTER, TType.KEYWORD_KEY],
            action=lambda x: (
                ast.AlterInstanceActionRotateInnodbMasterKey()
                if x[1].get_str_value().upper() == "INNODB"
                else ast.AlterInstanceActionRotateBinlogMasterKey()
                if x[1].get_str_value().upper() == "BINLOG"
                else None  # 这会导致语法错误，符合MySQL行为
            )
        ),
        # RELOAD TLS
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RELOAD, TType.KEYWORD_TLS],
            action=lambda _: ast.AlterInstanceActionReloadTls()
        ),
        # RELOAD TLS NO ROLLBACK ON ERROR
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RELOAD, TType.KEYWORD_TLS, TType.KEYWORD_NO, TType.KEYWORD_ROLLBACK,
                     TType.KEYWORD_ON, TType.KEYWORD_ERROR],
            action=lambda _: ast.AlterInstanceActionReloadTlsNoRollback()
        ),
        # RELOAD TLS FOR CHANNEL ident
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RELOAD, TType.KEYWORD_TLS, TType.KEYWORD_FOR, TType.KEYWORD_CHANNEL, "ident"],
            action=lambda x: ast.AlterInstanceActionReloadTlsForChannel(channel_name=x[4].get_str_value())
        ),
        # RELOAD TLS FOR CHANNEL ident NO ROLLBACK ON ERROR
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RELOAD, TType.KEYWORD_TLS, TType.KEYWORD_FOR, TType.KEYWORD_CHANNEL, "ident",
                     TType.KEYWORD_NO, TType.KEYWORD_ROLLBACK, TType.KEYWORD_ON, TType.KEYWORD_ERROR],
            action=lambda x: ast.AlterInstanceActionReloadTlsForChannelNoRollback(channel_name=x[4].get_str_value())
        ),
        # ENABLE INNODB REDO_LOG
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ENABLE, "ident", "ident"],
            action=lambda x: (
                ast.AlterInstanceActionEnableInnodbRedo()
                if x[1].get_str_value().upper() == "INNODB" and x[2].get_str_value().upper() == "REDO_LOG"
                else None  # 这会导致语法错误，符合MySQL行为
            )
        ),
        # DISABLE INNODB REDO_LOG
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DISABLE, "ident", "ident"],
            action=lambda x: (
                ast.AlterInstanceActionDisableInnodbRedo()
                if x[1].get_str_value().upper() == "INNODB" and x[2].get_str_value().upper() == "REDO_LOG"
                else None  # 这会导致语法错误，符合MySQL行为
            )
        ),
        # RELOAD KEYRING
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RELOAD, TType.KEYWORD_KEYRING],
            action=lambda _: ast.AlterInstanceActionReloadKeyring()
        )
    ]
)
