"""
语义组：标识符


"""

import metasequoia_parser as ms_parser
from metasequoia_sql_grammar.group_ident import GROUP_IDENT
from metasequoia_sql_grammar.group_ident import GROUP_IDENT_2D
from metasequoia_sql_grammar.group_ident import GROUP_IDENT_3D
from metasequoia_sql_grammar.group_ident import GROUP_SIMPLE_IDENT
from metasequoia_sql_grammar.group_ident import GROUP_SIMPLE_IDENT_LIST
from metasequoia_sql_grammar.group_literal import GROUP_INT_LITERAL
from metasequoia_sql_grammar.group_literal import GROUP_LITERAL
from metasequoia_sql_grammar.group_literal import GROUP_LITERAL_OR_NULL
from metasequoia_sql_grammar.group_literal import GROUP_NULL_LITERAL
from metasequoia_sql_grammar.group_literal import GROUP_NUM_LITERAL
from metasequoia_sql_grammar.group_literal import GROUP_TEMPORAL_LITERAL
from metasequoia_sql_grammar.group_literal import GROUP_TEXT_LITERAL
from metasequoia_sql_new.terminal import SqlTerminalType as TType


def build_grammar():
    grammar_builder = ms_parser.create_grammar(
        groups=[
            ms_parser.create_group(
                name="entry",
                rules=[
                    ms_parser.create_rule(symbols=["simple_ident_list"]),
                    ms_parser.create_rule(symbols=["literal_or_null"]),
                ]
            )
        ],
        terminal_type_enum=TType,
        start="entry",
        sr_priority=[],
    )

    # 标识符
    grammar_builder.group_append(GROUP_IDENT)
    grammar_builder.group_append(GROUP_IDENT_2D)
    grammar_builder.group_append(GROUP_IDENT_3D)
    grammar_builder.group_append(GROUP_SIMPLE_IDENT)
    grammar_builder.group_append(GROUP_SIMPLE_IDENT_LIST)

    # 字面值
    grammar_builder.group_append(GROUP_TEXT_LITERAL)
    grammar_builder.group_append(GROUP_INT_LITERAL)
    grammar_builder.group_append(GROUP_NUM_LITERAL)
    grammar_builder.group_append(GROUP_TEMPORAL_LITERAL)
    grammar_builder.group_append(GROUP_LITERAL)
    grammar_builder.group_append(GROUP_NULL_LITERAL)
    grammar_builder.group_append(GROUP_LITERAL_OR_NULL)

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
