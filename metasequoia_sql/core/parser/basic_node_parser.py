"""
抽象语法树（AST）解析：基础元素解析
"""

from metasequoia_sql.common import TokenScanner
from metasequoia_sql.core import node
from metasequoia_sql.core.parser.common import unify_name
from metasequoia_sql.errors import SqlParseError
from metasequoia_sql.lexical import AMTMark

__all__ = [
    "check_column_name_expression", "parse_column_name_expression",  # 判断、解析列名表达式
    "parse_table_name_expression",  # 解析表名表达式
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
    """解析表名表达式或子查询表达式"""
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
