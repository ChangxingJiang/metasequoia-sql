"""
通用表逻辑（general table）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "TABLE_REFERENCE_LIST",
    "TABLE_REFERENCE",
    "ESC_TABLE_REFERENCE",
    "TABLE_FACTOR",
    "TABLE_REFERENCE_LIST_PARENS",
]

# 在 DQL 和 DML 语句中的表元素的列表
TABLE_REFERENCE_LIST = ms_parser.create_group(
    name="table_reference_list",
    rules=[
        ms_parser.create_rule(
            symbols=["table_reference_list", TType.OPERATOR_COMMA, "table_reference"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["table_reference"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 在 DQL 和 DML 语句中的表元素
TABLE_REFERENCE = ms_parser.create_group(
    name="table_reference",
    rules=[
        ms_parser.create_rule(
            symbols=["table_factor"]
        ),
        ms_parser.create_rule(
            symbols=["joined_table"]
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LBRACE, TType.KEYWORD_OJ, "esc_table_reference", TType.OPERATOR_RBRACE],
            action=lambda x: x[2]
        )
    ]
)

# 不兼容 ODBC 语法的表元素
ESC_TABLE_REFERENCE = ms_parser.create_group(
    name="esc_table_reference",
    rules=[
        ms_parser.create_rule(
            symbols=["table_factor"]
        ),
        ms_parser.create_rule(
            symbols=["joined_table"]
        )
    ]
)

# 单个表元素
# - 包含任意层括号的 single_table
# - derived_table
# - 包含大于等于一层括号的 joined_table_parens
# - 包含任意层括号的 table_reference_list_parens
# - table_function
TABLE_FACTOR = ms_parser.create_group(
    name="table_factor",
    rules=[
        ms_parser.create_rule(
            symbols=["simple_table"]
        ),
        ms_parser.create_rule(
            symbols=["single_table_parens"]
        ),
        # TODO : derived_table
        # TODO : joined_table_parens
        ms_parser.create_rule(
            symbols=["table_reference_list_parens"]
        ),
        ms_parser.create_rule(
            symbols=["table_function"]
        )
    ]
)

# 包含任意层括号的在 DQL 和 DML 语句中的表元素的列表
TABLE_REFERENCE_LIST_PARENS = ms_parser.create_group(
    name="table_reference_list_parens",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "table_reference_list_parens", TType.OPERATOR_RPAREN],
            action=lambda x: x[1]
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "table_reference_list", TType.OPERATOR_COMMA, "table_reference",
                     TType.OPERATOR_RPAREN],
            action=lambda x: x[1] + [x[3]]
        )
    ]
)
