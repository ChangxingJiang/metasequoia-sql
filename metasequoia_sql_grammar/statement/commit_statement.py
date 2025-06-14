"""
COMMIT 语句（commit statement）
"""

import metasequoia_parser as ms_parser
from metasequoia_sql.ast import statement as ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "COMMIT_STATEMENT",
]

# `COMMIT` 语句
COMMIT_STATEMENT = ms_parser.create_group(
    name="commit_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[
                TType.KEYWORD_COMMIT,  # 0
                "opt_keyword_work",  # 1
                "opt_chain_type",  # 2
                "opt_release_type"  # 3
            ],
            action=lambda x: ast.CommitStatement(chain_type=x[2], release_type=x[3])
        )
    ]
)
