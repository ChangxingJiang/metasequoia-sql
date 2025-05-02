"""
JSON 表选项的语义组
"""

import metasequoia_parser as ms_parser

from metasequoia_sql_new import ast
from metasequoia_sql_new.terminal import SqlTerminalType as TType

__all__ = [
    "JSON_ON_RESPONSE",
    "JSON_ON_EMPTY",
    "JSON_ON_ERROR",
    "JSON_ON_EMPTY_OR_ERROR"
]

# Json 解析失败时的返回值
JSON_ON_RESPONSE = ms_parser.create_group(
    name="json_on_response",
    rules=[
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_ERROR],
            action=lambda x: ast.JsonOnResponse(
                response_type=ast.JsonOnResponseTypeEnum.ERROR
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_NULL],
            action=lambda x: ast.JsonOnResponse(
                response_type=ast.JsonOnResponseTypeEnum.NULL
            )
        ),
        ms_parser.create_rule(
            symbols=[TType.KEYWORD_DEFAULT, "signed_literal"],
            action=lambda x: ast.JsonOnResponse(
                response_type=ast.JsonOnResponseTypeEnum.DEFAULT,
                default_value=x[1]
            )
        )
    ]
)

# JSON 解析遇到空值时的处理方法
JSON_ON_EMPTY = ms_parser.create_group(
    name="json_on_empty",
    rules=[
        ms_parser.create_rule(
            symbols=["json_on_response", TType.KEYWORD_ON, TType.KEYWORD_EMPTY],
            action=lambda x: x[0]
        )
    ]
)

# Json 解析遇到错误时的处理方法
JSON_ON_ERROR = ms_parser.create_group(
    name="json_on_error",
    rules=[
        ms_parser.create_rule(
            symbols=["json_on_response", TType.KEYWORD_ON, TType.KEYWORD_ERROR],
            action=lambda x: x[0]
        )
    ]
)

# Json 解析遇到空值或错误时的处理方法
JSON_ON_EMPTY_OR_ERROR = ms_parser.create_group(
    name="json_on_empty_on_error",
    rules=[
        ms_parser.create_rule(
            symbols=["on_empty", "on_error"],
            action=lambda x: ast.JsonOnEmptyOnError(
                on_empty=x[0],
                on_error=x[1]
            )
        ),
        ms_parser.create_rule(
            symbols=["on_error", "on_empty"],
            action=lambda x: ast.JsonOnEmptyOnError(
                on_empty=x[1],
                on_error=x[0]
            )
        ),
        ms_parser.create_rule(
            symbols=["on_empty"],
            action=lambda x: ast.JsonOnEmptyOnError(
                on_empty=x[0],
                on_error=ast.JsonOnResponse.implicit()
            )
        ),
        ms_parser.create_rule(
            symbols=["on_error"],
            action=lambda x: ast.JsonOnEmptyOnError(
                on_empty=ast.JsonOnResponse.implicit(),
                on_error=x[0]
            )
        ),
        ms_parser.create_rule(
            symbols=[],
            action=lambda x: ast.JsonOnEmptyOnError(
                on_empty=ast.JsonOnResponse.implicit(),
                on_error=ast.JsonOnResponse.implicit()
            )
        ),
    ]
)
