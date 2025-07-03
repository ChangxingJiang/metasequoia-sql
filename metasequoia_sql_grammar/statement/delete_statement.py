"""
DELETE 语句（delete statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "DELETE_STATEMENT",
]

# `DELETE` 语句
DELETE_STATEMENT = ms_parser.create_group(
    name="delete_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                "opt_with_clause",  # 0
                TType.KEYWORD_DELETE,  # 1
                "opt_delete_option_list",  # 2
                TType.KEYWORD_FROM,  # 3
                "identifier",  # 4
                "opt_table_alias",  # 5
                "opt_partition_clause",  # 6
                "opt_where_clause",  # 7
                "opt_order_by_clause",  # 8
                "opt_simple_limit_clause"  # 9
            ],
            action=lambda x: ast.DeleteFromStatement(
                with_clause=x[0],
                options=x[2],
                table_name=x[4],
                table_alias=x[5],
                use_partition=x[6],
                where_clause=x[7],
                order_by_clause=x[8],
                limit_clause=x[9]
            )
        ),
        ms_parser.create_rule(
            symbols=[
                "opt_with_clause",  # 0
                TType.KEYWORD_DELETE,  # 1
                "opt_delete_option_list",  # 2
                "table_ident_opt_wild_list",  # 3
                TType.KEYWORD_FROM,  # 4
                "table_reference_list",  # 5
                "opt_where_clause"  # 6
            ],
            action=lambda x: ast.DeleteColumnFromStatement(
                with_clause=x[0],
                options=x[2],
                wild_table_list=x[3],
                from_table_list=x[5],
                where_clause=x[6]
            )
        ),
        ms_parser.create_rule(
            symbols=[
                "opt_with_clause",  # 0
                TType.KEYWORD_DELETE,  # 1
                "opt_delete_option_list",  # 2
                TType.KEYWORD_FROM,  # 3
                "table_ident_opt_wild_list",  # 4
                TType.KEYWORD_USING,  # 5
                "table_reference_list",  # 6
                "opt_where_clause"  # 7
            ],
            action=lambda x: ast.DeleteFromUsingStatement(
                with_clause=x[0],
                options=x[2],
                from_table_list=x[4],
                using_table_list=x[6],
                where_clause=x[7]
            )
        )
    ]
)
