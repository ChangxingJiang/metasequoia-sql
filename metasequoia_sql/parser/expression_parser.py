"""
字段表达式解析器
"""

from typing import List

from metasequoia_sql.ast.functions import parse_as_tokens
from metasequoia_sql.common.token_scanner import TokenScanner
from metasequoia_sql.errors import SqlParseError
from metasequoia_sql.objects.common import SQLColumnExpression


def parse_column_expression(scanner: TokenScanner):
    """解析字段表达式"""
    if scanner.get().equals("CASE"):
        return  # case 语句
    tokens = [scanner.pop()]
    while not scanner.is_finish:
        if scanner.get().is_compute_operator:  # 计算运算符
            tokens.append(scanner.pop())
            tokens.append(scanner.pop())
        elif scanner.get().is_parenthesis:  # 插入语：说明之前的部分是一个函数
            params: List[SQLColumnExpression] = []
            for param_scanner in scanner.pop_as_children_scanner_list_split_by_comma():
                params.append(parse_column_expression(param_scanner))
            function_name = tokens.pop().source

    return SQLColumnExpression(tokens)


def parse_function_call(scanner: TokenScanner):
    """解析函数调用：要求当前指针位置节点为函数名，下一个节点可能为函数参数

    MySQL 的无参函数可以不添加插入语，例如：

    ```sql
    SELECT CURRENT_DATE;
    ```
    """
    # 解析函数名称
    name_node = scanner.pop()
    if not name_node.is_maybe_function_name:
        raise SqlParseError(f"当前指针位置节点不可能为函数名称: node={name_node}")
    function_name = name_node.source

    # 解析函数参数
    params: List[SQLColumnExpression] = []
    if scanner.get().is_parenthesis:
        for param_scanner in scanner.pop_as_children_scanner_list_split_by_comma():
            params.append(parse_column_expression(param_scanner))



if __name__ == "__main__":
    print(
        parse_column_expression(TokenScanner([token for token in parse_as_tokens("a * b") if token.is_space is False])))
    print(parse_column_expression(
        TokenScanner([token for token in parse_as_tokens("a * b * c") if token.is_space is False])))
    print(
        parse_column_expression(TokenScanner([token for token in parse_as_tokens("a + b") if token.is_space is False])))
    print(parse_column_expression(
        TokenScanner([token for token in parse_as_tokens("trim(column1)") if token.is_space is False])))
