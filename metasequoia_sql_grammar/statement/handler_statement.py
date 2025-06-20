"""
HANDLER 语句（handler statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "HANDLER_STATEMENT",
]

# `HANDLER` 语句
HANDLER_STATEMENT = ms_parser.create_group(
    name="handler_statement",
    rules=[
        # HANDLER table_ident OPEN opt_table_alias
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_HANDLER, "table_identifier", TType.KEYWORD_OPEN, "opt_table_alias"],
            action=lambda x: ast.HandlerOpenStatement(table_ident=x[1], table_alias=x[3])
        ),
        # HANDLER ident CLOSE
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_HANDLER, "ident", TType.KEYWORD_CLOSE],
            action=lambda x: ast.HandlerCloseStatement(handler_name=x[1].get_str_value())
        ),
        # HANDLER ident READ handler_scan_function opt_where_clause opt_limit_clause
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_HANDLER, "ident", TType.KEYWORD_READ, "handler_scan_function",
                     "opt_where_clause", "opt_limit_clause"],
            action=lambda x: ast.HandlerTableScanStatement(
                handler_name=x[1].get_str_value(),
                scan_function=x[3],
                where_clause=x[4],
                limit_clause=x[5]
            )
        ),
        # HANDLER ident READ ident handler_rkey_function opt_where_clause opt_limit_clause
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_HANDLER, "ident", TType.KEYWORD_READ, "ident", "handler_rkey_function",
                     "opt_where_clause", "opt_limit_clause"],
            action=lambda x: ast.HandlerIndexScanStatement(
                handler_name=x[1].get_str_value(),
                index_name=x[3].get_str_value(),
                rkey_function=x[4],
                where_clause=x[5],
                limit_clause=x[6]
            )
        ),
        # HANDLER ident READ ident handler_rkey_mode ( values ) opt_where_clause opt_limit_clause
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_HANDLER, "ident", TType.KEYWORD_READ, "ident", "handler_rkey_mode",
                     TType.OPERATOR_LPAREN, "row_value_list", TType.OPERATOR_RPAREN, "opt_where_clause",
                     "opt_limit_clause"],
            action=lambda x: ast.HandlerIndexRangeScanStatement(
                handler_name=x[1].get_str_value(),
                index_name=x[3].get_str_value(),
                rkey_mode=x[4],
                values=x[6],
                where_clause=x[8],
                limit_clause=x[9]
            )
        )
    ]
)
