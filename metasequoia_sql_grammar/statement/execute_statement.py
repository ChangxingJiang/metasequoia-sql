"""
EXECUTE 语句（execute statement）
"""

import metasequoia_parser as ms_parser

from metasequoia_sql import ast
from metasequoia_sql.terminal import SqlTerminalType as TType

__all__ = [
    "EXECUTE_STATEMENT",
    "EXECUTE_USING",
]

# `EXECUTE` 语句
EXECUTE_STATEMENT = ms_parser.create_group(
    name="execute_statement",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_EXECUTE, "ident", "execute_using"],
            action=lambda x: ast.ExecuteStatement(statement_name=x[1], using_variables=x[2])
        )
    ]
)

# `EXECUTE` 语句的 `USING` 子句
EXECUTE_USING = ms_parser.create_group(
    name="execute_using",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_USING, "user_variable_list"],
            action=lambda x: x[1]
        ),
        ms_parser.template.rule.EMPTY_RETURN_LIST
    ]
)
