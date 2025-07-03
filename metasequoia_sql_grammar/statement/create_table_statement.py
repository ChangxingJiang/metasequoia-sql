"""
CREATE TABLE 语句（create table statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CREATE_TABLE_STATEMENT",
    "OPT_CREATE_TABLE_OPTION_1",
    "OPT_CREATE_TABLE_OPTION_2",
    "OPT_CREATE_TABLE_OPTION_3",
    "AS_CREATE_QUERY_EXPRESSION",
]

# `CREATE TABLE` 语句
CREATE_TABLE_STATEMENT = ms_parser.create_group(
    name="create_table_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CREATE,  # 0
                "opt_keyword_temporary",  # 1
                TType.KEYWORD_TABLE,  # 2
                "opt_keyword_if_not_exists",  # 3
                "identifier",  # 4
                TType.OPERATOR_LPAREN,  # 5
                "table_element_list",  # 6
                TType.OPERATOR_RPAREN,  # 7
                "opt_create_table_option_1"  # 8
            ],
            action=lambda x: ast.CreateTableStatementAsDefinition(
                temporary=x[1],
                if_not_exists=x[3],
                table_ident=x[4],
                table_element_list=x[6],
                opt_create_table_option_list=x[8].opt_create_table_option_list,
                opt_partition_clause=x[8].opt_partition_clause,
                on_duplicate=x[8].on_duplicate,
                opt_query_expression=x[8].opt_query_expression
            )
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CREATE,  # 0
                "opt_keyword_temporary",  # 1
                TType.KEYWORD_TABLE,  # 2
                "opt_keyword_if_not_exists",  # 3
                "identifier",  # 4
                "opt_create_table_option_1"  # 5
            ],
            action=lambda x: ast.CreateTableStatementAsDefinition(
                temporary=x[1],
                if_not_exists=x[3],
                table_ident=x[4],
                table_element_list=[],
                opt_create_table_option_list=x[5].opt_create_table_option_list,
                opt_partition_clause=x[5].opt_partition_clause,
                on_duplicate=x[5].on_duplicate,
                opt_query_expression=x[5].opt_query_expression
            )
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CREATE,  # 0
                "opt_keyword_temporary",  # 1
                TType.KEYWORD_TABLE,  # 2
                "opt_keyword_if_not_exists",  # 3
                "identifier",  # 4
                TType.KEYWORD_LIKE,  # 5
                "identifier"  # 6
            ],
            action=lambda x: ast.CreateTableStatementAsLike(
                temporary=x[1],
                if_not_exists=x[3],
                table_ident=x[4],
                like_table_ident=x[6]
            )
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CREATE,  # 0
                "opt_keyword_temporary",  # 1
                TType.KEYWORD_TABLE,  # 2
                "opt_keyword_if_not_exists",  # 3
                "identifier",  # 4
                TType.OPERATOR_LPAREN,  # 5
                TType.KEYWORD_LIKE,  # 6
                "identifier",  # 7
                TType.OPERATOR_RPAREN  # 8
            ],
            action=lambda x: ast.CreateTableStatementAsLike(
                temporary=x[1],
                if_not_exists=x[3],
                table_ident=x[4],
                like_table_ident=x[7]
            )
        ),
    ]
)

# `CREATE TABLE` 的选项（第 1 层）
OPT_CREATE_TABLE_OPTION_1 = ms_parser.create_group(
    name="opt_create_table_option_1",
    rules=[
        ms_parser.create_rule(
            symbols=["create_table_option_list", "opt_create_table_option_2"],
            action=lambda x: x[1].set_create_table_option_list(x[0])
        ),
        ms_parser.create_rule(
            symbols=["opt_create_table_option_2"]
        )
    ]
)

# `CREATE TABLE` 的选项（第 2 层）
OPT_CREATE_TABLE_OPTION_2 = ms_parser.create_group(
    name="opt_create_table_option_2",
    rules=[
        ms_parser.create_rule(
            symbols=["ddl_partition_by_clause", "opt_create_table_option_3"],
            action=lambda x: x[1].set_partition_clause(x[0])
        ),
        ms_parser.create_rule(
            symbols=["opt_create_table_option_3"]
        )
    ]
)

# `CREATE TABLE` 的选项（第 3 层）
OPT_CREATE_TABLE_OPTION_3 = ms_parser.create_group(
    name="opt_create_table_option_3",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.TempCreateTableOption(
                opt_create_table_option_list=[],
                opt_partition_clause=None,
                on_duplicate=ast.OnDuplicate.DEFAULT,
                opt_query_expression=None
            )
        ),
        ms_parser.create_rule(
            symbols=["on_duplicate", "as_create_query_expression"],
            action=lambda x: ast.TempCreateTableOption(
                opt_create_table_option_list=[],
                opt_partition_clause=None,
                on_duplicate=x[0],
                opt_query_expression=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=["as_create_query_expression"],
            action=lambda x: ast.TempCreateTableOption(
                opt_create_table_option_list=[],
                opt_partition_clause=None,
                on_duplicate=ast.OnDuplicate.DEFAULT,
                opt_query_expression=x[0]
            )
        ),
    ]
)

# 可选择是否包含前置 `AS` 关键字的查询表达式
AS_CREATE_QUERY_EXPRESSION = ms_parser.create_group(
    name="as_create_query_expression",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AS, "query_expression"],
            action=lambda x: x[1]
        ),
        ms_parser.create_rule(
            symbols=["query_expression"],
            action=lambda x: x[0]
        )
    ]
)
