"""
UPDATE 语句（update statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "UPDATE_ELEMENT_LIST",
    "UPDATE_ELEMENT",
]

# `UPDATE` 语句
UPDATE_STATEMENT = ms_parser.create_group(
    name="update_statement",
    rules=[
        ms_parser.create_rule(
            symbols=["opt_with_clause",  # 0
                     TType.KEYWORD_UPDATE,  # 1
                     "opt_keyword_low_priority",  # 2
                     "opt_keyword_ignore",  # 3
                     "table_reference_list",  # 4
                     TType.KEYWORD_SET,  # 5
                     "update_element_list",  # 6
                     "opt_where_clause",  # 7
                     "opt_order_by_clause",  # 8
                     "opt_simple_limit_clause"],  # 9
            action=lambda x: ast.UpdateStatement(
                with_clause=x[0],
                options=x[2] | x[3],
                table_list=x[4],
                update_list=x[6],
                where_clause=x[7],
                order_by_clause=x[8],
                limit_clause=x[9]
            )
        )
    ]
)

# `UPDATE` 语句中的更新项的列表
UPDATE_ELEMENT_LIST = ms_parser.create_group(
    name="update_element_list",
    rules=[
        ms_parser.create_rule(
            symbols=["update_element_list", TType.OPERATOR_COMMA, "update_element"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["update_element"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# `UPDATE` 语句中的更新项
UPDATE_ELEMENT = ms_parser.create_group(
    name="update_element",
    rules=[
        ms_parser.create_rule(
            symbols=["simple_ident", "equal", "expr_or_default"],
            action=lambda x: ast.UpdateElement(column_name=x[0], column_value=x[2])
        )
    ]
)
