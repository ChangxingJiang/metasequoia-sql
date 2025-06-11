"""
DDL 表元素（ddl table element）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    # 表元素
    "TABLE_ELEMENT_LIST",
    "TABLE_ELEMENT",

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
    "INDEX_DEFINITION",
    "OPT_INDEX_NAME_AND_TYPE",
    "INDEX_KEY_DEFINITION_LIST",
    "INDEX_KEY_DEFINITION",
    "INDEX_KEY_DEFINITION_WITH_EXPR_LIST",
    "INDEX_KEY_DEFINITION_WITH_EXPR",
    "CONSTRAINT_INDEX_TYPE",
    "OPT_KEYWORD_KEY_OR_INDEX",
    "KEYWORD_KEY_OR_INDEX",
    "OPT_CONSTRAINT_ENFORCEMENT",
    "CONSTRAINT_ENFORCEMENT",
]

# DDL 定义表中的元素的列表
TABLE_ELEMENT_LIST = ms_parser.create_group(
    name="table_element_list",
    rules=[
        ms_parser.create_rule(
            symbols=["table_element_list", TType.OPERATOR_COMMA, "table_element"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["table_element"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# DDL 定义表中的元素
TABLE_ELEMENT = ms_parser.create_group(
    name="table_element",
    rules=[
        ms_parser.create_rule(
            symbols=["column_definition"]
        ),
        ms_parser.create_rule(
            symbols=["index_definition"]
        )
    ]
)

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
                "identifier",  # 1
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

# DDL 的索引定义信息
INDEX_DEFINITION = ms_parser.create_group(
    name="index_definition",
    rules=[
        ms_parser.create_rule(
            symbols=[
                "keyword_key_or_index",  # 0
                "opt_index_name_and_type",  # 1
                TType.OPERATOR_LPAREN,  # 2
                "index_key_definition_with_expr_list",  # 3
                TType.OPERATOR_RPAREN,  # 4
                "opt_normal_index_attribute_list",  # 5
            ],
            action=lambda x: ast.IndexDefinition(
                index_type=ast.EnumIndexType.KEY,
                index_name=x[1].index_name,
                index_structure_type=x[1].index_structure_type,
                index_key_list=x[3],
                index_options=x[5]
            )
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_FULLTEXT,  # 0
                "opt_keyword_key_or_index",  # 1
                "opt_ident",  # 2
                TType.OPERATOR_LPAREN,  # 3
                "index_key_definition_with_expr_list",  # 4
                TType.OPERATOR_RPAREN,  # 5
                "opt_fulltext_index_attribute_list",  # 6
            ],
            action=lambda x: ast.IndexDefinition(
                index_type=ast.EnumIndexType.FULLTEXT,
                index_name=x[2],
                index_structure_type=None,
                index_key_list=x[4],
                index_options=x[6]
            )
        ),
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_SPATIAL,  # 0
                "opt_keyword_key_or_index",  # 1
                "opt_ident",  # 2
                TType.OPERATOR_LPAREN,  # 3
                "index_key_definition_with_expr_list",  # 4
                TType.OPERATOR_RPAREN,  # 5
                "opt_spatial_index_attribute_list",  # 6
            ],
            action=lambda x: ast.IndexDefinition(
                index_type=ast.EnumIndexType.SPATIAL,
                index_name=x[2],
                index_structure_type=None,
                index_key_list=x[4],
                index_options=x[6]
            )
        ),
        ms_parser.create_rule(
            symbols=[
                "opt_constraint_name",  # 0
                "constraint_index_type",  # 1
                "opt_index_name_and_type",  # 2
                TType.OPERATOR_LPAREN,  # 3
                "index_key_definition_with_expr_list",  # 4
                TType.OPERATOR_RPAREN,  # 5
                "opt_normal_index_attribute_list",  # 6
            ],
            action=lambda x: ast.IndexDefinition(
                index_type=x[1],
                index_name=x[2].index_name if x[2].index_name is not None else x[0],
                index_structure_type=x[2].index_structure_type,
                index_key_list=x[4],
                index_options=x[6]
            )
        ),
        ms_parser.create_rule(
            symbols=[
                "opt_constraint_name",  # 0
                TType.KEYWORD_FOREIGN,  # 1
                TType.KEYWORD_KEY,  # 2
                "opt_ident",  # 3
                TType.OPERATOR_LPAREN,  # 4
                "index_key_definition_list",  # 5
                TType.OPERATOR_RPAREN,  # 6
                "references_definition",  # 7
            ],
            action=lambda x: ast.ForeignKeyDefinition(
                constraint_name=x[0],
                index_name=x[3],
                column_list=x[5],
                references=x[7]
            )
        ),
        ms_parser.create_rule(
            symbols=[
                "opt_constraint_name",  # 0
                "check_constraint",  # 1
                "opt_constraint_enforcement",  # 2
            ],
            action=lambda x: ast.CheckConstraintDefinition(
                constraint_name=x[0],
                check_expression=x[1],
                enforced=x[2]
            )
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

# 索引字段定义的列表
INDEX_KEY_DEFINITION_LIST = ms_parser.create_group(
    name="index_key_definition_list",
    rules=[
        ms_parser.create_rule(
            symbols=["index_key_definition_list", TType.OPERATOR_COMMA, "index_key_definition"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["index_key_definition"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 索引字段定义
INDEX_KEY_DEFINITION = ms_parser.create_group(
    name="index_key_definition",
    rules=[
        ms_parser.create_rule(
            symbols=["ident", "opt_order_direction"],
            action=lambda x: ast.IndexKeyDefinition.create_by_column(
                column_name=x[0].get_str_value(),
                index_length=None,
                order_direction=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=["ident", TType.OPERATOR_LPAREN, TType.LITERAL_INT_NUM, TType.OPERATOR_LPAREN,
                     "opt_order_direction"],
            action=lambda x: ast.IndexKeyDefinition.create_by_column(
                column_name=x[0].get_str_value(),
                index_length=int(x[2]),
                order_direction=x[4]
            )
        )
    ]
)

# 包含使用表达式的索引字段定义的列表
INDEX_KEY_DEFINITION_WITH_EXPR_LIST = ms_parser.create_group(
    name="index_key_definition_with_expr_list",
    rules=[
        ms_parser.create_rule(
            symbols=["index_key_definition_with_expr_list", TType.OPERATOR_COMMA,
                     "index_key_definition_with_expr"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["index_key_definition_with_expr"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 包含使用表达式的索引字段定义
INDEX_KEY_DEFINITION_WITH_EXPR = ms_parser.create_group(
    name="index_key_definition_with_expr",
    rules=[
        ms_parser.create_rule(
            symbols=["index_key_definition"]
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN, "opt_order_direction"],
            action=lambda x: ast.IndexKeyDefinition.create_by_expression(
                expression=x[1],
                order_direction=x[3]
            )
        )
    ]
)

# 约束类索引类型（主键索引或唯一索引）
CONSTRAINT_INDEX_TYPE = ms_parser.create_group(
    name="constraint_index_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PRIMARY, TType.KEYWORD_KEY],
            action=lambda _: ast.EnumIndexType.PRIMARY
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UNIQUE, "opt_keyword_key_or_index"],
            action=lambda _: ast.EnumIndexType.UNIQUE
        )
    ]
)

# 可选的 `KEY`、`INDEX` 或 `INDEXES` 关键字
OPT_KEYWORD_KEY_OR_INDEX = ms_parser.create_group(
    name="opt_keyword_key_or_index",
    rules=[
        ms_parser.create_rule(
            symbols=["keyword_key_or_index"],
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# `KEY`、`INDEX` 或 `INDEXES` 关键字
KEYWORD_KEY_OR_INDEX = ms_parser.create_group(
    name="keyword_key_or_index",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_KEY]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INDEX]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INDEXES]
        )
    ]
)

# 可选的 `ENFORCED`、`NOT ENFORCED` 关键字
OPT_CONSTRAINT_ENFORCEMENT = ms_parser.create_group(
    name="opt_constraint_enforcement",
    rules=[
        ms_parser.create_rule(
            symbols=["constraint_enforcement"],
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# `ENFORCED`、`NOT ENFORCED` 关键字
CONSTRAINT_ENFORCEMENT = ms_parser.create_group(
    name="constraint_enforcement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NOT, TType.KEYWORD_ENFORCED],
            action=lambda _: False
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ENFORCED],
            action=lambda _: True
        )
    ]
)
