"""
INSTALL/UNINSTALL 语句（install/uninstall statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "INSTALL_SET_RVALUE",
    "INSTALL_SET_VALUE",
    "INSTALL_SET_VALUE_LIST",
    "OPT_INSTALL_SET_VALUE_LIST",
    "INSTALL_STATEMENT",
    "UNINSTALL_STATEMENT",
]

# `INSTALL` 语句的 `SET` 子句中的右值
INSTALL_SET_RVALUE = ms_parser.create_group(
    name="install_set_rvalue",
    rules=[
        ms_parser.create_rule(
            symbols=["expr"],
            action=lambda x: x[0]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ON],
            action=lambda x: ast.OnExpression()
        )
    ]
)

# `INSTALL` 语句的 `SET` 子句中的单个值
INSTALL_SET_VALUE = ms_parser.create_group(
    name="install_set_value",
    rules=[
        ms_parser.create_rule(
            symbols=[
                "install_option_type",  # 0
                "variable_identifier",  # 1
                "equal",  # 2
                "install_set_rvalue"  # 3
            ],
            action=lambda x: ast.InstallSetValue(option_type=x[0], variable=x[1], value=x[3])
        )
    ]
)

# `INSTALL` 语句的 `SET` 子句中值的列表
INSTALL_SET_VALUE_LIST = ms_parser.create_group(
    name="install_set_value_list",
    rules=[
        ms_parser.create_rule(
            symbols=["install_set_value"],
            action=lambda x: [x[0]]
        ),
        ms_parser.create_rule(
            symbols=["install_set_value_list", TType.OPERATOR_COMMA, "install_set_value"],
            action=lambda x: x[0] + [x[2]]
        )
    ]
)

# 可选的 `INSTALL` 语句的 `SET` 子句中值的列表
OPT_INSTALL_SET_VALUE_LIST = ms_parser.create_group(
    name="opt_install_set_value_list",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SET, "install_set_value_list"],
            action=lambda x: x[1]
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)

# `INSTALL` 语句
INSTALL_STATEMENT = ms_parser.create_group(
    name="install_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_INSTALL,  # 0
                TType.KEYWORD_PLUGIN,  # 1
                "ident",  # 2
                TType.KEYWORD_SONAME,  # 3
                "text_literal_sys"  # 4
            ],
            action=lambda x: ast.InstallPluginStatement(plugin_name=x[2], soname=x[4])
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_INSTALL,  # 0
                TType.KEYWORD_COMPONENT,  # 1
                "text_literal_sys_list",  # 2
                "opt_install_set_value_list"  # 3
            ],
            action=lambda x: ast.InstallComponentStatement(component_list=x[2], set_value_list=x[3])
        )
    ]
)

# `UNINSTALL` 语句
UNINSTALL_STATEMENT = ms_parser.create_group(
    name="uninstall_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_UNINSTALL,  # 0
                TType.KEYWORD_PLUGIN,  # 1
                "ident"  # 2
            ],
            action=lambda x: ast.UninstallPluginStatement(plugin_name=x[2])
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_UNINSTALL,  # 0
                TType.KEYWORD_COMPONENT,  # 1
                "text_literal_sys_list"  # 2
            ],
            action=lambda x: ast.UninstallComponentStatement(component_list=x[2])
        )
    ]
)
