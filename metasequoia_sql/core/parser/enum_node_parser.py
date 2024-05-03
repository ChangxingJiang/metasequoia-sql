"""
抽象语法树（AST）解析：枚举类节点
"""

from metasequoia_sql.common import TokenScanner
from metasequoia_sql.core import node
from metasequoia_sql.errors import SqlParseError

__all__ = [
    "check_insert_type", "parse_insert_type",  # 判断、解析插入类型
    "check_join_type", "parse_join_type",  # 判断、解析关联类型
    "parse_order_type",  # 解析排序类型（排序类型不需要判断，任何元素都可以是排序类型）
    "check_union_type", "parse_union_type",  # 判断、解析排序类型
    "check_compare_operator", "parse_compare_operator",  # 判断、解析比较运算符
    "check_compute_operator", "parse_compute_operator",  # 判断、解析计算运算符
    "check_logical_operator", "parse_logical_operator",  # 判断、解析逻辑运算符
]


def check_insert_type(scanner: TokenScanner) -> bool:
    """判断是否为插入类型"""
    return (scanner.search_and_move("INSERT", "INTO") or
            scanner.search_and_move("INSERT", "OVERWRITE"))


def parse_insert_type(scanner: TokenScanner) -> node.ASTInsertType:
    """解析插入类型"""
    if scanner.search_and_move("INSERT", "INTO"):
        return node.ASTInsertType(enum=node.EnumInsertType.INSERT_INTO)
    if scanner.search_and_move("INSERT", "OVERWRITE"):
        return node.ASTInsertType(enum=node.EnumInsertType.INSERT_OVERWRITE)
    raise SqlParseError(f"未知的 INSERT 类型: {scanner}")


def check_join_type(scanner: TokenScanner) -> bool:
    """判断是否为关联类型"""
    for join_type in node.EnumJoinType:
        if scanner.search(*join_type.value):
            return True
    return False


def parse_join_type(scanner: TokenScanner) -> node.ASTJoinType:
    """解析关联类型"""
    for join_type in node.EnumJoinType:
        if scanner.search_and_move(*join_type.value):
            return node.ASTJoinType(enum=join_type)
    raise SqlParseError(f"无法解析的关联类型: {scanner}")


def check_union_type(scanner: TokenScanner) -> bool:
    """判断是否为组合类型"""
    for union_type in node.EnumUnionType:
        if scanner.search(*union_type.value):
            return True
    return False


def parse_order_type(scanner: TokenScanner) -> node.ASTOrderType:
    """解析排序类型"""
    if scanner.search_and_move("DESC"):
        return node.ASTOrderType(enum=node.EnumOrderType.DESC)
    if scanner.search_and_move("ASC"):
        return node.ASTOrderType(enum=node.EnumOrderType.ASC)
    return node.ASTOrderType(enum=node.EnumOrderType.ASC)


def parse_union_type(scanner: TokenScanner) -> node.ASTUnionType:
    """解析组合类型"""
    for union_type in node.EnumUnionType:
        if scanner.search_and_move(*union_type.value):
            return node.ASTUnionType(enum=union_type)
    raise SqlParseError(f"无法解析的组合类型: {scanner}")


def check_compare_operator(scanner: TokenScanner) -> bool:
    """判断是否为比较运算符"""
    return scanner.get_as_source() in {"=", "!=", "<>", "<", "<=", ">", ">="}


def parse_compare_operator(scanner: TokenScanner) -> node.ASTCompareOperator:
    """解析比较运算符"""
    compare_operator_hash = {
        "=": node.EnumCompareOperator.EQUAL_TO,
        "<": node.EnumCompareOperator.LESS_THAN,
        "<=": node.EnumCompareOperator.LESS_THAN_OR_EQUAL,
        ">": node.EnumCompareOperator.GREATER_THAN,
        ">=": node.EnumCompareOperator.GREATER_THAN_OR_EQUAL,
        "!=": node.EnumCompareOperator.NOT_EQUAL_TO,
        "<>": node.EnumCompareOperator.NOT_EQUAL_TO
    }
    compare_operator = compare_operator_hash.get(scanner.pop_as_source())
    if compare_operator is not None:
        return node.ASTCompareOperator(enum=compare_operator)
    raise SqlParseError(f"无法解析的比较运算符: {scanner}")


def check_compute_operator(scanner: TokenScanner) -> bool:
    """判断是否为计算运算符"""
    for compute_operator in node.EnumComputeOperator:
        if scanner.search(*compute_operator.value):
            return True
    return False


def parse_compute_operator(scanner: TokenScanner) -> node.ASTComputeOperator:
    """解析计算运算符"""
    for compute_operator in node.EnumComputeOperator:
        if scanner.search_and_move(*compute_operator.value):
            return node.ASTComputeOperator(enum=compute_operator)
    raise SqlParseError(f"无法解析的计算运算符: {scanner}")


def check_logical_operator(scanner: TokenScanner) -> bool:
    """判断是否为逻辑运算符"""
    return scanner.get_as_source() in {"AND", "OR"}


def parse_logical_operator(scanner: TokenScanner) -> node.ASTLogicalOperator:
    """解析逻辑运算符"""
    for logical_operator in node.EnumLogicalOperator:
        if scanner.search_and_move(*logical_operator.value):
            return node.ASTLogicalOperator(enum=logical_operator)
    raise SqlParseError(f"无法解析的逻辑运算符: {scanner}")
