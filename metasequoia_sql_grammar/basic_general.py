"""
通用的基础元素语义组
"""

import metasequoia_parser as ms_parser
from metasequoia_sql_new import ast
from metasequoia_sql_new.terminal import SqlTerminalType as TType

__all__ = [
    "GENERAL_OPT_OF",
]

# 可选的 OPT 关键字
# 对应 MySQL 语义组：opt_of
GENERAL_OPT_OF = ms_parser.create_group(
    name="opt_of",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_OF]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)
