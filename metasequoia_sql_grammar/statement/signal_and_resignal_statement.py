# pylint: disable=R0801

"""
SIGNAL/RESIGNAL 语句（signal or resignal statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "SIGNAL_STATEMENT",
    "RESIGNAL_STATEMENT",

    # 信号值
    "OPT_SIGNAL_VALUE",
    "SIGNAL_VALUE",

    # `SET` 关键字引导的信号项子句
    "OPT_SET_SIGNAL_INFORMATION",
    "SIGNAL_INFORMATION_ITEM_LIST",
    "SIGNAL_ALLOWED_EXPR",
]

# SIGNAL 语句
SIGNAL_STATEMENT = ms_parser.create_group(
    name="signal_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SIGNAL, "signal_value", "opt_set_signal_information"],
            action=lambda x: ast.SignalStatement(signal_value=x[1], information_items=x[2])
        )
    ]
)

# RESIGNAL 语句
RESIGNAL_STATEMENT = ms_parser.create_group(
    name="resignal_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RESIGNAL, "opt_signal_value", "opt_set_signal_information"],
            action=lambda x: ast.ResignalStatement(signal_value=x[1], information_items=x[2])
        )
    ]
)

# `RESIGNAL` 语句中可选的信号值
OPT_SIGNAL_VALUE = ms_parser.create_group(
    name="opt_signal_value",
    rules=[
        ms_parser.create_rule(
            symbols=["signal_value"],
            action=lambda x: x[0]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# `SIGNAL` 和 `RESIGNAL` 语句中的信号值
SIGNAL_VALUE = ms_parser.create_group(
    name="signal_value",
    rules=[
        ms_parser.create_rule(
            symbols=["ident"],
            action=lambda x: x[0].get_str_value()
        ),
        ms_parser.create_rule(
            symbols=["sql_state"],
            action=lambda x: x[0]
        )
    ]
)

# `SIGNAL` 和 `RESIGNAL` 语句中可选的 `SET` 关键字引导的信号项子句
OPT_SET_SIGNAL_INFORMATION = ms_parser.create_group(
    name="opt_set_signal_information",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SET, "signal_information_item_list"],
            action=lambda x: x[1]
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)

# `SIGNAL` 和 `RESIGNAL` 语句中的信息项列表
SIGNAL_INFORMATION_ITEM_LIST = ms_parser.create_group(
    name="signal_information_item_list",
    rules=[
        ms_parser.create_rule(
            symbols=["signal_condition_type", TType.OPERATOR_EQ, "signal_allowed_expr"],
            action=lambda x: [ast.SignalInformation(item_name=x[0], item_value=x[2])]
        ),
        ms_parser.create_rule(
            symbols=["signal_information_item_list", TType.OPERATOR_COMMA, "signal_condition_type", TType.OPERATOR_EQ,
                     "signal_allowed_expr"],
            action=lambda x: x[0] + [ast.SignalInformation(item_name=x[2], item_value=x[4])]
        )
    ]
)

# `SIGNAL` 和 `RESIGNAL` 语句中信息项的值允许的表达式
SIGNAL_ALLOWED_EXPR = ms_parser.create_group(
    name="signal_allowed_expr",
    rules=[
        ms_parser.create_rule(
            symbols=["literal_or_null"],
            action=lambda x: x[0]
        ),
        ms_parser.create_rule(
            symbols=["system_or_user_variable"],
            action=lambda x: x[0]
        ),
        ms_parser.create_rule(
            symbols=["simple_ident"],
            action=lambda x: x[0]
        )
    ]
)
