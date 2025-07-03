# pylint: disable=R0801

"""
LOAD 语句（load statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "LOAD_STATEMENT",
    "OPT_SOURCE_COUNT",
    "OPT_XML_ROWS_IDENTIFIED_BY",
    "OPT_IGNORE_LINES",
    "FIELD_OR_VAR",
    "FIELDS_OR_VARS",
    "OPT_FIELD_OR_VAR_SPEC",
    "LOAD_DATA_SET_ELEM",
    "LOAD_DATA_SET_LIST",
    "OPT_LOAD_DATA_SET_SPEC",
    "OPT_LOAD_PARALLEL",
    "OPT_LOAD_MEMORY",
    "OPT_LOAD_ALGORITHM",
]

# LOAD 语句
LOAD_STATEMENT = ms_parser.create_group(
    name="load_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_LOAD,  # 0
                "data_or_xml",  # 1
                "load_data_lock",  # 2
                "opt_keyword_from",  # 3
                "opt_keyword_local",  # 4
                "load_source_type",  # 5
                "text_literal_sys",  # 6
                "opt_source_count",  # 7
                "opt_keyword_in_primary_key_order",  # 8
                "opt_on_duplicate",  # 9
                TType.KEYWORD_INTO,  # 10
                TType.KEYWORD_TABLE,  # 11
                "identifier",  # 12
                "opt_partition_clause",  # 13
                "opt_load_data_charset",  # 14
                "opt_xml_rows_identified_by",  # 15
                "opt_field_term",  # 16
                "opt_line_term",  # 17
                "opt_ignore_lines",  # 18
                "opt_field_or_var_spec",  # 19
                "opt_load_data_set_spec",  # 20
                "opt_load_parallel",  # 21
                "opt_load_memory",  # 22
                "opt_load_algorithm"  # 23
            ],
            action=lambda x: ast.LoadStatement(
                data_type=x[1],
                load_data_lock=x[2],
                is_local=x[4],
                source_type=x[5],
                source_file=x[6].get_str_value(),
                source_count=x[7],
                in_primary_key_order=x[8],
                on_duplicate=x[9],
                table_ident=x[12],
                use_partition=x[13],
                load_data_charset=x[14],
                xml_rows_identified_by=x[15],
                field_option=x[16],
                line_option=x[17],
                ignore_lines=x[18],
                field_or_var_list=x[19],
                load_data_set_list=x[20],
                parallel_count=x[21],
                memory_size=x[22],
                use_bulk_algorithm=x[23]
            )
        )
    ]
)

# 可选的数据源计数
OPT_SOURCE_COUNT = ms_parser.create_group(
    name="opt_source_count",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: 0
        ),
        ms_parser.create_rule(
            symbols=[TType.WORD_COUNT, TType.LITERAL_INT_NUM],
            action=lambda x: x[1].value
        )
    ]
)

# 可选的 XML 行标识符
OPT_XML_ROWS_IDENTIFIED_BY = ms_parser.create_group(
    name="opt_xml_rows_identified_by",
    rules=[
        ms_parser.template.rule.EMPTY_RETURN_NULL,
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ROWS, TType.KEYWORD_IDENTIFIED, TType.KEYWORD_BY, "text_string"],
            action=lambda x: x[3].get_str_value()
        )
    ]
)

# 可选的忽略行数
OPT_IGNORE_LINES = ms_parser.create_group(
    name="opt_ignore_lines",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: 0
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_IGNORE, TType.LITERAL_INT_NUM, "keyword_lines_or_rows"],
            action=lambda x: x[1].value
        )
    ]
)

# 可选的字段或变量列表
OPT_FIELD_OR_VAR_SPEC = ms_parser.create_group(
    name="opt_field_or_var_spec",
    rules=[
        ms_parser.template.rule.EMPTY_RETURN_LIST,
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "fields_or_vars", TType.OPERATOR_RPAREN],
            action=lambda x: x[1]
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, TType.OPERATOR_RPAREN],
            action=lambda _: []
        )
    ]
)

# 字段或变量的列表
FIELDS_OR_VARS = ms_parser.create_group(
    name="fields_or_vars",
    rules=[
        ms_parser.create_rule(
            symbols=["fields_or_vars", TType.OPERATOR_COMMA, "field_or_var"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["field_or_var"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# 字段或变量
FIELD_OR_VAR = ms_parser.create_group(
    name="field_or_var",
    rules=[
        ms_parser.create_rule(
            symbols=["simple_ident"],
            action=lambda x: x[0]
        ),
        ms_parser.create_rule(
            symbols=["user_variable"],
            action=lambda x: x[0]
        )
    ]
)

# 可选的 LOAD 数据设置列表
OPT_LOAD_DATA_SET_SPEC = ms_parser.create_group(
    name="opt_load_data_set_spec",
    rules=[
        ms_parser.template.rule.EMPTY_RETURN_LIST,
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SET, "load_data_set_list"],
            action=lambda x: x[1]
        )
    ]
)

# LOAD 数据设置列表
LOAD_DATA_SET_LIST = ms_parser.create_group(
    name="load_data_set_list",
    rules=[
        ms_parser.create_rule(
            symbols=["load_data_set_list", TType.OPERATOR_COMMA, "load_data_set_elem"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["load_data_set_elem"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# LOAD 数据设置元素
LOAD_DATA_SET_ELEM = ms_parser.create_group(
    name="load_data_set_elem",
    rules=[
        ms_parser.create_rule(
            symbols=["simple_ident", "equal", "expr_or_default"],
            action=lambda x: ast.LoadDataSetElement(variable=x[0], expression=x[2])
        )
    ]
)

# 可选的并行加载选项
OPT_LOAD_PARALLEL = ms_parser.create_group(
    name="opt_load_parallel",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: 0
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_PARALLEL, TType.OPERATOR_EQ, TType.LITERAL_INT_NUM],
            action=lambda x: x[2].int
        )
    ]
)

# 可选的内存选项
OPT_LOAD_MEMORY = ms_parser.create_group(
    name="opt_load_memory",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: 0
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_MEMORY, TType.OPERATOR_EQ, TType.LITERAL_INT_NUM],
            action=lambda x: x[2].int
        )
    ]
)

# 可选的算法选项
OPT_LOAD_ALGORITHM = ms_parser.create_group(
    name="opt_load_algorithm",
    rules=[
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: False
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALGORITHM, TType.OPERATOR_EQ, TType.KEYWORD_BULK],
            action=lambda _: True
        )
    ]
)
