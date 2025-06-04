"""
INSERT 语句和 REPLACE 语句（insert or replace statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "INSERT_STATEMENT",
    "REPLACE_STATEMENT",
    "INSERT_FROM_CONSTRUCTOR",
    "INSERT_VALUES",
    "KEYWORD_VALUE_OR_VALUES",
    "ROW_VALUE_LIST",
    "ROW_VALUE",
    "INSERT_FROM_QUERY",
    "OPT_INSERT_UPDATE_LIST",
]

# INSERT 语句
INSERT_STATEMENT = ms_parser.create_group(
    name="insert_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_INSERT,  # 0
                "opt_insert_option",  # 1
                "opt_keyword_ignore",  # 2
                "opt_keyword_into",  # 3
                "table_ident",  # 4
                "opt_partition_clause",  # 5
                "insert_from_constructor",  # 6
                "opt_insert_alias",  # 7
                "opt_insert_update_list",  # 8
            ],
            action=lambda x: ast.InsertOrReplaceStatement.create_insert_by_values(
                dml_option=x[1] | x[2],
                table_name=x[4],
                use_partition=x[5],
                column_list=x[6].column_list,
                value_list=x[6].value_list,
                table_alias=x[7].table_alias,
                column_alias_list=x[7].column_alias_list,
                on_duplicate_key_update_list=x[8]
            )
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_INSERT,  # 0
                "opt_insert_option",  # 1
                "opt_keyword_ignore",  # 2
                "opt_keyword_into",  # 3
                "table_ident",  # 4
                "opt_partition_clause",  # 5
                TType.KEYWORD_SET,  # 6
                "update_element_list",  # 7
                "opt_insert_alias",  # 8
                "opt_insert_update_list",  # 9
            ],
            action=lambda x: ast.InsertOrReplaceStatement.create_insert_by_set(
                dml_option=x[1] | x[2],
                table_name=x[4],
                use_partition=x[5],
                set_update_list=x[7],
                table_alias=x[8].table_alias,
                column_alias_list=x[8].column_alias_list,
                on_duplicate_key_update_list=x[9]
            )
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_INSERT,  # 0
                "opt_insert_option",  # 1
                "opt_keyword_ignore",  # 2
                "opt_keyword_into",  # 3
                "table_ident",  # 4
                "opt_partition_clause",  # 5
                "insert_from_query",  # 6
                "opt_insert_update_list",  # 7
            ],
            action=lambda x: ast.InsertOrReplaceStatement.create_insert_by_query(
                dml_option=x[1] | x[2],
                table_name=x[4],
                use_partition=x[5],
                column_list=x[6].column_list,
                query_expression=x[6].query_expression,
                on_duplicate_key_update_list=x[7]
            )
        )
    ]
)

# REPLACE 语句
REPLACE_STATEMENT = ms_parser.create_group(
    name="replace_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_REPLACE,  # 0
                "opt_replace_option",  # 1
                "opt_keyword_into",  # 2
                "table_ident",  # 3
                "opt_partition_clause",  # 4
                "insert_from_constructor",  # 5
            ],
            action=lambda x: ast.InsertOrReplaceStatement.create_replace_by_values(
                dml_option=x[1],
                table_name=x[3],
                use_partition=x[4],
                column_list=x[5].column_list,
                value_list=x[5].value_list
            )
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_REPLACE,  # 0
                "opt_replace_option",  # 1
                "opt_keyword_into",  # 2
                "table_ident",  # 3
                "opt_partition_clause",  # 4
                TType.KEYWORD_SET,  # 5
                "update_element_list",  # 6
            ],
            action=lambda x: ast.InsertOrReplaceStatement.create_replace_by_set(
                dml_option=x[1],
                table_name=x[3],
                use_partition=x[4],
                set_update_list=x[5]
            )
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_REPLACE,  # 0
                "opt_replace_option",  # 1
                "opt_keyword_into",  # 2
                "table_ident",  # 3
                "opt_partition_clause",  # 4
                "insert_from_query",  # 5
            ],
            action=lambda x: ast.InsertOrReplaceStatement.create_replace_by_query(
                dml_option=x[1],
                table_name=x[3],
                use_partition=x[4],
                column_list=x[5].column_list,
                query_expression=x[5].query_expression,
            )
        )
    ]
)

# 通过值列表构造的多行数据
INSERT_FROM_CONSTRUCTOR = ms_parser.create_group(
    name="insert_from_constructor",
    rules=[
        ms_parser.create_rule(
            symbols=["insert_values"],
            action=lambda x: ast.TempInsertColumnAndValue(column_list=[], value_list=x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, TType.OPERATOR_RPAREN, "insert_values"],
            action=lambda x: ast.TempInsertColumnAndValue(column_list=[], value_list=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "simple_ident_list", TType.OPERATOR_RPAREN, "insert_values"],
            action=lambda x: ast.TempInsertColumnAndValue(column_list=x[1], value_list=x[3])
        )
    ]
)

# 通过查询构造的多行数据
INSERT_FROM_QUERY = ms_parser.create_group(
    name="insert_from_query",
    rules=[
        ms_parser.create_rule(
            symbols=["query_expression"],
            action=lambda x: ast.TempInsertColumnAndQuery(column_list=[], query_expression=x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, TType.OPERATOR_RPAREN, "query_expression"],
            action=lambda x: ast.TempInsertColumnAndQuery(column_list=[], query_expression=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "simple_ident_list", TType.OPERATOR_RPAREN, "query_expression"],
            action=lambda x: ast.TempInsertColumnAndQuery(column_list=x[1], query_expression=x[3])
        ),
    ]
)

# `VALUE` 或 `VALUES` 关键字引导的多行数据
INSERT_VALUES = ms_parser.create_group(
    name="insert_values",
    rules=[
        ms_parser.create_rule(
            symbols=["keyword_value_or_values", "row_value_list"],
            action=lambda x: x[1]
        )
    ]
)

# `VALUE` 关键字或 `VALUES` 关键字
KEYWORD_VALUE_OR_VALUES = ms_parser.create_group(
    name="keyword_value_or_values",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_VALUE]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_VALUES]
        )
    ]
)

# `INSERT` 和 `REPLACE` 语句中的行数据的列表
ROW_VALUE_LIST = ms_parser.create_group(
    name="row_value_list",
    rules=[
        ms_parser.create_rule(
            symbols=["row_value_list", TType.OPERATOR_COMMA, "row_value"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["row_value"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# `INSERT` 和 `REPLACE` 语句中的行数据
ROW_VALUE = ms_parser.create_group(
    name="row_value",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "opt_expr_or_default_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.RowValue(value_list=x[1])
        )
    ]
)

# `INSERT` 语句中 `AS` 关键字引导的表别名和字段别名
OPT_INSERT_ALIAS = ms_parser.create_group(
    name="opt_insert_alias",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AS, "ident", "opt_ident_list_parens"],
            action=lambda x: ast.TempInsertAlias(table_alias=x[1].get_str_value(), column_alias_list=x[2])
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.TempInsertAlias(table_alias=None, column_alias_list=None)
        )
    ]
)

# 可选的 `ON DUPLICATE KEY UPDATE` 子句
OPT_INSERT_UPDATE_LIST = ms_parser.create_group(
    name="opt_insert_update_list",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ON, TType.KEYWORD_DUPLICATE, TType.KEYWORD_KEY, TType.KEYWORD_UPDATE,
                     "update_element_list"],
            action=lambda x: x[4]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: []
        )
    ]
)
