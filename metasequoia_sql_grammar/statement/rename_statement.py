"""
重命名语句的语法规则。
"""

import metasequoia_parser as ms_parser
from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "RENAME_STATEMENT",
    "TABLE_TO_TABLE_LIST",
    "TABLE_TO_TABLE",
    "RENAME_USER_LIST"
]

# `RENAME` 语句
RENAME_STATEMENT = ms_parser.create_group(
    name="rename_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RENAME, "keyword_table_or_tables", "rename_table_list"],
            action=lambda x: ast.RenameTableStatement(table_pairs=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RENAME, TType.KEYWORD_USER, "rename_user_list"],
            action=lambda x: ast.RenameUserStatement(user_pairs=x[2])
        )
    ]
)

# `RENAME` 语句中的表重命名对的列表
TABLE_TO_TABLE_LIST = ms_parser.create_group(
    name="rename_table_list",
    rules=[
        ms_parser.create_rule(
            symbols=["rename_table_item"],
            action=lambda x: [x[0]]
        ),
        ms_parser.create_rule(
            symbols=["rename_table_list", TType.OPERATOR_COMMA, "rename_table_item"],
            action=lambda x: x[0] + [x[2]]
        )
    ]
)

# `RENAME` 语句中的表重命名对
TABLE_TO_TABLE = ms_parser.create_group(
    name="rename_table_item",
    rules=[
        ms_parser.create_rule(
            symbols=["identifier", TType.KEYWORD_TO, "identifier"],
            action=lambda x: (x[0], x[2])
        )
    ]
)

# `RENAME` 语句中的用户重命名对的列表
RENAME_USER_LIST = ms_parser.create_group(
    name="rename_user_list",
    rules=[
        ms_parser.create_rule(
            symbols=["user_name", TType.KEYWORD_TO, "user_name"],
            action=lambda x: [(x[0], x[2])]
        ),
        ms_parser.create_rule(
            symbols=["rename_user_list", TType.OPERATOR_COMMA, "user_name", TType.KEYWORD_TO, "user_name"],
            action=lambda x: x[0] + [(x[2], x[4])]
        )
    ]
)
