"""
关联表（joined table）
"""

import metasequoia_parser as ms_parser
from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "JOINED_TABLE",
    "JOINED_TABLE_PARENS",
    "NATURAL_JOIN_TYPE",
    "INNER_JOIN_TYPE",
    "OUTER_JOIN_TYPE",
    "OPT_KEYWORD_INNER",
    "OPT_KEYWORD_OUTER",
]

# 关联表
JOINED_TABLE = ms_parser.create_group(
    name="joined_table",
    rules=[
        ms_parser.create_rule(
            symbols=["table_reference", "inner_join_type", "table_reference", TType.KEYWORD_ON, "expr"],
            action=lambda x: ast.JoinedTableOn(left_operand=x[0], join_type=x[1], right_operand=x[2], on_condition=x[4])
        ),
        ms_parser.create_rule(
            symbols=["table_reference", "inner_join_type", "table_reference", TType.KEYWORD_USING,
                     TType.OPERATOR_LPAREN, "ident_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.JoinedTableUsing(left_operand=x[0], join_type=x[1], right_operand=x[2],
                                                  using_list=x[5])
        ),
        ms_parser.create_rule(
            symbols=["table_reference", "outer_join_type", "table_reference", TType.KEYWORD_ON, "expr"],
            action=lambda x: ast.JoinedTableOn(left_operand=x[0], join_type=x[1], right_operand=x[2], on_condition=x[4])
        ),
        ms_parser.create_rule(
            symbols=["table_reference", "outer_join_type", "table_reference", TType.KEYWORD_USING,
                     TType.OPERATOR_LPAREN, "ident_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.JoinedTableUsing(left_operand=x[0], join_type=x[1], right_operand=x[2],
                                                  using_list=x[5])
        ),
        ms_parser.create_rule(
            symbols=["table_reference", "inner_join_type", "table_reference"],
            action=lambda x: ast.CrossJoinedTable(left_operand=x[0], join_type=x[1], right_operand=x[2]),
            sr_priority_as=TType.CONDITIONLESS_JOIN
        ),
        ms_parser.create_rule(
            symbols=["table_reference", "natural_join_type", "table_factor"],
            action=lambda x: ast.NaturalJoinedTable(left_operand=x[0], join_type=x[1], right_operand=x[2])
        )
    ]
)

# 包含大于等于一层括号的关联表
JOINED_TABLE_PARENS = ms_parser.create_group(
    name="joined_table_parens",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "joined_table_parens", TType.OPERATOR_RPAREN],
            action=lambda x: x[1]
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "joined_table", TType.OPERATOR_RPAREN],
            action=lambda x: x[1]
        )
    ]
)

# 自然连接的关键字
NATURAL_JOIN_TYPE = ms_parser.create_group(
    name="natural_join_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NATURAL, "opt_keyword_inner", TType.KEYWORD_JOIN],
            action=lambda _: ast.EnumJoinType.NATURAL_INNER
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NATURAL, TType.KEYWORD_RIGHT, "opt_keyword_outer", TType.KEYWORD_JOIN],
            action=lambda _: ast.EnumJoinType.NATURAL_RIGHT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NATURAL, TType.KEYWORD_LEFT, "opt_keyword_outer", TType.KEYWORD_JOIN],
            action=lambda _: ast.EnumJoinType.NATURAL_LEFT
        )
    ]
)

# 内连接的关键字
INNER_JOIN_TYPE = ms_parser.create_group(
    name="inner_join_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_JOIN],
            action=lambda _: ast.EnumJoinType.JOIN
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INNER, TType.KEYWORD_JOIN],
            action=lambda _: ast.EnumJoinType.INNER_JOIN
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CROSS, TType.KEYWORD_JOIN],
            action=lambda _: ast.EnumJoinType.CROSS_JOIN
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STRAIGHT_JOIN],
            action=lambda _: ast.EnumJoinType.STRAIGHT_JOIN
        )
    ]
)

# 外关联的关键字
OUTER_JOIN_TYPE = ms_parser.create_group(
    name="outer_join_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LEFT, "opt_keyword_outer", TType.KEYWORD_JOIN],
            action=lambda _: ast.EnumJoinType.LEFT_OUTER_JOIN
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RIGHT, "opt_keyword_outer", TType.KEYWORD_JOIN],
            action=lambda _: ast.EnumJoinType.RIGHT_OUTER_JOIN
        )
    ]
)

# 可选的 INNER 关键字
OPT_KEYWORD_INNER = ms_parser.create_group(
    name="opt_keyword_inner",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INNER]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的 OUTER 关键字
OPT_KEYWORD_OUTER = ms_parser.create_group(
    name="opt_keyword_outer",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_OUTER]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)
