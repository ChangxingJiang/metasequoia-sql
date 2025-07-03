"""
窗口子句的语义组
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "WINDOW_BORDER_TYPE",
    "OPT_WINDOW_EXCLUDE",
    "WINDOW_FRAME_START",
    "WINDOW_FRAME_BOUND",
    "WINDOW_FRAME_EXTENT",
    "OPT_WINDOW_FRAME_CLAUSE",
    "WINDOW_NAME_OR_SPEC",
    "WINDOWING_CLAUSE",
    "OPT_WINDOWING_CLAUSE",
]

# 窗口的边界类型
# 对应 MySQL 语义组：window_frame_units
WINDOW_BORDER_TYPE = ms_parser.create_group(
    name="window_border_type",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ROWS],
            action=lambda _: ast.WindowBorderTypeEnum.ROWS
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_RANGE],
            action=lambda _: ast.WindowBorderTypeEnum.RANGE
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_GROUPS],
            action=lambda _: ast.WindowBorderTypeEnum.GROUPS
        )
    ]
)

# 窗口函数中可选的 EXCLUDE 子句
# 对应 MySQL 语义组：opt_window_frame_exclusion
OPT_WINDOW_EXCLUDE = ms_parser.create_group(
    name="opt_window_exclude",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXCLUDE, TType.KEYWORD_CURRENT, TType.KEYWORD_ROW],
            action=lambda _: ast.WindowExclusionTypeEnum.CURRENT_ROW
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXCLUDE, TType.KEYWORD_GROUP],
            action=lambda _: ast.WindowExclusionTypeEnum.GROUP
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXCLUDE, TType.KEYWORD_TIES],
            action=lambda _: ast.WindowExclusionTypeEnum.TIES
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXCLUDE, TType.KEYWORD_NO, TType.KEYWORD_OTHERS],
            action=lambda _: ast.WindowExclusionTypeEnum.NO_OTHERS
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.WindowExclusionTypeEnum.NULL
        )
    ]
)

# 窗口开始边界
# 对应 MySQL 语义组：window_frame_start
WINDOW_FRAME_START = ms_parser.create_group(
    name="window_frame_start",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UNBOUNDED, TType.KEYWORD_PRECEDING],
            action=lambda x: ast.WindowBorder.create_unbounded_preceding()
        ),
        ms_parser.create_rule(
            symbols=["num_literal", TType.KEYWORD_PRECEDING],
            action=lambda x: ast.WindowBorder.create_value_preceding(value=x[0])
        ),
        ms_parser.create_rule(
            symbols=["param_marker", TType.KEYWORD_PRECEDING],
            action=lambda x: ast.WindowBorder.create_value_preceding(value=x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INTERVAL, "expr", "interval_time_unit", TType.KEYWORD_PRECEDING],
            action=lambda x: ast.WindowBorder.create_interval_preceding(value=x[1], time_unit=x[2])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_CURRENT, TType.KEYWORD_ROW],
            action=lambda x: ast.WindowBorder.create_current_row()
        )
    ]
)

# 窗口开始边界或窗口结束边界
# 对应 MySQL 语义组：window_frame_bound
WINDOW_FRAME_BOUND = ms_parser.create_group(
    name="window_frame_bound",
    rules=[
        ms_parser.create_rule(
            symbols=["window_frame_start"],
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_UNBOUNDED, TType.KEYWORD_FOLLOWING],
            action=lambda x: ast.WindowBorder.create_unbounded_following()
        ),
        ms_parser.create_rule(
            symbols=["num_literal", TType.KEYWORD_FOLLOWING],
            action=lambda x: ast.WindowBorder.create_value_following(value=x[0])
        ),
        ms_parser.create_rule(
            symbols=["param_marker", TType.KEYWORD_FOLLOWING],
            action=lambda x: ast.WindowBorder.create_value_following(value=x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_INTERVAL, "expr", "interval_time_unit", TType.KEYWORD_FOLLOWING],
            action=lambda x: ast.WindowBorder.create_interval_following(value=x[1], time_unit=x[2])
        )
    ]
)

# 窗口的开始和结束边界
# 对应 MySQL 语义组：window_frame_extent + window_frame_between
WINDOW_FRAME_EXTENT = ms_parser.create_group(
    name="window_frame_extent",
    rules=[
        ms_parser.create_rule(
            symbols=["window_frame_start"],
            action=lambda x: ast.WindowBorders.create_by_start_border(start_border=x[0])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_BETWEEN, "window_frame_bound", TType.KEYWORD_AND, "window_frame_bound"],
            action=lambda x: ast.WindowBorders(start_border=x[1], end_border=x[3])
        )
    ]
)

# 窗口框架（包括边界类型、边界值、排除值）
# 对应 MySQL 语义组：opt_window_frame_clause
OPT_WINDOW_FRAME_CLAUSE = ms_parser.create_group(
    name="opt_window_frame_clause",
    rules=[
        ms_parser.create_rule(
            symbols=["window_border_type", "window_frame_extent", "opt_window_exclude"],
            action=lambda x: ast.WindowFrame(border_type=x[0], borders=x[1], exclusion=x[2])
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)

# OVER 关键字引导的窗口子句中的窗口名或窗口定义语句
# 对应 MySQL 语义组：window_name_or_spec + window_spec + window_spec_details
WINDOW_NAME_OR_SPEC = ms_parser.create_group(
    name="window_name_or_spec",
    rules=[
        ms_parser.create_rule(
            symbols=["ident"],
            action=lambda x: ast.Window.create_by_name(name=x[0].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_LPAREN, "opt_ident", "opt_partition_by_clause", "opt_order_by_clause",
                     "opt_window_frame_clause", TType.OPERATOR_RPAREN],
            action=lambda x: ast.Window(name=x[1], partition_clause=x[2], order_clause=x[3], frame_clause=x[4])
        )
    ]
)

# OVER 关键字引导的窗口子句
# 对应 MySQL 语义组：windowing_clause
WINDOWING_CLAUSE = ms_parser.create_group(
    name="windowing_clause",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_OVER, "window_name_or_spec"],
            action=lambda x: x[1]
        )
    ]
)

# 可选的 OVER 关键字引导的窗口子句
# 对应 MySQL 语义组：opt_windowing_clause
OPT_WINDOWING_CLAUSE = ms_parser.create_group(
    name="opt_windowing_clause",
    rules=[
        ms_parser.create_rule(
            symbols=["windowing_clause"],
        ),
        ms_parser.template.rule.EMPTY_RETURN_NULL
    ]
)
