"""
通用表达式的语义组
"""

import metasequoia_parser as ms_parser

from metasequoia_sql_new import ast
from metasequoia_sql_new.terminal import SqlTerminalType as TType

__all__ = [
    "GENERAL_SIMPLE_EXPR"
]

# 简单表达式 TODO 未完成
# 对应 MySQL 语义组：simple_expr
GENERAL_SIMPLE_EXPR = ms_parser.create_group(
    name="simple_expr",
    rules=[
        ms_parser.create_rule(
            symbols=["simple_ident"],
        ),
        ms_parser.create_rule(
            symbols=["literal_or_null"],
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_PLUS, "simple_expr"],
            action=lambda x: x[1]
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_SUB, "simple_expr"],
            action=lambda x: ast.FuncNegative(operand=x[1])
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_TILDE, "simple_expr"],
            action=lambda x: ast.FuncBitNot(operand=x[1])
        )
    ]
)
