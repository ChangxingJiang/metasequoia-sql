"""
CREATE SRS 语句（create srs statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CREATE_SRS_STATEMENT",
    "OPT_SRS_ATTRIBUTES",
    "SRS_ATTRIBUTES",
    "SRS_ATTRIBUTE",
]

# `CREATE SRS` 语句
CREATE_SRS_STATEMENT = ms_parser.create_group(
    name="create_srs_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CREATE, TType.KEYWORD_OR, TType.KEYWORD_REPLACE,
                     TType.KEYWORD_SPATIAL, TType.KEYWORD_REFERENCE, TType.KEYWORD_SYSTEM,
                     "int_literal_or_hex", "opt_srs_attribute_list"],
            action=lambda x: ast.CreateSrsStatement(
                srid=x[6].value,
                attributes=x[7],
                or_replace=True,
                if_not_exists=False
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CREATE, TType.KEYWORD_SPATIAL, TType.KEYWORD_REFERENCE, TType.KEYWORD_SYSTEM,
                     "opt_keyword_if_not_exists", "int_literal_or_hex", "opt_srs_attribute_list"],
            action=lambda x: ast.CreateSrsStatement(
                srid=x[5].value,
                attributes=x[6],
                or_replace=False,
                if_not_exists=x[4]
            )
        )
    ]
)

# 可选的 SRS 属性列表
OPT_SRS_ATTRIBUTES = ms_parser.create_group(
    name="opt_srs_attribute_list",
    rules=[
        ms_parser.create_rule(
            symbols=["srs_attribute_list"]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: []
        )
    ]
)

# SRS 属性列表
SRS_ATTRIBUTES = ms_parser.create_group(
    name="srs_attribute_list",
    rules=[
        ms_parser.create_rule(
            symbols=["srs_attribute_list", "srs_attribute"],
            action=lambda x: x[0] + [x[1]]
        ),
        ms_parser.create_rule(
            symbols=["srs_attribute"],
            action=lambda x: [x[0]]
        )
    ]
)

# SRS 属性
SRS_ATTRIBUTE = ms_parser.create_group(
    name="srs_attribute",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NAME, "text_literal_sys"],
            action=lambda x: ast.SrsAttribute(
                attribute_type=ast.SrsAttributeType.NAME,
                value=x[1].get_str_value()
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DEFINITION, "text_literal_sys"],
            action=lambda x: ast.SrsAttribute(
                attribute_type=ast.SrsAttributeType.DEFINITION,
                value=x[1].get_str_value()
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ORGANIZATION, "text_literal_sys",
                     TType.KEYWORD_IDENTIFIED, TType.KEYWORD_BY, "int_literal_or_hex"],
            action=lambda x: ast.SrsAttribute(
                attribute_type=ast.SrsAttributeType.ORGANIZATION,
                value=x[1].get_str_value(),
                organization_coordsys_id=x[4].value
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DESCRIPTION, "text_literal_sys"],
            action=lambda x: ast.SrsAttribute(
                attribute_type=ast.SrsAttributeType.DESCRIPTION,
                value=x[1].get_str_value()
            )
        )
    ]
)
