"""
函数选项（function option）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ALTER_FUNCTION_OPTION_LIST",
    "ALTER_FUNCTION_OPTION",
    "CREATE_FUNCTION_OPTION_LIST",
    "CREATE_FUNCTION_OPTION",
]

# `ALTER FUNCTION` 和 `ALTER PROCEDURE` 语句中的函数选项的列表
ALTER_FUNCTION_OPTION_LIST = ms_parser.create_group(
    name="alter_function_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["alter_function_option_list", "alter_function_option"],
            action=ms_parser.template.action.LIST_APPEND_1
        ),
        ms_parser.create_rule(
            symbols=["alter_function_option"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# `ALTER FUNCTION` 和 `ALTER PROCEDURE` 语句中的函数选项
ALTER_FUNCTION_OPTION = ms_parser.create_group(
    name="alter_function_option",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COMMENT, "text_literal_sys"],
            action=lambda x: ast.FunctionOptionComment(comment=x[1].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LANGUAGE, TType.KEYWORD_SQL],
            action=lambda _: ast.FunctionOptionLanguageSql()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LANGUAGE, "ident"],
            action=lambda x: ast.FunctionOptionLanguageIdent(language=x[1].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NO, TType.KEYWORD_SQL],
            action=lambda _: ast.FunctionOptionNoSql()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CONTAINS, TType.KEYWORD_SQL],
            action=lambda _: ast.FunctionOptionContainsSql()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_READS, TType.KEYWORD_SQL, TType.KEYWORD_DATA],
            action=lambda _: ast.FunctionOptionReadsSqlData()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MODIFIES, TType.KEYWORD_SQL, TType.KEYWORD_DATA],
            action=lambda _: ast.FunctionOptionModifiesSqlData()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SQL, TType.KEYWORD_SECURITY, TType.KEYWORD_DEFINER],
            action=lambda _: ast.FunctionOptionSqlSecurity(security=ast.EnumSqlSecurity.DEFINER)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SQL, TType.KEYWORD_SECURITY, TType.KEYWORD_INVOKER],
            action=lambda _: ast.FunctionOptionSqlSecurity(security=ast.EnumSqlSecurity.INVOKER)
        )
    ]
)

# CREATE FUNCTION/PROCEDURE 语句中的函数选项列表
CREATE_FUNCTION_OPTION_LIST = ms_parser.create_group(
    name="create_function_option_list",
    rules=[
        ms_parser.template.rule.EMPTY_RETURN_LIST,
        ms_parser.create_rule(
            symbols=["create_function_option_list", "create_function_option"],
            action=ms_parser.template.action.LIST_APPEND_1
        )
    ]
)

# `CREATE FUNCTION` 和 `CREATE PROCEDURE` 语句中的函数选项
CREATE_FUNCTION_OPTION = ms_parser.create_group(
    name="create_function_option",
    rules=[
        ms_parser.create_rule(
            symbols=["alter_function_option"]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DETERMINISTIC],
            action=lambda _: ast.FunctionOptionDeterministic(is_deterministic=True)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NOT, TType.KEYWORD_DETERMINISTIC],
            action=lambda _: ast.FunctionOptionDeterministic(is_deterministic=False)
        )
    ]
)
