"""
DDL 表元素（ddl table element）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    # 字段信息
    "COLUMN_DEFINITION",
    "FIELD_DEFINITION",
    "OPT_GENERATED_ALWAYS",
    "OPT_STORED_ATTRIBUTE",
    "OPT_REFERENCES_DEFINITION",
    "REFERENCES_DEFINITION",
    "OPT_MATCH_CLAUSE",
    "OPT_ON_UPDATE_ON_DELETE",
    "REFERENCE_ACTION_OPTION",

    # 索引信息
    "OPT_INDEX_NAME_AND_TYPE",
]

# DDL 的字段定义信息（含外键约束）
COLUMN_DEFINITION = ms_parser.create_group(
    name="column_definition",
    rules=[
        ms_parser.create_rule(
            symbols=["ident", "field_definition", "opt_references_definition"],
            action=lambda x: ast.ColumnDefinition(
                column_name=x[0].get_str_value(),
                field_definition=x[1],
                references_definition=x[2]
            )
        )
    ]
)

# DDL 的字段基本信息
FIELD_DEFINITION = ms_parser.create_group(
    name="field_definition",
    rules=[
        ms_parser.create_rule(
            symbols=["field_type", "opt_column_attribute_list"],
            action=lambda x: ast.FieldDefinition(field_type=x[0], attribute_list=x[1])
        ),
        ms_parser.create_rule(
            symbols=[
                "field_type",  # 0
                "opt_collate",  # 1
                "opt_generated_always",  # 2
                TType.KEYWORD_AS,  # 3
                TType.OPERATOR_LPAREN,  # 4
                "expr",  # 5
                TType.OPERATOR_RPAREN,  # 6
                "opt_stored_attribute",  # 7
                "opt_column_attribute_list"  # 8
            ],
            action=lambda x: ast.GeneratedFieldDefinition(
                field_type=x[0],
                collate_charset=x[1],
                generated_always=x[2],
                generated_expression=x[5],
                stored_attribute=x[7],
                attribute_list=x[8]
            )
        )
    ]
)

# 可选的 `GENERATED ALWAYS` 关键字
OPT_GENERATED_ALWAYS = ms_parser.create_group(
    name="opt_generated_always",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GENERATED, TType.KEYWORD_ALWAYS],
            action=lambda _: True
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: False
        )
    ]
)

# 可选的 `VIRTUAL` 或 `STORED` 关键字
OPT_STORED_ATTRIBUTE = ms_parser.create_group(
    name="opt_stored_attribute",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_VIRTUAL],
            action=lambda _: ast.EnumStoredAttribute.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STORED],
            action=lambda _: ast.EnumStoredAttribute.STORED
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumStoredAttribute.DEFAULT
        )
    ]
)

# 可选的 `REFERENCES` 关键字引导的指定外键约束子句
OPT_REFERENCES_DEFINITION = ms_parser.create_group(
    name="opt_references_definition",
    rules=[
        ms_parser.create_rule(
            symbols=["references_definition"],
            action=lambda x: x[0]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: None
        )
    ]
)

# `REFERENCES` 关键字引导的指定外键约束子句
REFERENCES_DEFINITION = ms_parser.create_group(
    name="references_definition",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_REFERENCES,  # 0
                "table_ident",  # 1
                "opt_ident_list_parens",  # 2
                "opt_match_clause",  # 3
                "opt_on_update_on_delete"  # 4
            ],
            action=lambda x: ast.ReferencesDefinition(
                table_ident=x[1],
                column_list=x[2],
                match_clause=x[3],
                on_delete=x[4].on_delete,
                on_update=x[4].on_update
            )
        )
    ]
)

# 外键约束中可选的 `MATCH` 子句
OPT_MATCH_CLAUSE = ms_parser.create_group(
    name="opt_match_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MATCH, TType.KEYWORD_FULL],
            action=lambda _: ast.EnumReferenceMatch.MATCH_FULL
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MATCH, TType.KEYWORD_PARTIAL],
            action=lambda _: ast.EnumReferenceMatch.MATCH_PARTIAL
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MATCH, TType.KEYWORD_SIMPLE],
            action=lambda _: ast.EnumReferenceMatch.MATCH_SIMPLE
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.EnumReferenceMatch.DEFAULT
        )
    ]
)

# `REFERENCES` 指定外键约束子句中的 `ON UPDATE` 和 `ON DELETE` 子句
OPT_ON_UPDATE_ON_DELETE = ms_parser.create_group(
    name="opt_on_update_on_delete",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ON, TType.KEYWORD_UPDATE, "reference_action_option"],
            action=lambda x: ast.TempOnUpdateOnDelete(on_update=x[2], on_delete=ast.EnumReferenceActionOption.DEFAULT)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ON, TType.KEYWORD_DELETE, "reference_action_option"],
            action=lambda x: ast.TempOnUpdateOnDelete(on_update=ast.EnumReferenceActionOption.DEFAULT, on_delete=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ON, TType.KEYWORD_UPDATE, "reference_action_option",
                     TType.KEYWORD_ON, TType.KEYWORD_DELETE, "reference_action_option"],
            action=lambda x: ast.TempOnUpdateOnDelete(on_update=x[2], on_delete=x[5])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ON, TType.KEYWORD_DELETE, "reference_action_option",
                     TType.KEYWORD_ON, TType.KEYWORD_UPDATE, "reference_action_option"],
            action=lambda x: ast.TempOnUpdateOnDelete(on_update=x[5], on_delete=x[2])
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.TempOnUpdateOnDelete(on_update=ast.EnumReferenceActionOption.DEFAULT,
                                                      on_delete=ast.EnumReferenceActionOption.DEFAULT)
        )
    ]
)

# REFERENCE 子句中指定外键变化时行为的选项
REFERENCE_ACTION_OPTION = ms_parser.create_group(
    name="reference_action_option",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RESTRICT],
            action=lambda _: ast.EnumReferenceActionOption.RESTRICT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CASCADE],
            action=lambda _: ast.EnumReferenceActionOption.CASCADE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SET, TType.KEYWORD_NULL],
            action=lambda _: ast.EnumReferenceActionOption.SET_NULL
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NO, TType.KEYWORD_ACTION],
            action=lambda _: ast.EnumReferenceActionOption.NO_ACTION
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SET, TType.KEYWORD_DEFAULT],
            action=lambda _: ast.EnumReferenceActionOption.SET_DEFAULT
        )
    ]
)

# 可选的索引名称和索引数据结构
OPT_INDEX_NAME_AND_TYPE = ms_parser.create_group(
    name="opt_index_name_and_type",
    rules=[
        ms_parser.create_rule(
            symbols=["opt_ident"],
            action=lambda x: ast.TempIndexNameAndType(index_name=x[0],
                                                      index_structure_type=ast.EnumIndexStructureType.DEFAULT)
        ),
        ms_parser.create_rule(
            symbols=["opt_ident", TType.KEYWORD_USING, "index_structure_type"],
            action=lambda x: ast.TempIndexNameAndType(index_name=x[0], index_structure_type=x[2])
        ),
        ms_parser.create_rule(
            symbols=["ident", TType.KEYWORD_TYPE, "index_structure_type"],
            action=lambda x: ast.TempIndexNameAndType(index_name=x[0], index_structure_type=x[2])
        ),
    ]
)
