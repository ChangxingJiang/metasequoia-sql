"""
ROLLBACK 语句（rollback statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "ROLLBACK_STATEMENT"
]

# `ROLLBACK` 语句
ROLLBACK_STATEMENT = ms_parser.create_group(
    name="rollback_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ROLLBACK, "opt_keyword_work", "opt_chain_type", "opt_release_type"],
            action=lambda x: ast.RollbackTransactionStatement(chain=x[2], release=x[3])
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ROLLBACK, "opt_keyword_work", TType.KEYWORD_TO, "opt_keyword_savepoint", "ident"],
            action=lambda x: ast.RollbackToSavepointStatement(savepoint_name=x[4].get_str_value())
        )
    ]
)
