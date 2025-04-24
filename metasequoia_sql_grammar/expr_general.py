"""
通用表达式的语义组
"""

import metasequoia_parser as ms_parser

from metasequoia_sql_new import ast
from metasequoia_sql_new.terminal import SqlTerminalType as TType

__all__ = [
    "GENERAL_SIMPLE_EXPR",
    "GENERAL_BIT_EXPR",
    "GENERAL_PREDICATE",
    "GENERAL_BOOL_EXPR",
    "GENERAL_EXPR",
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
            action=lambda x: x[1],
            sr_priority_as=TType.NEG
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_SUB, "simple_expr"],
            action=lambda x: ast.FuncNegative(operand=x[1]),
            sr_priority_as=TType.NEG
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_TILDE, "simple_expr"],
            action=lambda x: ast.FuncBitNot(operand=x[1]),
            sr_priority_as=TType.NEG
        )
    ]
)

# 位表达式 TODO 未完成
# 对应 MySQL 语义组：bit_expr
GENERAL_BIT_EXPR = ms_parser.create_group(
    name="bit_expr",
    rules=[
        ms_parser.create_rule(
            symbols=["bit_expr", TType.OPERATOR_BAR, "bit_expr"],
            action=lambda x: ast.FuncBitOr(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_BAR
        ),
        ms_parser.create_rule(
            symbols=["bit_expr", TType.OPERATOR_AMP, "bit_expr"],
            action=lambda x: ast.FuncBitOr(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_AMP
        ),
        ms_parser.create_rule(
            symbols=["bit_expr", TType.OPERATOR_LT_LT, "bit_expr"],
            action=lambda x: ast.FuncShiftLeft(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_LT_LT
        ),
        ms_parser.create_rule(
            symbols=["bit_expr", TType.OPERATOR_GT_GT, "bit_expr"],
            action=lambda x: ast.FuncShiftRight(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_GT_GT
        ),
        ms_parser.create_rule(
            symbols=["bit_expr", TType.OPERATOR_PLUS, "bit_expr"],
            action=lambda x: ast.FuncPlus(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_PLUS
        ),
        ms_parser.create_rule(
            symbols=["bit_expr", TType.OPERATOR_SUB, "bit_expr"],
            action=lambda x: ast.FuncMinus(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_SUB
        ),
        ms_parser.create_rule(
            symbols=["bit_expr", TType.OPERATOR_STAR, "bit_expr"],
            action=lambda x: ast.FuncMul(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_STAR
        ),
        ms_parser.create_rule(
            symbols=["bit_expr", TType.OPERATOR_SLASH, "bit_expr"],
            action=lambda x: ast.FuncDiv(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_SLASH
        ),
        ms_parser.create_rule(
            symbols=["bit_expr", TType.OPERATOR_PERCENT, "bit_expr"],
            action=lambda x: ast.FuncMod(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_PERCENT
        ),
        ms_parser.create_rule(
            symbols=["bit_expr", TType.KEYWORD_DIV, "bit_expr"],
            action=lambda x: ast.FuncDivInt(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.KEYWORD_DIV
        ),
        ms_parser.create_rule(
            symbols=["bit_expr", TType.KEYWORD_MOD, "bit_expr"],
            action=lambda x: ast.FuncMod(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.KEYWORD_MOD
        ),
        ms_parser.create_rule(
            symbols=["bit_expr", TType.OPERATOR_CARET, "bit_expr"],
            action=lambda x: ast.FuncBitXor(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.OPERATOR_CARET
        ),
        ms_parser.create_rule(
            symbols=["simple_expr"],
            sr_priority_as=TType.OPERATOR_COLON_EQ
        )
    ]
)

# 谓语表达式 TODO 未完成
# 对应 MySQL 语义组：predicate
GENERAL_PREDICATE = ms_parser.create_group(
    name="predicate",
    rules=[
        ms_parser.create_rule(
            symbols=["bit_expr", TType.KEYWORD_MEMBER, "opt_of", TType.OPERATOR_LPAREN, "simple_expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.FuncMemberOf(left_operand=x[0], right_operand=x[4])
        ),
        ms_parser.create_rule(
            symbols=["bit_expr", TType.KEYWORD_BETWEEN, "bit_expr", TType.KEYWORD_AND, "predicate"],
            action=lambda x: ast.FuncBetween(first_operand=x[0], second_operand=x[2], third_operand=x[4])
        ),
        ms_parser.create_rule(
            symbols=["bit_expr", TType.KEYWORD_NOT, TType.KEYWORD_BETWEEN, "bit_expr", TType.KEYWORD_AND, "predicate"],
            action=lambda x: ast.FuncNotBetween(first_operand=x[0], second_operand=x[3], third_operand=x[5])
        ),
        ms_parser.create_rule(
            symbols=["bit_expr", TType.KEYWORD_SOUNDS, TType.KEYWORD_LIKE, "bit_expr"],
            action=lambda x: ast.FuncSoundsLike(left_operand=x[0], right_operand=x[3])
        ),
        ms_parser.create_rule(
            symbols=["bit_expr", TType.KEYWORD_LIKE, "simple_expr"],
            action=lambda x: ast.FuncLike(first_operand=x[0], second_operand=x[2], third_operand=None)
        ),
        ms_parser.create_rule(
            symbols=["bit_expr", TType.KEYWORD_LIKE, "simple_expr", TType.KEYWORD_ESCAPE, "simple_expr"],
            action=lambda x: ast.FuncLike(first_operand=x[0], second_operand=x[2], third_operand=x[4]),
            sr_priority_as=TType.KEYWORD_LIKE
        ),
        ms_parser.create_rule(
            symbols=["bit_expr", TType.KEYWORD_NOT, TType.KEYWORD_LIKE, "simple_expr"],
            action=lambda x: ast.FuncNotLike(first_operand=x[0], second_operand=x[3], third_operand=None)
        ),
        ms_parser.create_rule(
            symbols=["bit_expr", TType.KEYWORD_NOT, TType.KEYWORD_LIKE, "simple_expr", TType.KEYWORD_ESCAPE,
                     "simple_expr"],
            action=lambda x: ast.FuncNotLike(first_operand=x[0], second_operand=x[3], third_operand=x[5]),
            sr_priority_as=TType.KEYWORD_LIKE
        ),
        ms_parser.create_rule(
            symbols=["bit_expr", TType.KEYWORD_REGEXP, "bit_expr"],
            action=lambda x: ast.FuncRegexp(left_operand=x[0], right_operand=x[1])
        ),
        ms_parser.create_rule(
            symbols=["bit_expr", TType.KEYWORD_NOT, TType.KEYWORD_REGEXP, "bit_expr"],
            action=lambda x: ast.FuncNotRegexp(left_operand=x[0], right_operand=x[2])
        ),
        ms_parser.create_rule(
            symbols=["bit_expr"],
            sr_priority_as=TType.OPERATOR_COLON_EQ
        )
    ]
)

# 布尔表达式 TODO 待完成
# 对应 MySQL 语义组：bool_pri
GENERAL_BOOL_EXPR = ms_parser.create_group(
    name="bool_expr",
    rules=[
        ms_parser.create_rule(
            symbols=["bool_expr", TType.KEYWORD_IS, TType.KEYWORD_NULL],
            action=lambda x: ast.FuncIsNull(operand=x[0]),
            sr_priority_as=TType.KEYWORD_IS
        ),
        ms_parser.create_rule(
            symbols=["bool_expr", TType.KEYWORD_IS, TType.KEYWORD_NOT, TType.KEYWORD_NULL],
            action=lambda x: ast.FuncIsNotNull(operand=x[0]),
            sr_priority_as=TType.KEYWORD_IS
        ),
        ms_parser.create_rule(
            symbols=["bool_expr", "operator_compare", "predicate"],
            action=lambda x: ast.FuncCompare(left_operand=x[0], right_operand=x[2], operator=x[1])
        ),
        ms_parser.create_rule(
            symbols=["predicate"],
            sr_priority_as=TType.OPERATOR_COLON_EQ
        )
    ]
)

# 一般表达式 TODO 待完成
# 对应 MySQL 语义组：expr
GENERAL_EXPR = ms_parser.create_group(
    name="expr",
    rules=[
        ms_parser.create_rule(
            symbols=["expr", TType.KEYWORD_OR, "expr"],
            action=lambda x: ast.FuncOr(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.KEYWORD_OR
        ),
        ms_parser.create_rule(
            symbols=["expr", TType.KEYWORD_XOR, "expr"],
            action=lambda x: ast.FuncXor(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.KEYWORD_XOR
        ),
        ms_parser.create_rule(
            symbols=["expr", TType.KEYWORD_AND, "expr"],
            action=lambda x: ast.FuncAnd(left_operand=x[0], right_operand=x[2]),
            sr_priority_as=TType.KEYWORD_AND
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NOT, "expr"],
            action=lambda x: ast.FuncNot(operand=x[1]),
            sr_priority_as=TType.KEYWORD_NOT
        ),
        ms_parser.create_rule(
            symbols=["bool_expr", TType.KEYWORD_IS, TType.KEYWORD_TRUE],
            action=lambda x: ast.FuncIsTrue(operand=x[0]),
            sr_priority_as=TType.KEYWORD_IS
        ),
        ms_parser.create_rule(
            symbols=["bool_expr", TType.KEYWORD_IS, TType.KEYWORD_NOT, TType.KEYWORD_TRUE],
            action=lambda x: ast.FuncIsNotTrue(operand=x[0]),
            sr_priority_as=TType.KEYWORD_IS
        ),
        ms_parser.create_rule(
            symbols=["bool_expr", TType.KEYWORD_IS, TType.KEYWORD_FALSE],
            action=lambda x: ast.FuncIsFalse(operand=x[0]),
            sr_priority_as=TType.KEYWORD_IS
        ),
        ms_parser.create_rule(
            symbols=["bool_expr", TType.KEYWORD_IS, TType.KEYWORD_NOT, TType.KEYWORD_FALSE],
            action=lambda x: ast.FuncIsNotFalse(operand=x[0]),
            sr_priority_as=TType.KEYWORD_IS
        ),
        ms_parser.create_rule(
            symbols=["bool_expr", TType.KEYWORD_IS, TType.KEYWORD_UNKNOWN],
            action=lambda x: ast.FuncIsUnknown(operand=x[0]),
            sr_priority_as=TType.KEYWORD_IS
        ),
        ms_parser.create_rule(
            symbols=["bool_expr", TType.KEYWORD_IS, TType.KEYWORD_NOT, TType.KEYWORD_UNKNOWN],
            action=lambda x: ast.FuncIsNotUnknown(operand=x[0]),
            sr_priority_as=TType.KEYWORD_IS
        ),
        ms_parser.create_rule(
            symbols=["bool_expr"],
            sr_priority_as=TType.OPERATOR_COLON_EQ
        )
    ]
)
