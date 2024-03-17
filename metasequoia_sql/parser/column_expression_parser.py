"""
字段表达式解析器
"""

from metasequoia_sql import ast

from metasequoia_sql.ast.functions import parse
from metasequoia_sql.common.text_scanner import TextScanner


def parse_column_expression(scanner: TextScanner):
    """解析字段表达式"""


if __name__ == "__main__":
    parse_column_expression(TextScanner(parse("a * b"))[0])
