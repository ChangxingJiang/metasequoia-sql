"""
CREATE PROCEDURE 语句（create procedure statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CREATE_PROCEDURE_STATEMENT",
    "OPT_PROCEDURE_PARAM_LIST",
    "PROCEDURE_PARAM_LIST",
    "PROCEDURE_PARAM",
]

# `CREATE PROCEDURE` 语句
CREATE_PROCEDURE_STATEMENT = ms_parser.create_group(
    name="create_procedure_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_CREATE,  # 0
                "opt_definer_clause",  # 1
                TType.KEYWORD_PROCEDURE,  # 2
                "opt_keyword_if_not_exists",  # 3
                "identifier",  # 4
                TType.OPERATOR_LPAREN,  # 5
                "opt_procedure_param_list",  # 6
                TType.OPERATOR_RPAREN,  # 7
                "create_function_option_list",  # 8
                "stored_routine_body",  # 9
            ],
            action=lambda x: ast.CreateProcedureStatement(
                definer=x[1],
                if_not_exists=x[3],
                procedure_name=x[4],
                param_list=x[6],
                option_list=x[8],
                body=x[9]
            )
        )
    ]
)

# 可选的存储过程参数列表
OPT_PROCEDURE_PARAM_LIST = ms_parser.create_group(
    name="opt_procedure_param_list",
    rules=[
        ms_parser.template.rule.EMPTY_RETURN_LIST,
        ms_parser.create_rule(
            symbols=["procedure_param_list"]
        )
    ]
)

# 存储过程参数列表
PROCEDURE_PARAM_LIST = ms_parser.create_group(
    name="procedure_param_list",
    rules=[
        ms_parser.create_rule(
            symbols=["procedure_param_list", TType.OPERATOR_COMMA, "procedure_param"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["procedure_param"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 存储过程参数
PROCEDURE_PARAM = ms_parser.create_group(
    name="procedure_param",
    rules=[
        ms_parser.create_rule(
            symbols=["procedure_param_mode", "ident", "field_type", "opt_collate"],
            action=lambda x: ast.ProcedureParam(
                param_mode=x[0],
                param_name=x[1].get_str_value(),
                param_type=x[2],
                param_collate=x[3]
            )
        )
    ]
)
