# pylint: disable=R0801

"""
CREATE VIEW 语句（create view statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CREATE_VIEW_STATEMENT"
]

# `ALTER VIEW` 语句
CREATE_VIEW_STATEMENT = ms_parser.create_group(
    name="create_view_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_ALTER,  # 0
                "opt_keyword_on_replace",  # 1
                "opt_view_algorithm_type",  # 2
                "opt_definer_clause",  # 3
                "view_suid_type",  # 4
                TType.KEYWORD_VIEW,  # 5
                "identifier",  # 6
                "opt_ident_list_parens",  # 7
                TType.KEYWORD_AS,  # 8
                "query_expression",  # 9
                "opt_check_option"  # 10
            ],
            action=lambda x: ast.CreateViewStatement(
                replace=x[1],
                algorithm=x[2],
                definer=x[3],
                suid=x[4],
                table_ident=x[6],
                column_list=x[7],
                query_expression=x[9],
                check_option=x[10]
            )
        )
    ]
)
