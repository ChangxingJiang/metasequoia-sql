"""
字段表达式解析器
"""

import enum
from typing import List

from metasequoia_sql.ast.functions import parse_as_tokens
from metasequoia_sql.common.token_scanner import TokenScanner
from metasequoia_sql.errors import SqlParseError
from metasequoia_sql.objects.common import SQLSimpleExpression, SQLFunction

__all__ = ["parse_simple_expression_or_case_expression", "parse_sql_function"]


class ParseColumnExpressionStatus(enum.Enum):
    BEFORE_EXPRESSION = 1  # 当前指针位置一定属于当前表达式
    AFTER_EXPRESSION = 2  # 不确定当前指针位置是否属于当前表达式
    FINISH_EXPRESSION = 3  # 当前指针位置一定不属于当前表达式


def parse_simple_expression_or_case_expression(scanner: TokenScanner):
    """解析字段表达式"""
    if scanner.get().equals("CASE"):
        return  # TODO 处理 case 语句

    status = ParseColumnExpressionStatus.BEFORE_EXPRESSION
    tokens = []
    while not scanner.is_finish:
        if status == ParseColumnExpressionStatus.BEFORE_EXPRESSION:
            # 当前指针位置是函数名
            if scanner.now.is_maybe_function_name and scanner.next is not None and scanner.next.is_parenthesis:
                tokens.append(parse_sql_function(scanner))
            # 当前指针位置是插入语
            elif scanner.now.is_parenthesis:
                tokens.append(parse_simple_expression_or_case_expression(scanner.pop_as_children_scanner()))
            # 当前指针位置是其他元素
            else:
                tokens.append(scanner.pop())
            status = ParseColumnExpressionStatus.AFTER_EXPRESSION
        elif status == ParseColumnExpressionStatus.AFTER_EXPRESSION:
            # 当前指针元素是计算运算符
            if scanner.now.is_compute_operator:
                tokens.append(scanner.pop())
                status = ParseColumnExpressionStatus.AFTER_EXPRESSION
            else:
                status = ParseColumnExpressionStatus.FINISH_EXPRESSION
        elif status == ParseColumnExpressionStatus.FINISH_EXPRESSION:
            break  # TODO 检查别名

    return SQLSimpleExpression(tokens)


def parse_sql_function(scanner: TokenScanner) -> SQLFunction:
    """解析函数调用：要求当前指针位置节点为函数名，下一个节点可能为函数参数，解析为 SQLFunction 对象"""
    # 解析函数名称
    name_node = scanner.pop()
    if not name_node.is_maybe_function_name:
        raise SqlParseError(f"当前指针位置节点不可能为函数名称: node={name_node}")
    function_name: str = name_node.source

    # 解析函数参数
    function_params: List[SQLSimpleExpression] = []
    if not scanner.is_finish and scanner.get().is_parenthesis:
        for param_scanner in scanner.pop_as_children_scanner_list_split_by_comma():
            function_params.append(parse_simple_expression_or_case_expression(param_scanner))

    # 构造目标类
    return SQLFunction(function_name, function_params)


if __name__ == "__main__":
    print(parse_sql_function(
        TokenScanner([token for token in parse_as_tokens("trim(column1)") if token.is_space is False])))

    print(
        parse_simple_expression_or_case_expression(TokenScanner([token for token in parse_as_tokens("a * b") if token.is_space is False])))
    print(parse_simple_expression_or_case_expression(
        TokenScanner([token for token in parse_as_tokens("a * b * c") if token.is_space is False])))
    print(
        parse_simple_expression_or_case_expression(TokenScanner([token for token in parse_as_tokens("a + b") if token.is_space is False])))
