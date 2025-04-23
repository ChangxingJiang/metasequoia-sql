"""
语义组：标识符


"""

import metasequoia_parser as ms_parser
from metasequoia_sql_grammar.expr_general import GENERAL_SIMPLE_EXPR
from metasequoia_sql_grammar.ident_general import GENERAL_IDENT_2
from metasequoia_sql_grammar.ident_general import GENERAL_IDENT_3
from metasequoia_sql_grammar.ident_general import GENERAL_IDENT_SYS
from metasequoia_sql_grammar.ident_general import GENERAL_SIMPLE_IDENT
from metasequoia_sql_grammar.ident_general import GENERAL_SIMPLE_IDENT_LIST
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
from metasequoia_sql_grammar.literal_general import GENERAL_SIGNED_LITERAL
from metasequoia_sql_grammar.literal_general import GENERAL_SIGNED_LITERAL_OR_NULL
from metasequoia_sql_grammar.literal_general import GENERAL_TEMPORAL_LITERAL
from metasequoia_sql_grammar.literal_general import GENERAL_TEXT_LITERAL
from metasequoia_sql_grammar.literal_general import GENERAL_TEXT_LITERAL_SYS
from metasequoia_sql_grammar.literal_general import GENERAL_TEXT_STRING
from metasequoia_sql_new.terminal import SqlTerminalType as TType


def build_grammar():
    grammar_builder = ms_parser.create_grammar(
        groups=[
            ms_parser.create_group(
                name="entry",
                rules=[
                    ms_parser.create_rule(symbols=["simple_ident_list"]),
                    ms_parser.create_rule(symbols=["text_literal"]),
                    ms_parser.create_rule(symbols=["simple_expr"]),
                ]
            )
        ],
        terminal_type_enum=TType,
        start="entry",
        sr_priority=[],
    )

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

    # 表达式
    grammar_builder.group_append(GENERAL_SIMPLE_EXPR)

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
