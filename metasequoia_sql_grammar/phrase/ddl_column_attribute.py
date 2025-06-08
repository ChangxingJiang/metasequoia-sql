"""
DDL 字段属性（ddl column attribute）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "OPT_COLUMN_ATTRIBUTE_LIST",
    "COLUMN_ATTRIBUTE_LIST",
    "COLUMN_ATTRIBUTE",
    "NOW_OR_SIGNED_LITERAL",
    "COLUMN_FORMAT",
    "STORAGE_MEDIA",
    "OPT_CONSTRAINT_NAME",
    "CHECK_CONSTRAINT",
]

# 可选的 DDL 字段属性的列表
OPT_COLUMN_ATTRIBUTE_LIST = ms_parser.create_group(
    name="opt_column_attribute_list",
    rules=[
        ms_parser.create_rule(
            symbols=["column_attribute_list"]
        ),
        ms_parser.template.group.EMPTY_LIST
    ]
)

# DDL 字段属性的列表
COLUMN_ATTRIBUTE_LIST = ms_parser.create_group(
    name="column_attribute_list",
    rules=[
        ms_parser.create_rule(
            symbols=["column_attribute_list", "column_attribute"],
            action=ms_parser.template.action.LIST_APPEND_1
        ),
        ms_parser.create_rule(
            symbols=["column_attribute"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# DDL 字段属性
COLUMN_ATTRIBUTE = ms_parser.create_group(
    name="column_attribute",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NULL],
            action=lambda x: ast.ColumnAttrNull()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NOT, TType.KEYWORD_NULL],
            action=lambda x: ast.ColumnAttrNotNull()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NOT, TType.KEYWORD_SECONDARY],
            action=lambda x: ast.ColumnAttrNotSecondary()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DEFAULT, "now_or_signed_literal"],
            action=lambda x: ast.ColumnAttrDefaultValue(default_value=x[1])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DEFAULT, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_LPAREN],
            action=lambda x: ast.ColumnAttrDefaultExpression(default_expression=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ON, TType.KEYWORD_UPDATE, "now_expression"],
            action=lambda x: ast.ColumnAttrOnUpdate(on_update_value=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AUTO_INCREMENT],
            action=lambda x: ast.ColumnAttrAutoIncrement()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SERIAL, TType.KEYWORD_DEFAULT, TType.KEYWORD_VALUE],
            action=lambda x: ast.ColumnAttrSerialDefaultValue()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PRIMARY, TType.KEYWORD_KEY],
            action=lambda x: ast.ColumnAttrPrimaryKey()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_KEY],
            action=lambda x: ast.ColumnAttrKey()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UNIQUE],
            action=lambda x: ast.ColumnAttrUnique()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UNIQUE, TType.KEYWORD_KEY],
            action=lambda x: ast.ColumnAttrUniqueKey()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COMMENT, "text_literal_sys"],
            action=lambda x: ast.ColumnAttrComment(comment=x[1].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COLLATE, "charset_name"],
            action=lambda x: ast.ColumnAttrCollate(charset=x[1])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COLUMN_FORMAT, "column_format"],
            action=lambda x: ast.ColumnAttrColumnFormat(column_format=x[1])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STORAGE, "storage_media"],
            action=lambda x: ast.ColumnAttrStorageMedia(storage_media=x[1])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SRID, "int_literal_or_hex"],
            action=lambda x: ast.ColumnAttrSrid(srid=x[1].value)
        ),
        ms_parser.create_rule(
            symbols=["opt_constraint_name", "check_constraint"],
            action=lambda x: ast.ColumnAttrConstraint(constraint_name=x[0], check_expression=x[1])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ENFORCED],
            action=lambda x: ast.ColumnAttrEnforced()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NOT, TType.KEYWORD_ENFORCED],
            action=lambda x: ast.ColumnAttrNotEnforced()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ENGINE_ATTRIBUTE, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.ColumnAttrEngineAttribute(attribute=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SECONDARY_ENGINE_ATTRIBUTE, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.ColumnAttrSecondaryEngineAttribute(attribute=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_VISIBLE],
            action=lambda x: ast.ColumnAttrVisible()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INVISIBLE],
            action=lambda x: ast.ColumnAttrInvisible()
        )
    ]
)

# `NOW` 关键字或数值字面值
NOW_OR_SIGNED_LITERAL = ms_parser.create_group(
    name="now_or_signed_literal",
    rules=[
        ms_parser.create_rule(
            symbols=["now_expression"],
        ),
        ms_parser.create_rule(
            symbols=["signed_literal_or_null"],
        )
    ]
)

# DDL 字段存储格式的枚举
COLUMN_FORMAT = ms_parser.create_group(
    name="column_format",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DEFAULT],
            action=lambda x: ast.EnumColumnFormat.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FIXED],
            action=lambda x: ast.EnumColumnFormat.FIXED
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DYNAMIC],
            action=lambda x: ast.EnumColumnFormat.DYNAMIC
        )
    ]
)

# DDL 字段存储介质的枚举
STORAGE_MEDIA = ms_parser.create_group(
    name="storage_media",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DEFAULT],
            action=lambda x: ast.EnumStorageMedia.DEFAULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DISK],
            action=lambda x: ast.EnumStorageMedia.DISK
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MEMORY],
            action=lambda x: ast.EnumStorageMedia.MEMORY
        )
    ]
)

# 可选的 `CONSTRAINT` 关键字引导的约束名称
OPT_CONSTRAINT_NAME = ms_parser.create_group(
    name="opt_constraint_name",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CONSTRAINT, "opt_ident"],
            action=lambda x: x[1]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)

# 指定约束条件的 `CHECK` 子句
CHECK_CONSTRAINT = ms_parser.create_group(
    name="check_constraint",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHECK, TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_LPAREN],
            action=lambda x: x[2]
        )
    ]
)
