"""
一般表达式的解析逻辑
"""

from metasequoia_sql import ast
from metasequoia_sql.common.token_scanner import TokenScanner
from metasequoia_sql.objects.new_select import *
from metasequoia_sql.parser import basic_element


def maybe_literal_expression(scanner: TokenScanner) -> bool:
    """判断是否为字面值表达式

    Examples
    --------
    >>> maybe_literal_expression(TokenScanner(ast.parse_as_tokens("1 WHERE"), ignore_space=True))
    True
    >>> maybe_literal_expression(TokenScanner(ast.parse_as_tokens("2.5 WHERE"), ignore_space=True))
    True
    >>> maybe_literal_expression(TokenScanner(ast.parse_as_tokens("'a' WHERE"), ignore_space=True))
    True
    >>> maybe_literal_expression(TokenScanner(ast.parse_as_tokens("x'3f' WHERE"), ignore_space=True))
    True
    >>> maybe_literal_expression(TokenScanner(ast.parse_as_tokens("TRUE WHERE"), ignore_space=True))
    True
    >>> maybe_literal_expression(TokenScanner(ast.parse_as_tokens("true WHERE"), ignore_space=True))
    True
    >>> maybe_literal_expression(TokenScanner(ast.parse_as_tokens("False WHERE"), ignore_space=True))
    True
    >>> maybe_literal_expression(TokenScanner(ast.parse_as_tokens("b'1' WHERE"), ignore_space=True))
    True
    >>> maybe_literal_expression(TokenScanner(ast.parse_as_tokens("null WHERE"), ignore_space=True))
    True
    >>> maybe_literal_expression(TokenScanner(ast.parse_as_tokens("NULL WHERE"), ignore_space=True))
    True
    >>> maybe_literal_expression(TokenScanner(ast.parse_as_tokens("cnt WHERE"), ignore_space=True))
    False
    >>> maybe_literal_expression(TokenScanner(ast.parse_as_tokens("table_name.column_name WHERE"), ignore_space=True))
    False
    """
    return basic_element.maybe_literal(scanner)


def parse_literal_expression(scanner: TokenScanner) -> SQLLiteralExpression:
    """解析字面值表达式

    Examples
    --------
    >>> parse_literal_expression(TokenScanner(ast.parse_as_tokens("1 WHERE"), ignore_space=True))
    <SQLLiteralExpression source=1>
    >>> parse_literal_expression(TokenScanner(ast.parse_as_tokens("2.5 WHERE"), ignore_space=True))
    <SQLLiteralExpression source=2.5>
    >>> parse_literal_expression(TokenScanner(ast.parse_as_tokens("'a' WHERE"), ignore_space=True))
    <SQLLiteralExpression source='a'>
    >>> parse_literal_expression(TokenScanner(ast.parse_as_tokens("x'3f' WHERE"), ignore_space=True))
    <SQLLiteralExpression source=x'3F'>
    >>> parse_literal_expression(TokenScanner(ast.parse_as_tokens("TRUE WHERE"), ignore_space=True))
    <SQLLiteralExpression source=TRUE>
    >>> parse_literal_expression(TokenScanner(ast.parse_as_tokens("true WHERE"), ignore_space=True))
    <SQLLiteralExpression source=TRUE>
    >>> parse_literal_expression(TokenScanner(ast.parse_as_tokens("False WHERE"), ignore_space=True))
    <SQLLiteralExpression source=FALSE>
    >>> parse_literal_expression(TokenScanner(ast.parse_as_tokens("b'1' WHERE"), ignore_space=True))
    <SQLLiteralExpression source=b'1'>
    >>> parse_literal_expression(TokenScanner(ast.parse_as_tokens("null WHERE"), ignore_space=True))
    <SQLLiteralExpression source=NULL>
    >>> parse_literal_expression(TokenScanner(ast.parse_as_tokens("NULL WHERE"), ignore_space=True))
    <SQLLiteralExpression source=NULL>
    >>> parse_literal_expression(TokenScanner(ast.parse_as_tokens("cnt WHERE"), ignore_space=True))
    Traceback (most recent call last):
    ...
    metasequoia_sql.errors.SqlParseError: 未知的字面值: <ASTOther source=cnt>
    >>> parse_literal_expression(TokenScanner(ast.parse_as_tokens("table_name.column_name WHERE"), ignore_space=True))
    Traceback (most recent call last):
    ...
    metasequoia_sql.errors.SqlParseError: 未知的字面值: <ASTOther source=table_name.column_name>
    """
    return SQLLiteralExpression(literal=basic_element.parse_literal(scanner))
