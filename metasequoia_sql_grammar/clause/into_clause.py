"""
INTO 子句（into clause）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal.terminal_type import SqlTerminalType as TType

__all__ = [
    "OPT_INTO_CLAUSE",
    "INTO_DESTINATION",
    "OPT_LOAD_DATA_CHARSET",
    "OPT_FIELD_TERM",
    "FIELD_TERM_LIST",
    "FIELD_TERM",
    "OPT_LINE_TERM",
    "LINE_TERM_LIST",
    "LINE_TERM",
]

# 可选的 INTO 子句
OPT_INTO_CLAUSE = ms_parser.create_group(
    name="opt_into_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INTO, "into_destination"],
            action=lambda x: x[1]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)

# INTO 子句中的写入目标
INTO_DESTINATION = ms_parser.create_group(
    name="into_destination",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_OUTFILE, "text_literal_sys", "opt_load_data_charset", "opt_field_term",
                     "opt_line_term"],
            action=lambda x: ast.IntoClauseOutfile(file_path=x[1], charset=x[2], field_option=x[3], line_option=x[4])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DUMPFILE, "text_literal_sys"],
            action=lambda x: ast.IntoClauseDumpfile(file_path=x[1])
        ),
        ms_parser.create_rule(
            symbols=["user_or_local_variable_list"],
            action=lambda x: ast.IntoClauseVariable(variable_list=x[0])
        )
    ]
)

# 可选的 INTO 子句和 LOAD 语句中指定字符集的子句
OPT_LOAD_DATA_CHARSET = ms_parser.create_group(
    name="opt_load_data_charset",
    rules=[
        ms_parser.create_rule(
            symbols=["keyword_charset", "charset_name"],
            action=lambda x: x[1]
        ),
        ms_parser.template.group.EMPTY_NULL
    ]
)

# 可选的 COLUMNS 引导的外部文件字段格式选项的列表
OPT_FIELD_TERM = ms_parser.create_group(
    name="opt_field_term",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COLUMNS, "field_term_list"],
            action=lambda x: x[1]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.FileFieldOption()
        )
    ]
)

# 外部文件字段格式选项的列表
FIELD_TERM_LIST = ms_parser.create_group(
    name="field_term_list",
    rules=[
        ms_parser.create_rule(
            symbols=["field_term_list", "field_term"],
            action=lambda x: x[0].merge(x[1])
        ),
        ms_parser.create_rule(
            symbols=["field_term"]
        )
    ]
)

# 外部文件字段格式选项
FIELD_TERM = ms_parser.create_group(
    name="field_term",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TERMINATED, TType.KEYWORD_BY, "text_string"],
            action=lambda x: ast.FileFieldOption(terminated_by=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_OPTIONALLY, TType.KEYWORD_ENCLOSED, TType.KEYWORD_BY, "text_string"],
            action=lambda x: ast.FileFieldOption(optionally_enclosed_by=x[3].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ENCLOSED, TType.KEYWORD_BY, "text_string"],
            action=lambda x: ast.FileFieldOption(enclosed_by=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ESCAPED, TType.KEYWORD_BY, "text_string"],
            action=lambda x: ast.FileFieldOption(escaped_by=x[2].get_str_value())
        )
    ]
)

# 可选的 LINES 引导的外部文件行格式选项的列表
OPT_LINE_TERM = ms_parser.create_group(
    name="opt_line_term",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_COLUMNS, "line_term_list"],
            action=lambda x: x[1]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.FileLineOption()
        )
    ]
)

# 外部文件行格式选项的列表
LINE_TERM_LIST = ms_parser.create_group(
    name="line_term_list",
    rules=[
        ms_parser.create_rule(
            symbols=["line_term_list", "line_term"],
            action=lambda x: x[0].merge(x[1])
        ),
        ms_parser.create_rule(
            symbols=["line_term"]
        )
    ]
)

# 外部文件行格式选项
LINE_TERM = ms_parser.create_group(
    name="line_term",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TERMINATED, TType.KEYWORD_BY, "text_string"],
            action=lambda x: ast.FileLineOption(terminated_by=x[2].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STARTING, TType.KEYWORD_BY, "text_string"],
            action=lambda x: ast.FileLineOption(starting_by=x[2].get_str_value())
        ),
    ]
)
