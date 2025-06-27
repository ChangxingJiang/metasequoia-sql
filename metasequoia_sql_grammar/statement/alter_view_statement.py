# pylint: disable=R0801

"""
ALTER VIEW 语句（alter view statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ALTER_VIEW_STATEMENT"
]

# `ALTER VIEW` 语句
ALTER_VIEW_STATEMENT = ms_parser.create_group(
    name="alter_view_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_ALTER,  # 0
                "opt_view_algorithm_type",  # 1
                "opt_definer_clause",  # 2
                "view_suid_type",  # 3
                TType.KEYWORD_VIEW,  # 4
                "identifier",  # 5
                "opt_ident_list_parens",  # 6
                TType.KEYWORD_AS,  # 7
                "query_expression",  # 8
                "alter_view_statement"  # 9
            ],
            action=lambda x: ast.AlterViewStatement(
                algorithm=x[1],
                definer=x[2],
                suid=x[3],
                table_ident=x[5],
                column_list=x[6],
                query_expression=x[8],
                check_option=x[9]
            )
        )
    ]
)
