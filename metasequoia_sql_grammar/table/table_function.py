"""
生成表函数（table function）

参考文档：https://dev.mysql.com/doc/refman/8.4/en/json-table-functions.html
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "JSON_TABLE_COLUMN_TYPE",
    "JSON_TABLE_COLUMN",
    "JSON_TABLE_COLUMN_LIST",
    "JSON_TABLE_COLUMNS_CLAUSE",
    "TABLE_FUNCTION",
]

# JSON_TABLE 函数中的字段类型
JSON_TABLE_COLUMN_TYPE = ms_parser.create_group(
    name="json_table_column_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXISTS],
            action=lambda x: ast.JsonTableColumnType.EXISTS
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.JsonTableColumnType.DEFAULT
        )
    ]
)

# JSON_TABLE 函数中的字段
JSON_TABLE_COLUMN = ms_parser.create_group(
    name="json_table_column",
    rules=[
        ms_parser.create_rule(
            symbols=["ident", TType.KEYWORD_FOR, TType.KEYWORD_ORDINALITY],
            action=lambda x: ast.JsonTableColumnForOrdinality(column_name=x[0].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=["ident", "field_type", "opt_collate", "json_table_column_type", TType.KEYWORD_PATH, "text_literal",
                     "json_on_empty_on_error"],
            action=lambda x: ast.JsonTableColumnForPath(column_name=x[0].get_str_value(), field_type=x[1],
                                                        collate=x[2], column_type=x[3], json_path=x[5],
                                                        json_on_empty_on_error=x[6])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NESTED, TType.KEYWORD_PATH, "text_literal", "json_table_columns_clause"],
            action=lambda x: ast.JsonTableColumnForNestedColumns(json_path=x[2], column_list=x[3])
        )
    ]
)

# JSON_TABLE 函数中的字段的列表
JSON_TABLE_COLUMN_LIST = ms_parser.create_group(
    name="json_table_column_list",
    rules=[
        ms_parser.create_rule(
            symbols=["json_table_column_list", TType.OPERATOR_COMMA, "json_table_column"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["json_table_column"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# JSON_TABLE 函数中的 COLUMNS 子句
JSON_TABLE_COLUMNS_CLAUSE = ms_parser.create_group(
    name="json_table_columns_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COLUMNS, TType.OPERATOR_LPAREN, "json_table_column_list", TType.OPERATOR_RPAREN],
            action=lambda x: x[2]
        )
    ]
)

# 生成表函数
TABLE_FUNCTION = ms_parser.create_group(
    name="table_function",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_JSON_TABLE, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_COMMA, "text_literal",
                     "json_table_columns_clause", TType.OPERATOR_RPAREN, "opt_table_alias"],
            action=lambda x: ast.TableFunctionJsonTable(json_doc=x[2], json_path=x[4], column_list=x[5],
                                                        table_alias=x[7])
        )
    ]
)
