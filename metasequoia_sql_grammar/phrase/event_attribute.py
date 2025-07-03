"""
事件属性（event attribute）语义组
"""

import metasequoia_parser as ms_parser

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_EVENT_RENAME",
    "OPT_EVENT_COMMENT",
]

# 可选的事件重命名
OPT_EVENT_RENAME = ms_parser.create_group(
    name="opt_event_rename",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RENAME, TType.KEYWORD_TO, "identifier"],
            action=lambda x: x[2]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的事件注释
OPT_EVENT_COMMENT = ms_parser.create_group(
    name="opt_event_comment",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COMMENT, "text_literal_sys"],
            action=lambda x: x[1].get_str_value()
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)
