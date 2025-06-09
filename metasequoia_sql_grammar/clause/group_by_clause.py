"""
GROUP BY 子句（group by clause）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal.terminal_type import SqlTerminalType as TType

__all__ = [
    "OPT_GROUP_BY_CLAUSE",
    "OLAP_OPT",
]

# 可选的 GROUP BY 子句
OPT_GROUP_BY_CLAUSE = ms_parser.create_group(
    name="opt_group_by_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GROUP, TType.KEYWORD_BY, "expr_list", "olap_opt"],
            action=lambda x: ast.GroupByClause(columns=x[2], olap_opt=x[3])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GROUP, TType.KEYWORD_BY, TType.KEYWORD_ROLLUP, "expr_list"],
            action=lambda x: ast.GroupByClause(columns=x[3], olap_opt=ast.EnumOlapOpt.ROLLUP)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GROUP, TType.KEYWORD_BY, TType.KEYWORD_CUBE, "expr_list"],
            action=lambda x: ast.GroupByClause(columns=x[3], olap_opt=ast.EnumOlapOpt.CUBE)
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# GROUP BY 子句中的分组统计信息规则
OLAP_OPT = ms_parser.create_group(
    name="olap_opt",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITH_ROLLUP],
            action=lambda _: ast.EnumOlapOpt.ROLLUP
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumOlapOpt.DEFAULT
        )
    ]
)
