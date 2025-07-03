"""
CREATE INDEX 语句（create index statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CREATE_INDEX_STATEMENT",
    "OPT_KEYWORD_UNIQUE",
]

# `CREATE INDEX` 语句
CREATE_INDEX_STATEMENT = ms_parser.create_group(
    name="create_index_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CREATE,  # 0
                "opt_keyword_unique",  # 1
                TType.KEYWORD_INDEX,  # 2
                "ident",  # 3
                "opt_index_type_clause",  # 4
                TType.KEYWORD_ON,  # 5
                "identifier",  # 6
                TType.OPERATOR_LPAREN,  # 7
                "index_key_definition_with_expr_list",  # 8
                TType.OPERATOR_RPAREN,  # 9
                "opt_normal_index_attribute_list",  # 10
                "opt_alter_option_lock_and_algorithm",  # 11
            ],
            action=lambda x: ast.CreateIndexStmt(
                index_type=x[1],
                index_name=x[3],
                index_structure_type=x[4],
                table_name=x[6],
                index_key_list=x[8],
                index_options=x[10],
                alter_lock=x[11].lock,
                alter_algorithm=x[11].algorithm
            )
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CREATE,  # 0
                TType.KEYWORD_FULLTEXT,  # 1
                TType.KEYWORD_INDEX,  # 2
                "ident",  # 3
                TType.KEYWORD_ON,  # 4
                "identifier",  # 5
                TType.OPERATOR_LPAREN,  # 6
                "index_key_definition_with_expr_list",  # 7
                TType.OPERATOR_RPAREN,  # 8
                "opt_fulltext_index_attribute_list",  # 9
                "opt_alter_option_lock_and_algorithm",  # 10
            ],
            action=lambda x: ast.CreateIndexStmt(
                index_type=ast.EnumIndexType.FULLTEXT,
                index_name=x[3],
                index_structure_type=None,
                table_name=x[5],
                index_key_list=x[7],
                index_options=x[9],
                alter_lock=x[10].lock,
                alter_algorithm=x[10].algorithm
            )
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CREATE,  # 0
                TType.KEYWORD_SPATIAL,  # 1
                TType.KEYWORD_INDEX,  # 2
                "ident",  # 3
                TType.KEYWORD_ON,  # 4
                "identifier",  # 5
                TType.OPERATOR_LPAREN,  # 6
                "index_key_definition_with_expr_list",  # 7
                TType.OPERATOR_RPAREN,  # 8
                "opt_spatial_index_attribute_list",  # 9
                "opt_alter_option_lock_and_algorithm",  # 10
            ],
            action=lambda x: ast.CreateIndexStmt(
                index_type=ast.EnumIndexType.SPATIAL,
                index_name=x[3],
                index_structure_type=None,
                table_name=x[5],
                index_key_list=x[7],
                index_options=x[9],
                alter_lock=x[10].lock,
                alter_algorithm=x[10].algorithm
            )
        )
    ]
)

# 可选的 `UNIQUE` 关键字
OPT_KEYWORD_UNIQUE = ms_parser.create_group(
    name="opt_keyword_unique",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UNIQUE],
            action=lambda _: ast.EnumIndexType.UNIQUE
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumIndexType.KEY
        )
    ]
)
