# pylint: disable=R0801

"""
CREATE FUNCTION 语句（create function statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CREATE_FUNCTION_STATEMENT",
    "OPT_FUNCTION_PARAM_LIST",
    "FUNCTION_PARAM_LIST",
    "FUNCTION_PARAM",
]

# `CREATE FUNCTION` 语句
CREATE_FUNCTION_STATEMENT = ms_parser.create_group(
    name="create_function_statement",
    rules=[
        # 标准存储函数
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CREATE,  # 0
                "opt_definer_clause",  # 1
                TType.KEYWORD_FUNCTION,  # 2
                "opt_keyword_if_not_exists",  # 3
                "identifier",  # 4
                TType.OPERATOR_LPAREN,  # 5
                "opt_function_param_list",  # 6
                TType.OPERATOR_RPAREN,  # 7
                TType.KEYWORD_RETURNS,  # 8
                "field_type",  # 9
                "opt_collate",  # 10
                "create_function_option_list",  # 11
                "stored_routine_body",  # 12
            ],
            action=lambda x: ast.CreateFunctionStandardStatement(
                definer=x[1],
                if_not_exists=x[3],
                function_name=x[4],
                param_list=x[6],
                return_type=x[9],
                return_collate=x[10],
                option_list=x[11],
                body=x[12]
            )
        ),
        # 聚合 UDF 函数
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CREATE,  # 0
                TType.KEYWORD_AGGREGATE,  # 1
                TType.KEYWORD_FUNCTION,  # 2
                "opt_keyword_if_not_exists",  # 3
                "ident",  # 4
                TType.KEYWORD_RETURNS,  # 5
                "udf_return_type",  # 6
                TType.KEYWORD_SONAME,  # 7
                "text_literal_sys",  # 8
            ],
            action=lambda x: ast.CreateFunctionAggregateUdfStatement(
                if_not_exists=x[3],
                function_name=x[4].get_str_value(),
                return_type=x[6],
                library_name=x[8].get_str_value()
            )
        ),
        # 标准 UDF 函数
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CREATE,  # 0
                TType.KEYWORD_FUNCTION,  # 1
                "opt_keyword_if_not_exists",  # 2
                "ident",  # 3
                TType.KEYWORD_RETURNS,  # 4
                "udf_return_type",  # 5
                TType.KEYWORD_SONAME,  # 6
                "text_literal_sys",  # 7
            ],
            action=lambda x: ast.CreateFunctionUdfStatement(
                if_not_exists=x[2],
                function_name=x[3].get_str_value(),
                return_type=x[5],
                library_name=x[7].get_str_value()
            )
        )
    ]
)

# 可选的存储函数参数列表
OPT_FUNCTION_PARAM_LIST = ms_parser.create_group(
    name="opt_function_param_list",
    rules=[
        ms_parser.template.rule.EMPTY_RETURN_LIST,
        ms_parser.create_rule(
            symbols=["function_param_list"]
        )
    ]
)

# 存储函数参数列表
FUNCTION_PARAM_LIST = ms_parser.create_group(
    name="function_param_list",
    rules=[
        ms_parser.create_rule(
            symbols=["function_param_list", TType.OPERATOR_COMMA, "function_param"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["function_param"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 存储函数参数
FUNCTION_PARAM = ms_parser.create_group(
    name="function_param",
    rules=[
        ms_parser.create_rule(
            symbols=["ident", "field_type", "opt_collate"],
            action=lambda x: ast.FunctionParam(
                param_name=x[0].get_str_value(),
                param_type=x[1],
                param_collate=x[2]
            )
        )
    ]
)
