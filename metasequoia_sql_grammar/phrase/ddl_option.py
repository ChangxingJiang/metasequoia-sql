"""
DDL 选项（ddl option）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "CREATE_TABLE_OPTION_LIST",
    "CREATE_TABLE_OPTION_LIST_SPACE_SEPARATED",
    "CREATE_TABLE_OPTION",
    "TERNARY_OPTION",
    "ROW_FORMAT",
    "DEFAULT_CHARSET_OPTION",
    "DEFAULT_COLLATE_OPTION",
    "MERGE_INSERT_TYPE",
    "AUTOEXTEND_SIZE_OPTION",
]

# 逗号或空格分隔的 `CREATE TABLE` 语句中的表属性的列表
CREATE_TABLE_OPTION_LIST = ms_parser.create_group(
    name="create_table_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["create_table_option_list", "opt_comma", "create_table_option"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["create_table_option"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 空格分隔的 `CREATE TABLE` 语句中的表属性的列表
CREATE_TABLE_OPTION_LIST_SPACE_SEPARATED = ms_parser.create_group(
    name="create_table_option_list_space_separated",
    rules=[
        ms_parser.create_rule(
            symbols=["create_table_option_list_space_separated", "create_table_option"],
            action=ms_parser.template.action.LIST_APPEND_1
        ),
        ms_parser.create_rule(
            symbols=["create_table_option"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# `CREATE TABLE` 语句中的表属性
CREATE_TABLE_OPTION = ms_parser.create_group(
    name="create_table_option",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ENGINE, "opt_equal", "ident_or_text"],
            action=lambda x: ast.DdlOptionEngine(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SECONDARY_ENGINE, "opt_equal", TType.KEYWORD_NULL],
            action=lambda x: ast.DdlOptionSecondaryEngine(value=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SECONDARY_ENGINE, "opt_equal", "ident_or_text"],
            action=lambda x: ast.DdlOptionSecondaryEngine(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MAX_ROWS, "opt_equal", "num_literal"],
            action=lambda x: ast.DdlOptionMaxRows(value=x[2].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MIN_ROWS, "opt_equal", "num_literal"],
            action=lambda x: ast.DdlOptionMinRows(value=x[2].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AVG_ROW_LENGTH, "opt_equal", "num_literal"],
            action=lambda x: ast.DdlOptionAvgRowLength(value=x[2].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PASSWORD, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.DdlOptionPassword(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COMMENT, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.DdlOptionComment(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COMPRESSION, "opt_equal", "ident_or_text"],
            action=lambda x: ast.DdlOptionCompression(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ENCRYPTION, "opt_equal", "ident_or_text"],
            action=lambda x: ast.DdlOptionEncryption(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AUTO_INCREMENT, "opt_equal", "num_literal"],
            action=lambda x: ast.DdlOptionAutoIncrement(value=x[2].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PACK_KEYS, "opt_equal", "ternary_option"],
            action=lambda x: ast.DdlOptionPackKey(value=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STATS_AUTO_RECALC, "opt_equal", "ternary_option"],
            action=lambda x: ast.DdlOptionStatsAutoRecalc(value=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STATS_PERSISTENT, "opt_equal", "ternary_option"],
            action=lambda x: ast.DdlOptionStatsPersistent(value=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STATS_SAMPLE_PAGES, "opt_equal", "ternary_option"],
            action=lambda x: ast.DdlOptionStatsSamplePages(value=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHECKSUM, "opt_equal", "num_literal_or_hex"],
            action=lambda x: ast.DdlOptionChecksum(value=x[2].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TABLE_CHECKSUM, "opt_equal", "num_literal_or_hex"],
            action=lambda x: ast.DdlOptionTableChecksum(value=x[2].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DELAY_KEY_WRITE, "opt_equal", "num_literal_or_hex"],
            action=lambda x: ast.DdlOptionDelayKeyWrite(value=x[2].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ROW_FORMAT, "opt_equal", "row_format"],
            action=lambda x: ast.DdlOptionRowFormat(value=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UNION, "opt_equal", TType.OPERATOR_LPAREN, "opt_identifier_list",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.DdlOptionUnion(table_list=x[3])
        ),
        ms_parser.create_rule(
            symbols=["default_charset_option"]
        ),
        ms_parser.create_rule(
            symbols=["default_collate_option"]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INSERT_METHOD, "opt_equal", "merge_insert_type"],
            action=lambda x: ast.DdlOptionInsertMethod(value=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DATA, TType.KEYWORD_DIRECTORY, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.DdlOptionDataDirectory(value=x[3].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INDEX, TType.KEYWORD_DIRECTORY, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.DdlOptionIndexDirectory(value=x[3].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TABLESPACE, "opt_equal", "ident"],
            action=lambda x: ast.DdlOptionTableSpace(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STORAGE, TType.KEYWORD_DISK],
            action=lambda x: ast.DdlOptionStorage(value=ast.EnumStorageType.DISK)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STORAGE, TType.KEYWORD_MEMORY],
            action=lambda x: ast.DdlOptionStorage(value=ast.EnumStorageType.MEMORY)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CONNECTION, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.DdlOptionConnection(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_KEY_BLOCK_SIZE, "opt_equal", "num_literal"],
            action=lambda x: ast.DdlOptionKeyBlockSize(value=x[2].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_START, TType.KEYWORD_TRANSACTION],
            action=lambda _: ast.DdlOptionStartTransaction()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ENGINE_ATTRIBUTE, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.DdlOptionEngineAttribute(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SECONDARY_ENGINE_ATTRIBUTE, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.DdlOptionSecondaryEngineAttribute(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=["autoextend_size_option"]
        )
    ]
)

# 整数字面值、十六进制字面值或 `DEFAULT` 关键字
TERNARY_OPTION = ms_parser.create_group(
    name="ternary_option",
    rules=[
        ms_parser.create_rule(
            symbols=["num_literal_or_hex"]
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DEFAULT],
            action=lambda _: ast.DefaultValue()
        )
    ]
)

# 行格式类型的枚举值
ROW_FORMAT = ms_parser.create_group(
    name="row_format",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DEFAULT],
            action=lambda _: ast.EnumRowFormat.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FIXED],
            action=lambda _: ast.EnumRowFormat.FIXED
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DYNAMIC],
            action=lambda _: ast.EnumRowFormat.DYNAMIC
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COMPRESSED],
            action=lambda _: ast.EnumRowFormat.COMPRESSED
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REDUNDANT],
            action=lambda _: ast.EnumRowFormat.REDUNDANT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COMPACT],
            action=lambda _: ast.EnumRowFormat.COMPACT
        )
    ]
)

# 指定默认字符集的数据库选项或表选项
DEFAULT_CHARSET_OPTION = ms_parser.create_group(
    name="default_charset_option",
    rules=[
        ms_parser.create_rule(
            symbols=["opt_keyword_default", "keyword_charset", "opt_equal", "charset_name"],
            action=lambda x: ast.DdlOptionDefaultCharset(value=x[3])
        )
    ]
)

# 指定默认排序规则的数据库选项或表选项
DEFAULT_COLLATE_OPTION = ms_parser.create_group(
    name="default_collate_option",
    rules=[
        ms_parser.create_rule(
            symbols=["opt_keyword_default", TType.KEYWORD_COLLATE, "opt_equal", "charset_name"],
            action=lambda x: ast.DdlOptionDefaultCollate(value=x[3])
        )
    ]
)

# 向 MERGE 表插入数据的类型的枚举值
MERGE_INSERT_TYPE = ms_parser.create_group(
    name="merge_insert_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NO],
            action=lambda _: ast.EnumMergeInsertType.NO
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FIRST],
            action=lambda _: ast.EnumMergeInsertType.FIRST
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LAST],
            action=lambda _: ast.EnumMergeInsertType.LAST
        )
    ]
)

# 指定表空间每次自动扩展的大小属性
AUTOEXTEND_SIZE_OPTION = ms_parser.create_group(
    name="autoextend_size_option",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AUTOEXTEND_SIZE, "opt_equal", "size_number"],
            action=lambda x: ast.DdlOptionAutoextendSize(value=x[2])
        )
    ]
)
