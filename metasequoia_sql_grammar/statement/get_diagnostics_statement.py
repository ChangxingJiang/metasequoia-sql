"""
GET DIAGNOSTICS 语句（get diagnostics statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "GET_DIAGNOSTICS_STATEMENT",
    "DIAGNOSTICS_INFORMATION",
    "STATEMENT_INFORMATION",
    "STATEMENT_INFORMATION_ITEM",
    "CONDITION_INFORMATION",
    "CONDITION_INFORMATION_ITEM",
    "SIMPLE_TARGET_SPECIFICATION",
]

# `GET DIAGNOSTICS` 语句
GET_DIAGNOSTICS_STATEMENT = ms_parser.create_group(
    name="get_diagnostics_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GET, "which_area", TType.KEYWORD_DIAGNOSTICS, "diagnostics_information"],
            action=lambda x: ast.GetDiagnosticsStatement(
                which_area=x[1],
                diagnostics_information=x[3]
            )
        )
    ]
)

# 诊断信息
DIAGNOSTICS_INFORMATION = ms_parser.create_group(
    name="diagnostics_information",
    rules=[
        ms_parser.create_rule(
            symbols=["statement_information"],
            action=lambda x: ast.DiagnosticsInformation(
                statement_information=ast.StatementInformation(x[0])
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CONDITION, "signal_allowed_expr", "condition_information"],
            action=lambda x: ast.DiagnosticsInformation(
                condition_information=ast.ConditionInformation(
                    condition_number=x[1],
                    condition_information_item_list=x[2].condition_information_item_list
                )
            )
        )
    ]
)

# 语句诊断信息项的列表
STATEMENT_INFORMATION = ms_parser.create_group(
    name="statement_information",
    rules=[
        ms_parser.create_rule(
            symbols=["statement_information", TType.OPERATOR_COMMA, "statement_information_item"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["statement_information_item"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 语句诊断信息项
STATEMENT_INFORMATION_ITEM = ms_parser.create_group(
    name="statement_information_item",
    rules=[
        ms_parser.create_rule(
            symbols=["simple_target_specification", TType.OPERATOR_EQ, "statement_information_type"],
            action=lambda x: ast.StatementInformationItem(item_name=x[2], target_variable=x[0])
        )
    ]
)

# 条件诊断信息项的列表
CONDITION_INFORMATION = ms_parser.create_group(
    name="condition_information",
    rules=[
        ms_parser.create_rule(
            symbols=["condition_information", TType.OPERATOR_COMMA, "condition_information_item"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["condition_information_item"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 条件诊断信息项
CONDITION_INFORMATION_ITEM = ms_parser.create_group(
    name="condition_information_item",
    rules=[
        ms_parser.create_rule(
            symbols=["simple_target_specification", TType.OPERATOR_EQ, "condition_information_type"],
            action=lambda x: ast.ConditionInformationItem(item_name=x[2], target_variable=x[0])
        )
    ]
)

# 指定的诊断目标（变量或用户变量）
SIMPLE_TARGET_SPECIFICATION = ms_parser.create_group(
    name="simple_target_specification",
    rules=[
        ms_parser.create_rule(
            symbols=["identifier"],
            action=lambda x: x[0]
        ),
        ms_parser.create_rule(
            symbols=["user_variable"],
            action=lambda x: x[0]
        )
    ]
)
