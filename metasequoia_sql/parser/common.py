"""
通用基础节点的解析方法
"""

from metasequoia_sql.common import TokenScanner
from metasequoia_sql.errors import SqlParseError
from metasequoia_sql.objects.sql_compare_operator import SQLCompareOperator, EnumCompareOperator
from metasequoia_sql.objects.sql_compute_operator import SQLComputeOperator, EnumComputeOperator
from metasequoia_sql.objects.sql_insert_type import SQLInsertType, EnumInsertType
from metasequoia_sql.objects.sql_join_type import SQLJoinType, EnumJoinType
from metasequoia_sql.objects.sql_logical_operator import SQLLogicalOperator, EnumLogicalOperator
from metasequoia_sql.objects.sql_order_type import SQLOrderType, EnumOrderType
from metasequoia_sql.objects.sql_union_type import SQLUnionType, EnumUnionType

__all__ = ["check_insert_type", "parse_insert_type",
           "check_join_type", "parse_join_type",
           "check_order_type", "parse_order_type",
           "check_union_type", "parse_union_type",
           "check_compare_operator", "parse_compare_operator",
           "check_compute_operator", "parse_compute_operator",
           "check_logical_operator", "parse_logical_operator"]


def check_insert_type(scanner: TokenScanner) -> bool:
    """判断是否为插入类型"""
    return scanner.search_and_move("INSERT", "INTO") or scanner.search_and_move("INSERT", "OVERWRITE")


def parse_insert_type(scanner: TokenScanner) -> SQLInsertType:
    """解析插入类型"""
    if scanner.search_and_move("INSERT", "INTO"):
        return SQLInsertType(insert_type=EnumInsertType.INSERT_INTO)
    if scanner.search_and_move("INSERT", "OVERWRITE"):
        return SQLInsertType(insert_type=EnumInsertType.INSERT_OVERWRITE)
    raise SqlParseError(f"未知的 INSERT 类型: {scanner}")


def check_join_type(scanner: TokenScanner) -> bool:
    for join_type in EnumJoinType:
        if scanner.search(*join_type.value):
            return True
    return False


def parse_join_type(scanner: TokenScanner) -> SQLJoinType:
    for join_type in EnumJoinType:
        if scanner.search_and_move(*join_type.value):
            return SQLJoinType(join_type=join_type)
    raise SqlParseError(f"无法解析的关联类型: {scanner}")


def check_order_type() -> bool:
    """任何元素都可以是排序类型（省略升序），所以均返回 True"""
    return True


def parse_order_type(scanner: TokenScanner) -> SQLOrderType:
    if scanner.search_and_move("DESC"):
        return SQLOrderType(order_type=EnumOrderType.DESC)
    return SQLOrderType(order_type=EnumOrderType.ASC)


def check_union_type(scanner: TokenScanner) -> bool:
    for union_type in EnumUnionType:
        if scanner.search(*union_type.value):
            return True
    return False


def parse_union_type(scanner: TokenScanner) -> SQLUnionType:
    for union_type in EnumUnionType:
        if scanner.search_and_move(*union_type.value):
            return SQLUnionType(union_type=union_type)
    raise SqlParseError(f"无法解析的组合类型: {scanner}")


def check_compare_operator(scanner: TokenScanner) -> bool:
    return scanner.get_as_source() in {"=", "!=", "<>", "<", "<=", ">", ">="}


def parse_compare_operator(scanner: TokenScanner) -> SQLCompareOperator:
    compare_operator_hash = {
        "=": EnumCompareOperator.EQUAL_TO,
        "<": EnumCompareOperator.LESS_THAN,
        "<=": EnumCompareOperator.LESS_THAN_OR_EQUAL,
        ">": EnumCompareOperator.GREATER_THAN,
        ">=": EnumCompareOperator.GREATER_THAN_OR_EQUAL,
        "!=": EnumCompareOperator.NOT_EQUAL_TO,
        "<>": EnumCompareOperator.NOT_EQUAL_TO
    }
    compare_operator = compare_operator_hash.get(scanner.pop_as_source())
    if compare_operator is not None:
        return SQLCompareOperator(compare_operator=compare_operator)
    raise SqlParseError(f"无法解析的比较运算符: {scanner}")


def check_compute_operator(scanner: TokenScanner) -> bool:
    for compute_operator in EnumComputeOperator:
        if scanner.search(compute_operator.value):
            return True
    return False


def parse_compute_operator(scanner: TokenScanner) -> SQLComputeOperator:
    for compute_operator in EnumComputeOperator:
        if scanner.search_and_move(compute_operator.value):
            return SQLComputeOperator(compute_operator=compute_operator)
    raise SqlParseError(f"无法解析的计算运算符: {scanner}")


def check_logical_operator(scanner: TokenScanner) -> bool:
    return scanner.get_as_source() in {"AND", "OR", "NOT"}


def parse_logical_operator(scanner: TokenScanner) -> SQLLogicalOperator:
    for logical_operator in EnumLogicalOperator:
        if scanner.search_and_move(logical_operator.value):
            return SQLLogicalOperator(logical_operator=logical_operator)
    raise SqlParseError(f"无法解析的逻辑运算符: {scanner}")
