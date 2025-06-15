"""
线程优先级短语（thread priority phrase）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_THREAD_PRIORITY",
]

# 可选的线程优先级
OPT_THREAD_PRIORITY = ms_parser.create_group(
    name="opt_thread_priority",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_THREAD_PRIORITY, "opt_equal", "signed_int_num"],
            action=lambda x: ast.ThreadPriority(value=x[2])
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 正整数字面值或负整数字面值
SIGNED_INT_NUM = ms_parser.create_group(
    name="signed_int_num",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.LITERAL_INT_NUM],
            action=lambda x: int(x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_SUB, TType.LITERAL_INT_NUM],
            action=lambda x: -int(x[1])
        )
    ]
)
