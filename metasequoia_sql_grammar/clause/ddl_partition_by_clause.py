"""
DDL 中的 PARTITION BY 子句（ddl partition by clause）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal.terminal_type import SqlTerminalType as TType

__all__ = [
    # DDL 中的 PARTITION BY 子句
    "DDL_PARTITION_BY_CLAUSE",

    # DDL 的分区类型定义子句
    "PARTITION_TYPE_DEFINITION",
    "OPT_KEY_ALGORITHM",

    # `PARTITIONS` 关键字引导的指定分区数量子句
    "OPT_NUM_PARTITIONS",

    # 可选的子分区的定义子句
    "OPT_SUBPARTITION_TYPE_DEFINITION",
    "OPT_NUM_SUBPARTITIONS",

    # 分区定义子句
    "OPT_PARTITION_DEFINITION_LIST",
    "PARTITION_DEFINITION_LIST",
    "PARTITION_DEFINITION",

    # 分区值指定子句（用于分区定义子句）
    "OPT_PARTITION_VALUES",
    "PARTITION_VALUE_LIST_PARENS_LIST",
    "PARTITION_VALUE_LIST_PARENS",
    "PARTITION_VALUE_LIST",
    "PARTITION_VALUE",

    # 子分区定义子句（用于分区定义子句）
    "OPT_SUBPARTITION_DEFINITION_LIST",
    "SUBPARTITION_DEFINITION_LIST",
    "SUBPARTITION_DEFINITION",

    # 定义分区选项子句（用于分区定义子句）
    "OPT_PARTITION_OPTION_LIST",
    "PARTITION_OPTION_LIST",
    "PARTITION_OPTION",
]

# DDL 中的 PARTITION BY 子句
DDL_PARTITION_BY_CLAUSE = ms_parser.create_group(
    name="ddl_partition_by_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_PARTITION,  # 0
                TType.KEYWORD_BY,  # 1
                "partition_type_definition",  # 2
                "opt_num_partitions",  # 3
                "opt_subpartition_type_definition",  # 4
                "opt_partition_definition_list",  # 5
            ],
            action=lambda x: ast.DdlPartitionByClause(
                partition_type=x[2],
                num_partitions=x[3],
                subpartition_type=x[4],
                partition_list=x[5]
            )
        )
    ]
)

# DDL 的分区类型定义子句
PARTITION_TYPE_DEFINITION = ms_parser.create_group(
    name="partition_type_definition",
    rules=[
        ms_parser.create_rule(
            symbols=["opt_keyword_linear", TType.KEYWORD_KEY, "opt_key_algorithm", TType.OPERATOR_LPAREN,
                     "opt_ident_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.PartitionTypeDefinitionKey(key_algorithm=x[2], column_list=x[4])
        ),
        ms_parser.create_rule(
            symbols=["opt_keyword_linear", TType.KEYWORD_HASH, TType.OPERATOR_LPAREN, "binary_expr",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.PartitionTypeDefinitionHash(expression=x[3])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RANGE, TType.OPERATOR_LPAREN, "binary_expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.PartitionTypeDefinitionRange(expression=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RANGE, TType.KEYWORD_COLUMNS, TType.OPERATOR_LPAREN, "ident_list",
                     TType.OPERATOR_LPAREN],
            action=lambda x: ast.PartitionTypeDefinitionRangeColumns(column_list=x[3])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LIST, TType.OPERATOR_LPAREN, "binary_expr", TType.OPERATOR_RPAREN],
            action=lambda x: ast.PartitionTypeDefinitionList(expression=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_LIST, TType.KEYWORD_COLUMNS, TType.OPERATOR_LPAREN, "ident_list",
                     TType.OPERATOR_LPAREN],
            action=lambda x: ast.PartitionTypeDefinitionListColumns(column_list=x[3])
        )
    ]
)

# 可选的 `ALGORITHM` 关键字引导的指定分区算法子句
OPT_KEY_ALGORITHM = ms_parser.create_group(
    name="opt_key_algorithm",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALGORITHM, TType.OPERATOR_EQ, "int_literal_or_hex"],
            action=lambda x: x[2]
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的 `PARTITIONS` 关键字引导的指定分区数量子句
OPT_NUM_PARTITIONS = ms_parser.create_group(
    name="opt_num_partitions",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PARTITIONS, "int_literal_or_hex"],
            action=lambda x: x[1].value
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的子分区类型的定义子句
OPT_SUBPARTITION_TYPE_DEFINITION = ms_parser.create_group(
    name="opt_subpartition_type_definition",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SUBPARTITION, TType.KEYWORD_BY, "opt_keyword_linear", TType.KEYWORD_HASH,
                     TType.OPERATOR_LPAREN, "binary_expr", TType.OPERATOR_RPAREN, "opt_num_subpartitions"],
            action=lambda x: ast.SubPartitionTypeDefinitionByHash(expression=x[5], partition_num=x[7])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SUBPARTITION, TType.KEYWORD_BY, "opt_keyword_linear", TType.KEYWORD_KEY,
                     "opt_key_algorithm", TType.OPERATOR_LPAREN, "ident_list", TType.OPERATOR_RPAREN,
                     "opt_num_subpartitions"],
            action=lambda x: ast.SubPartitionTypeDefinitionByKey(key_algorithm=x[4], column_list=x[6],
                                                                 partition_num=x[8])
        )
    ]
)

# 可选的 `SUBPARTITION` 关键字引导的指定子分区数量子句
OPT_NUM_SUBPARTITIONS = ms_parser.create_group(
    name="opt_num_subpartitions",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SUBPARTITIONS, "int_literal_or_hex"],
            action=lambda x: x[1].value
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# 可选的括号嵌套的分区定义子句的列表
OPT_PARTITION_DEFINITION_LIST = ms_parser.create_group(
    name="opt_partition_definition_list",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "partition_definition_list", TType.OPERATOR_RPAREN],
            action=lambda x: x[1]
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)

# 分区定义子句的列表
PARTITION_DEFINITION_LIST = ms_parser.create_group(
    name="partition_definition_list",
    rules=[
        ms_parser.create_rule(
            symbols=["partition_definition_list", TType.OPERATOR_COMMA, "partition_definition"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["partition_definition"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 分区定义子句
PARTITION_DEFINITION = ms_parser.create_group(
    name="partition_definition",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PARTITION, "ident", "opt_partition_values",
                     "opt_partition_option_list", "opt_subpartition_definition_list"],
            action=lambda x: ast.PartitionDefinition(
                partition_name=x[1].get_str_value(),
                partition_values=x[2],
                partition_options=x[3],
                sub_partition_list=x[4]
            )
        )
    ]
)

# 可选的 `VALUES` 关键字引导的分区值列表子句
OPT_PARTITION_VALUES = ms_parser.create_group(
    name="opt_partition_values",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_VALUES, TType.KEYWORD_LESS, TType.KEYWORD_THAN, TType.KEYWORD_MAX_VALUE],
            action=lambda x: ast.PartitionValuesLessThanMaxValue()
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_VALUES, TType.KEYWORD_LESS, TType.KEYWORD_THAN, "partition_value_list_parens"],
            action=lambda x: ast.PartitionValuesLessThanList(value_list=x[3])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_VALUES, TType.KEYWORD_IN, "partition_value_list_parens"],
            action=lambda x: ast.PartitionValuesInValueList(value_list=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_VALUES, TType.KEYWORD_IN, TType.OPERATOR_LPAREN, "partition_value_list_parens_list",
                     TType.OPERATOR_RPAREN],
            action=lambda x: ast.PartitionValuesInValueMatrix(value_matrix=x[3])
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# “括号嵌套的分区值的列表” 的列表
PARTITION_VALUE_LIST_PARENS_LIST = ms_parser.create_group(
    name="partition_value_list_parens_list",
    rules=[
        ms_parser.create_rule(
            symbols=["partition_value_list_parens_list", TType.OPERATOR_COMMA, "partition_value_list_parens"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["partition_value_list_parens"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 括号嵌套的分区值的列表
PARTITION_VALUE_LIST_PARENS = ms_parser.create_group(
    name="partition_value_list_parens",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "partition_value_list", TType.OPERATOR_RPAREN],
            action=lambda x: x[1]
        )
    ]
)

# 分区值的列表
PARTITION_VALUE_LIST = ms_parser.create_group(
    name="partition_value_list",
    rules=[
        ms_parser.create_rule(
            symbols=["partition_value_list", TType.OPERATOR_COMMA, "partition_value"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["partition_value"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 分区值
PARTITION_VALUE = ms_parser.create_group(
    name="partition_value",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MAX_VALUE],
            action=lambda x: ast.PartitionValueMaxValue()
        ),
        ms_parser.create_rule(
            symbols=["binary_expr"],
            action=lambda x: ast.PartitionValueExpression(expression=x[0])
        )
    ]
)

# 可选的括号嵌套的定义子分区子句的列表
OPT_SUBPARTITION_DEFINITION_LIST = ms_parser.create_group(
    name="opt_subpartition_definition_list",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "subpartition_definition_list", TType.OPERATOR_RPAREN],
            action=lambda x: x[1]
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)

# 定义子分区子句的列表
SUBPARTITION_DEFINITION_LIST = ms_parser.create_group(
    name="subpartition_definition_list",
    rules=[
        ms_parser.create_rule(
            symbols=["subpartition_definition_list", TType.OPERATOR_COMMA, "subpartition_definition"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["subpartition_definition"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 定义子分区子句
SUBPARTITION_DEFINITION = ms_parser.create_group(
    name="subpartition_definition",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SUBPARTITION, "ident_or_text", "opt_partition_option_list"],
            action=lambda x: ast.SubPartitionDefinition(name=x[1], options=x[2])
        )
    ]
)

# 可选的分区配置选项的列表
OPT_PARTITION_OPTION_LIST = ms_parser.create_group(
    name="opt_partition_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["partition_option_list"]
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)

# 分区配置选项的列表
PARTITION_OPTION_LIST = ms_parser.create_group(
    name="partition_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["partition_option_list", "partition_option"],
            action=ms_parser.template.action.LIST_APPEND_1
        ),
        ms_parser.create_rule(
            symbols=["partition_option"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 分区配置选项
PARTITION_OPTION = ms_parser.create_group(
    name="partition_option",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TABLESPACE, "opt_equal", "ident"],
            action=lambda x: ast.PartitionOptionTablespace(value=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=["opt_keyword_storage", TType.KEYWORD_ENGINE, "opt_equal", "ident_or_text"],
            action=lambda x: ast.PartitionOptionStorageEngine(value=x[3].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NODEGROUP, "opt_equal", "int_literal_or_hex"],
            action=lambda x: ast.PartitionOptionNodeGroup(value=x[2].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MAX_ROWS, "opt_equal", "int_literal_or_hex"],
            action=lambda x: ast.PartitionOptionMaxRows(value=x[2].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MIN_ROWS, "opt_equal", "int_literal_or_hex"],
            action=lambda x: ast.PartitionOptionMinRows(value=x[2].value)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DATA, TType.KEYWORD_DIRECTORY, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.PartitionOptionDataDirectory(value=x[3].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INDEX, TType.KEYWORD_DIRECTORY, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.PartitionOptionIndexDirectory(value=x[3].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COMMENT, "opt_equal", "text_literal_sys"],
            action=lambda x: ast.PartitionOptionComment(value=x[2].get_str_value())
        )
    ]
)
