"""
别名的语义组
"""

import metasequoia_parser as ms_parser

from metasequoia_sql_new.terminal import SqlTerminalType as TType

__all__ = [
    "SELECT_ALIAS"
]

# 字段表达式和 UDF 表达式的别名
SELECT_ALIAS = ms_parser.create_group(
    name="opt_select_alias",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AS, "ident"],
            action=lambda x: x[1].get_str_value()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AS, "text_literal_sys"],
            action=lambda x: x[1].get_str_value()
        ),
        ms_parser.create_rule(
            symbols=["ident"],
            action=lambda x: x[0].get_str_value()
        ),
        ms_parser.create_rule(
            symbols=["text_literal_sys"],
            action=lambda x: x[0].get_str_value()
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)
