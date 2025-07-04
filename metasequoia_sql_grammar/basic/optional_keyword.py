"""
词语组合：可选的关键字
"""

import metasequoia_parser as ms_parser

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_KEYWORD_ALL",
    "OPT_KEYWORD_ARRAY",
    "OPT_KEYWORD_DEFAULT",
    "OPT_KEYWORD_EXTENDED",
    "OPT_KEYWORD_INTERVAL",
    "OPT_KEYWORD_INTO",
    "OPT_KEYWORD_OF",
    "OPT_KEYWORD_STORAGE",
    "OPT_KEYWORD_TEMPORARY",
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
