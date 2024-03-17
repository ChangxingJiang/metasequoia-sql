"""
字段表达式解析器
"""

from metasequoia_sql import ast

from metasequoia_sql.ast.functions import parse_as_tokens
from metasequoia_sql.common.token_scanner import TokenScanner


def parse_column_expression(scanner: TokenScanner):
    """解析字段表达式"""


if __name__ == "__main__":
    parse_column_expression(TokenScanner(parse_as_tokens("a * b")))
