"""
语义组：标识符

ident:
        IDENT
      | IDENT_QUOTED
"""

import metasequoia_parser as ms_parser

from metasequoia_sql_new import ast
from metasequoia_sql_new.terminal import SqlTerminalType as TType

# 标识符
GROUP_IDENT = ms_parser.create_group(
    name="ident",
    rules=[
        ms_parser.create_rule(symbols=[TType.IDENT], action=lambda x: ast.Ident(x[0])),
        ms_parser.create_rule(symbols=[TType.IDENT_QUOTED], action=lambda x: ast.Ident(x[0])),
    ]
)


def build_grammar():
    grammar_builder = ms_parser.create_grammar(
        groups=[
            ms_parser.create_group(
                name="entry",
                rules=[
                    ms_parser.create_rule(symbols=["ident"]),
                ]
            )
        ],
        terminal_type_enum=TType,
        start="entry",
        sr_priority=[],
    )
    grammar_builder.group_append(GROUP_IDENT)
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
