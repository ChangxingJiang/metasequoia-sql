"""
固定的词语组合
"""

import metasequoia_parser as ms_parser

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
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
    "KEYWORD_DESCRIBE_OR_EXPLAIN",
    "KEYWORD_TABLE_OR_TABLES",
    "KEYWORD_MASTER_OR_BINARY",
    "KEYWORD_FROM_OR_IN",
    "KEYWORD_KEYS_OR_INDEX",
    "KEYWORD_REPLICA_OR_SLAVE",
    "OPT_BRACES",
    "OPT_COMMA",
    "KEYWORD_CHARSET",
    "KEYWORD_NCHAR",
    "KEYWORD_VARCHAR",
    "KEYWORD_NVARCHAR",
    "OPT_EQUAL",
    "EQUAL",
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
            symbols=[TType.KEYWORD_ALL]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
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
