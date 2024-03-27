from metasequoia_sql.common.token_scanner import TokenScanner
from metasequoia_sql.objects.new_select import *
from metasequoia_sql import ast


def maybe_compute_operator(scanner: TokenScanner) -> bool:
    """检查是否可能为计算运算符"""
    return scanner.now.is_compute_operator


def parse_compute_operator(scanner: TokenScanner) -> SQLComputeOperator:
    """解析计算运算符"""
    token: ast.AST = scanner.pop()
    if token.source == "+":
        return SQLPlus()
    if token.source == "-":
        return SQLSubtract()
    if token.source == "*":
        return SQLMultiple()
    if token.source == "/":
        return SQLDivide()
