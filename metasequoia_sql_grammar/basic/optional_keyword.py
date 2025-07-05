"""
词语组合：可选的关键字
"""

import metasequoia_parser as ms_parser

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_KEYWORD_ALL",
    "OPT_KEYWORD_ARRAY",
    "OPT_KEYWORD_AS",
    "OPT_KEYWORD_COLUMN",
    "OPT_KEYWORD_DEFAULT",
    "OPT_KEYWORD_EXTENDED",
    "OPT_KEYWORD_FORCE",
    "OPT_KEYWORD_FROM",
    "OPT_KEYWORD_FULL",
    "OPT_KEYWORD_INNER",
    "OPT_KEYWORD_INTERVAL",
    "OPT_KEYWORD_INTO",
    "OPT_KEYWORD_LINEAR",
    "OPT_KEYWORD_OF",
    "OPT_KEYWORD_OUTER",
    "OPT_KEYWORD_SAVEPOINT",
    "OPT_KEYWORD_STORAGE",
    "OPT_KEYWORD_TABLE",
    "OPT_KEYWORD_TEMPORARY",
    "OPT_KEYWORD_WORK",
]

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

# 可选的 `ARRAY` 关键字
OPT_KEYWORD_ARRAY = ms_parser.create_group(
    name="opt_keyword_array",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ARRAY],
            action=ms_parser.template.action.RETURN_TRUE
        ),
        ms_parser.create_rule(
            symbols=[],
            action=ms_parser.template.action.RETURN_FALSE
        )
    ]
)

# 可选的 `AS` 关键字
OPT_KEYWORD_AS = ms_parser.create_group(
    name="opt_keyword_as",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AS]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的 `COLUMN` 关键字
OPT_KEYWORD_COLUMN = ms_parser.create_group(
    name="opt_keyword_column",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COLUMN]
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

# 可选的 `FROM` 关键字
OPT_KEYWORD_FROM = ms_parser.create_group(
    name="opt_keyword_from",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FROM]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
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

# 可选的 `INNER` 关键字
OPT_KEYWORD_INNER = ms_parser.create_group(
    name="opt_keyword_inner",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INNER]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的 `INTERVAL` 关键字
OPT_KEYWORD_INTERVAL = ms_parser.create_group(
    name="opt_keyword_interval",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INTERVAL],
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

# 可选的 `LINEAR` 关键字
OPT_KEYWORD_LINEAR = ms_parser.create_group(
    name="opt_keyword_linear",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LINEAR],
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的 `OF` 关键字
OPT_KEYWORD_OF = ms_parser.create_group(
    name="opt_keyword_of",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_OF]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的 `OUTER` 关键字
OPT_KEYWORD_OUTER = ms_parser.create_group(
    name="opt_keyword_outer",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_OUTER]
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
