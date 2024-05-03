"""
抽象语法树（AST）解析：基础元素解析
"""

from metasequoia_sql.common import TokenScanner
from metasequoia_sql.common.basic import is_float_literal, is_int_literal
from metasequoia_sql.core import node
from metasequoia_sql.core.parser.common import unify_name
from metasequoia_sql.errors import SqlParseError
from metasequoia_sql.lexical import AMTMark, AMTSingle

__all__ = [
    "check_column_name_expression", "parse_column_name_expression",  # 判断、解析列名表达式
    "parse_table_name_expression",  # 解析表名表达式
    "parse_function_name_expression",  # 解析函数名表达式
    "check_literal_expression", "parse_literal_expression",  # 判断、解析字面值表达式
    "parse_window_row_item", "parse_window_row",  # 解析窗口函数的行限制表达式
    "check_wildcard_expression", "parse_wildcard_expression",  # 判断、解析通配符表达式
    "check_alias_expression", "parse_alias_expression",  # 判断、解析别名表达式
]


def check_column_name_expression(scanner: TokenScanner) -> bool:
    """是否可能为列名表达式"""
    return ((scanner.search(AMTMark.NAME, ".", AMTMark.NAME)
             and not scanner.search(AMTMark.NAME, ".", AMTMark.NAME, AMTMark.PARENTHESIS))
            or (scanner.search(AMTMark.NAME)
                and not scanner.search(AMTMark.NAME, ".")
                and not scanner.search(AMTMark.NAME, AMTMark.PARENTHESIS)))


def parse_column_name_expression(scanner: TokenScanner) -> node.ASTColumnNameExpression:
    """解析列名表达式"""
    if (scanner.search(AMTMark.NAME, ".", AMTMark.NAME) and
            not scanner.search(AMTMark.NAME, ".", AMTMark.NAME, AMTMark.PARENTHESIS)):
        table_name = scanner.pop_as_source()
        scanner.pop()
        column_name = scanner.pop_as_source()
        return node.ASTColumnNameExpression(table_name=unify_name(table_name),
                                            column_name=unify_name(column_name))
    if (scanner.search(AMTMark.NAME)
            and not scanner.search(AMTMark.NAME, ".")
            and not scanner.search(AMTMark.NAME, AMTMark.PARENTHESIS)):
        return node.ASTColumnNameExpression(column_name=unify_name(scanner.pop_as_source()))
    raise SqlParseError(f"无法解析为表名表达式: {scanner}")


def parse_table_name_expression(scanner: TokenScanner) -> node.ASTTableNameExpression:
    """解析表名表达式"""
    if scanner.search(AMTMark.NAME, ".", AMTMark.NAME):
        schema_name = scanner.pop_as_source()
        scanner.pop()
        table_name = scanner.pop_as_source()
        return node.ASTTableNameExpression(schema=unify_name(schema_name), table=unify_name(table_name))
    if scanner.search(AMTMark.NAME):
        name_source = scanner.pop_as_source()
        if name_source.count(".") == 1:
            schema_name, table_name = name_source.strip("`").split(".")
        else:
            schema_name, table_name = None, name_source
        return node.ASTTableNameExpression(schema=unify_name(schema_name), table=unify_name(table_name))
    raise SqlParseError(f"无法解析为表名表达式: {scanner}")


def parse_function_name_expression(scanner: TokenScanner) -> node.ASTFunctionNameExpression:
    """解析函数名表达式"""
    if scanner.search(AMTMark.NAME, ".", AMTMark.NAME):
        schema_name = scanner.pop_as_source()
        scanner.pop()
        table_name = scanner.pop_as_source()
        return node.ASTFunctionNameExpression(schema_name=unify_name(schema_name), function_name=unify_name(table_name))
    if scanner.search(AMTMark.NAME):
        name_source = scanner.pop_as_source()
        if name_source.count(".") == 1:
            schema_name, table_name = name_source.strip("`").split(".")
        else:
            schema_name, table_name = None, name_source
        return node.ASTFunctionNameExpression(schema_name=unify_name(schema_name), function_name=unify_name(table_name))
    raise SqlParseError(f"无法解析为表名表达式: {scanner}")


def check_literal_expression(scanner: TokenScanner) -> bool:
    """判断是否为字面值：包含整型字面值、浮点型字面值、字符串型字面值、十六进制型字面值、布尔型字面值、位值型字面值、空值的字面值"""
    return scanner.search(AMTMark.LITERAL) or scanner.search("-")


def parse_literal_expression(scanner: TokenScanner) -> node.ASTLiteralExpression:
    """解析字面值：包含整型字面值、浮点型字面值、字符串型字面值、十六进制型字面值、布尔型字面值、位值型字面值、空值的字面值"""
    token = scanner.pop()
    if isinstance(token, AMTSingle):
        return node.ASTLiteralExpression(value=token.source)
    if token.equals("-") and (is_int_literal(scanner.get_as_source()) or is_float_literal(scanner.get_as_source())):
        next_token = scanner.pop()
        return node.ASTLiteralExpression(value=f"-{next_token.source}")
    raise SqlParseError(f"未知的字面值: {token}")


def parse_window_row_item(scanner: TokenScanner) -> node.ASTWindowRowItem:
    """解析窗口函数行限制中的行"""
    if scanner.search_and_move("CURRENT", "ROW"):
        return node.ASTWindowRowItem(row_type=node.EnumWindowRowType.CURRENT_ROW)
    if scanner.search_and_move("UNBOUNDED"):
        if scanner.search_and_move("PRECEDING"):
            return node.ASTWindowRowItem(row_type=node.EnumWindowRowType.PRECEDING, is_unbounded=True)
        if scanner.search_and_move("FOLLOWING"):
            return node.ASTWindowRowItem(row_type=node.EnumWindowRowType.FOLLOWING, is_unbounded=True)
        raise SqlParseError(f"无法解析的窗口函数限制行: {scanner}")
    row_num = int(scanner.pop_as_source())
    if scanner.search_and_move("PRECEDING"):
        return node.ASTWindowRowItem(row_type=node.EnumWindowRowType.PRECEDING, row_num=row_num)
    if scanner.search_and_move("FOLLOWING"):
        return node.ASTWindowRowItem(row_type=node.EnumWindowRowType.FOLLOWING, row_num=row_num)
    raise SqlParseError(f"无法解析的窗口函数限制行: {scanner}")


def parse_window_row(scanner: TokenScanner) -> node.ASTWindowRow:
    """解析窗口语句限制行的表达式"""
    scanner.match("ROWS", "BETWEEN")
    from_row = parse_window_row_item(scanner)
    scanner.match("AND")
    to_row = parse_window_row_item(scanner)
    return node.ASTWindowRow(from_row=from_row, to_row=to_row)


def check_wildcard_expression(scanner: TokenScanner) -> bool:
    """判断是否可能为通配符表达式"""
    return scanner.search("*") or scanner.search(AMTMark.NAME, ".", "*")


def parse_wildcard_expression(scanner: TokenScanner) -> node.ASTWildcardExpression:
    """解析通配符表达式"""
    if scanner.search_and_move("*"):
        return node.ASTWildcardExpression()
    if scanner.search(AMTMark.NAME, ".", "*"):
        schema_name = scanner.pop_as_source()
        scanner.pop()
        scanner.pop()
        return node.ASTWildcardExpression(table_name=schema_name)
    raise SqlParseError("无法解析为通配符表达式")


def check_alias_expression(scanner: TokenScanner) -> bool:
    """判断是否可能为别名表达式"""
    return scanner.search("AS") or scanner.search(AMTMark.NAME)


def parse_alias_expression(scanner: TokenScanner, must_has_as_keyword: bool = False) -> node.ASTAlisaExpression:
    """解析别名表达式

    Parameters
    ----------
    scanner : str
        词法扫描器
    must_has_as_keyword : bool, default = False
        是否必须包含 AS 关键字
    """
    if must_has_as_keyword is True:
        scanner.match("AS")
    else:
        scanner.search_and_move("AS")
    if not scanner.search(AMTMark.NAME):
        raise SqlParseError(f"无法解析为别名表达式: {scanner}")
    return node.ASTAlisaExpression(name=unify_name(scanner.pop_as_source()))
