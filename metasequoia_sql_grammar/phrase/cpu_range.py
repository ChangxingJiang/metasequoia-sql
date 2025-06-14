"""
CPU 范围（cpu range）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_RESOURCE_GROUP_VCPU_LIST",
    "CPU_NUM_OR_RANGE_LIST",
    "CPU_NUM_OR_RANGE",
]

# `VCPU` 关键字引导的指定 CPU 编号或范围列表的等式
OPT_RESOURCE_GROUP_VCPU_LIST = ms_parser.create_group(
    name="opt_resource_group_vcpu_list",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_VCPU,  # 0
                "opt_equal",  # 1
                "cpu_num_or_range_list"  # 2
            ],
            action=lambda x: x[2]
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)

# CPU 编号或范围的列表
CPU_NUM_OR_RANGE_LIST = ms_parser.create_group(
    name="cpu_num_or_range_list",
    rules=[
        ms_parser.create_rule(
            symbols=["cpu_num_or_range"],
            action=lambda x: [x[0]]
        ),
        ms_parser.create_rule(
            symbols=[
                "cpu_num_or_range_list",  # 0
                "opt_comma",  # 1
                "cpu_num_or_range"  # 2
            ],
            action=lambda x: x[0] + [x[2]]
        )
    ]
)

# CPU 编号或范围
CPU_NUM_OR_RANGE = ms_parser.create_group(
    name="cpu_num_or_range",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.LITERAL_INT_NUM],
            action=lambda x: ast.CpuRange(start=int(x[0]), end=None)
        ),
        ms_parser.create_rule(
            symbols=[
                TType.LITERAL_INT_NUM,  # 0
                TType.OPERATOR_SUB,  # 1
                TType.LITERAL_INT_NUM  # 2
            ],
            action=lambda x: ast.CpuRange(start=int(x[0]), end=int(x[2]))
        )
    ]
)
