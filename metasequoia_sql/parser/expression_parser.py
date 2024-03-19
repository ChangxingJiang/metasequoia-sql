"""
字段表达式解析器
"""

import enum
from typing import List

from metasequoia_sql.ast.functions import parse_as_tokens
from metasequoia_sql.common.token_scanner import TokenScanner
from metasequoia_sql.errors import SqlParseError
from metasequoia_sql.objects.common import SQLSimpleExpression, SQLFunction, SQLVariable
from metasequoia_sql.objects.data_source import DataSource

__all__ = ["parse_simple_expression_or_case_expression", "parse_sql_function"]


def check_sql_function(scanner: TokenScanner) -> bool:
    """判断 scanner 当前指针位置是否为函数调用"""
    return scanner.now.is_maybe_function_name and scanner.next is not None and scanner.next.is_parenthesis


def parse_sql_function(scanner: TokenScanner, data_source: DataSource) -> SQLFunction:
    """解析函数调用：要求当前指针位置节点为函数名，下一个节点可能为函数参数，解析为 SQLFunction 对象"""
    if not check_sql_function(scanner):
        raise SqlParseError(f"当前指针位置不满足解析函数调用: node={scanner}")

    # 解析函数名称
    function_name: str = scanner.pop().source

    # 解析函数参数
    function_params: List[SQLSimpleExpression] = []
    if not scanner.is_finish and scanner.get().is_parenthesis:
        for param_scanner in scanner.pop_as_children_scanner_list_split_by_comma():
            function_params.append(parse_simple_expression_or_case_expression(param_scanner, data_source))

    # 构造目标类
    return SQLFunction(function_name, function_params)


def check_sql_variable(scanner: TokenScanner, data_source: DataSource) -> bool:
    """判断 scanner 当前指针位置是否为变量引用"""
    if data_source == DataSource.MYSQL:
        return scanner.now.source.upper() in {"CURRENT_DATE", "CURRENT_TIME", "CURRENT_TIMESTAMP", "CURRENT_USER"}
    if data_source == DataSource.HIVE:
        return scanner.now.source.upper() in {"CURRENT_DATE", "CURRENT_TIMESTAMP"}


def parse_sql_variable(scanner: TokenScanner, data_source: DataSource) -> SQLVariable:
    """解析变量引用"""
    if not check_sql_variable(scanner, data_source):
        raise SqlParseError(f"当前指针位置不满足解析变量引用: node={scanner}")

    return SQLVariable(scanner.pop().source)


class ParseColumnExpressionStatus(enum.Enum):
    BEFORE_EXPRESSION = 1  # 当前指针位置一定属于当前表达式
    AFTER_EXPRESSION = 2  # 不确定当前指针位置是否属于当前表达式
    FINISH_EXPRESSION = 3  # 当前指针位置一定不属于当前表达式


def parse_simple_expression_or_case_expression(scanner: TokenScanner, data_source: DataSource):
    """解析基础表达式"""
    if scanner.get().equals("CASE"):
        return  # TODO 处理 case 语句

    status = ParseColumnExpressionStatus.BEFORE_EXPRESSION
    tokens = []
    while status != ParseColumnExpressionStatus.FINISH_EXPRESSION and not scanner.is_finish:
        if status == ParseColumnExpressionStatus.BEFORE_EXPRESSION:
            # 当前指针位置是函数调用
            if check_sql_function(scanner):
                tokens.append(parse_sql_function(scanner, data_source))
            # 当前指针位置是插入语
            elif scanner.now.is_parenthesis:
                tokens.append(parse_simple_expression_or_case_expression(scanner.pop_as_children_scanner(),
                                                                         data_source))
            # 当前指针位置是变量应用
            elif check_sql_variable(scanner, data_source):
                tokens.append(parse_sql_variable(scanner, data_source))
            # 当前指针位置是其他元素
            else:
                tokens.append(scanner.pop())
            status = ParseColumnExpressionStatus.AFTER_EXPRESSION
        elif status == ParseColumnExpressionStatus.AFTER_EXPRESSION:
            # 当前指针元素是计算运算符
            if scanner.now.is_compute_operator:
                tokens.append(scanner.pop())
                tokens.append(scanner.pop())
                status = ParseColumnExpressionStatus.AFTER_EXPRESSION
            else:
                status = ParseColumnExpressionStatus.FINISH_EXPRESSION

    return SQLSimpleExpression(tokens)


if __name__ == "__main__":
    print(parse_sql_function(
        TokenScanner([token for token in parse_as_tokens("trim(column1)") if token.is_space is False]),
        DataSource.MYSQL))
    print(parse_simple_expression_or_case_expression(
        TokenScanner([token for token in parse_as_tokens("a * b") if token.is_space is False]),
        DataSource.MYSQL))
    print(parse_simple_expression_or_case_expression(
        TokenScanner([token for token in parse_as_tokens("a * b * c") if token.is_space is False]),
        DataSource.MYSQL))
    print(parse_simple_expression_or_case_expression(
        TokenScanner([token for token in parse_as_tokens("a + b") if token.is_space is False]),
        DataSource.MYSQL))
