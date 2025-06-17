"""
固定的词语组合
"""

import metasequoia_parser as ms_parser

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    # 可选的关键字
    "OPT_KEYWORD_OF",
    "OPT_KEYWORD_ALL",
    "OPT_KEYWORD_INTO",
    "OPT_KEYWORD_DEFAULT",
    "OPT_KEYWORD_STORAGE",
    "OPT_KEYWORD_TEMPORARY",
    "OPT_KEYWORD_EXTENDED",
    "OPT_KEYWORD_IF_NOT_EXISTS",
    "OPT_KEYWORD_IF_EXISTS",
    "OPT_KEYWORD_FORCE",
    "OPT_KEYWORD_FULL",
    "OPT_KEYWORD_WORK",
    "OPT_KEYWORD_NO_WRITE_TO_BINLOG",
    "OPT_KEYWORD_TABLE",
    "OPT_KEYWORD_SAVEPOINT",
    "OPT_KEYWORD_VALUE",
    "OPT_KEYWORD_PRIVILEGES",
    "OPT_KEYWORD_WITH_ADMIN_OPTION",
    "OPT_KEYWORD_IGNORE_UNKNOWN_USER",
    "OPT_KEYWORD_GRANT_OPTION",
    "OPT_KEYWORD_CONVERT_XID",
    "OPT_KEYWORD_ONE_PHASE",
    "OPT_KEYWORD_COLUMN",

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

    # 可选的运算符
    "OPT_BRACES",
    "OPT_COMMA",
    "OPT_EQUAL",
    "EQUAL",
    "OPT_TO_OR_EQ_OR_AS",
]

# 可选的 `OPT` 关键字
OPT_KEYWORD_OF = ms_parser.create_group(
    name="opt_keyword_of",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_OF]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的 `ALL` 关键字
OPT_KEYWORD_ALL = ms_parser.create_group(
    name="opt_keyword_all",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALL],
            action=ms_parser.template.action.RETURN_TRUE
        ),
        ms_parser.create_rule(
            symbols=[],
            action=ms_parser.template.action.RETURN_FALSE
        )
    ]
)

# 可选的 `INTO` 关键字
OPT_KEYWORD_INTO = ms_parser.create_group(
    name="opt_keyword_into",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INTO]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的 `DEFAULT` 关键字
OPT_KEYWORD_DEFAULT = ms_parser.create_group(
    name="opt_keyword_default",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DEFAULT]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的 `STORAGE` 关键字
OPT_KEYWORD_STORAGE = ms_parser.create_group(
    name="opt_keyword_storage",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STORAGE]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的 `TEMPORARY` 关键字
OPT_KEYWORD_TEMPORARY = ms_parser.create_group(
    name="opt_keyword_temporary",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TEMPORARY],
            action=ms_parser.template.action.RETURN_TRUE
        ),
        ms_parser.create_rule(
            symbols=[],
            action=ms_parser.template.action.RETURN_FALSE
        )
    ]
)

# 可选的 `EXTENDED` 关键字
OPT_KEYWORD_EXTENDED = ms_parser.create_group(
    name="opt_keyword_extended",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXTENDED],
            action=ms_parser.template.action.RETURN_TRUE
        ),
        ms_parser.create_rule(
            symbols=[],
            action=ms_parser.template.action.RETURN_FALSE
        )
    ]
)

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

# 可选的 `FORCE` 关键字
OPT_KEYWORD_FORCE = ms_parser.create_group(
    name="opt_keyword_force",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FORCE],
            action=ms_parser.template.action.RETURN_TRUE
        ),
        ms_parser.create_rule(
            symbols=[],
            action=ms_parser.template.action.RETURN_FALSE
        )
    ]
)

# 可选的 `FULL` 关键字
OPT_KEYWORD_FULL = ms_parser.create_group(
    name="opt_keyword_full",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FULL],
            action=ms_parser.template.action.RETURN_TRUE
        ),
        ms_parser.create_rule(
            symbols=[],
            action=ms_parser.template.action.RETURN_FALSE
        )
    ]
)

# 可选的 `WORK` 关键字
OPT_KEYWORD_WORK = ms_parser.create_group(
    name="opt_keyword_work",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WORK],
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
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

# 可选的 `TABLE` 关键字
OPT_KEYWORD_TABLE = ms_parser.create_group(
    name="opt_keyword_table",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TABLE]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的 `SAVEPOINT` 关键字
OPT_KEYWORD_SAVEPOINT = ms_parser.create_group(
    name="opt_keyword_savepoint",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SAVEPOINT]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
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
