"""
一般表达式的解析逻辑
"""

from metasequoia_sql import ast
from metasequoia_sql.common.token_scanner import TokenScanner
from metasequoia_sql.errors import SqlParseError
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


def maybe_function_expression(scanner: TokenScanner) -> bool:
    """是否可能为函数表达式

    Examples
    --------
    >>> maybe_function_expression(TokenScanner(ast.parse_as_tokens("schema.function(param) AND"), ignore_space=True))
    True
    >>> maybe_function_expression(TokenScanner(ast.parse_as_tokens("`schema`.`function`(param) AND"), ignore_space=True))
    True
    >>> maybe_function_expression(TokenScanner(ast.parse_as_tokens("trim(column_name) AND"), ignore_space=True))
    True
    >>> maybe_function_expression(TokenScanner(ast.parse_as_tokens("2.5 WHERE"), ignore_space=True))
    False
    >>> maybe_function_expression(TokenScanner(ast.parse_as_tokens("coumn_name WHERE"), ignore_space=True))
    False
    """
    return ((scanner.now.is_maybe_function_name and
             scanner.next1 is not None and scanner.next1.is_parenthesis) or
            (scanner.now.is_maybe_function_name and
             scanner.next1 is not None and scanner.next1.is_dot and
             scanner.next2 is not None and scanner.next2.is_maybe_function_name and
             scanner.next3 is not None and scanner.next3.is_parenthesis
             ))


def parse_function_expression(scanner: TokenScanner) -> SQLFunctionExpression:
    """解析函数表达式

    Examples
    --------
    >>> parse_function_expression(TokenScanner(ast.parse_as_tokens("schema.function(param) AND"), ignore_space=True))
    <SQLFunctionExpression source=schema.function(param)>
    >>> parse_function_expression(TokenScanner(ast.parse_as_tokens("`schema`.`function`(param) AND"), ignore_space=True))
    <SQLFunctionExpression source=`schema`.`function`(param)>
    >>> parse_function_expression(TokenScanner(ast.parse_as_tokens("trim(column_name) AND"), ignore_space=True))
    <SQLFunctionExpression source=trim(None)>
    >>> parse_function_expression(TokenScanner(ast.parse_as_tokens("2.5 WHERE"), ignore_space=True))
    Traceback (most recent call last):
    ...
    metasequoia_sql.errors.SqlParseError: 无法解析为函数表达式: <TokenScanner tokens=[<ASTLiteralFloat source=2.5>, <ASTOther source=WHERE>], pos=0>
    >>> parse_function_expression(TokenScanner(ast.parse_as_tokens("coumn_name WHERE"), ignore_space=True))
    Traceback (most recent call last):
    ...
    metasequoia_sql.errors.SqlParseError: 无法解析为函数表达式: <TokenScanner tokens=[<ASTOther source=coumn_name>, <ASTOther source=WHERE>], pos=0>
    """
    if (scanner.now.is_maybe_function_name and
            scanner.next1 is not None and scanner.next1.is_parenthesis):
        schema_name = None
        function_name = scanner.pop().source
    elif (scanner.now.is_maybe_function_name and
          scanner.next1 is not None and scanner.next1.is_dot and
          scanner.next2 is not None and scanner.next2.is_maybe_function_name and
          scanner.next3 is not None and scanner.next3.is_parenthesis):
        schema_name = scanner.pop().source
        scanner.pop()
        function_name = scanner.pop().source
    else:
        raise SqlParseError(f"无法解析为函数表达式: {scanner}")

    function_params: List[SQLGeneralExpression] = []
    for param_scanner in scanner.pop_as_children_scanner_list_split_by_comma(ignore_space=True):
        function_params.append(parse_general_expression(param_scanner))

    return SQLFunctionExpression(schema_name=schema_name,
                                 function_name=function_name,
                                 function_params=function_params)


def maybe_column_name_expression(scanner: TokenScanner) -> bool:
    """是否可能为列名表达式

    Examples
    --------
    >>> maybe_column_name_expression(TokenScanner(ast.parse_as_tokens("schema.function(param) AND"), ignore_space=True))
    False
    >>> maybe_column_name_expression(TokenScanner(ast.parse_as_tokens("`schema`.`function`(param) AND"), ignore_space=True))
    False
    >>> maybe_column_name_expression(TokenScanner(ast.parse_as_tokens("schema.column AND"), ignore_space=True))
    True
    >>> maybe_column_name_expression(TokenScanner(ast.parse_as_tokens("`schema`.`column` AND"), ignore_space=True))
    True
    >>> maybe_column_name_expression(TokenScanner(ast.parse_as_tokens("trim(column_name) AND"), ignore_space=True))
    False
    >>> maybe_column_name_expression(TokenScanner(ast.parse_as_tokens("2.5 WHERE"), ignore_space=True))
    False
    >>> maybe_column_name_expression(TokenScanner(ast.parse_as_tokens("coumn_name WHERE"), ignore_space=True))
    True
    """
    return ((scanner.now.is_maybe_function_name and
             (scanner.next1 is None or (not scanner.next1.is_dot and
                                        not scanner.next1.is_parenthesis and
                                        not scanner.next1.is_compute_operator))) or
            (scanner.now.is_maybe_function_name and
             scanner.next1 is not None and scanner.next1.is_dot and
             scanner.next2 is not None and scanner.next2.is_maybe_function_name and
             (scanner.next3 is None or (not scanner.next3.is_dot and
                                        not scanner.next3.is_parenthesis and
                                        not scanner.next3.is_compute_operator)))
            )


def parse_column_name_expression(scanner: TokenScanner) -> SQLColumnNameExpression:
    """解析列名表达式

    Examples
    --------
    >>> parse_column_name_expression(TokenScanner(ast.parse_as_tokens("schema.function(param) AND"), ignore_space=True))
    Traceback (most recent call last):
    ...
    metasequoia_sql.errors.SqlParseError: 无法解析为表名表达式: <TokenScanner tokens=[<ASTOther source=schema>, <ASTCommon source=.>, <ASTOther source=function>, <ASTParenthesis children=[<ASTOther source=param>]>, <ASTCommon source=AND>], pos=0>
    >>> parse_column_name_expression(TokenScanner(ast.parse_as_tokens("`schema`.`function`(param) AND"), ignore_space=True))
    Traceback (most recent call last):
    ...
    metasequoia_sql.errors.SqlParseError: 无法解析为表名表达式: <TokenScanner tokens=[<ASTIdentifier source=`schema`>, <ASTCommon source=.>, <ASTIdentifier source=`function`>, <ASTParenthesis children=[<ASTOther source=param>]>, <ASTCommon source=AND>], pos=0>
    >>> parse_column_name_expression(TokenScanner(ast.parse_as_tokens("schema.column AND"), ignore_space=True))
    <SQLColumnNameExpression source=schema.column>
    >>> parse_column_name_expression(TokenScanner(ast.parse_as_tokens("`schema`.`column` AND"), ignore_space=True))
    <SQLColumnNameExpression source=`schema`.`column`>
    >>> parse_column_name_expression(TokenScanner(ast.parse_as_tokens("trim(column_name) AND"), ignore_space=True))
    Traceback (most recent call last):
    ...
    metasequoia_sql.errors.SqlParseError: 无法解析为表名表达式: <TokenScanner tokens=[<ASTOther source=trim>, <ASTParenthesis children=[<ASTOther source=column_name>]>, <ASTCommon source=AND>], pos=0>
    >>> parse_column_name_expression(TokenScanner(ast.parse_as_tokens("2.5 WHERE"), ignore_space=True))
    Traceback (most recent call last):
    ...
    metasequoia_sql.errors.SqlParseError: 无法解析为表名表达式: <TokenScanner tokens=[<ASTLiteralFloat source=2.5>, <ASTOther source=WHERE>], pos=0>
    >>> parse_column_name_expression(TokenScanner(ast.parse_as_tokens("coumn_name WHERE"), ignore_space=True))
    <SQLColumnNameExpression source=coumn_name>
    """
    if (scanner.now.is_maybe_function_name and
            (scanner.next1 is None or (not scanner.next1.is_dot and
                                       not scanner.next1.is_parenthesis and
                                       not scanner.next1.is_compute_operator))):
        return SQLColumnNameExpression(None, scanner.now.source)
    if (scanner.now.is_maybe_function_name and
            scanner.next1 is not None and scanner.next1.is_dot and
            scanner.next2 is not None and scanner.next2.is_maybe_function_name and
            (scanner.next3 is None or (not scanner.next3.is_dot and
                                       not scanner.next3.is_parenthesis and
                                       not scanner.next3.is_compute_operator))):
        return SQLColumnNameExpression(scanner.now.source, scanner.next2.source)
    raise SqlParseError(f"无法解析为表名表达式: {scanner}")


def parse_general_expression(scanner: TokenScanner) -> SQLGeneralExpression:
    """解析一般表达式"""
