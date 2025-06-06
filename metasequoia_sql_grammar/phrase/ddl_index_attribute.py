"""
DDL 索引属性（ddl index attribute）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_SPATIAL_INDEX_ATTRIBUTE_LIST",
    "SPATIAL_INDEX_ATTRIBUTE_LIST",
    "SPATIAL_INDEX_ATTRIBUTE",
    "OPT_FULLTEXT_INDEX_ATTRIBUTE_LIST",
    "FULLTEXT_INDEX_ATTRIBUTE_LIST",
    "FULLTEXT_INDEX_ATTRIBUTE",
    "OPT_NORMAL_INDEX_ATTRIBUTE_LIST",
    "NORMAL_INDEX_ATTRIBUTE_LIST",
    "NORMAL_INDEX_ATTRIBUTE",
    "COMMON_INDEX_ATTRIBUTE",
    "INDEX_TYPE_CLAUSE",
    "INDEX_STRUCTURE_TYPE",
]

# 可选的 `SPATIAL` 类型索引的属性的列表
OPT_SPATIAL_INDEX_ATTRIBUTE_LIST = ms_parser.create_group(
    name="opt_spatial_index_attribute_list",
    rules=[
        ms_parser.create_rule(
            symbols=["spatial_index_attribute_list"]
        ),
        ms_parser.template.group.EMPTY_LIST
    ]
)

# `SPATIAL` 类型索引的属性的列表
SPATIAL_INDEX_ATTRIBUTE_LIST = ms_parser.create_group(
    name="spatial_index_attribute_list",
    rules=[
        ms_parser.create_rule(
            symbols=["spatial_index_attribute_list", "spatial_index_attribute"],
            action=ms_parser.template.action.LIST_APPEND_1
        ),
        ms_parser.create_rule(
            symbols=["spatial_index_attribute"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# `SPATIAL` 类型索引的属性
SPATIAL_INDEX_ATTRIBUTE = ms_parser.create_group(
    name="spatial_index_attribute",
    rules=[
        ms_parser.create_rule(
            symbols=["common_index_attribute"]
        )
    ]
)

# 可选的 `FULLTEXT` 类型索引的属性的列表
OPT_FULLTEXT_INDEX_ATTRIBUTE_LIST = ms_parser.create_group(
    name="opt_fulltext_index_attribute_list",
    rules=[
        ms_parser.create_rule(
            symbols=["fulltext_index_attribute_list"]
        ),
        ms_parser.template.group.EMPTY_LIST
    ]
)

# `FULLTEXT` 类型索引的属性的列表
FULLTEXT_INDEX_ATTRIBUTE_LIST = ms_parser.create_group(
    name="fulltext_index_attribute_list",
    rules=[
        ms_parser.create_rule(
            symbols=["fulltext_index_attribute_list", "fulltext_index_attribute"],
            action=ms_parser.template.action.LIST_APPEND_1
        ),
        ms_parser.create_rule(
            symbols=["fulltext_index_attribute"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# `FULLTEXT` 类型索引的属性
FULLTEXT_INDEX_ATTRIBUTE = ms_parser.create_group(
    name="fulltext_index_attribute",
    rules=[
        ms_parser.create_rule(
            symbols=["common_index_attribute"]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITH, TType.KEYWORD_PARSER, "ident_sys"],
            action=lambda x: ast.IndexAttrWithParser(parser_name=x[2].get_str_value())
        )
    ]
)

# 可选的普通类型索引的属性的列表
OPT_NORMAL_INDEX_ATTRIBUTE_LIST = ms_parser.create_group(
    name="opt_normal_index_attribute_list",
    rules=[
        ms_parser.create_rule(
            symbols=["normal_index_attribute_list"]
        ),
        ms_parser.template.group.EMPTY_LIST
    ]
)

# 普通类型索引的属性的列表
NORMAL_INDEX_ATTRIBUTE_LIST = ms_parser.create_group(
    name="normal_index_attribute_list",
    rules=[
        ms_parser.create_rule(
            symbols=["normal_index_attribute_list", "normal_index_attribute"],
            action=ms_parser.template.action.LIST_APPEND_1
        ),
        ms_parser.create_rule(
            symbols=["normal_index_attribute"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 普通类型索引的属性
NORMAL_INDEX_ATTRIBUTE = ms_parser.create_group(
    name="normal_index_attribute",
    rules=[
        ms_parser.create_rule(
            symbols=["common_index_attribute"]
        ),
        ms_parser.create_rule(
            symbols=["index_type_clause"]
        )
    ]
)

# 各索引类型通用的属性
COMMON_INDEX_ATTRIBUTE = ms_parser.create_group(
    name="common_index_attribute",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_KEY_BLOCK_SIZE, "opt_equal", "num_literal_or_hex"],
            action=lambda x: ast.IndexAttrKeyBlockSize(block_size=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COMMENT, "text_literal_sys"],
            action=lambda x: ast.IndexAttrComment(comment=x[1].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_VISIBLE],
            action=lambda x: ast.IndexAttrVisible()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INVISIBLE],
            action=lambda x: ast.IndexAttrInvisible()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ENGINE_ATTRIBUTE, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.IndexAttrEngineAttribute(attribute=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SECONDARY_ENGINE_ATTRIBUTE, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.IndexAttrSecondaryEngineAttribute(attribute=x[2].get_str_value())
        )
    ]
)

# 指定索引数据结构类型的子句
INDEX_TYPE_CLAUSE = ms_parser.create_group(
    name="index_type_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_USING, "index_structure_type"],
            action=lambda x: ast.IndexAttrUsingIndexType(index_structure_type=x[1])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TYPE, "index_structure_type"],
            action=lambda x: ast.IndexAttrUsingIndexType(index_structure_type=x[1])
        )
    ]
)

# 索引数据结构类型
INDEX_STRUCTURE_TYPE = ms_parser.create_group(
    name="index_structure_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BTREE],
            action=lambda _: ast.EnumIndexStructureType.BTREE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RTREE],
            action=lambda _: ast.EnumIndexStructureType.RTREE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_HASH],
            action=lambda _: ast.EnumIndexStructureType.HASH
        )
    ]
)
