"""
ANALYZE TABLE 语句（analyze table statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ANALYZE_TABLE_STATEMENT",
    "OPT_HISTOGRAM",
    "OPT_HISTOGRAM_UPDATE_PARAM"
]

# `ANALYZE TABLE` 语句
ANALYZE_TABLE_STATEMENT = ms_parser.create_group(
    name="analyze_table_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ANALYZE, "opt_keyword_no_write_to_binlog", "keyword_table_or_tables",
                     "identifier_list", "opt_histogram"],
            action=lambda x: ast.AnalyzeTableStatement(no_write_to_binlog=x[1], table_list=x[3], opt_histogram=x[4])
        )
    ]
)

# 可选的直方图参数
OPT_HISTOGRAM = ms_parser.create_group(
    name="opt_histogram",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UPDATE, TType.KEYWORD_HISTOGRAM, TType.KEYWORD_ON, "ident_list",
                     "opt_histogram_update_param"],
            action=lambda x: ast.Histogram(
                command_type=ast.EnumHistogramCommandType.UPDATE,
                column_list=x[3],
                update_param=x[4]
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DROP, TType.KEYWORD_HISTOGRAM, TType.KEYWORD_ON, "ident_list"],
            action=lambda x: ast.Histogram(
                command_type=ast.EnumHistogramCommandType.DROP,
                column_list=x[3],
                update_param=None
            )
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.Histogram(
                command_type=ast.EnumHistogramCommandType.NONE,
                column_list=[],
                update_param=None
            )
        )
    ]
)

# 直方图的更新参数
OPT_HISTOGRAM_UPDATE_PARAM = ms_parser.create_group(
    name="opt_histogram_update_param",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_WITH, TType.LITERAL_INT_NUM, TType.KEYWORD_BUCKETS],
            action=lambda x: ast.HistogramUpdateParam(num_buckets=int(x[1]), data=None)
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_USING, TType.KEYWORD_DATA, "text_literal_sys"],
            action=lambda x: ast.HistogramUpdateParam(num_buckets=None, data=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.HistogramUpdateParam(num_buckets=None, data=None)
        )
    ]
)
