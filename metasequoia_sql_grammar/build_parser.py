"""
语义组：标识符


"""

import metasequoia_parser as ms_parser

from metasequoia_sql_grammar.basic_general import GENERAL_OPT_OF
from metasequoia_sql_grammar.dql_general import GENERAL_GROUP_BY_LIST
from metasequoia_sql_grammar.dql_general import GENERAL_OPT_ORDER_BY_CLAUSE
from metasequoia_sql_grammar.dql_general import GENERAL_ORDER_BY_LIST
from metasequoia_sql_grammar.dql_general import GENERAL_ORDER_EXPR
from metasequoia_sql_grammar.enum_general import GENERAL_OPERATOR_COMPARE
from metasequoia_sql_grammar.enum_general import GENERAL_OPT_ORDER_DIRECTION
from metasequoia_sql_grammar.enum_general import GENERAL_ORDER_DIRECTION
from metasequoia_sql_grammar.expr_general import GENERAL_BINARY_EXPR
from metasequoia_sql_grammar.expr_general import GENERAL_BOOL_EXPR
from metasequoia_sql_grammar.expr_general import GENERAL_EXPR
from metasequoia_sql_grammar.expr_general import GENERAL_PREDICATE_EXPR
from metasequoia_sql_grammar.expr_general import GENERAL_SIMPLE_EXPR
from metasequoia_sql_grammar.ident_general import GENERAL_IDENT_2
from metasequoia_sql_grammar.ident_general import GENERAL_IDENT_3
from metasequoia_sql_grammar.ident_general import GENERAL_IDENT_SYS
from metasequoia_sql_grammar.ident_general import GENERAL_SIMPLE_IDENT
from metasequoia_sql_grammar.ident_general import GENERAL_SIMPLE_IDENT_LIST
from metasequoia_sql_grammar.ident_general import OPT_IDENT
from metasequoia_sql_grammar.ident_mysql import MYSQL_IDENT
from metasequoia_sql_grammar.ident_mysql import MYSQL_IDENT_KEYWORD
from metasequoia_sql_grammar.ident_mysql import MYSQL_IDENT_KEYWORDS_AMBIGUOUS_1_ROLES_AND_LABELS
from metasequoia_sql_grammar.ident_mysql import MYSQL_IDENT_KEYWORDS_AMBIGUOUS_2_LABELS
from metasequoia_sql_grammar.ident_mysql import MYSQL_IDENT_KEYWORDS_AMBIGUOUS_3_ROLES
from metasequoia_sql_grammar.ident_mysql import MYSQL_IDENT_KEYWORDS_AMBIGUOUS_4_SYSTEM_VARIABLES
from metasequoia_sql_grammar.ident_mysql import MYSQL_IDENT_KEYWORDS_UNAMBIGUOUS
from metasequoia_sql_grammar.ident_mysql import MYSQL_LABEL_IDENT
from metasequoia_sql_grammar.ident_mysql import MYSQL_LABEL_KEYWORD
from metasequoia_sql_grammar.ident_mysql import MYSQL_ROLE_IDENT
from metasequoia_sql_grammar.ident_mysql import MYSQL_ROLE_KEYWORD
from metasequoia_sql_grammar.ident_mysql import MYSQL_VARIABLE_IDENT
from metasequoia_sql_grammar.ident_mysql import MYSQL_VARIABLE_KEYWORD
from metasequoia_sql_grammar.literal_general import GENERAL_INT_LITERAL
from metasequoia_sql_grammar.literal_general import GENERAL_LITERAL
from metasequoia_sql_grammar.literal_general import GENERAL_LITERAL_OR_NULL
from metasequoia_sql_grammar.literal_general import GENERAL_NULL_LITERAL
from metasequoia_sql_grammar.literal_general import GENERAL_NUM_LITERAL
from metasequoia_sql_grammar.literal_general import GENERAL_PARAM_MARKER
from metasequoia_sql_grammar.literal_general import GENERAL_SIGNED_LITERAL
from metasequoia_sql_grammar.literal_general import GENERAL_SIGNED_LITERAL_OR_NULL
from metasequoia_sql_grammar.literal_general import GENERAL_TEMPORAL_LITERAL
from metasequoia_sql_grammar.literal_general import GENERAL_TEXT_LITERAL
from metasequoia_sql_grammar.literal_general import GENERAL_TEXT_LITERAL_SYS
from metasequoia_sql_grammar.literal_general import GENERAL_TEXT_STRING
from metasequoia_sql_grammar.time_unit import INTERVAL_TIME_UNIT
from metasequoia_sql_grammar.time_unit import TIME_UNIT
from metasequoia_sql_grammar.window_clause import OPT_PARTITION_CLAUSE
from metasequoia_sql_grammar.window_clause import OPT_WINDOWING_CLAUSE
from metasequoia_sql_grammar.window_clause import OPT_WINDOW_EXCLUDE
from metasequoia_sql_grammar.window_clause import OPT_WINDOW_FRAME_CLAUSE
from metasequoia_sql_grammar.window_clause import WINDOWING_CLAUSE
from metasequoia_sql_grammar.window_clause import WINDOW_BORDER_TYPE
from metasequoia_sql_grammar.window_clause import WINDOW_FRAME_BOUND
from metasequoia_sql_grammar.window_clause import WINDOW_FRAME_EXTENT
from metasequoia_sql_grammar.window_clause import WINDOW_FRAME_START
from metasequoia_sql_grammar.window_clause import WINDOW_NAME_OR_SPEC
from metasequoia_sql_new.terminal import SqlTerminalType as TType


def build_grammar():
    grammar_builder = ms_parser.create_grammar(
        groups=[
            ms_parser.create_group(
                name="entry",
                rules=[
                    # ms_parser.create_rule(symbols=["simple_ident_list"]),
                    # ms_parser.create_rule(symbols=["text_literal"]),
                    ms_parser.create_rule(symbols=["opt_windowing_clause"]),
                ]
            )
        ],
        terminal_type_enum=TType,
        start="entry",
        sr_priority=[
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_INTO],
                combine_type=ms_parser.COMBINE_RIGHT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.EMPTY_FROM_CLAUSE],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.OPERATOR_LPAREN, TType.OPERATOR_RPAREN],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.SUBQUERY_AS_EXPR],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_INTERVAL],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_BINARY, TType.KEYWORD_COLLATE],
                combine_type=ms_parser.COMBINE_RIGHT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_NOT, TType.KEYWORD_NOT2],
                combine_type=ms_parser.COMBINE_RIGHT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.NEG, TType.OPERATOR_TILDE],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.OPERATOR_BAR_BAR],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.OPERATOR_CARET],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.OPERATOR_STAR, TType.OPERATOR_SLASH, TType.OPERATOR_PERCENT, TType.KEYWORD_DIV,
                         TType.KEYWORD_MOD],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.OPERATOR_SUB, TType.OPERATOR_PLUS],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.OPERATOR_LT_LT, TType.OPERATOR_GT_GT],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.OPERATOR_AMP],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.OPERATOR_BAR],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.OPERATOR_EQ, TType.OPERATOR_LT_EQ_GT, TType.OPERATOR_GT_EQ, TType.OPERATOR_GT,
                         TType.OPERATOR_LT_EQ, TType.OPERATOR_LT, TType.OPERATOR_BANG_EQ, TType.KEYWORD_IS,
                         TType.KEYWORD_LIKE, TType.KEYWORD_REGEXP, TType.KEYWORD_IN],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_BETWEEN, TType.KEYWORD_CASE, TType.KEYWORD_WHEN, TType.KEYWORD_THEN,
                         TType.KEYWORD_ELSE],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_AND, TType.OPERATOR_AMP_AMP],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_XOR],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_OR],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.OPERATOR_COLON_EQ],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_JOIN, TType.KEYWORD_INNER, TType.STRAIGHT_JOIN, TType.KEYWORD_NATURAL,
                         TType.KEYWORD_LEFT, TType.KEYWORD_RIGHT, TType.KEYWORD_ON, TType.KEYWORD_USING],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.CONDITIONLESS_JOIN],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_INTERSECT],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_UNION, TType.KEYWORD_EXCEPT],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_UNIQUE, TType.KEYWORD_KEY],
                combine_type=ms_parser.COMBINE_RIGHT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_USED_AS_KEYWORD],
                combine_type=ms_parser.COMBINE_LEFT
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.LITERAL_TEXT_STRING],
                combine_type=ms_parser.COMBINE_NONASSOC
            ),
            ms_parser.create_sr_priority(
                symbols=[TType.KEYWORD_USED_AS_IDENT],
                combine_type=ms_parser.COMBINE_LEFT
            )
        ]
    )

    # 时间单位类型
    grammar_builder.group_append(INTERVAL_TIME_UNIT)
    grammar_builder.group_append(TIME_UNIT)

    # 窗口子句
    grammar_builder.group_append(WINDOW_BORDER_TYPE)
    grammar_builder.group_append(OPT_WINDOW_EXCLUDE)
    grammar_builder.group_append(WINDOW_FRAME_START)
    grammar_builder.group_append(WINDOW_FRAME_BOUND)
    grammar_builder.group_append(WINDOW_FRAME_EXTENT)
    grammar_builder.group_append(OPT_WINDOW_FRAME_CLAUSE)
    grammar_builder.group_append(OPT_PARTITION_CLAUSE)
    grammar_builder.group_append(WINDOW_NAME_OR_SPEC)
    grammar_builder.group_append(WINDOWING_CLAUSE)
    grammar_builder.group_append(OPT_WINDOWING_CLAUSE)

    # 基础元素
    grammar_builder.group_append(GENERAL_OPT_OF)
    grammar_builder.group_append(GENERAL_OPERATOR_COMPARE)

    # 标识符
    grammar_builder.group_append(GENERAL_IDENT_SYS)
    grammar_builder.group_append(MYSQL_IDENT_KEYWORDS_UNAMBIGUOUS)
    grammar_builder.group_append(MYSQL_IDENT_KEYWORDS_AMBIGUOUS_1_ROLES_AND_LABELS)
    grammar_builder.group_append(MYSQL_IDENT_KEYWORDS_AMBIGUOUS_2_LABELS)
    grammar_builder.group_append(MYSQL_IDENT_KEYWORDS_AMBIGUOUS_3_ROLES)
    grammar_builder.group_append(MYSQL_IDENT_KEYWORDS_AMBIGUOUS_4_SYSTEM_VARIABLES)
    grammar_builder.group_append(MYSQL_IDENT_KEYWORD)
    grammar_builder.group_append(MYSQL_LABEL_KEYWORD)
    grammar_builder.group_append(MYSQL_ROLE_KEYWORD)
    grammar_builder.group_append(MYSQL_VARIABLE_KEYWORD)
    grammar_builder.group_append(MYSQL_IDENT)
    grammar_builder.group_append(MYSQL_LABEL_IDENT)
    grammar_builder.group_append(MYSQL_ROLE_IDENT)
    grammar_builder.group_append(MYSQL_VARIABLE_IDENT)
    grammar_builder.group_append(GENERAL_IDENT_2)
    grammar_builder.group_append(GENERAL_IDENT_3)
    grammar_builder.group_append(GENERAL_SIMPLE_IDENT)
    grammar_builder.group_append(GENERAL_SIMPLE_IDENT_LIST)
    grammar_builder.group_append(OPT_IDENT)

    # 字面值
    grammar_builder.group_append(GENERAL_TEXT_LITERAL_SYS)
    grammar_builder.group_append(GENERAL_INT_LITERAL)
    grammar_builder.group_append(GENERAL_NUM_LITERAL)
    grammar_builder.group_append(GENERAL_TEMPORAL_LITERAL)
    grammar_builder.group_append(GENERAL_LITERAL)
    grammar_builder.group_append(GENERAL_NULL_LITERAL)
    grammar_builder.group_append(GENERAL_LITERAL_OR_NULL)
    grammar_builder.group_append(GENERAL_TEXT_LITERAL)
    grammar_builder.group_append(GENERAL_TEXT_STRING)
    grammar_builder.group_append(GENERAL_SIGNED_LITERAL)
    grammar_builder.group_append(GENERAL_SIGNED_LITERAL_OR_NULL)
    grammar_builder.group_append(GENERAL_PARAM_MARKER)

    # 表达式
    grammar_builder.group_append(GENERAL_SIMPLE_EXPR)
    grammar_builder.group_append(GENERAL_BINARY_EXPR)
    grammar_builder.group_append(GENERAL_PREDICATE_EXPR)
    grammar_builder.group_append(GENERAL_BOOL_EXPR)
    grammar_builder.group_append(GENERAL_EXPR)

    # DQL 语句
    grammar_builder.group_append(GENERAL_GROUP_BY_LIST)
    grammar_builder.group_append(GENERAL_ORDER_DIRECTION)
    grammar_builder.group_append(GENERAL_OPT_ORDER_DIRECTION)
    grammar_builder.group_append(GENERAL_ORDER_EXPR)
    grammar_builder.group_append(GENERAL_ORDER_BY_LIST)
    grammar_builder.group_append(GENERAL_OPT_ORDER_BY_CLAUSE)

    return grammar_builder.build()


if __name__ == "__main__":
    import os

    repository_path = os.path.dirname(os.path.dirname(__file__))
    parser_path = os.path.join(repository_path, "metasequoia_sql_new", "syntax", "parser.py")

    parser = ms_parser.parser.ParserLALR1(build_grammar())
    source_code = ms_parser.compiler.compile_lalr1(parser, import_list=[
        "from metasequoia_sql_new import ast"
    ])
    with open(parser_path, "w+", encoding="UTF-8") as file:
        for row in source_code:
            file.write(f"{row}\n")
