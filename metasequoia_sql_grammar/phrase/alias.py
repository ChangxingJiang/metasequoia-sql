"""
别名的语义组
"""

import metasequoia_parser as ms_parser

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_KEYWORD_AS",
    "OPT_SELECT_ALIAS",
    "OPT_TABLE_ALIAS",
]

# 可选的 AS 关键字
OPT_KEYWORD_AS = ms_parser.create_group(
    name="opt_keyword_as",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AS]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的字段表达式和 UDF 表达式的别名
OPT_SELECT_ALIAS = ms_parser.create_group(
    name="opt_select_alias",
    rules=[
        ms_parser.create_rule(
            symbols=["opt_keyword_as", "ident"],
            action=lambda x: x[1].get_str_value()
        ),
        ms_parser.create_rule(
            symbols=["opt_keyword_as", "text_literal_sys"],
            action=lambda x: x[1].get_str_value()
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的表表达式的别名
OPT_TABLE_ALIAS = ms_parser.create_group(
    name="opt_table_alias",
    rules=[
        ms_parser.create_rule(
            symbols=["opt_keyword_as", "ident"],
            action=lambda x: x[1].get_str_value()
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)
