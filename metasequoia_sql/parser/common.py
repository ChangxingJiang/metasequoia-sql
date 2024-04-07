"""
基础元素的解析逻辑

TODO 使用 search 替代直接使用 now 判断
TODO 整理各种函数的共同规律
"""

from metasequoia_sql import ast
from metasequoia_sql.common.token_scanner import TokenScanner, build_token_scanner
from metasequoia_sql.objects.core import *


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
    return not scanner.is_finish and scanner.now.is_compute_operator


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
    if token.source == "%":
        return SQLMod()
    if token.source == "||":
        return SQLConcat()
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
    return not scanner.is_finish and scanner.now.is_compare_operator


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
    >>> parse_compare_operator(TokenScanner(ast.parse_as_tokens("IS NULL"), ignore_space=True))
    <SQLIs>
    >>> parse_compare_operator(TokenScanner(ast.parse_as_tokens("IS NOT NULL"), ignore_space=True))
    <SQLIs>
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
    if token.source == "IS":
        return SQLIs()
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
    return not scanner.is_finish and scanner.now.is_logical_operator


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
    return not scanner.is_finish and scanner.now.is_literal


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
    metasequoia_sql.errors.SqlParseError: 未知的字面值: <ASTOther source=table_name>
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
    return maybe_literal(scanner)


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
    metasequoia_sql.errors.SqlParseError: 未知的字面值: <ASTOther source=table_name>
    """
    return SQLLiteralExpression(literal=parse_literal(scanner))


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
    return not scanner.is_finish and (
            (scanner.now.is_maybe_name and
             scanner.next1 is not None and scanner.next1.is_parenthesis) or
            (scanner.now.is_maybe_name and
             scanner.next1 is not None and scanner.next1.is_dot and
             scanner.next2 is not None and scanner.next2.is_maybe_name and
             scanner.next3 is not None and scanner.next3.is_parenthesis
             ))


def parse_cast_data_type(scanner: TokenScanner) -> SQLEnumCastDataType:
    """解析 CAST 函数表达式中的类型"""
    for cast_type in SQLEnumCastDataType:
        if scanner.search_and_move(cast_type.value):
            return cast_type
    raise SqlParseError(f"无法解析的 CAST 函数表达式中的类型: {scanner}")


def parse_cast_function_expression(scanner: TokenScanner) -> SQLCastFunctionExpression:
    """解析 CAST 函数表达式"""
    column_expression = parse_general_expression(scanner)
    scanner.match("AS")
    signed = scanner.search_and_move("SIGNED")
    cast_type = parse_cast_data_type(scanner)
    if not scanner.is_finish and scanner.now.is_parenthesis:
        parenthesis_scanner = scanner.pop_as_children_scanner()
        cast_params: Optional[List[SQLGeneralExpression]] = []
        for param_scanner in parenthesis_scanner.split_by_comma():
            cast_params.append(parse_general_expression(param_scanner))
            if not param_scanner.is_finish:
                raise SqlParseError(f"无法解析函数参数: {param_scanner}")
    else:
        cast_params = None
    if not scanner.is_finish:
        raise SqlParseError(f"无法解析CAST函数参数: {scanner}")
    cast_data_type = SQLCastDataType(signed=signed, data_type=cast_type, params=cast_params)
    return SQLCastFunctionExpression(column_expression=column_expression, cast_type=cast_data_type)


def parse_extract_function_expression(parenthesis_scanner: TokenScanner) -> SQLExtractFunctionExpression:
    """解析 EXTRACT 函数表达式"""
    extract_name = parse_general_expression(parenthesis_scanner)
    parenthesis_scanner.match("FROM")
    column_expression = parse_general_expression(parenthesis_scanner)
    if not parenthesis_scanner.is_finish:
        raise SqlParseError(f"无法解析EXTRACT函数参数: {parenthesis_scanner}")
    return SQLExtractFunctionExpression(extract_name=extract_name, column_expression=column_expression)


def parse_if_function_expression(parenthesis_scanner: TokenScanner) -> SQLFunctionExpression:
    """解析 IF 函数表达式"""
    function_params: List[SQLGeneralExpression] = []
    first_param = True
    for param_scanner in parenthesis_scanner.split_by_comma():
        if first_param is True:
            function_params.append(parse_condition_expression(param_scanner))
            first_param = False
        else:
            function_params.append(parse_general_expression(param_scanner))
        if not param_scanner.is_finish:
            raise SqlParseError(f"无法解析函数参数: {param_scanner}")
    return SQLFunctionExpression(schema_name=None, function_name="IF", function_params=function_params)


def _parse_function_name(scanner: TokenScanner) -> Tuple[Optional[str], str]:
    """解析函数表达式函数的 schema 名和 function 名"""
    if (scanner.now.is_maybe_name and
            scanner.next1 is not None and scanner.next1.is_parenthesis):
        return None, scanner.pop().source
    if (scanner.now.is_maybe_name and
            scanner.next1 is not None and scanner.next1.is_dot and
            scanner.next2 is not None and scanner.next2.is_maybe_name and
            scanner.next3 is not None and scanner.next3.is_parenthesis):
        schema_name = scanner.pop().source
        scanner.pop()
        return schema_name, scanner.pop().source
    raise SqlParseError(f"无法解析为函数表达式: {scanner}")


def parse_function_expression(scanner: TokenScanner) -> SQLFunctionExpression:
    """解析函数表达式

    Examples
    --------
    >>> parse_function_expression(TokenScanner(ast.parse_as_tokens("schema.function(param) AND"), ignore_space=True))
    <SQLFunctionExpression source=schema.function(<SQLColumnNameExpression source=param>)>
    >>> parse_function_expression(TokenScanner(ast.parse_as_tokens("`schema`.`function`(param) AND"), ignore_space=True))
    <SQLFunctionExpression source=`schema`.`function`(<SQLColumnNameExpression source=param>)>
    >>> parse_function_expression(TokenScanner(ast.parse_as_tokens("trim(column_name) AND"), ignore_space=True))
    <SQLFunctionExpression source=trim(<SQLColumnNameExpression source=column_name>)>
    >>> parse_function_expression(TokenScanner(ast.parse_as_tokens("2.5 WHERE"), ignore_space=True))
    Traceback (most recent call last):
    ...
    metasequoia_sql.errors.SqlParseError: 无法解析为函数表达式: <TokenScanner tokens=[<ASTLiteralFloat source=2.5>, <ASTOther source=WHERE>], pos=0>
    >>> parse_function_expression(TokenScanner(ast.parse_as_tokens("coumn_name WHERE"), ignore_space=True))
    Traceback (most recent call last):
    ...
    metasequoia_sql.errors.SqlParseError: 无法解析为函数表达式: <TokenScanner tokens=[<ASTOther source=coumn_name>, <ASTOther source=WHERE>], pos=0>
    """
    schema_name, function_name = _parse_function_name(scanner)

    if function_name.upper() == "CAST":
        return parse_cast_function_expression(scanner.pop_as_children_scanner())
    if function_name.upper() == "EXTRACT":
        return parse_extract_function_expression(scanner.pop_as_children_scanner())
    if function_name.upper() == "IF":
        return parse_if_function_expression(scanner.pop_as_children_scanner())

    parenthesis_scanner = scanner.pop_as_children_scanner()
    if function_name.upper() == "SUBSTRING":
        # 将 MySQL 和 PostgreSQL 中的 "SUBSTRING(str1 FROM 3 FOR 2)" 格式化为 "SUBSTRING(str1, 3, 2)"
        parenthesis_scanner = TokenScanner([
            element if not element.equals("FROM") and not element.equals("FOR") else ast.ASTComma()
            for element in parenthesis_scanner.elements])

    is_distinct = False
    if function_name.upper() in {"COUNT", "SUM", "MIN", "MAX", "AVG"} and parenthesis_scanner.now.equals("DISTINCT"):
        parenthesis_scanner.pop()
        is_distinct = True

    function_params: List[SQLGeneralExpression] = []
    for param_scanner in parenthesis_scanner.split_by_comma():
        function_params.append(parse_general_expression(param_scanner))
        if not param_scanner.is_finish:
            raise SqlParseError(f"无法解析函数参数: {param_scanner}")

    if schema_name is None and function_name.upper() in {"COUNT", "SUM", "MIN", "MAX", "AVG"}:
        return SQLAggregationFunctionExpression(function_name=function_name,
                                                function_params=function_params,
                                                is_distinct=is_distinct)
    else:
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
    return not scanner.is_finish and (
            (scanner.now.is_maybe_name and
             (scanner.next1 is None or (not scanner.next1.is_dot and not scanner.next1.is_parenthesis))) or
            (scanner.now.is_maybe_name and
             scanner.next1 is not None and scanner.next1.is_dot and
             scanner.next2 is not None and scanner.next2.is_maybe_name and
             (scanner.next3 is None or not scanner.next3.is_parenthesis))
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
    if (scanner.now.is_maybe_name and
            (scanner.next1 is None or (not scanner.next1.is_dot and not scanner.next1.is_parenthesis))):
        return SQLColumnNameExpression(None, scanner.pop().source)
    if (scanner.now.is_maybe_name and
            scanner.next1 is not None and scanner.next1.is_dot and
            scanner.next2 is not None and scanner.next2.is_maybe_name and
            (scanner.next3 is None or not scanner.next3.is_parenthesis)):
        table_name = scanner.pop().source
        scanner.pop()
        column_name = scanner.pop().source
        return SQLColumnNameExpression(table_name, column_name)
    raise SqlParseError(f"无法解析为表名表达式: {scanner}")


def maybe_case_expression(scanner: TokenScanner) -> bool:
    """判断是否可能为 CASE 表达式

    Examples
    --------
    >>> maybe_case_expression(TokenScanner(ast.parse_as_tokens("CASE WHEN 2 THEN 3 ELSE 4 END"), ignore_space=True))
    True
    >>> maybe_case_expression(TokenScanner(ast.parse_as_tokens("3 + 5"), ignore_space=True))
    False
    """
    return not scanner.is_finish and scanner.now.equals("CASE")


def parse_case_expression(scanner: TokenScanner) -> Union[SQLCaseExpression, SQLCaseValueExpression]:
    """解析 CASE 表达式

    Examples
    --------
    >>> parse_case_expression(build_token_scanner("CASE WHEN 2 THEN 3 ELSE 4 END"))
    <SQLCaseExpression source=CASE
        WHEN <SQLLiteralExpression source=2> THEN <SQLLiteralExpression source=3>
        ELSE <SQLLiteralExpression source=4>
    END>
    >>> parse_case_expression(build_token_scanner("3 + 5"))
    Traceback (most recent call last):
    ...
    metasequoia_sql.errors.SqlParseError: 无法解析为CASE表达式: <TokenScanner tokens=[<ASTLiteralInteger source=3>, <ASTCommon source=+>, <ASTLiteralInteger source=5>], pos=1>
    """
    scanner.match("CASE")
    if scanner.search("WHEN"):
        # 第 1 种格式的 CASE 表达式
        cases = []
        else_value = None
        while scanner.search_and_move("WHEN"):
            when_expression = parse_condition_expression(scanner)
            scanner.match("THEN")
            case_expression = parse_general_expression(scanner)
            cases.append((when_expression, case_expression))
        if scanner.search_and_move("ELSE"):
            else_value = parse_general_expression(scanner)
        scanner.match("END")
        return SQLCaseExpression(cases=cases, else_value=else_value)
    else:
        # 第 2 种格式的 CASE 表达式
        case_value = parse_general_expression(scanner)
        cases = []
        else_value = None
        while scanner.search_and_move("WHEN"):
            when_expression = parse_general_expression(scanner)
            scanner.match("THEN")
            case_expression = parse_general_expression(scanner)
            cases.append((when_expression, case_expression))
        if scanner.search_and_move("ELSE"):
            else_value = parse_general_expression(scanner)
        scanner.match("END")
        return SQLCaseValueExpression(case_value=case_value, cases=cases, else_value=else_value)


# 窗口函数名称集合
WINDOW_FUNCTION_NAME_SET = {"ROW_NUMBER", "RANK", "DENSE_RANK", "SUM", "MIN", "MAX", "AVG", "LAG", "LEAD",
                            "FIRST_VALUE", "LAST_VALUE", "NTILE"}


def maybe_window_expression(scanner: TokenScanner) -> bool:
    """判断是否可能为窗口函数

    Examples
    --------
    >>> maybe_window_expression(build_token_scanner("ROW_NUMBER() OVER (PARTITION BY column1 ORDER BY column2) AS column3"))
    True
    >>> maybe_window_expression(build_token_scanner("3 + 5"))
    False
    """
    return not scanner.is_finish and (
            scanner.now.is_maybe_name and scanner.now.source.upper() in WINDOW_FUNCTION_NAME_SET and
            scanner.next1 is not None and scanner.next1.is_parenthesis and
            scanner.next2 is not None and scanner.next2.equals("OVER") and
            scanner.next3 is not None and scanner.next3.is_parenthesis)


def parse_window_expression(scanner: TokenScanner) -> SQLWindowExpression:
    """解析窗口函数

    TODO 支持 ROW BETWEEN 的语法

    Examples
    --------
    >>> parse_window_expression(build_token_scanner("ROW_NUMBER() OVER (PARTITION BY column1 ORDER BY column2) AS column3"))
    <SQLWindowExpression source=<SQLFunctionExpression source=ROW_NUMBER()> OVER (PARTITION BY <SQLColumnNameExpression source=column1>ORDER BY <SQLColumnNameExpression source=column2>)>
    >>> parse_window_expression(build_token_scanner("3 + 5"))
    Traceback (most recent call last):
    ...
    metasequoia_sql.errors.SqlParseError: 无法解析为函数表达式: <TokenScanner tokens=[<ASTLiteralInteger source=3>, <ASTCommon source=+>, <ASTLiteralInteger source=5>], pos=0>
    """
    window_function = parse_function_expression(scanner)
    partition_by = None
    order_by = None
    if not scanner.pop().equals("OVER"):
        raise SqlParseError(f"无法解析为窗口表达式: {scanner}")
    parenthesis_scanner = scanner.pop_as_children_scanner()
    if parenthesis_scanner.search_and_move("PARTITION", "BY"):
        partition_by = parse_general_expression(parenthesis_scanner, maybe_window=False)
    if parenthesis_scanner.search_and_move("ORDER", "BY"):
        order_by = parse_general_expression(parenthesis_scanner, maybe_window=False)
    return SQLWindowExpression(window_function=window_function, partition_by=partition_by, order_by=order_by)


def _parse_general_expression_element(scanner: TokenScanner, maybe_window: bool) -> SQLGeneralExpression:
    """解析一般表达式中的一个元素"""
    if maybe_case_expression(scanner):
        return parse_case_expression(scanner)
    if maybe_window is True and maybe_window_expression(scanner):
        return parse_window_expression(scanner)
    if maybe_function_expression(scanner):
        return parse_function_expression(scanner)
    if maybe_literal_expression(scanner):
        return parse_literal_expression(scanner)
    if maybe_column_name_expression(scanner):
        return parse_column_name_expression(scanner)
    if scanner.now.is_parenthesis:
        return parse_general_parenthesis(scanner)
    if maybe_wildcard_expression(scanner):
        return parse_wildcard_expression(scanner)
    raise SqlParseError(f"未知的一般表达式元素: {scanner}")


def parse_general_expression(scanner: TokenScanner, maybe_window: bool = True) -> SQLGeneralExpression:
    """解析一般表达式"""
    elements = [_parse_general_expression_element(scanner, maybe_window)]
    while not scanner.is_finish and maybe_compute_operator(scanner):
        elements.append(parse_compute_operator(scanner))
        elements.append(_parse_general_expression_element(scanner, maybe_window))
    if len(elements) > 1:
        return SQLComputeExpression(elements=elements)  # 如果超过 1 个元素，则返回计算表达式（多项式）
    else:
        return elements[0]  # 如果只有 1 个元素，则返回该元素的表达式


def parse_table_name_expression(scanner: TokenScanner) -> Union[SQLTableNameExpression, SQLSubQueryExpression]:
    """解析表名表达式或子查询表达式

    Examples
    --------
    >>> parse_table_name_expression(build_token_scanner("table1.column1 AS t1"))
    <SQLTableNameExpression source=table1.column1>
    """
    if (scanner.now.is_maybe_name and
            (scanner.next1 is None or (not scanner.next1.is_dot and not scanner.next1.is_parenthesis))):
        return SQLTableNameExpression(None, scanner.pop().source)
    if (scanner.now.is_maybe_name and
            scanner.next1 is not None and scanner.next1.is_dot and
            scanner.next2 is not None and scanner.next2.is_maybe_name and
            (scanner.next3 is None or not scanner.next3.is_parenthesis)):
        schema_name = scanner.pop().source
        scanner.pop()
        table_name = scanner.pop().source
        return SQLTableNameExpression(schema_name, table_name)
    if is_sub_query_parenthesis(scanner):
        return parse_sub_query_parenthesis(scanner)
    raise SqlParseError(f"无法解析为表名表达式: {scanner}")


def parse_bool_expression(scanner: TokenScanner) -> SQLBoolExpression:
    """解析布尔值表达式

    Examples
    --------
    >>> parse_bool_expression(build_token_scanner("column1 > 3"))
    <SQLBoolCompareExpression source=<SQLColumnNameExpression source=column1> <SQLGreaterThan> <SQLLiteralExpression source=3>>
    >>> parse_bool_expression(build_token_scanner("t2.column1 > 3"))
    <SQLBoolCompareExpression source=<SQLColumnNameExpression source=t2.column1> <SQLGreaterThan> <SQLLiteralExpression source=3>>
    >>> parse_bool_expression(build_token_scanner("t2.column1 + 3 > 3"))
    <SQLBoolCompareExpression source=<SQLComputeExpression source=<SQLColumnNameExpression source=t2.column1> <SQLPlus> <SQLLiteralExpression source=3>> <SQLGreaterThan> <SQLLiteralExpression source=3>>
    >>> parse_bool_expression(build_token_scanner("column1 BETWEEN 3 AND 4"))
    <SQLBoolBetweenExpression source=<SQLColumnNameExpression source=column1> BETWEEN <SQLLiteralExpression source=3> TO <SQLLiteralExpression source=4>>
    >>> parse_bool_expression(build_token_scanner("column1 + 3 BETWEEN 3 AND 4"))
    <SQLBoolBetweenExpression source=<SQLComputeExpression source=<SQLColumnNameExpression source=column1> <SQLPlus> <SQLLiteralExpression source=3>> BETWEEN <SQLLiteralExpression source=3> TO <SQLLiteralExpression source=4>>
    """
    if scanner.search_and_move("EXISTS"):
        after_value = parse_sub_query_parenthesis(scanner)
        return SQLBoolExistsExpression(is_not=False, after_value=after_value)
    if scanner.search_and_move("NOT", "EXISTS"):
        after_value = parse_sub_query_parenthesis(scanner)
        return SQLBoolExistsExpression(is_not=True, after_value=after_value)
    before_value = parse_general_expression(scanner)
    if scanner.search_and_move("BETWEEN"):
        # "... BETWEEN ... AND ..."
        from_value = parse_general_expression(scanner)
        if not scanner.pop().equals("AND"):
            raise SqlParseError(f"无法解析为 BETWEEN 布尔值表达式: {scanner}")
        to_value = parse_general_expression(scanner)
        return SQLBoolBetweenExpression(before_value=before_value, from_value=from_value, to_value=to_value)
    if scanner.search_and_move("IS"):
        # ".... IS ...." 或 "... IS NOT ..."
        if scanner.search_and_move("NOT"):
            is_not = True
        else:
            is_not = False
        after_value = parse_general_expression(scanner)
        return SQLBoolIsExpression(is_not=is_not, before_value=before_value, after_value=after_value)
    if scanner.search_and_move("IN"):
        # "... IN (1, 2, 3)" 或 "... IN (SELECT ... )"
        after_value = parse_in_parenthesis(scanner)
        return SQLBoolInExpression(is_not=False, before_value=before_value, after_value=after_value)
    if scanner.search_and_move("NOT", "IN"):
        after_value = parse_in_parenthesis(scanner)
        return SQLBoolInExpression(is_not=True, before_value=before_value, after_value=after_value)
    if scanner.search_and_move("LIKE"):
        after_value = parse_general_expression(scanner)
        return SQLBoolLikeExpression(is_not=False, before_value=before_value, after_value=after_value)
    if scanner.search_and_move("NOT LIKE"):
        after_value = parse_general_expression(scanner)
        return SQLBoolLikeExpression(is_not=True, before_value=before_value, after_value=after_value)
    if maybe_compare_operator(scanner):
        # "... > ..."
        compare_operator = parse_compare_operator(scanner)
        after_value = parse_general_expression(scanner)
        return SQLBoolCompareExpression(operator=compare_operator, before_value=before_value, after_value=after_value)
    raise SqlParseError(f"无法解析为布尔值表达式: {scanner}")


def maybe_alias_expression(scanner: TokenScanner) -> bool:
    """判断是否可能为别名表达式

    Examples
    --------
    >>> maybe_alias_expression(build_token_scanner("t1"))
    True
    >>> maybe_alias_expression(build_token_scanner("AS t1"))
    True
    >>> maybe_alias_expression(build_token_scanner("WHERE"))
    False
    """
    return not scanner.is_finish and (scanner.now.equals("AS") or scanner.now.is_maybe_name)


def parse_alias_expression(scanner: TokenScanner) -> SQLAlisaExpression:
    """解析别名表达式

    Examples
    --------
    >>> parse_alias_expression(build_token_scanner("t1"))
    <SQLAlisaExpression source=AS t1>
    >>> parse_alias_expression(build_token_scanner("AS t1"))
    <SQLAlisaExpression source=AS t1>
    >>> parse_alias_expression(build_token_scanner("WHERE"))
    Traceback (most recent call last):
    ...
    metasequoia_sql.errors.SqlParseError: 无法解析为别名表达式: <TokenScanner tokens=[<ASTCommon source=WHERE>], pos=0>
    """
    scanner.search_and_move("AS")
    if not scanner.now.is_maybe_name:
        raise SqlParseError(f"无法解析为别名表达式: {scanner}")
    return SQLAlisaExpression(alias_name=scanner.pop().source)


def parse_condition_expression(scanner: TokenScanner) -> SQLConditionExpression:
    """解析条件表达式

    Examples
    --------
    >>> parse_condition_expression(build_token_scanner("column1 > 3 AND column2 > 2 WHERE"))
    <SQLConditionExpression source=<SQLBoolCompareExpression source=<SQLColumnNameExpression source=column1> <SQLGreaterThan> <SQLLiteralExpression source=3>> <SQLAndOperator> <SQLBoolCompareExpression source=<SQLColumnNameExpression source=column2> <SQLGreaterThan> <SQLLiteralExpression source=2>>>
    >>> parse_condition_expression(build_token_scanner("column1 > 3 OR column2 > 2 WHERE"))
    <SQLConditionExpression source=<SQLBoolCompareExpression source=<SQLColumnNameExpression source=column1> <SQLGreaterThan> <SQLLiteralExpression source=3>> <SQLOrOperator> <SQLBoolCompareExpression source=<SQLColumnNameExpression source=column2> <SQLGreaterThan> <SQLLiteralExpression source=2>>>
    >>> parse_condition_expression(build_token_scanner("column1 > 3 OR column2 BETWEEN 2 AND 4 WHERE"))
    <SQLConditionExpression source=<SQLBoolCompareExpression source=<SQLColumnNameExpression source=column1> <SQLGreaterThan> <SQLLiteralExpression source=3>> <SQLOrOperator> <SQLBoolBetweenExpression source=<SQLColumnNameExpression source=column2> BETWEEN <SQLLiteralExpression source=2> TO <SQLLiteralExpression source=4>>>
    """

    def parse_single():
        if scanner.search("NOT"):
            elements.append(parse_logical_operator(scanner))
        if scanner.now.is_parenthesis:
            elements.append(parse_condition_expression(scanner.pop_as_children_scanner()))  # 插入语，子句也应该是一个条件表达式
        else:
            elements.append(parse_bool_expression(scanner))

    elements: List[Union["SQLConditionExpression", SQLBoolExpression, SQLLogicalOperator]] = []
    parse_single()  # 解析第 1 个表达式元素
    while not scanner.is_finish and scanner.now.source.upper() in {"AND", "OR"}:  # 如果是用 AND 和 OR 连接的多个表达式，则继续解析
        elements.append(parse_logical_operator(scanner))
        parse_single()

    return SQLConditionExpression(elements=elements)


def parse_join_on_expression(scanner: TokenScanner) -> SQLJoinOnExpression:
    """解析 ON 关联表达式

    Examples
    --------
    >>> parse_join_on_expression(build_token_scanner("ON t1.column1 = t2.column2"))
    <SQLJoinOnExpression source=ON <SQLConditionExpression source=<SQLBoolCompareExpression source=<SQLColumnNameExpression source=t1.column1> <SQLEqualTo> <SQLColumnNameExpression source=t2.column2>>>>
    """
    if not scanner.pop().equals("ON"):
        raise SqlParseError(f"无法解析为 ON 关联表达式: {scanner}")
    return SQLJoinOnExpression(condition=parse_condition_expression(scanner))


def parse_join_using_expression(scanner: TokenScanner) -> SQLJoinUsingExpression:
    """解析 USING 关联表达式

    Examples
    --------
    >>> parse_join_using_expression(build_token_scanner("USING(column1, column2)"))
    <SQLJoinUsingExpression source=<SQLFunctionExpression source=USING(<SQLColumnNameExpression source=column1>, <SQLColumnNameExpression source=column2>)>>
    >>> parse_join_using_expression(build_token_scanner("using(column1, column2)"))
    <SQLJoinUsingExpression source=<SQLFunctionExpression source=using(<SQLColumnNameExpression source=column1>, <SQLColumnNameExpression source=column2>)>>
    """
    if not scanner.now.equals("USING"):
        raise SqlParseError(f"无法解析为 USING 关联表达式: {scanner}")
    return SQLJoinUsingExpression(using_function=parse_function_expression(scanner))


def is_join_expression(scanner: TokenScanner) -> bool:
    """判断是否为关联表达式"""
    return scanner.search("ON") or scanner.search("USING")


def parse_join_expression(scanner: TokenScanner) -> SQLJoinExpression:
    """解析关联表达式

    Examples
    --------
    >>> parse_join_on_expression(build_token_scanner("ON t1.column1 = t2.column2"))
    <SQLJoinOnExpression source=ON <SQLConditionExpression source=<SQLBoolCompareExpression source=<SQLColumnNameExpression source=t1.column1> <SQLEqualTo> <SQLColumnNameExpression source=t2.column2>>>>
    >>> parse_join_using_expression(build_token_scanner("USING(column1, column2)"))
    <SQLJoinUsingExpression source=<SQLFunctionExpression source=USING(<SQLColumnNameExpression source=column1>, <SQLColumnNameExpression source=column2>)>>
    >>> parse_join_using_expression(build_token_scanner("using(column1, column2)"))
    <SQLJoinUsingExpression source=<SQLFunctionExpression source=using(<SQLColumnNameExpression source=column1>, <SQLColumnNameExpression source=column2>)>>
    """
    if scanner.search("ON"):
        return parse_join_on_expression(scanner)
    if scanner.search("USING"):
        return parse_join_using_expression(scanner)
    raise SqlParseError(f"无法解析为关联表达式: {scanner}")


def maybe_wildcard_expression(scanner: TokenScanner) -> bool:
    """判断是否可能为通配符表达式

    Examples
    --------
    >>> maybe_wildcard_expression(build_token_scanner("*"))
    True
    >>> maybe_wildcard_expression(build_token_scanner("t1.*"))
    True
    """
    return not scanner.is_finish and (scanner.now.is_maybe_wildcard or
                                      (scanner.now.is_maybe_name and
                                       scanner.next1 is not None and scanner.next1.is_dot and
                                       scanner.next2 is not None and scanner.next2.is_maybe_wildcard))


def parse_wildcard_expression(scanner: TokenScanner) -> SQLWildcardExpression:
    """解析通配符表达式

    Examples
    --------
    >>> parse_wildcard_expression(build_token_scanner("*"))
    <SQLWildcardExpression source=*>
    >>> parse_wildcard_expression(build_token_scanner("t1.*"))
    <SQLWildcardExpression source=t1.*>
    """
    if scanner.now.is_maybe_wildcard:
        scanner.pop()
        return SQLWildcardExpression(schema=None)
    if (scanner.now.is_maybe_name and
            scanner.next1 is not None and scanner.next1.is_dot and
            scanner.next2 is not None and scanner.next2.is_maybe_wildcard):
        schema_name = scanner.pop().source
        scanner.pop()
        scanner.pop()
        return SQLWildcardExpression(schema=schema_name)
    raise SqlParseError("无法解析为通配符表达式")


def parse_table_expression(scanner: TokenScanner) -> SQLTableExpression:
    """解析表名表达式

    Examples
    --------
    >>> parse_table_expression(build_token_scanner("schema1.table1 AS t1"))
    <SQLTableExpression source=<SQLTableNameExpression source=schema1.table1> AS <SQLAlisaExpression source=AS t1>>
    """
    table_name_expression = parse_table_name_expression(scanner)
    alias_expression = parse_alias_expression(scanner) if maybe_alias_expression(scanner) else None
    return SQLTableExpression(table=table_name_expression, alias=alias_expression)


def parse_column_expression(scanner: TokenScanner) -> SQLColumnExpression:
    """解析列名表达式

    Examples
    --------
    >>> parse_column_expression(build_token_scanner("table1.column1 AS t1"))
    <SQLColumnExpression source=<SQLFunctionExpression source=TRIM(<SQLColumnNameExpression source=column1>)> AS <SQLAlisaExpression source=AS t1>>
    >>> parse_column_expression(build_token_scanner("3 + 5 AS t1"))
    <SQLColumnExpression source=<SQLComputeExpression source=<SQLLiteralExpression source=3> <SQLPlus> <SQLLiteralExpression source=5>> AS <SQLAlisaExpression source=AS t1>>
    >>> parse_column_expression(build_token_scanner("TRIM(column1) AS t1"))
    <SQLColumnExpression source=<SQLFunctionExpression source=TRIM(<SQLColumnNameExpression source=column1>)> AS <SQLAlisaExpression source=AS t1>>
    """
    general_expression = parse_general_expression(scanner)
    alias_expression = parse_alias_expression(scanner) if maybe_alias_expression(scanner) else None
    return SQLColumnExpression(column=general_expression, alias=alias_expression)


def parse_value_expression(scanner: TokenScanner) -> SQLValueExpression:
    """解析值表达式"""
    values = []
    for value_scanner in scanner.pop_as_children_scanner_list_split_by_comma():
        values.append(parse_general_expression(value_scanner))
    return SQLValueExpression(values=values)


def maybe_limit_clause(scanner: TokenScanner) -> bool:
    """是否可能为 LIMIT 子句

    Examples
    --------
    >>> maybe_limit_clause(build_token_scanner("LIMIT 2, 5"))
    True
    >>> maybe_limit_clause(build_token_scanner("LIMIT 5 OFFSET 2"))
    True
    >>> maybe_limit_clause(build_token_scanner("ORDER BY column1"))
    False
    """
    return scanner.search("LIMIT")


def parse_limit_clause(scanner: TokenScanner) -> SQLLimitClause:
    """解析 LIMIT 子句

    Examples
    --------
    >>> parse_limit_clause(build_token_scanner("LIMIT 2, 5"))
    <SQLLimitClause source=LIMIT 2, 5>
    >>> parse_limit_clause(build_token_scanner("LIMIT 5 OFFSET 2"))
    <SQLLimitClause source=LIMIT 2, 5>
    """
    if not scanner.search_and_move("LIMIT"):
        raise SqlParseError("无法解析为 LIMIT 子句")
    cnt_1 = parse_literal_expression(scanner).as_int()
    mark = scanner.pop()
    if mark.is_comma:
        offset_int = cnt_1
        limit_int = parse_literal_expression(scanner).as_int()
    elif mark.equals("OFFSET"):
        offset_int = parse_literal_expression(scanner).as_int()
        limit_int = cnt_1
    else:
        raise SqlParseError("无法解析为 LIMIT 子句")

    return SQLLimitClause(limit=limit_int, offset=offset_int)


def maybe_order_by_clause(scanner: TokenScanner) -> bool:
    """是否可能为 ORDER BY 子句

    Examples
    --------
    >>> maybe_order_by_clause(build_token_scanner("ORDER BY column1, column2"))
    True
    >>> maybe_order_by_clause(build_token_scanner("ORDER BY column1, column2 DESC"))
    True
    >>> maybe_order_by_clause(build_token_scanner("ORDER BY trim(column1) ASC, column2"))
    True
    >>> maybe_order_by_clause(build_token_scanner("WHERE trim(column1) IS NOT NULL"))
    False
    """
    return scanner.search("ORDER", "BY")


def parse_order_by_clause(scanner: TokenScanner) -> SQLOrderByClause:
    """解析 ORDER BY 子句

    Examples
    --------
    >>> parse_order_by_clause(build_token_scanner("ORDER BY column1, column2"))
    <SQLOrderByClause source=ORDER BY <SQLColumnNameExpression source=column1>, <SQLColumnNameExpression source=column2>>
    >>> parse_order_by_clause(build_token_scanner("ORDER BY column1, column2 DESC"))
    <SQLOrderByClause source=ORDER BY <SQLColumnNameExpression source=column1>, <SQLColumnNameExpression source=column2> DESC>
    >>> parse_order_by_clause(build_token_scanner("ORDER BY trim(column1) ASC, column2"))
    <SQLOrderByClause source=ORDER BY <SQLFunctionExpression source=trim(<SQLColumnNameExpression source=column1>)>>
    """

    def parse_single():
        column = parse_general_expression(scanner)
        if not scanner.is_finish and scanner.search_and_move("DESC"):
            order = SQLEnumOrderType.DESC
        else:
            order = SQLEnumOrderType.ASC
        columns.append((column, order))

    scanner.match("ORDER", "BY")
    columns = []
    parse_single()
    while not scanner.is_finish and scanner.now.is_comma:
        scanner.pop()
        parse_single()

    return SQLOrderByClause(columns=columns)


def maybe_having_clause(scanner: TokenScanner) -> bool:
    """是否可能为 HAVING 子句

    Examples
    --------
    >>> maybe_having_clause(build_token_scanner("HAVING column1 > 3 AND column2 > 2"))
    True
    >>> maybe_having_clause(build_token_scanner("HAVING column1 > 3 OR column2 > 2"))
    True
    >>> maybe_having_clause(build_token_scanner("HAVING column1 > 3 OR column2 BETWEEN 2 AND 4"))
    True
    >>> maybe_having_clause(build_token_scanner("WHERE column1 > 3 OR column2 BETWEEN 2 AND 4"))
    False
    """
    return scanner.search("HAVING")


def parse_having_clause(scanner: TokenScanner) -> SQLHavingClause:
    """解析 HAVING 子句

    Examples
    --------
    >>> parse_having_clause(build_token_scanner("HAVING column1 > 3 AND column2 > 2"))
    <SQLHavingClause source=HAVING <SQLConditionExpression source=<SQLBoolCompareExpression source=<SQLColumnNameExpression source=column1> <SQLGreaterThan> <SQLLiteralExpression source=3>> <SQLAndOperator> <SQLBoolCompareExpression source=<SQLColumnNameExpression source=column2> <SQLGreaterThan> <SQLLiteralExpression source=2>>>>
    >>> parse_having_clause(build_token_scanner("HAVING column1 > 3 OR column2 > 2"))
    <SQLHavingClause source=HAVING <SQLConditionExpression source=<SQLBoolCompareExpression source=<SQLColumnNameExpression source=column1> <SQLGreaterThan> <SQLLiteralExpression source=3>> <SQLOrOperator> <SQLBoolCompareExpression source=<SQLColumnNameExpression source=column2> <SQLGreaterThan> <SQLLiteralExpression source=2>>>>
    >>> parse_having_clause(build_token_scanner("HAVING column1 > 3 OR column2 BETWEEN 2 AND 4"))
    <SQLHavingClause source=HAVING <SQLConditionExpression source=<SQLBoolCompareExpression source=<SQLColumnNameExpression source=column1> <SQLGreaterThan> <SQLLiteralExpression source=3>> <SQLOrOperator> <SQLBoolBetweenExpression source=<SQLColumnNameExpression source=column2> BETWEEN <SQLLiteralExpression source=2> TO <SQLLiteralExpression source=4>>>>
    """
    scanner.match("HAVING")
    return SQLHavingClause(condition=parse_condition_expression(scanner))


def maybe_group_by_clause(scanner: TokenScanner) -> bool:
    """判断是否可能为 GROUP BY 子句

    Examples
    --------
    >>> maybe_group_by_clause(build_token_scanner("GROUP BY column1, column2"))
    True
    >>> maybe_group_by_clause(build_token_scanner("GROUP BY column1, column2 DESC"))
    True
    >>> maybe_group_by_clause(build_token_scanner("GROUP BY trim(column1) ASC, column2"))
    True
    >>> maybe_group_by_clause(build_token_scanner("WHERE trim(column1) IS NOT NULL"))
    False
    """
    return scanner.search("GROUP", "BY")


def parse_group_by_clause(scanner: TokenScanner) -> SQLGroupByClause:
    """解析 GROUP BY 子句

    Examples
    --------
    >>> parse_group_by_clause(build_token_scanner("GROUP BY column1, column2"))
    <SQLGroupByClause source=GROUP BY <SQLColumnNameExpression source=column1>, <SQLColumnNameExpression source=column2>>
    >>> parse_group_by_clause(build_token_scanner("GROUP BY column1, column2 DESC"))
    <SQLGroupByClause source=GROUP BY <SQLColumnNameExpression source=column1>, <SQLColumnNameExpression source=column2>>
    >>> parse_group_by_clause(build_token_scanner("GROUP BY trim(column1) ASC, column2"))
    <SQLGroupByClause source=GROUP BY <SQLFunctionExpression source=trim(<SQLColumnNameExpression source=column1>)>>
    """
    scanner.match("GROUP", "BY")
    if scanner.search_and_move("GROUPING", "SETS"):
        grouping_list = []
        for grouping_scanner in scanner.pop_as_children_scanner_list_split_by_comma():
            if grouping_scanner.now.is_parenthesis:
                parenthesis_scanner_list = grouping_scanner.pop_as_children_scanner_list_split_by_comma()
                columns_list = [parse_general_expression(parenthesis_scanner)
                                for parenthesis_scanner in parenthesis_scanner_list]
                grouping_list.append(columns_list)
            else:
                grouping_list.append([parse_general_expression(grouping_scanner)])
        return SQLGroupingSetsGroupByClause(grouping_list=grouping_list)
    else:
        columns = [parse_general_expression(scanner)]
        while not scanner.is_finish and scanner.now.is_comma:
            scanner.pop()
            columns.append(parse_general_expression(scanner))
        with_rollup = False
        if scanner.search_and_move("WITH", "ROLLUP"):
            with_rollup = True
        return SQLNormalGroupByClause(columns=columns, with_rollup=with_rollup)


def maybe_where_clause(scanner: TokenScanner) -> bool:
    """判断是否可能为 WHERE 子句

    Examples
    --------
    >>> maybe_where_clause(build_token_scanner("WHERE column1 > 3 AND column2 > 2"))
    True
    >>> maybe_where_clause(build_token_scanner("WHERE column1 > 3 OR column2 > 2"))
    True
    >>> maybe_where_clause(build_token_scanner("WHERE column1 > 3 OR column2 BETWEEN 2 AND 4"))
    True
    >>> maybe_where_clause(build_token_scanner("HAVING column1 > 3 OR column2 BETWEEN 2 AND 4"))
    False
    """
    return scanner.search("WHERE")


def parse_where_clause(scanner: TokenScanner) -> SQLWhereClause:
    """解析 WHERE 子句

    Examples
    --------
    >>> parse_where_clause(build_token_scanner("WHERE column1 > 3 AND column2 > 2"))
    <SQLWhereClause source=WHERE <SQLConditionExpression source=<SQLBoolCompareExpression source=<SQLColumnNameExpression source=column1> <SQLGreaterThan> <SQLLiteralExpression source=3>> <SQLAndOperator> <SQLBoolCompareExpression source=<SQLColumnNameExpression source=column2> <SQLGreaterThan> <SQLLiteralExpression source=2>>>>
    >>> parse_where_clause(build_token_scanner("WHERE column1 > 3 OR column2 > 2"))
    <SQLWhereClause source=WHERE <SQLConditionExpression source=<SQLBoolCompareExpression source=<SQLColumnNameExpression source=column1> <SQLGreaterThan> <SQLLiteralExpression source=3>> <SQLOrOperator> <SQLBoolCompareExpression source=<SQLColumnNameExpression source=column2> <SQLGreaterThan> <SQLLiteralExpression source=2>>>>
    >>> parse_where_clause(build_token_scanner("WHERE column1 > 3 OR column2 BETWEEN 2 AND 4"))
    <SQLWhereClause source=WHERE <SQLConditionExpression source=<SQLBoolCompareExpression source=<SQLColumnNameExpression source=column1> <SQLGreaterThan> <SQLLiteralExpression source=3>> <SQLOrOperator> <SQLBoolBetweenExpression source=<SQLColumnNameExpression source=column2> BETWEEN <SQLLiteralExpression source=2> TO <SQLLiteralExpression source=4>>>>
    """
    scanner.match("WHERE")
    return SQLWhereClause(condition=parse_condition_expression(scanner))


def maybe_join_clause(scanner: TokenScanner) -> bool:
    """判断是否为 JOIN 子句

    Examples
    --------
    >>> maybe_join_clause(build_token_scanner("LEFT JOIN table2 AS t2 ON t1.column1 = t2.column1"))
    True
    >>> maybe_join_clause(build_token_scanner("LEFT JOIN schema2.table2 AS t2 ON t1.column1 = t2.column1"))
    True
    >>> maybe_join_clause(build_token_scanner("WHERE column1 > 3 OR column2 BETWEEN 2 AND 4"))
    False
    """
    return (scanner.search("JOIN") or
            scanner.search("INNER", "JOIN") or
            scanner.search("LEFT", "JOIN") or
            scanner.search("LEFT", "OUTER", "JOIN") or
            scanner.search("RIGHT", "JOIN") or
            scanner.search("RIGHT", "OUTER", "JOIN") or
            scanner.search("FULL", "JOIN") or
            scanner.search("FULL", "OUTER", "JOIN") or
            scanner.search("CROSS", "JOIN"))


def _parse_join_type(scanner: TokenScanner) -> SQLEnumJoinType:
    """解析关联类型"""
    if scanner.search_and_move("JOIN"):
        return SQLEnumJoinType.JOIN
    if scanner.search_and_move("INNER", "JOIN"):
        return SQLEnumJoinType.INNER_JOIN
    if scanner.search_and_move("LEFT", "JOIN"):
        return SQLEnumJoinType.LEFT_JOIN
    if scanner.search_and_move("LEFT", "OUTER", "JOIN"):
        return SQLEnumJoinType.LEFT_OUTER_JOIN
    if scanner.search_and_move("RIGHT", "JOIN"):
        return SQLEnumJoinType.RIGHT_JOIN
    if scanner.search_and_move("RIGHT", "OUTER", "JOIN"):
        return SQLEnumJoinType.RIGHT_OUTER_JOIN
    if scanner.search_and_move("FULL", "JOIN"):
        return SQLEnumJoinType.FULL_JOIN
    if scanner.search_and_move("FULL", "OUTER", "JOIN"):
        return SQLEnumJoinType.FULL_OUTER_JOIN
    if scanner.search_and_move("CROSS", "JOIN"):
        return SQLEnumJoinType.CROSS_JOIN
    raise SqlParseError(f"无法解析的关联类型: {scanner}")


def parse_join_clause(scanner: TokenScanner) -> SQLJoinClause:
    """解析 JOIN 子句

    Examples
    --------
    >>> parse_join_clause(build_token_scanner("LEFT JOIN table2 AS t2 ON t1.column1 = t2.column1"))
    <SQLJoinClause source=LEFT JOIN <SQLTableExpression source=<SQLTableNameExpression source=table2> AS <SQLAlisaExpression source=AS t2>> <SQLJoinOnExpression source=ON <SQLConditionExpression source=<SQLBoolCompareExpression source=<SQLColumnNameExpression source=t1.column1> <SQLEqualTo> <SQLColumnNameExpression source=t2.column1>>>>>
    >>> parse_join_clause(build_token_scanner("LEFT JOIN schema2.table2 AS t2 ON t1.column1 = t2.column1"))
    <SQLJoinClause source=LEFT JOIN <SQLTableExpression source=<SQLTableNameExpression source=schema2.table2> AS <SQLAlisaExpression source=AS t2>> <SQLJoinOnExpression source=ON <SQLConditionExpression source=<SQLBoolCompareExpression source=<SQLColumnNameExpression source=t1.column1> <SQLEqualTo> <SQLColumnNameExpression source=t2.column1>>>>>
    """
    join_type = _parse_join_type(scanner)
    table_expression = parse_table_expression(scanner)
    if is_join_expression(scanner):
        join_rule = parse_join_expression(scanner)
    else:
        join_rule = None
    return SQLJoinClause(join_type=join_type, table=table_expression, join_rule=join_rule)


def maybe_from_clause(scanner: TokenScanner) -> bool:
    """判断是否为 FROM 子句

    Examples
    --------
    >>> maybe_from_clause(build_token_scanner("FROM schema1.table1 AS t1"))
    True
    >>> maybe_from_clause(build_token_scanner("FROM schema1.table1 AS t1, schema2.table2 AS t2"))
    True
    >>> maybe_from_clause(build_token_scanner("LEFT JOIN table2 AS t2 ON t1.column1 = t2.column1"))
    False
    """
    return scanner.search("FROM")


def parse_from_clause(scanner: TokenScanner) -> SQLFromClause:
    """解析 FROM 子句

    Examples
    --------
    >>> parse_from_clause(build_token_scanner("FROM schema1.table1 AS t1"))
    <SQLFromClause source=FROM <SQLTableExpression source=<SQLTableNameExpression source=schema1.table1> AS <SQLAlisaExpression source=AS t1>>>
    >>> parse_from_clause(build_token_scanner("FROM schema1.table1 AS t1, schema2.table2 AS t2"))
    <SQLFromClause source=FROM <SQLTableExpression source=<SQLTableNameExpression source=schema1.table1> AS <SQLAlisaExpression source=AS t1>>, <SQLTableExpression source=<SQLTableNameExpression source=schema2.table2> AS <SQLAlisaExpression source=AS t2>>>
    """
    scanner.match("FROM")
    tables = [parse_table_expression(scanner)]
    while not scanner.is_finish and scanner.now.is_comma:
        scanner.pop()
        tables.append(parse_table_expression(scanner))
    return SQLFromClause(tables=tables)


def maybe_select_clause(scanner: TokenScanner) -> bool:
    """判断是否为 SELECT 子句

    Examples
    --------
    >>> maybe_from_clause(build_token_scanner("SELECT column1 AS c1, TRIM(column2) AS c2 FROM table1"))
    True
    >>> maybe_from_clause(build_token_scanner("SELECT column1 AS c1"))
    True
    >>> maybe_from_clause(build_token_scanner("FROM table1"))
    False
    """
    return scanner.search("SELECT")


def parse_select_clause(scanner: TokenScanner) -> SQLSelectClause:
    """解析 SELECT 子句

    Examples
    --------
    >>> parse_select_clause(build_token_scanner("SELECT column1 AS c1, TRIM(column2) AS c2 FROM table1"))
    <SQLSelectClause source=SELECT <SQLColumnExpression source=<SQLColumnNameExpression source=column1> AS <SQLAlisaExpression source=AS c1>>,
    <SQLColumnExpression source=<SQLFunctionExpression source=TRIM(<SQLColumnNameExpression source=column2>)> AS <SQLAlisaExpression source=AS c2>>>
    >>> parse_select_clause(build_token_scanner("SELECT DISTINCT column1 AS c1"))
    <SQLSelectClause source=SELECT DISTINCT <SQLColumnExpression source=<SQLColumnNameExpression source=column1> AS <SQLAlisaExpression source=AS c1>>>
    """

    scanner.match("SELECT")
    distinct = scanner.search_and_move("DISTINCT")
    columns = [parse_column_expression(scanner)]
    while not scanner.is_finish and scanner.now.is_comma:
        scanner.pop()
        columns.append(parse_column_expression(scanner))
    return SQLSelectClause(distinct=distinct, columns=columns)


def _parse_single_with_table(scanner: TokenScanner) -> Tuple[str, SQLSelectStatement]:
    """解析一个 WITH 临时表"""
    table_name = scanner.pop_as_source()
    scanner.match("AS")
    table_statement = parse_select_statement(scanner.pop_as_children_scanner(), with_clause=SQLWithClause.empty())
    return table_name, table_statement


def parse_with_clause(scanner: TokenScanner) -> Optional[SQLWithClause]:
    """解析 WITH 子句"""
    if scanner.search_and_move("WITH"):
        tables = [_parse_single_with_table(scanner)]
        while scanner.search_and_move(","):
            table_statement = _parse_single_with_table(scanner)
            tables.append(table_statement)  # 将前置的 WITH 作为当前解析临时表的 WITH 子句
        return SQLWithClause(tables=tables)
    else:
        return None


def maybe_select_statement(scanner: TokenScanner) -> bool:
    """判断是否可能为 SELECT 语句"""
    return scanner.search("SELECT")


def parse_single_select_statement(scanner: TokenScanner,
                                  with_clause: Optional[SQLWithClause] = None
                                  ) -> SQLSingleSelectStatement:
    """

    Parameters
    ----------
    scanner : TokenScanner
        扫描器
    with_clause : Optional[SQLWithClause], default = None
        前置 with 语句，如果该参数为 None 的话，则会尝试匹配 WITH 语句

    Returns
    -------

    """
    if with_clause is None:
        with_clause = parse_with_clause(scanner)
    select_clause = parse_select_clause(scanner)
    from_clause = parse_from_clause(scanner) if maybe_from_clause(scanner) else None
    join_clause = []
    while maybe_join_clause(scanner):
        join_clause.append(parse_join_clause(scanner))
    where_clause = parse_where_clause(scanner) if maybe_where_clause(scanner) else None
    group_by_clause = parse_group_by_clause(scanner) if maybe_group_by_clause(scanner) else None
    having_clause = parse_having_clause(scanner) if maybe_having_clause(scanner) else None
    order_by_clause = parse_order_by_clause(scanner) if maybe_order_by_clause(scanner) else None
    limit_clause = parse_limit_clause(scanner) if maybe_limit_clause(scanner) else None
    return SQLSingleSelectStatement(
        with_clause=with_clause,
        select_clause=select_clause,
        from_clause=from_clause,
        join_clauses=join_clause,
        where_clause=where_clause,
        group_by_clause=group_by_clause,
        having_clause=having_clause,
        order_by_clause=order_by_clause,
        limit_clause=limit_clause
    )


def parse_select_statement(scanner: TokenScanner,
                           with_clause: Optional[SQLWithClause] = None) -> SQLSelectStatement:
    """解析 SELECT 语句"""
    if with_clause is None:
        with_clause = parse_with_clause(scanner)
    result = [parse_single_select_statement(scanner, with_clause=with_clause)]
    while not scanner.is_finish:
        for union_type in SQLEnumUnionType:
            if scanner.search_and_move(*union_type.value):
                result.append(SQLUnionKeyword(union_type=union_type))
                result.append(parse_single_select_statement(scanner, with_clause=with_clause))
                break
        else:
            break
    if not scanner.is_finish:
        raise SqlParseError(f"没有解析完成: {scanner}")

    if len(result) > 1:
        return SQLUnionSelectStatement(with_clause=with_clause, elements=result)
    else:
        return result[0]


def is_sub_query_parenthesis(scanner: TokenScanner) -> bool:
    """判断是否为子查询的插入语"""
    parenthesis_scanner: TokenScanner = scanner.get_as_children_scanner()
    return maybe_select_statement(parenthesis_scanner)


def parse_sub_query_parenthesis(scanner: TokenScanner) -> SQLSubQueryExpression:
    """解析子查询的插入语"""
    return SQLSubQueryExpression(select_statement=parse_select_statement(scanner.pop_as_children_scanner()))


def parse_general_parenthesis(scanner: TokenScanner) -> SQLGeneralExpression:
    """解析一般表达式中的插入语：插入语可能为一般表达式或子查询"""
    if is_sub_query_parenthesis(scanner):
        return parse_sub_query_parenthesis(scanner)
    return parse_general_expression(scanner.pop_as_children_scanner())


def parse_in_parenthesis(scanner: TokenScanner) -> SQLGeneralExpression:
    """解析 IN 关键字后的插入语：插入语可能为子查询或值表达式"""
    if is_sub_query_parenthesis(scanner):
        return parse_sub_query_parenthesis(scanner)
    return parse_value_expression(scanner)


def parse_sql_column_type(scanner: TokenScanner) -> SQLColumnType:
    """解析字段类型：要求当前指针位置节点为函数名，下一个节点可能为函数参数也可能不是，解析为 SQLColumnType 对象"""
    # 解析字段类型名称
    function_name: str = scanner.pop().source

    # 解析字段类型参数
    if not scanner.is_finish and scanner.now.is_parenthesis:
        function_params: List[SQLGeneralExpression] = []
        for param_scanner in scanner.pop_as_children_scanner_list_split_by_comma():
            function_params.append(parse_general_expression(param_scanner))
        return SQLColumnType(function_name, function_params)
    else:
        return SQLColumnType(function_name, [])