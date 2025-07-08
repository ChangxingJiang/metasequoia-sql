"""
修改命令（alter command）的语义组
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    # 在 ALTER TABLE 语句中直接使用的修改命令
    "OPT_ALTER_TABLE_ACTIONS",
    "STANDALONE_ALTER_TABLE_ACTION",

    # 修改命令
    "OPT_ALTER_COMMAND_LIST",
    "ALTER_COMMAND_LIST",
    "ALTER_COMMAND",

    # 各种修改命令
    "STANDALONE_ALTER_COMMANDS",
    "ALTER_LIST_ITEM",
    "ALTER_TABLE_PARTITION_OPTIONS",

    # 修改命令中的元素
    "ALL_OR_ALT_PART_NAME_LIST",
    "OPT_PLACE",
    "ALTER_ORDER_EXPR_LIST",
    "ALTER_ORDER_EXPR",
]

# 可选的包含窗口相关修改命令的修改命令的列表
OPT_ALTER_TABLE_ACTIONS = ms_parser.create_group(
    name="opt_alter_table_actions",
    rules=[
        ms_parser.create_rule(
            symbols=["opt_alter_command_list"],
            action=lambda x: x[0]
        ),
        ms_parser.create_rule(
            symbols=["opt_alter_command_list", "alter_table_partition_options"],
            action=lambda x: x[0] + [x[1]]
        )
    ]
)

# `ALTER` 命令的修饰选项的列表和独立的 `ALTER` 修改命令
STANDALONE_ALTER_TABLE_ACTION = ms_parser.create_group(
    name="standalone_alter_table_action",
    rules=[
        ms_parser.create_rule(
            symbols=["standalone_alter_commands"],
            action=lambda x: [x[0]]
        ),
        ms_parser.create_rule(
            symbols=["alter_command_modifier_list",TType.OPERATOR_COMMA, "standalone_alter_commands"],
            action=lambda x: x[0].get_list() + [x[2]]
        ),
    ]
)

# 可选的修改命令的列表
OPT_ALTER_COMMAND_LIST = ms_parser.create_group(
    name="opt_alter_command_list",
    rules=[
        ms_parser.create_rule(
            symbols=["alter_command_list"],
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)

# 修改命令的列表
ALTER_COMMAND_LIST = ms_parser.create_group(
    name="alter_command_list",
    rules=[
        ms_parser.create_rule(
            symbols=["alter_command_list", TType.OPERATOR_COMMA, "alter_command"],
            action=lambda x: x[0] + x[2]
        ),
        ms_parser.create_rule(
            symbols=["alter_command"],
            action=lambda x: x[0]
        )
    ]
)

# 单个修改命令
ALTER_COMMAND = ms_parser.create_group(
    name="alter_command",
    rules=[
        ms_parser.create_rule(
            symbols=["alter_list_item"],
            action=lambda x: [x[0]]
        ),
        ms_parser.create_rule(
            symbols=["alter_command_modifier"],
            action=lambda x: x[0].get_list()
        ),
        ms_parser.create_rule(
            symbols=["create_table_option_list_space_separated"],
            action=lambda x: x[0]
        )
    ]
)

# 独立的 `ALTER` 修改命令
STANDALONE_ALTER_COMMANDS = ms_parser.create_group(
    name="standalone_alter_commands",
    rules=[
        # DISCARD TABLESPACE
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DISCARD, TType.KEYWORD_TABLESPACE],
            action=lambda _: ast.AlterDiscardTablespace()
        ),
        # IMPORT TABLESPACE
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IMPORT, TType.KEYWORD_TABLESPACE],
            action=lambda _: ast.AlterImportTablespace()
        ),
        # ADD PARTITION opt_keyword_no_write_to_binlog
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ADD, TType.KEYWORD_PARTITION, "opt_keyword_no_write_to_binlog"],
            action=lambda x: ast.AlterAddPartition(no_write_to_binlog=x[2])
        ),
        # ADD PARTITION opt_keyword_no_write_to_binlog '(' part_def_list ')'
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ADD, TType.KEYWORD_PARTITION, "opt_keyword_no_write_to_binlog",
                     TType.OPERATOR_LPAREN, "partition_definition_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.AlterAddPartitionByDefinitionList(no_write_to_binlog=x[2], partition_list=x[4])
        ),
        # ADD PARTITION opt_keyword_no_write_to_binlog PARTITIONS real_ulong_num
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ADD, TType.KEYWORD_PARTITION, "opt_keyword_no_write_to_binlog",
                     TType.KEYWORD_PARTITIONS, "int_literal_or_hex"],
            action=lambda x: ast.AlterAddPartitionByPartitionNum(no_write_to_binlog=x[2], num_partition=x[4].value)
        ),
        # DROP PARTITION ident_string_list
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_PARTITION, "ident_list"],
            action=lambda x: ast.AlterDropPartition(partition_list=x[2])
        ),
        # REBUILD PARTITION opt_keyword_no_write_to_binlog all_or_alt_part_name_list
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REBUILD, TType.KEYWORD_PARTITION, "opt_keyword_no_write_to_binlog",
                     "all_or_alt_part_name_list"],
            action=lambda x: ast.AlterRebuildPartition(no_write_to_binlog=x[2], partition_list=x[3])
        ),
        # OPTIMIZE PARTITION opt_keyword_no_write_to_binlog all_or_alt_part_name_list
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_OPTIMIZE, TType.KEYWORD_PARTITION, "opt_keyword_no_write_to_binlog",
                     "all_or_alt_part_name_list"],
            action=lambda x: ast.AlterOptimizePartition(no_write_to_binlog=x[2], partition_list=x[3])
        ),
        # ANALYZE PARTITION opt_keyword_no_write_to_binlog all_or_alt_part_name_list
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ANALYZE, TType.KEYWORD_PARTITION, "opt_keyword_no_write_to_binlog",
                     "all_or_alt_part_name_list"],
            action=lambda x: ast.AlterAnalyzePartition(no_write_to_binlog=x[2], partition_list=x[3])
        ),
        # CHECK PARTITION all_or_alt_part_name_list opt_check_type_list
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHECK, TType.KEYWORD_PARTITION, "all_or_alt_part_name_list",
                     "opt_check_type_list"],
            action=lambda x: ast.AlterCheckPartition(partition_list=x[2], check_type=x[3])
        ),
        # REPAIR PARTITION opt_keyword_no_write_to_binlog all_or_alt_part_name_list opt_repair_type_list
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REPAIR, TType.KEYWORD_PARTITION, "opt_keyword_no_write_to_binlog",
                     "all_or_alt_part_name_list", "opt_repair_type_list"],
            action=lambda x: ast.AlterRepairPartition(no_write_to_binlog=x[2], partition_list=x[3], repair_type=x[4])
        ),
        # COALESCE PARTITION opt_keyword_no_write_to_binlog real_ulong_num
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COALESCE, TType.KEYWORD_PARTITION, "opt_keyword_no_write_to_binlog",
                     "int_literal_or_hex"],
            action=lambda x: ast.AlterCoalescePartition(no_write_to_binlog=x[2], num_partition=x[3].value)
        ),
        # TRUNCATE PARTITION all_or_alt_part_name_list
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TRUNCATE, TType.KEYWORD_PARTITION, "all_or_alt_part_name_list"],
            action=lambda x: ast.AlterTruncatePartition(partition_list=x[2])
        ),
        # REORGANIZE PARTITION opt_keyword_no_write_to_binlog
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REORGANIZE, TType.KEYWORD_PARTITION, "opt_keyword_no_write_to_binlog"],
            action=lambda x: ast.AlterReorganizePartition(no_write_to_binlog=x[2])
        ),
        # REORGANIZE PARTITION opt_keyword_no_write_to_binlog ident_string_list INTO '(' part_def_list ')'
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REORGANIZE, TType.KEYWORD_PARTITION, "opt_keyword_no_write_to_binlog",
                     "ident_list", TType.KEYWORD_INTO, TType.OPERATOR_LPAREN, "partition_definition_list",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.AlterReorganizePartitionInto(no_write_to_binlog=x[2],
                                                              source_partition_list=x[3],
                                                              target_partition_list=x[6])
        ),
        # EXCHANGE PARTITION ident WITH TABLE table_ident opt_with_validation
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXCHANGE, TType.KEYWORD_PARTITION, "ident",
                     TType.KEYWORD_WITH, TType.KEYWORD_TABLE, "identifier", "opt_alter_option_with_validation"],
            action=lambda x: ast.AlterExchangePartition(partition_name=x[2].get_str_value(),
                                                        table=x[5], with_validation=x[6])
        ),
        # DISCARD PARTITION all_or_alt_part_name_list TABLESPACE
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DISCARD, TType.KEYWORD_PARTITION, "all_or_alt_part_name_list",
                     TType.KEYWORD_TABLESPACE],
            action=lambda x: ast.AlterDiscardPartitionTablespace(partition_list=x[2])
        ),
        # IMPORT PARTITION all_or_alt_part_name_list TABLESPACE
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IMPORT, TType.KEYWORD_PARTITION, "all_or_alt_part_name_list",
                     TType.KEYWORD_TABLESPACE],
            action=lambda x: ast.AlterImportPartitionTablespace(partition_list=x[2])
        ),
        # SECONDARY_LOAD
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SECONDARY_LOAD],
            action=lambda _: ast.AlterSecondaryLoad()
        ),
        # SECONDARY_UNLOAD
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SECONDARY_UNLOAD],
            action=lambda _: ast.AlterSecondaryUnload()
        ),
    ]
)

# `ALTER TABLE` 修改命令
ALTER_LIST_ITEM = ms_parser.create_group(
    name="alter_list_item",
    rules=[
        # ADD opt_column ident field_definition opt_references opt_place
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ADD, "opt_keyword_column", "ident", "field_definition", "opt_references_definition",
                     "opt_place"],
            action=lambda x: ast.AlterAddColumn(column_name=x[2].get_str_value(), field_definition=x[3], place=x[5])
        ),
        # ADD opt_column '(' table_element_list ')'
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ADD, "opt_keyword_column", TType.OPERATOR_LPAREN, "table_element_list",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.AlterAddColumns(table_element_list=x[3])
        ),
        # ADD table_constraint_definition
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ADD, "index_definition"],
            action=lambda x: ast.AlterAddConstraint(constraint_definition=x[1])
        ),
        # CHANGE opt_column ident ident field_definition opt_place
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CHANGE, "opt_keyword_column", "ident", "ident", "field_definition", "opt_place"],
            action=lambda x: ast.AlterChangeColumn(
                old_column_name=x[2].get_str_value(),
                new_column_name=x[3].get_str_value(),
                field_definition=x[4],
                place=x[5]
            )
        ),
        # MODIFY opt_column ident field_definition opt_place
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MODIFY, "opt_keyword_column", "ident", "field_definition", "opt_place"],
            action=lambda x: ast.AlterModifyColumn(column_name=x[2].get_str_value(), field_definition=x[3], place=x[4])
        ),
        # DROP opt_column ident opt_restrict
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, "opt_keyword_column", "ident", "opt_drop_restrict"],
            action=lambda x: ast.AlterDropColumn(column_name=x[2].get_str_value(), drop_restrict=x[3])
        ),
        # DROP FOREIGN KEY ident
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_FOREIGN, TType.KEYWORD_KEY, "ident"],
            action=lambda x: ast.AlterDropForeignKey(key_name=x[3].get_str_value())
        ),
        # DROP PRIMARY KEY
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_PRIMARY, TType.KEYWORD_KEY],
            action=lambda _: ast.AlterDropPrimaryKey()
        ),
        # DROP key_or_index ident
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, "keyword_key_or_index", "ident"],
            action=lambda x: ast.AlterDropKey(key_name=x[2].get_str_value())
        ),
        # DROP CHECK ident
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_CHECK, "ident"],
            action=lambda x: ast.AlterDropCheckConstraint(constraint_name=x[2].get_str_value())
        ),
        # DROP CONSTRAINT ident
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_CONSTRAINT, "ident"],
            action=lambda x: ast.AlterDropConstraint(constraint_name=x[2].get_str_value())
        ),
        # DISABLE KEYS
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DISABLE, TType.KEYWORD_KEYS],
            action=lambda _: ast.AlterDisableKeys()
        ),
        # ENABLE KEYS
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ENABLE, TType.KEYWORD_KEYS],
            action=lambda _: ast.AlterEnableKeys()
        ),
        # ALTER opt_column ident SET DEFAULT signed_literal_or_null
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALTER, "opt_keyword_column", "ident", TType.KEYWORD_SET, TType.KEYWORD_DEFAULT,
                     "signed_literal_or_null"],
            action=lambda x: ast.AlterSetDefaultValue(column_name=x[2].get_str_value(), default_value=x[5])
        ),
        # ALTER opt_column ident SET DEFAULT '(' expr ')'
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALTER, "opt_keyword_column", "ident", TType.KEYWORD_SET, TType.KEYWORD_DEFAULT,
                     TType.OPERATOR_LPAREN, "expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.AlterSetDefaultExpression(column_name=x[2].get_str_value(), default_expression=x[6])
        ),
        # ALTER opt_column ident DROP DEFAULT
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALTER, "opt_keyword_column", "ident", TType.KEYWORD_DROP, TType.KEYWORD_DEFAULT],
            action=lambda x: ast.AlterDropDefault(column_name=x[2].get_str_value())
        ),
        # ALTER opt_column ident SET visibility
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALTER, "opt_keyword_column", "ident", TType.KEYWORD_SET,
                     "keyword_visible_or_invisible"],
            action=lambda x: ast.AlterSetColumnVisibility(column_name=x[2].get_str_value(), visibility=x[4])
        ),
        # ALTER INDEX ident visibility
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALTER, TType.KEYWORD_INDEX, "ident", "keyword_visible_or_invisible"],
            action=lambda x: ast.AlterSetIndexVisibility(index_name=x[2].get_str_value(), visibility=x[3])
        ),
        # ALTER CHECK ident constraint_enforcement
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALTER, TType.KEYWORD_CHECK, "ident", "constraint_enforcement"],
            action=lambda x: ast.AlterEnforceCheckConstraint(constraint_name=x[2].get_str_value(), enforcement=x[3])
        ),
        # ALTER CONSTRAINT ident constraint_enforcement
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALTER, TType.KEYWORD_CONSTRAINT, "ident", "constraint_enforcement"],
            action=lambda x: ast.AlterEnforceConstraint(constraint_name=x[2].get_str_value(), enforcement=x[3])
        ),
        # RENAME opt_to table_ident
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RENAME, "opt_to_or_eq_or_as", "identifier"],
            action=lambda x: ast.AlterRenameTable(new_table_name=x[2])
        ),
        # RENAME key_or_index ident TO ident
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RENAME, "keyword_key_or_index", "ident", TType.KEYWORD_TO, "ident"],
            action=lambda x: ast.AlterRenameKey(old_key_name=x[2].get_str_value(), new_key_name=x[4].get_str_value())
        ),
        # RENAME COLUMN ident TO ident
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RENAME, TType.KEYWORD_COLUMN, "ident", TType.KEYWORD_TO, "ident"],
            action=lambda x: ast.AlterRenameColumn(old_column_name=x[2].get_str_value(),
                                                   new_column_name=x[4].get_str_value())
        ),
        # CONVERT TO character_set charset_name opt_collate
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CONVERT, TType.KEYWORD_TO, "keyword_charset", "charset_name", "opt_collate"],
            action=lambda x: ast.AlterConvertToCharset(charset=x[3], collation=x[4])
        ),
        # CONVERT TO character_set DEFAULT opt_collate
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CONVERT, TType.KEYWORD_TO, "keyword_charset", TType.KEYWORD_DEFAULT, "opt_collate"],
            action=lambda x: ast.AlterConvertToDefaultCharset(collation=x[4])
        ),
        # FORCE
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FORCE],
            action=lambda _: ast.AlterForce()
        ),
        # ORDER BY alter_order_expr_list
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ORDER, TType.KEYWORD_BY, "alter_order_expr_list"],
            action=lambda x: ast.AlterOrderBy(order_list=x[2])
        )
    ]
)

# 窗口相关的修改命令
ALTER_TABLE_PARTITION_OPTIONS = ms_parser.create_group(
    name="alter_table_partition_options",
    rules=[
        ms_parser.create_rule(
            symbols=["ddl_partition_by_clause"],
            action=lambda x: ast.AlterPartitionBy(partition_clause=x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_REMOVE, TType.KEYWORD_PARTITIONING],
            action=lambda _: ast.AlterRemovePartitioning()
        )
    ]
)

# `ALL` 关键字或指定分区名称列表
ALL_OR_ALT_PART_NAME_LIST = ms_parser.create_group(
    name="all_or_alt_part_name_list",
    rules=[
        # ALL
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALL],
            action=lambda _: None
        ),
        # ident_string_list
        ms_parser.create_rule(
            symbols=["ident_list"],
            action=lambda x: x[0]
        ),
    ]
)

# 可选的变更字段插入位置
OPT_PLACE = ms_parser.create_group(
    name="opt_place",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.AlterPlaceDefault()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_AFTER, "ident"],
            action=lambda x: ast.AlterPlaceAfter(column_name=x[1].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_FIRST],
            action=lambda _: ast.AlterPlaceFirst()
        )
    ]
)

# `ALTER` 排序表达式的列表
ALTER_ORDER_EXPR_LIST = ms_parser.create_group(
    name="alter_order_expr_list",
    rules=[
        ms_parser.create_rule(
            symbols=["alter_order_expr_list", TType.OPERATOR_COMMA, "alter_order_expr"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["alter_order_expr"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# `ALTER` 排序表达式
ALTER_ORDER_EXPR = ms_parser.create_group(
    name="alter_order_expr",
    rules=[
        ms_parser.create_rule(
            symbols=["simple_ident", "opt_order_direction"],
            action=lambda x: ast.OrderExpression(column=x[0], direction=x[1])
        )
    ]
)
