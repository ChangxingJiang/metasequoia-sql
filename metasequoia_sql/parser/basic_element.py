"""
基础元素的解析逻辑
"""

from metasequoia_sql import ast
from metasequoia_sql.common.token_scanner import TokenScanner
from metasequoia_sql.errors import SqlParseError
from metasequoia_sql.objects.new_select import *


def maybe_compute_operator(scanner: TokenScanner) -> bool:
    """检查是否可能为计算运算符

    Examples
    --------
    >>> maybe_compute_operator(TokenScanner(ast.parse_as_tokens("+ 3"), ignore_space=True))
    True
    >>> maybe_compute_operator(TokenScanner(ast.parse_as_tokens("- 3"), ignore_space=True))
    True
    >>> maybe_compute_operator(TokenScanner(ast.parse_as_tokens("* 3"), ignore_space=True))
    True
    >>> maybe_compute_operator(TokenScanner(ast.parse_as_tokens("/ 3"), ignore_space=True))
    True
    >>> maybe_compute_operator(TokenScanner(ast.parse_as_tokens("3 + 3"), ignore_space=True))
    False
    """
    return scanner.now.is_compute_operator


def parse_compute_operator(scanner: TokenScanner) -> SQLComputeOperator:
    """解析计算运算符

    Examples
    --------
    >>> parse_compute_operator(TokenScanner(ast.parse_as_tokens("+ 3"), ignore_space=True))
    <SQLPlus>
    >>> parse_compute_operator(TokenScanner(ast.parse_as_tokens("- 3"), ignore_space=True))
    <SQLSubtract>
    >>> parse_compute_operator(TokenScanner(ast.parse_as_tokens("* 3"), ignore_space=True))
    <SQLMultiple>
    >>> parse_compute_operator(TokenScanner(ast.parse_as_tokens("/ 3"), ignore_space=True))
    <SQLDivide>
    >>> parse_compute_operator(TokenScanner(ast.parse_as_tokens("3 + 3"), ignore_space=True))
    Traceback (most recent call last):
    ...
    metasequoia_sql.errors.SqlParseError: 未知的计算运算符: <ASTLiteralInteger source=3>
    """
    token: ast.AST = scanner.pop()
    if token.source == "+":
        return SQLPlus()
    if token.source == "-":
        return SQLSubtract()
    if token.source == "*":
        return SQLMultiple()
    if token.source == "/":
        return SQLDivide()
    raise SqlParseError(f"未知的计算运算符: {token}")


def maybe_compare_operator(scanner: TokenScanner) -> bool:
    """检查是否可能为比较运算符

    Examples
    --------
    >>> maybe_compare_operator(TokenScanner(ast.parse_as_tokens("= 3"), ignore_space=True))
    True
    >>> maybe_compare_operator(TokenScanner(ast.parse_as_tokens("< 3"), ignore_space=True))
    True
    >>> maybe_compare_operator(TokenScanner(ast.parse_as_tokens("<= 3"), ignore_space=True))
    True
    >>> maybe_compare_operator(TokenScanner(ast.parse_as_tokens("> 3"), ignore_space=True))
    True
    >>> maybe_compare_operator(TokenScanner(ast.parse_as_tokens(">= 3"), ignore_space=True))
    True
    >>> maybe_compare_operator(TokenScanner(ast.parse_as_tokens("!= 3"), ignore_space=True))
    True
    >>> maybe_compare_operator(TokenScanner(ast.parse_as_tokens("<> 3"), ignore_space=True))
    True
    >>> maybe_compare_operator(TokenScanner(ast.parse_as_tokens("3 + 3"), ignore_space=True))
    False
    """
    return scanner.now.is_compare_operator


def parse_compare_operator(scanner: TokenScanner) -> SQLCompareOperator:
    """解析比较运算符

    Examples
    --------
    >>> parse_compare_operator(TokenScanner(ast.parse_as_tokens("= 3"), ignore_space=True))
    <SQLEqualTo>
    >>> parse_compare_operator(TokenScanner(ast.parse_as_tokens("< 3"), ignore_space=True))
    <SQLLessThan>
    >>> parse_compare_operator(TokenScanner(ast.parse_as_tokens("<= 3"), ignore_space=True))
    <SQLLessThanOrEqual>
    >>> parse_compare_operator(TokenScanner(ast.parse_as_tokens("> 3"), ignore_space=True))
    <SQLGreaterThan>
    >>> parse_compare_operator(TokenScanner(ast.parse_as_tokens(">= 3"), ignore_space=True))
    <SQLGreaterThanOrEqual>
    >>> parse_compare_operator(TokenScanner(ast.parse_as_tokens("!= 3"), ignore_space=True))
    <SQLNotEqualTo>
    >>> parse_compare_operator(TokenScanner(ast.parse_as_tokens("<> 3"), ignore_space=True))
    <SQLNotEqualTo>
    >>> parse_compare_operator(TokenScanner(ast.parse_as_tokens("3 + 3"), ignore_space=True))
    Traceback (most recent call last):
    ...
    metasequoia_sql.errors.SqlParseError: 未知的比较运算符: <ASTLiteralInteger source=3>
    """
    token: ast.AST = scanner.pop()
    if token.source == "=":
        return SQLEqualTo()
    if token.source == "<":
        return SQLLessThan()
    if token.source == "<=":
        return SQLLessThanOrEqual()
    if token.source == ">":
        return SQLGreaterThan()
    if token.source == ">=":
        return SQLGreaterThanOrEqual()
    if token.source in {"!=", "<>"}:
        return SQLNotEqualTo()
    raise SqlParseError(f"未知的比较运算符: {token}")


def maybe_logical_operator(scanner: TokenScanner) -> bool:
    """判断逻辑运算符：包含 AND、OR、NOT

    Examples
    --------
    >>> maybe_logical_operator(TokenScanner(ast.parse_as_tokens("AND a > 1"), ignore_space=True))
    True
    >>> maybe_logical_operator(TokenScanner(ast.parse_as_tokens("NOT a > 1"), ignore_space=True))
    True
    >>> maybe_logical_operator(TokenScanner(ast.parse_as_tokens("OR a > 1"), ignore_space=True))
    True
    >>> maybe_logical_operator(TokenScanner(ast.parse_as_tokens("a > 1"), ignore_space=True))
    False
    """
    return scanner.now.is_logical_operator


def parse_logical_operator(scanner: TokenScanner) -> SQLLogicalOperator:
    """解析逻辑运算符：包含 AND、OR、NOT

    Examples
    --------
    >>> parse_logical_operator(TokenScanner(ast.parse_as_tokens("AND a > 1"), ignore_space=True))
    <SQLAndOperator>
    >>> parse_logical_operator(TokenScanner(ast.parse_as_tokens("OR a > 1"), ignore_space=True))
    <SQLOrOperator>
    >>> parse_logical_operator(TokenScanner(ast.parse_as_tokens("NOT a > 1"), ignore_space=True))
    <SQLNotOperator>
    >>> parse_logical_operator(TokenScanner(ast.parse_as_tokens("a > 1"), ignore_space=True))
    Traceback (most recent call last):
    ...
    metasequoia_sql.errors.SqlParseError: 未知的逻辑运算符: <ASTOther source=a>
    """
    token: ast.AST = scanner.pop()
    if token.source == "AND":
        return SQLAndOperator()
    if token.source == "OR":
        return SQLOrOperator()
    if token.source == "NOT":
        return SQLNotOperator()
    raise SqlParseError(f"未知的逻辑运算符: {token}")


def maybe_literal(scanner: TokenScanner) -> bool:
    """判断是否为字面值：包含整型字面值、浮点型字面值、字符串型字面值、十六进制型字面值、布尔型字面值、位值型字面值、空值的字面值

    Examples
    --------
    >>> maybe_literal(TokenScanner(ast.parse_as_tokens("1 WHERE"), ignore_space=True))
    True
    >>> maybe_literal(TokenScanner(ast.parse_as_tokens("2.5 WHERE"), ignore_space=True))
    True
    >>> maybe_literal(TokenScanner(ast.parse_as_tokens("'a' WHERE"), ignore_space=True))
    True
    >>> maybe_literal(TokenScanner(ast.parse_as_tokens("x'3f' WHERE"), ignore_space=True))
    True
    >>> maybe_literal(TokenScanner(ast.parse_as_tokens("TRUE WHERE"), ignore_space=True))
    True
    >>> maybe_literal(TokenScanner(ast.parse_as_tokens("true WHERE"), ignore_space=True))
    True
    >>> maybe_literal(TokenScanner(ast.parse_as_tokens("False WHERE"), ignore_space=True))
    True
    >>> maybe_literal(TokenScanner(ast.parse_as_tokens("b'1' WHERE"), ignore_space=True))
    True
    >>> maybe_literal(TokenScanner(ast.parse_as_tokens("null WHERE"), ignore_space=True))
    True
    >>> maybe_literal(TokenScanner(ast.parse_as_tokens("NULL WHERE"), ignore_space=True))
    True
    >>> maybe_literal(TokenScanner(ast.parse_as_tokens("cnt WHERE"), ignore_space=True))
    False
    >>> maybe_literal(TokenScanner(ast.parse_as_tokens("table_name.column_name WHERE"), ignore_space=True))
    False
    """
    return scanner.now.is_literal


def parse_literal(scanner: TokenScanner) -> SQLLiteral:
    """解析字面值：包含整型字面值、浮点型字面值、字符串型字面值、十六进制型字面值、布尔型字面值、位值型字面值、空值的字面值

    Examples
    --------
    >>> parse_literal(TokenScanner(ast.parse_as_tokens("1 WHERE"), ignore_space=True))
    <SQLLiteralInteger source=1>
    >>> parse_literal(TokenScanner(ast.parse_as_tokens("2.5 WHERE"), ignore_space=True))
    <SQLLiteralFloat source=2.5>
    >>> parse_literal(TokenScanner(ast.parse_as_tokens("'a' WHERE"), ignore_space=True))
    <SQLLiteralString source='a'>
    >>> parse_literal(TokenScanner(ast.parse_as_tokens("x'3f' WHERE"), ignore_space=True))
    <SQLLiteralHex source=x'3F'>
    >>> parse_literal(TokenScanner(ast.parse_as_tokens("TRUE WHERE"), ignore_space=True))
    <SQLLiteralBool source=TRUE>
    >>> parse_literal(TokenScanner(ast.parse_as_tokens("true WHERE"), ignore_space=True))
    <SQLLiteralBool source=TRUE>
    >>> parse_literal(TokenScanner(ast.parse_as_tokens("False WHERE"), ignore_space=True))
    <SQLLiteralBool source=FALSE>
    >>> parse_literal(TokenScanner(ast.parse_as_tokens("b'1' WHERE"), ignore_space=True))
    <SQLLiteralBit source=b'1'>
    >>> parse_literal(TokenScanner(ast.parse_as_tokens("null WHERE"), ignore_space=True))
    <SQLLiteralNull source=NULL>
    >>> parse_literal(TokenScanner(ast.parse_as_tokens("NULL WHERE"), ignore_space=True))
    <SQLLiteralNull source=NULL>
    >>> parse_literal(TokenScanner(ast.parse_as_tokens("cnt WHERE"), ignore_space=True))
    Traceback (most recent call last):
    ...
    metasequoia_sql.errors.SqlParseError: 未知的字面值: <ASTOther source=cnt>
    >>> parse_literal(TokenScanner(ast.parse_as_tokens("table_name.column_name WHERE"), ignore_space=True))
    Traceback (most recent call last):
    ...
    metasequoia_sql.errors.SqlParseError: 未知的字面值: <ASTOther source=table_name.column_name>
    """
    token: ast.AST = scanner.pop()
    if isinstance(token, ast.ASTLiteralInteger):
        return SQLLiteralInteger(token.literal_value)
    if isinstance(token, ast.ASTLiteralFloat):
        return SQLLiteralFloat(token.literal_value)
    if isinstance(token, ast.ASTLiteralString):
        return SQLLiteralString(token.literal_value)
    if isinstance(token, ast.ASTLiteralHex):
        return SQLLiteralHex(token.literal_value)
    if isinstance(token, ast.ASTLiteralBool):
        return SQLLiteralBool(token.literal_value)
    if isinstance(token, ast.ASTLiteralBit):
        return SQLLiteralBit(token.literal_value)
    if isinstance(token, ast.ASTLiteralNull):
        return SQLLiteralNull()
    raise SqlParseError(f"未知的字面值: {token}")
