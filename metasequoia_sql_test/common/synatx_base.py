from metasequoia_sql import ast
from metasequoia_sql import parse_statement

__all__ = [
    "get_select_first_expression"
]


def get_select_first_expression(sql: str):
    """获取 SELECT 语句的第一个表达式"""
    node = parse_statement(sql)
    assert isinstance(node, ast.SelectStatement)
    first_select_item = node.get_select_item(0)
    assert isinstance(first_select_item, ast.ExpressionWithAlias)
    return first_select_item.expression
