"""
SELECT 语句（select statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    # 初级查询的第 1 种结构：简单查询
    "SIMPLE_QUERY",
    "OPT_SELECT_OPTION_LIST",
    "SELECT_OPTION_LIST",
    "SELECT_OPTION",
    "SELECT_ITEM_LIST",
    "SELECT_ITEM",
    "TABLE_WILD",

    # 初级查询的第 2 种结构：值列表构造
    "TABLE_VALUE_CONSTRUCTOR",
    "ROW_VALUE_EXPLICIT_LIST",
    "ROW_VALUE_EXPLICIT",

    # 初级查询的第 3 种结构：表名称指定
    "EXPLICIT_TABLE",

    # 初级查询
    "QUERY_PRIMARY",

    # 中级查询
    "QUERY_SECONDARY",
    "UNION_OPTION",

    # 高级查询
    "QUERY_EXPRESSION"
]

# 简单查询（包括查询选项、查询字段表达式、INTO 子句、FROM 子句、WHERE 子句、GROUP BY 子句、HAVING 子句、WINDOW 子句和 QUALIFY 子句）
SIMPLE_QUERY = ms_parser.create_group(
    name="simple_query",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SELECT, "opt_select_option_list", "select_item_list", "opt_into_clause",
                     "opt_from_clause", "opt_where_clause", "opt_group_by_clause", "opt_having_clause",
                     "opt_window_clause", "opt_qualify_clause"],
            action=lambda x: ast.SimpleQuery(
                select_option=x[1],
                select_item_list=x[2],
                into_clause=x[3],
                from_clause=x[4],
                where_clause=x[5],
                group_by_clause=x[6],
                having_clause=x[7],
                window_clause=x[8],
                qualify_clause=x[9]
            )
        )
    ]
)

# 可选的查询选项的列表
OPT_SELECT_OPTION_LIST = ms_parser.create_group(
    name="opt_select_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["select_option_list"]
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.SelectOption.DEFAULT
        )
    ]
)

# 查询选项的列表
SELECT_OPTION_LIST = ms_parser.create_group(
    name="select_option_list",
    rules=[
        ms_parser.create_rule(
            symbols=["select_option_list", "select_option"],
            action=lambda x: x[0] | x[1]
        ),
        ms_parser.create_rule(
            symbols=["select_option"],
            action=lambda x: x[0]
        )
    ]
)

# 查询选项
SELECT_OPTION = ms_parser.create_group(
    name="select_option",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_STRAIGHT_JOIN],
            action=lambda _: ast.SelectOption.STRAIGHT_JOIN
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_HIGH_PRIORITY],
            action=lambda _: ast.SelectOption.HIGH_PRIORITY
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DISTINCT],
            action=lambda _: ast.SelectOption.DISTINCT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SQL_SMALL_RESULT],
            action=lambda _: ast.SelectOption.SQL_SMALL_RESULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SQL_BIG_RESULT],
            action=lambda _: ast.SelectOption.SQL_BIG_RESULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SQL_BUFFER_RESULT],
            action=lambda _: ast.SelectOption.SQL_BUFFER_RESULT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SQL_CALC_FOUND_ROWS],
            action=lambda _: ast.SelectOption.SQL_CALC_FOUND_ROWS
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALL],
            action=lambda _: ast.SelectOption.ALL
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_SQL_NO_CACHE],
            action=lambda _: ast.SelectOption.SQL_NO_CACHE
        )
    ]
)

# SELECT 子句中的查询字段表达式的列表
SELECT_ITEM_LIST = ms_parser.create_group(
    name="select_item_list",
    rules=[
        ms_parser.create_rule(
            symbols=["select_item_list", TType.OPERATOR_COMMA, "select_item"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["select_item"],
            action=ms_parser.template.action.LIST_INIT_0
        ),
        ms_parser.create_rule(
            symbols=[TType.OPERATOR_STAR],
            action=lambda _: [ast.Wild()]
        )
    ]
)

# SELECT 子句中的查询字段表达式
SELECT_ITEM = ms_parser.create_group(
    name="select_item",
    rules=[
        ms_parser.create_rule(
            symbols=["table_wild"]
        ),
        ms_parser.create_rule(
            symbols=["expr", "opt_select_alias"],
            action=lambda x: ast.ExpressionWithAlias(expression=x[0], alias=x[1])
        )
    ]
)

# 表中所有字段的通配符
TABLE_WILD = ms_parser.create_group(
    name="table_wild",
    rules=[
        ms_parser.create_rule(
            symbols=["ident", TType.OPERATOR_DOT, TType.OPERATOR_STAR],
            action=lambda x: ast.TableWild(schema_name=None, table_name=x[0].get_str_value())
        ),
        ms_parser.create_rule(
            symbols=["ident", TType.OPERATOR_DOT, "ident", TType.OPERATOR_DOT, TType.OPERATOR_STAR],
            action=lambda x: ast.TableWild(schema_name=x[0].get_str_value(), table_name=x[2].get_str_value())
        )
    ]
)

# 通过值列表构造的表
TABLE_VALUE_CONSTRUCTOR = ms_parser.create_group(
    name="table_value_constructor",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_VALUES, "row_value_explicit_list"],
            action=lambda x: ast.TableValueConstructor(row_list=x[1])
        )
    ]
)

# `ROW` 关键字引导的值列表的列表
ROW_VALUE_EXPLICIT_LIST = ms_parser.create_group(
    name="row_value_explicit_list",
    rules=[
        ms_parser.create_rule(
            symbols=["row_value_explicit_list", TType.OPERATOR_COMMA, "row_value_explicit"],
            action=ms_parser.template.action.LIST_APPEND_2
        ),
        ms_parser.create_rule(
            symbols=["row_value_explicit"],
            action=ms_parser.template.action.LIST_INIT_0
        )
    ]
)

# `ROW` 关键字引导的值列表
ROW_VALUE_EXPLICIT = ms_parser.create_group(
    name="row_value_explicit",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ROW, TType.OPERATOR_LPAREN, "opt_expr_or_default_list", TType.OPERATOR_RPAREN],
            action=lambda x: ast.Row(value_list=x[2])
        )
    ]
)

# 明确指定表的查询
EXPLICIT_TABLE = ms_parser.create_group(
    name="explicit_table",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_TABLE, "table_ident"],
            action=lambda x: ast.ExplicitTable(table_ident=x[1])
        )
    ]
)

# 初级查询（简单查询、通过值列表构造的查询或明确指定表的查询）
QUERY_PRIMARY = ms_parser.create_group(
    name="query_primary",
    rules=[
        ms_parser.create_rule(
            symbols=["simple_query"]
        ),
        ms_parser.create_rule(
            symbols=["table_value_constructor"]
        ),
        ms_parser.create_rule(
            symbols=["explicit_table"]
        )
    ]
)

# 中级查询（在初级查询的基础上，包含 `UNION`、`EXCEPT` 或 `INTERSECT`）
QUERY_SECONDARY = ms_parser.create_group(
    name="query_expression_body",
    rules=[
        ms_parser.create_rule(
            symbols=["query_primary"]
        ),
        ms_parser.create_rule(
            symbols=["query_expression_body", TType.KEYWORD_UNION, "union_option", "query_expression_body"],
            action=lambda x: ast.Union(left_operand=x[0], union_option=x[2], right_operand=x[3])
        ),
        ms_parser.create_rule(
            symbols=["query_expression_body", TType.KEYWORD_EXCEPT, "union_option", "query_expression_body"],
            action=lambda x: ast.Except(left_operand=x[0], union_option=x[2], right_operand=x[3])
        ),
        ms_parser.create_rule(
            symbols=["query_expression_body", TType.KEYWORD_INTERSECT, "union_option", "query_expression_body"],
            action=lambda x: ast.Intersect(left_operand=x[0], union_option=x[2], right_operand=x[3])
        )
    ]
)

# 联合类型
UNION_OPTION = ms_parser.create_group(
    name="union_option",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DISTINCT],
            action=lambda _: ast.UnionOption.DISTINCT
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ALL],
            action=lambda _: ast.UnionOption.ALL
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda _: ast.UnionOption.DEFAULT
        )
    ]
)

# 高级查询（在中级查询的基础上，包含 `WITH`、`ORDER BY` 和 `LIMIT` 子句）
QUERY_EXPRESSION = ms_parser.create_group(
    name="query_expression",
    rules=[
        ms_parser.create_rule(
            symbols=["query_expression_body", "opt_order_by_clause", "opt_limit_clause"],
            action=lambda x: ast.QueryExpression(query_body=x[0], order_by_clause=x[1], limit_clause=x[2])
        )
    ]
)
