"""
语义组：标识符


"""

import metasequoia_parser as ms_parser

from metasequoia_sql_grammar.group_ident import GROUP_IDENT
from metasequoia_sql_grammar.group_ident import GROUP_IDENT_2D
from metasequoia_sql_grammar.group_ident import GROUP_IDENT_3D
from metasequoia_sql_grammar.group_ident import GROUP_SIMPLE_IDENT
from metasequoia_sql_grammar.group_ident import GROUP_SIMPLE_IDENT_LIST
from metasequoia_sql_new import ast
from metasequoia_sql_new.terminal import SqlTerminalType as TType

GROUP_TEXT_LITERAL = ms_parser.create_group(
    name="text_literal",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.LITERAL_TEXT_STRING],
            action=lambda x: ast.TextLiteral(value=x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.LITERAL_NCHAR_STRING],
            action=lambda x: ast.TextLiteral(value=x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.LITERAL_UNDERSCORE_CHARSET],
            action=lambda x: ast.TextLiteral(value=x[0])
        ),
    ]
)

GROUP_NUM_LITERAL = ms_parser.create_group(
    name="num_literal",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.LITERAL_NUM],
            action=lambda x: ast.Ident(x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.LITERAL_NCHAR_STRING],
            action=lambda x: ast.Ident(x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.LITERAL_UNDERSCORE_CHARSET],
            action=lambda x: ast.Ident(x[0])
        ),
    ]
)


def build_grammar():
    grammar_builder = ms_parser.create_grammar(
        groups=[
            ms_parser.create_group(
                name="entry",
                rules=[
                    ms_parser.create_rule(symbols=["simple_ident_list"]),
                ]
            )
        ],
        terminal_type_enum=TType,
        start="entry",
        sr_priority=[],
    )
    grammar_builder.group_append(GROUP_IDENT)
    grammar_builder.group_append(GROUP_IDENT_2D)
    grammar_builder.group_append(GROUP_IDENT_3D)
    grammar_builder.group_append(GROUP_SIMPLE_IDENT)
    grammar_builder.group_append(GROUP_SIMPLE_IDENT_LIST)
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
