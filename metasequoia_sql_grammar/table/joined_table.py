"""
关联表（joined table）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql.terminal import SqlTerminalType as TType

# 自然连接类型
NATURAL_JOIN_TYPE = ms_parser.create_group(
    name="natural_join_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NATURAL, ""]
        )
    ]
)

# 可选的 INNER 关键字
OPT_KEYWORD_INNER = ms_parser.create_group(
    name="opt_keyword_inner",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INNER]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)

# 可选的 OUTER 关键字
OPT_KEYWORD_OUTER = ms_parser.create_group(
    name="opt_keyword_outer",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_OUTER]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)
