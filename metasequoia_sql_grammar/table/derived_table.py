"""
派生表（derived table）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "DERIVED_TABLE"
]

DERIVED_TABLE = ms_parser.create_group(
    name="derived_table",
    rules=[
        ms_parser.create_rule(
            symbols=["subquery", "opt_table_alias", "opt_ident_list_parens"],
            action=lambda x: ast.DerivedTable(lateral=False, query_expression=x[0], table_alias=x[1], column_list=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LATERAL, "subquery", "opt_table_alias", "opt_ident_list_parens"],
            action=lambda x: ast.DerivedTable(lateral=True, query_expression=x[0], table_alias=x[1], column_list=x[2])
        )
    ]
)
