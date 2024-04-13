# pylint: disable=C0302

"""
基础元素的解析逻辑

因为不同解析函数之间需要相互调用，所以脚本文件不可避免地需要超过 1000 行，故忽略 pylint C0302。

TODO 使用 search 替代直接使用 now 判断
TODO 整理各种函数的共同规律
"""

from typing import Optional, Tuple, List, Union

from metasequoia_sql import ast
from metasequoia_sql.common import TokenScanner, build_token_scanner
from metasequoia_sql.core.objects import *
from metasequoia_sql.core.static import *
from metasequoia_sql.errors import SqlParseError

__all__ = [
    # ------------------------------ 基础元素解析 ------------------------------
    # 判断、解析插入类型
    "check_insert_type", "parse_insert_type",

    # 判断、解析关联类型
    "check_join_type", "parse_join_type",

    # 判断、解析排序类型
    "check_order_type", "parse_order_type",

    # 判断、解析组合类型
    "check_union_type", "parse_union_type",

    # 判断、解析比较运算符
    "check_compare_operator", "parse_compare_operator",

    # 判断、解析计算运算符
    "check_compute_operator", "parse_compute_operator",

    # 判断、解析逻辑运算符
    "check_logical_operator", "parse_logical_operator",

    # ------------------------------ 一般表达式解析 ------------------------------
    # 判断、解析字面值表达式
    "check_literal_expression", "parse_literal_expression",

    # 判断、解析列名表达式
    "check_column_name_expression", "parse_column_name_expression",

    # 判断、解析函数表达式
    # TODO 将 CAST_DATA_TYPE 提出作为一个基础类型节点
    # TODO 将 function_name 提出作为一个专有表达式
    "check_function_expression", "parse_cast_data_type", "parse_cast_function_expression",
    "parse_extract_function_expression", "parse_if_function_expression", "parse_function_name",
    "parse_function_expression",

    # 解析布尔值表达式
    "parse_bool_expression",

    # 判断、解析窗口表达式
    "check_window_expression", "parse_window_expression",

    # 判断、解析通配符表达式
    "check_wildcard_expression", "parse_wildcard_expression",

    # 解析条件表达式
    "parse_condition_expression",

    # 判断、解析 CASE 表达式
    "check_case_expression", "parse_case_expression",

    # 解析值表达式
    "parse_value_expression",

    # 判断、解析子查询表达式
    "check_sub_query_parenthesis", "parse_sub_query_expression",

    # 解析一般表达式
    "parse_general_expression",

    # ------------------------------ 专有表达式解析 ------------------------------
    # 解析表名表达式
    "parse_table_name_expression",

    # 判断、解析表名表达式
    "check_alias_expression", "parse_alias_expression",

    # 判断、解析关联表达式
    "check_join_expression", "parse_join_on_expression", "parse_join_using_expression", "parse_join_expression",

    # 解析字段类型表达式
    "parse_column_type_expression",

    # 解析表表达式
    "parse_table_expression",

    # 解析列表达式
    "parse_column_expression",

    # 解析等式表达式
    "parse_equal_expression",

    # 判断、解析分区表达式
    "check_partition_expression", "parse_partition_expression",

    # 判断、解析声明外键表达式
    "check_foreign_key_expression", "parse_foreign_key_expression",

    # 判断、解析声明索引表达式
    "check_primary_index_expression", "parse_primary_index_expression", "check_unique_index_expression",
    "parse_unique_index_expression", "check_normal_index_expression", "parse_normal_index_expression",
    "check_fulltext_expression", "parse_fulltext_expression",

    # 解析声明字段表达式
    "parse_define_column_expression",

    # 解析配置名称表达式和配置值表达式
    "parse_config_name_expression", "parse_config_value_expression",

    # ------------------------------ 子句解析 ------------------------------
    # 判断、解析 SELECT 子句
    "check_select_clause", "parse_select_clause",

    # 判断、解析 FROM 子句
    "check_from_clause", "parse_from_clause",

    # 判断、解析 LATERAL VIEW 子句
    "check_lateral_view_clause", "parse_lateral_view_clause",

    # 判断、解析 JOIN 子句
    "check_join_clause", "parse_join_clause",

    # 判断、解析 WHERE 子句
    "check_where_clause", "parse_where_clause",

    # 判断、解析 GROUP BY 子句
    "check_group_by_clause", "parse_group_by_clause",

    # 判断、解析 HAVING 子句
    "check_having_clause", "parse_having_clause",

    # 判断、解析 ORDER BY 子句
    "check_order_by_clause", "parse_order_by_clause",

    # 判断、解析 LIMIT 子句
    "check_limit_clause", "parse_limit_clause",

    # 解析 WITH 子句
    "parse_with_clause",

    # ------------------------------ 语句解析 ------------------------------
    # 判断、解析 SELECT 语句
    "check_select_statement", "parse_single_select_statement", "parse_select_statement",

    # 判断、解析 INSERT 语句
    "check_insert_statement", "parse_insert_statement",

    # 判断、解析 SET 语句
    "check_set_statement", "parse_set_statement",

    # 解析 CREATE TABLE 语句
    "parse_create_table_statement",

    # 通用表达式解析
    "parse_statements"
]


def _unify_input_scanner(scanner_or_string: Union[TokenScanner, str]) -> TokenScanner:
    """格式化输入的参数，将字符串格式的 SQL 语句统一为词法扫描器 TokenScanner"""
    if isinstance(scanner_or_string, TokenScanner):
        return scanner_or_string
    if isinstance(scanner_or_string, str):
        return build_token_scanner(scanner_or_string)
    raise SqlParseError(f"未知的参数类型: {scanner_or_string} (type={type(scanner_or_string)})")


def check_insert_type(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否为插入类型"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.search_and_move("INSERT", "INTO") or scanner.search_and_move("INSERT", "OVERWRITE")


def parse_insert_type(scanner_or_string: Union[TokenScanner, str]) -> SQLInsertType:
    """解析插入类型"""
    scanner = _unify_input_scanner(scanner_or_string)
    if scanner.search_and_move("INSERT", "INTO"):
        return SQLInsertType(insert_type=EnumInsertType.INSERT_INTO)
    if scanner.search_and_move("INSERT", "OVERWRITE"):
        return SQLInsertType(insert_type=EnumInsertType.INSERT_OVERWRITE)
    raise SqlParseError(f"未知的 INSERT 类型: {scanner}")


def check_join_type(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否为关联类型"""
    scanner = _unify_input_scanner(scanner_or_string)
    for join_type in EnumJoinType:
        if scanner.search(*join_type.value):
            return True
    return False


def parse_join_type(scanner_or_string: Union[TokenScanner, str]) -> SQLJoinType:
    """解析关联类型"""
    scanner = _unify_input_scanner(scanner_or_string)
    for join_type in EnumJoinType:
        if scanner.search_and_move(*join_type.value):
            return SQLJoinType(join_type=join_type)
    raise SqlParseError(f"无法解析的关联类型: {scanner}")


def check_order_type() -> bool:
    """判断是否为排序类型：任何元素都可以是排序类型（省略升序），所以均返回 True"""
    return True


def parse_order_type(scanner_or_string: Union[TokenScanner, str]) -> SQLOrderType:
    """解析排序类型"""
    scanner = _unify_input_scanner(scanner_or_string)
    if scanner.search_and_move("DESC"):
        return SQLOrderType(order_type=EnumOrderType.DESC)
    if scanner.search_and_move("ASC"):
        return SQLOrderType(order_type=EnumOrderType.ASC)
    return SQLOrderType(order_type=EnumOrderType.ASC)


def check_union_type(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否为组合类型"""
    scanner = _unify_input_scanner(scanner_or_string)
    for union_type in EnumUnionType:
        if scanner.search(*union_type.value):
            return True
    return False


def parse_union_type(scanner_or_string: Union[TokenScanner, str]) -> SQLUnionType:
    """解析组合类型"""
    scanner = _unify_input_scanner(scanner_or_string)
    for union_type in EnumUnionType:
        if scanner.search_and_move(*union_type.value):
            return SQLUnionType(union_type=union_type)
    raise SqlParseError(f"无法解析的组合类型: {scanner}")


def check_compare_operator(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否为比较运算符"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.get_as_source() in {"=", "!=", "<>", "<", "<=", ">", ">="}


def parse_compare_operator(scanner_or_string: Union[TokenScanner, str]) -> SQLCompareOperator:
    """解析比较运算符"""
    scanner = _unify_input_scanner(scanner_or_string)
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


def check_compute_operator(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否为计算运算符"""
    scanner = _unify_input_scanner(scanner_or_string)
    for compute_operator in EnumComputeOperator:
        if scanner.search(compute_operator.value):
            return True
    return False


def parse_compute_operator(scanner_or_string: Union[TokenScanner, str]) -> SQLComputeOperator:
    """解析计算运算符"""
    scanner = _unify_input_scanner(scanner_or_string)
    for compute_operator in EnumComputeOperator:
        if scanner.search_and_move(compute_operator.value):
            return SQLComputeOperator(compute_operator=compute_operator)
    raise SqlParseError(f"无法解析的计算运算符: {scanner}")


def check_logical_operator(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否为逻辑运算符"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.get_as_source() in {"AND", "OR", "NOT"}


def parse_logical_operator(scanner_or_string: Union[TokenScanner, str]) -> SQLLogicalOperator:
    """解析逻辑运算符"""
    scanner = _unify_input_scanner(scanner_or_string)
    for logical_operator in EnumLogicalOperator:
        if scanner.search_and_move(logical_operator.value):
            return SQLLogicalOperator(logical_operator=logical_operator)
    raise SqlParseError(f"无法解析的逻辑运算符: {scanner}")


def check_literal_expression(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否为字面值：包含整型字面值、浮点型字面值、字符串型字面值、十六进制型字面值、布尔型字面值、位值型字面值、空值的字面值"""
    scanner = _unify_input_scanner(scanner_or_string)
    return not scanner.is_finish and (scanner.now.is_literal or scanner.now.equals("-"))


def parse_literal_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLLiteralExpression:
    """解析字面值：包含整型字面值、浮点型字面值、字符串型字面值、十六进制型字面值、布尔型字面值、位值型字面值、空值的字面值"""
    scanner = _unify_input_scanner(scanner_or_string)
    token: ast.AST = scanner.pop()
    if isinstance(token, ast.ASTLiteralInteger):
        return SQLLiteralIntegerExpression(token.literal_value)
    if isinstance(token, ast.ASTLiteralFloat):
        return SQLLiteralFloatExpression(token.literal_value)
    if isinstance(token, ast.ASTLiteralString):
        return SQLLiteralStringExpression(token.literal_value)
    if isinstance(token, ast.ASTLiteralHex):
        return SQLLiteralHexExpression(token.literal_value)
    if isinstance(token, ast.ASTLiteralBool):
        return SQLLiteralBoolExpression(token.literal_value)
    if isinstance(token, ast.ASTLiteralBit):
        return SQLLiteralBitExpression(token.literal_value)
    if isinstance(token, ast.ASTLiteralNull):
        return SQLLiteralNullExpression()
    if token.equals("-") and isinstance(scanner.now, ast.ASTLiteralInteger):
        next_token = scanner.pop()
        return SQLLiteralIntegerExpression(-next_token.literal_value)
    if token.equals("-") and isinstance(scanner.now, ast.ASTLiteralFloat):
        next_token = scanner.pop()
        return SQLLiteralFloatExpression(-next_token.literal_value)
    raise SqlParseError(f"未知的字面值: {token}")


def check_column_name_expression(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """是否可能为列名表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    return not scanner.is_finish and (
            (scanner.now.is_maybe_name and
             (scanner.next1 is None or (not scanner.next1.is_dot and not scanner.next1.is_parenthesis))) or
            (scanner.now.is_maybe_name and
             scanner.next1 is not None and scanner.next1.is_dot and
             scanner.next2 is not None and scanner.next2.is_maybe_name and
             (scanner.next3 is None or not scanner.next3.is_parenthesis))
    )


def parse_column_name_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLColumnNameExpression:
    """解析列名表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    if (scanner.now.is_maybe_name and
            (scanner.next1 is None or (not scanner.next1.is_dot and not scanner.next1.is_parenthesis))):
        return SQLColumnNameExpression(None, scanner.pop_as_source())
    if (scanner.now.is_maybe_name and
            scanner.next1 is not None and scanner.next1.is_dot and
            scanner.next2 is not None and scanner.next2.is_maybe_name and
            (scanner.next3 is None or not scanner.next3.is_parenthesis)):
        table_name = scanner.pop_as_source()
        scanner.pop()
        column_name = scanner.pop_as_source()
        return SQLColumnNameExpression(table_name, column_name)
    raise SqlParseError(f"无法解析为表名表达式: {scanner}")


def check_function_expression(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """是否可能为函数表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    return not scanner.is_finish and (
            (scanner.now.is_maybe_name and
             scanner.next1 is not None and scanner.next1.is_parenthesis) or
            (scanner.now.is_maybe_name and
             scanner.next1 is not None and scanner.next1.is_dot and
             scanner.next2 is not None and scanner.next2.is_maybe_name and
             scanner.next3 is not None and scanner.next3.is_parenthesis
             ))


def parse_cast_data_type(scanner_or_string: Union[TokenScanner, str]) -> EnumCastDataType:
    """解析 CAST 函数表达式中的类型"""
    scanner = _unify_input_scanner(scanner_or_string)
    for cast_type in EnumCastDataType:
        if scanner.search_and_move(cast_type.value):
            return cast_type
    raise SqlParseError(f"无法解析的 CAST 函数表达式中的类型: {scanner}")


def parse_cast_function_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLCastFunctionExpression:
    """解析 CAST 函数表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    column_expression = parse_general_expression(scanner)
    scanner.match("AS")
    signed = scanner.search_and_move("SIGNED")
    cast_type = parse_cast_data_type(scanner)
    if not scanner.is_finish and scanner.now_is_parenthesis:
        parenthesis_scanner = scanner.pop_as_children_scanner()
        cast_params: Optional[List[SQLGeneralExpression]] = []
        for param_scanner in parenthesis_scanner.split_by(","):
            cast_params.append(parse_general_expression(param_scanner))
            if not param_scanner.is_finish:
                raise SqlParseError(f"无法解析函数参数: {param_scanner}")
    else:
        cast_params = None
    if not scanner.is_finish:
        raise SqlParseError(f"无法解析CAST函数参数: {scanner}")
    cast_data_type = SQLCastDataType(signed=signed, data_type=cast_type, params=cast_params)
    return SQLCastFunctionExpression(column_expression=column_expression, cast_type=cast_data_type)


def parse_extract_function_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLExtractFunctionExpression:
    """解析 EXTRACT 函数表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    extract_name = parse_general_expression(scanner)
    scanner.match("FROM")
    column_expression = parse_general_expression(scanner)
    if not scanner.is_finish:
        raise SqlParseError(f"无法解析EXTRACT函数参数: {scanner}")
    return SQLExtractFunctionExpression(extract_name=extract_name, column_expression=column_expression)


def parse_if_function_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLFunctionExpression:
    """解析 IF 函数表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    function_params: List[SQLGeneralExpression] = []
    first_param = True
    for param_scanner in scanner.split_by(","):
        if first_param is True:
            function_params.append(parse_condition_expression(param_scanner))
            first_param = False
        else:
            function_params.append(parse_general_expression(param_scanner))
        if not param_scanner.is_finish:
            raise SqlParseError(f"无法解析函数参数: {param_scanner}")
    return SQLFunctionExpression(schema_name=None, function_name="IF", function_params=function_params)


def parse_function_name(scanner_or_string: Union[TokenScanner, str]) -> Tuple[Optional[str], str]:
    """解析函数表达式函数的 schema 名和 function 名"""
    scanner = _unify_input_scanner(scanner_or_string)
    if (scanner.now.is_maybe_name and
            scanner.next1 is not None and scanner.next1.is_parenthesis):
        return None, scanner.pop_as_source()
    if (scanner.now.is_maybe_name and
            scanner.next1 is not None and scanner.next1.is_dot and
            scanner.next2 is not None and scanner.next2.is_maybe_name and
            scanner.next3 is not None and scanner.next3.is_parenthesis):
        schema_name = scanner.pop_as_source()
        scanner.pop()
        return schema_name, scanner.pop_as_source()
    raise SqlParseError(f"无法解析为函数表达式: {scanner}")


def parse_function_expression(scanner_or_string: Union[TokenScanner, str]) -> Union[SQLFunctionExpression]:
    """解析函数表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    schema_name, function_name = parse_function_name(scanner)

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
    for param_scanner in parenthesis_scanner.split_by(","):
        function_params.append(parse_general_expression(param_scanner))
        if not param_scanner.is_finish:
            raise SqlParseError(f"无法解析函数参数: {param_scanner}")

    if schema_name is None and function_name.upper() in {"COUNT", "SUM", "MIN", "MAX", "AVG"}:
        return SQLAggregationFunctionExpression(function_name=function_name,
                                                function_params=function_params,
                                                is_distinct=is_distinct)
    return SQLFunctionExpression(schema_name=schema_name,
                                 function_name=function_name,
                                 function_params=function_params)


def parse_function_expression_maybe_with_array_index(scanner_or_string: Union[TokenScanner, str]
                                                     ) -> Union[SQLFunctionExpression, SQLArrayIndexExpression]:
    """解析函数表达式，并解析函数表达式后可能包含的数组下标"""
    scanner = _unify_input_scanner(scanner_or_string)
    array_expression = parse_function_expression(scanner)
    if scanner.is_finish or not scanner.now.is_array_index:
        return array_expression
    idx = int(scanner.pop_as_source().lstrip("[").rstrip("]"))
    return SQLArrayIndexExpression(array_expression=array_expression, idx=idx)


def parse_bool_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLBoolExpression:
    """解析布尔值表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    if scanner.search_and_move("EXISTS"):
        after_value = parse_sub_query_expression(scanner)
        return SQLBoolExistsExpression(is_not=False, after_value=after_value)
    if scanner.search_and_move("NOT", "EXISTS"):
        after_value = parse_sub_query_expression(scanner)
        return SQLBoolExistsExpression(is_not=True, after_value=after_value)
    before_value = parse_general_expression(scanner)
    if scanner.search_and_move("BETWEEN"):
        # "... BETWEEN ... AND ..."
        from_value = parse_general_expression(scanner)
        if not scanner.search_and_move("AND"):
            raise SqlParseError(f"无法解析为 BETWEEN 布尔值表达式: {scanner}")
        to_value = parse_general_expression(scanner)
        return SQLBoolBetweenExpression(before_value=before_value, from_value=from_value, to_value=to_value)
    if scanner.search_and_move("IS"):
        # ".... IS ...." 或 "... IS NOT ..."
        is_not = scanner.search_and_move("NOT")
        after_value = parse_general_expression(scanner)
        return SQLBoolIsExpression(is_not=is_not, before_value=before_value, after_value=after_value)
    if scanner.search_and_move("IN"):
        # "... IN (1, 2, 3)" 或 "... IN (SELECT ... )"
        after_value = _parse_in_parenthesis(scanner)
        return SQLBoolInExpression(is_not=False, before_value=before_value, after_value=after_value)
    if scanner.search_and_move("NOT", "IN"):
        after_value = _parse_in_parenthesis(scanner)
        return SQLBoolInExpression(is_not=True, before_value=before_value, after_value=after_value)
    if scanner.search_and_move("LIKE"):
        after_value = parse_general_expression(scanner)
        return SQLBoolLikeExpression(is_not=False, before_value=before_value, after_value=after_value)
    if scanner.search_and_move("NOT LIKE"):
        after_value = parse_general_expression(scanner)
        return SQLBoolLikeExpression(is_not=True, before_value=before_value, after_value=after_value)
    if check_compare_operator(scanner):
        # "... > ..."
        compare_operator = parse_compare_operator(scanner)
        after_value = parse_general_expression(scanner)
        return SQLBoolCompareExpression(operator=compare_operator, before_value=before_value, after_value=after_value)
    raise SqlParseError(f"无法解析为布尔值表达式: {scanner}")


def check_window_expression(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否可能为窗口函数"""
    scanner = _unify_input_scanner(scanner_or_string)
    return not scanner.is_finish and (
            scanner.now.is_maybe_name and scanner.now.source.upper() in WINDOW_FUNCTION_NAME_SET and
            scanner.next1 is not None and scanner.next1.is_parenthesis and
            scanner.next2 is not None and scanner.next2.equals("OVER") and
            scanner.next3 is not None and scanner.next3.is_parenthesis)


def parse_window_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLWindowExpression:
    """解析窗口函数

    TODO 支持 ROW BETWEEN 的语法

    """
    scanner = _unify_input_scanner(scanner_or_string)
    window_function = parse_function_expression_maybe_with_array_index(scanner)
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


def check_wildcard_expression(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否可能为通配符表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    return not scanner.is_finish and (scanner.now.is_maybe_wildcard or
                                      (scanner.now.is_maybe_name and
                                       scanner.next1 is not None and scanner.next1.is_dot and
                                       scanner.next2 is not None and scanner.next2.is_maybe_wildcard))


def parse_wildcard_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLWildcardExpression:
    """解析通配符表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    if scanner.now.is_maybe_wildcard:
        scanner.pop()
        return SQLWildcardExpression(schema=None)
    if (scanner.now.is_maybe_name and
            scanner.next1 is not None and scanner.next1.is_dot and
            scanner.next2 is not None and scanner.next2.is_maybe_wildcard):
        schema_name = scanner.pop_as_source()
        scanner.pop()
        scanner.pop()
        return SQLWildcardExpression(schema=schema_name)
    raise SqlParseError("无法解析为通配符表达式")


def parse_condition_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLConditionExpression:
    """解析条件表达式"""
    scanner = _unify_input_scanner(scanner_or_string)

    def parse_single():
        if scanner.search("NOT"):
            elements.append(parse_logical_operator(scanner))
        if scanner.now_is_parenthesis:
            elements.append(parse_condition_expression(scanner.pop_as_children_scanner()))  # 插入语，子句也应该是一个条件表达式
        else:
            elements.append(parse_bool_expression(scanner))

    elements: List[Union["SQLConditionExpression", SQLBoolExpression, SQLLogicalOperator]] = []
    parse_single()  # 解析第 1 个表达式元素
    while not scanner.is_finish and scanner.now.source.upper() in {"AND", "OR"}:  # 如果是用 AND 和 OR 连接的多个表达式，则继续解析
        elements.append(parse_logical_operator(scanner))
        parse_single()

    return SQLConditionExpression(elements=elements)


def check_case_expression(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否可能为 CASE 表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.search("CASE")


def parse_case_expression(scanner_or_string: Union[TokenScanner, str]
                          ) -> Union[SQLCaseExpression, SQLCaseValueExpression]:
    """解析 CASE 表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
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


def parse_value_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLValueExpression:
    """解析值表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    values = []
    for value_scanner in scanner.pop_as_children_scanner_list_split_by(","):
        values.append(parse_general_expression(value_scanner))
    return SQLValueExpression(values=values)


def check_sub_query_parenthesis(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否为子查询的插入语"""
    scanner = _unify_input_scanner(scanner_or_string)
    return check_select_statement(scanner.get_as_children_scanner())


def parse_sub_query_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLSubQueryExpression:
    """解析子查询表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    return SQLSubQueryExpression(select_statement=parse_select_statement(scanner.pop_as_children_scanner()))


def _parse_in_parenthesis(scanner_or_string: Union[TokenScanner, str]) -> SQLGeneralExpression:
    """解析 IN 关键字后的插入语：插入语可能为子查询或值表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    if check_sub_query_parenthesis(scanner):
        return parse_sub_query_expression(scanner)
    return parse_value_expression(scanner)


def _parse_general_parenthesis(scanner_or_string: Union[TokenScanner, str]) -> SQLGeneralExpression:
    """解析一般表达式中的插入语：插入语可能为一般表达式或子查询"""
    scanner = _unify_input_scanner(scanner_or_string)
    if check_sub_query_parenthesis(scanner):
        return parse_sub_query_expression(scanner)
    return parse_general_expression(scanner.pop_as_children_scanner())


def _parse_general_expression_element(scanner_or_string: Union[TokenScanner, str],
                                      maybe_window: bool) -> SQLGeneralExpression:
    """解析一般表达式中的一个元素

    # TODO 将非一般表达式的子类移出一般表达式
    """
    scanner = _unify_input_scanner(scanner_or_string)
    if check_case_expression(scanner):
        return parse_case_expression(scanner)
    if maybe_window is True and check_window_expression(scanner):
        return parse_window_expression(scanner)
    if check_function_expression(scanner):
        return parse_function_expression_maybe_with_array_index(scanner)
    if check_literal_expression(scanner):
        return parse_literal_expression(scanner)
    if check_column_name_expression(scanner):
        return parse_column_name_expression(scanner)
    if scanner.now_is_parenthesis:
        return _parse_general_parenthesis(scanner)
    if check_wildcard_expression(scanner):
        return parse_wildcard_expression(scanner)
    raise SqlParseError(f"未知的一般表达式元素: {scanner}")


def parse_general_expression(scanner_or_string: Union[TokenScanner, str],
                             maybe_window: bool = True) -> SQLGeneralExpression:
    """解析一般表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    elements = [_parse_general_expression_element(scanner, maybe_window)]
    while check_compute_operator(scanner):
        elements.append(parse_compute_operator(scanner))
        elements.append(_parse_general_expression_element(scanner, maybe_window))
    if len(elements) == 1:
        return elements[0]  # 如果只有 1 个元素，则返回该元素的表达式
    return SQLComputeExpression(elements=elements)  # 如果超过 1 个元素，则返回计算表达式（多项式）


def parse_config_name_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLConfigNameExpression:
    """解析配置名称表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    config_name_list = [scanner.pop_as_source()]
    while not scanner.is_finish and scanner.now.is_dot:
        scanner.pop()
        config_name_list.append(scanner.pop_as_source())
    return SQLConfigNameExpression(config_name=".".join(config_name_list))


def parse_config_value_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLConfigValueExpression:
    """解析配置值表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    return SQLConfigValueExpression(config_value=scanner.pop_as_source())


def parse_table_name_expression(scanner_or_string: Union[TokenScanner, str]
                                ) -> Union[SQLTableNameExpression, SQLSubQueryExpression]:
    """解析表名表达式或子查询表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    if (scanner.now.is_maybe_name and
            (scanner.next1 is None or (not scanner.next1.is_dot and not scanner.next1.is_parenthesis))):
        return SQLTableNameExpression(None, scanner.pop_as_source())
    if (scanner.now.is_maybe_name and
            scanner.next1 is not None and scanner.next1.is_dot and
            scanner.next2 is not None and scanner.next2.is_maybe_name and
            (scanner.next3 is None or not scanner.next3.is_parenthesis)):
        schema_name = scanner.pop_as_source()
        scanner.pop()
        table_name = scanner.pop_as_source()
        return SQLTableNameExpression(schema_name, table_name)
    if check_sub_query_parenthesis(scanner):
        return parse_sub_query_expression(scanner)
    raise SqlParseError(f"无法解析为表名表达式: {scanner}")


def check_alias_expression(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否可能为别名表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    return not scanner.is_finish and (scanner.now.equals("AS") or scanner.now.is_maybe_name)


def parse_alias_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLAlisaExpression:
    """解析别名表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    scanner.search_and_move("AS")
    if not scanner.now.is_maybe_name:
        raise SqlParseError(f"无法解析为别名表达式: {scanner}")
    return SQLAlisaExpression(alias_name=scanner.pop_as_source())


def check_join_expression(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否为关联表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.search("ON") or scanner.search("USING")


def parse_join_on_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLJoinOnExpression:
    """解析 ON 关联表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    if not scanner.search_and_move("ON"):
        raise SqlParseError(f"无法解析为 ON 关联表达式: {scanner}")
    return SQLJoinOnExpression(condition=parse_condition_expression(scanner))


def parse_join_using_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLJoinUsingExpression:
    """解析 USING 关联表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    if not scanner.search("USING"):
        raise SqlParseError(f"无法解析为 USING 关联表达式: {scanner}")
    return SQLJoinUsingExpression(using_function=parse_function_expression(scanner))


def parse_join_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLJoinExpression:
    """解析关联表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    if scanner.search("ON"):
        return parse_join_on_expression(scanner)
    if scanner.search("USING"):
        return parse_join_using_expression(scanner)
    raise SqlParseError(f"无法解析为关联表达式: {scanner}")


def parse_column_type_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLColumnTypeExpression:
    """解析 DDL 的字段类型：要求当前指针位置节点为函数名，下一个节点可能为函数参数也可能不是，解析为 SQLColumnType 对象"""
    scanner = _unify_input_scanner(scanner_or_string)

    # 解析字段类型名称
    function_name: str = scanner.pop_as_source()

    # 解析字段类型参数
    if not scanner.is_finish and scanner.now_is_parenthesis:
        function_params: List[SQLGeneralExpression] = []
        for param_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            function_params.append(parse_general_expression(param_scanner))
        return SQLColumnTypeExpression(function_name, function_params)
    return SQLColumnTypeExpression(function_name, [])


def parse_table_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLTableExpression:
    """解析表名表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    table_name_expression = parse_table_name_expression(scanner)
    alias_expression = parse_alias_expression(scanner) if check_alias_expression(scanner) else None
    return SQLTableExpression(table=table_name_expression, alias=alias_expression)


def parse_column_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLColumnExpression:
    """解析列名表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    general_expression = parse_general_expression(scanner)
    alias_expression = parse_alias_expression(scanner) if check_alias_expression(scanner) else None
    return SQLColumnExpression(column=general_expression, alias=alias_expression)


def parse_equal_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLEqualExpression:
    """解析等式表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    before_value = parse_general_expression(scanner)
    scanner.match("=")
    after_value = parse_general_expression(scanner)
    return SQLEqualExpression(before_value=before_value, after_value=after_value)


def check_partition_expression(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否可能为分区表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.search("PARTITION")


def parse_partition_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLPartitionExpression:
    """解析分区表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    scanner.match("PARTITION")
    partition_list = []
    for partition_scanner in scanner.pop_as_children_scanner_list_split_by(","):
        partition_list.append(parse_equal_expression(partition_scanner))
    return SQLPartitionExpression(partition_list=partition_list)


def check_foreign_key_expression(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否为外键表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.search("CONSTRAINT")


def parse_foreign_key_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLForeignKeyExpression:
    """解析外键表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    scanner.match("CONSTRAINT")
    constraint_name = scanner.pop_as_source()
    scanner.match("FOREIGN", "KEY")
    slave_columns = [column_scanner.pop_as_source()
                     for column_scanner in scanner.pop_as_children_scanner_list_split_by(",")]
    scanner.match("REFERENCES")
    master_table_name = scanner.pop_as_source()
    master_columns = [column_scanner.pop_as_source()
                      for column_scanner in scanner.pop_as_children_scanner_list_split_by(",")]
    return SQLForeignKeyExpression(
        constraint_name=constraint_name,
        slave_columns=slave_columns,
        master_table_name=master_table_name,
        master_columns=master_columns
    )


def check_primary_index_expression(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否为主键表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.search("PRIMARY", "KEY")


def parse_primary_index_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLPrimaryIndexExpression:
    """解析主键表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    scanner.match("PRIMARY", "KEY")
    columns = [column_scanner.pop_as_source()
               for column_scanner in scanner.pop_as_children_scanner_list_split_by(",")]
    return SQLPrimaryIndexExpression(columns=columns)


def check_unique_index_expression(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否为唯一键表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.search("UNIQUE", "KEY")


def parse_unique_index_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLUniqueIndexExpression:
    """解析唯一键表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    scanner.match("UNIQUE", "KEY")
    name = scanner.pop_as_source()
    columns = [column_scanner.pop_as_source()
               for column_scanner in scanner.pop_as_children_scanner_list_split_by(",")]
    return SQLUniqueIndexExpression(name=name, columns=columns)


def check_normal_index_expression(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否为一般索引表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.search("KEY")


def parse_normal_index_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLNormalIndexExpression:
    """解析一般索引表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    scanner.match("KEY")
    name = scanner.pop_as_source()
    columns = [column_scanner.pop_as_source()
               for column_scanner in scanner.pop_as_children_scanner_list_split_by(",")]
    return SQLNormalIndexExpression(name=name, columns=columns)


def check_fulltext_expression(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否为全文索引表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.search("FULLTEXT", "KEY")


def parse_fulltext_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLFulltextIndexExpression:
    """解析全文索引表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    scanner.match("FULLTEXT", "KEY")
    name = scanner.pop_as_source()
    columns = [column_scanner.pop_as_source()
               for column_scanner in scanner.pop_as_children_scanner_list_split_by(",")]
    return SQLFulltextIndexExpression(name=name, columns=columns)


def parse_define_column_expression(scanner_or_string: Union[TokenScanner, str]) -> SQLDefineColumnExpression:
    """解析 DDL 的字段表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    # 解析顺序固定的信息
    column_name = scanner.pop_as_source()
    column_type = parse_column_type_expression(scanner)

    # 解析顺序可能不定的字段信息
    comment: Optional[str] = None
    is_unsigned: bool = False
    is_zerofill: bool = False
    character_set: Optional[str] = None
    collate: Optional[str] = None
    is_allow_null: bool = False
    is_not_null: bool = False
    is_auto_increment: bool = False
    default: Optional[SQLGeneralExpression] = None
    on_update: Optional[SQLGeneralExpression] = None
    while not scanner.is_finish:
        if scanner.search_and_move("NOT", "NULL"):
            is_not_null = True
        elif scanner.search_and_move("NULL"):
            is_allow_null = True
        elif scanner.search_and_move("CHARACTER", "SET"):
            character_set = scanner.pop_as_source()
        elif scanner.search_and_move("COLLATE"):
            collate = scanner.pop_as_source()
        elif scanner.search_and_move("DEFAULT"):
            default = parse_general_expression(scanner)
        elif scanner.search_and_move("COMMENT"):
            comment = scanner.pop_as_source()
        elif scanner.search_and_move("ON", "UPDATE"):  # ON UPDATE
            on_update = parse_general_expression(scanner)
        elif scanner.search_and_move("AUTO_INCREMENT"):
            is_auto_increment = True
        elif scanner.search_and_move("UNSIGNED"):
            is_unsigned = True
        elif scanner.search_and_move("ZEROFILL"):
            is_zerofill = True
        else:
            raise SqlParseError(f"无法解析的 DDL 字段表达式的字段属性: {scanner}")

    # 构造 DDL 字段表达式对象
    return SQLDefineColumnExpression(
        column_name=column_name,
        column_type=column_type,
        comment=comment,
        is_unsigned=is_unsigned,
        is_zerofill=is_zerofill,
        character_set=character_set,
        collate=collate,
        is_allow_null=is_allow_null,
        is_not_null=is_not_null,
        is_auto_increment=is_auto_increment,
        default=default,
        on_update=on_update
    )


def check_select_clause(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否为 SELECT 子句"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.search("SELECT")


def parse_select_clause(scanner_or_string: Union[TokenScanner, str]) -> SQLSelectClause:
    """解析 SELECT 子句"""
    scanner = _unify_input_scanner(scanner_or_string)
    scanner.match("SELECT")
    distinct = scanner.search_and_move("DISTINCT")
    columns = [parse_column_expression(scanner)]
    while not scanner.is_finish and scanner.now.is_comma:
        scanner.pop()
        columns.append(parse_column_expression(scanner))
    return SQLSelectClause(distinct=distinct, columns=columns)


def check_from_clause(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否为 FROM 子句"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.search("FROM")


def parse_from_clause(scanner_or_string: Union[TokenScanner, str]) -> SQLFromClause:
    """解析 FROM 子句"""
    scanner = _unify_input_scanner(scanner_or_string)
    scanner.match("FROM")
    tables = [parse_table_expression(scanner)]
    while not scanner.is_finish and scanner.now.is_comma:
        scanner.pop()
        tables.append(parse_table_expression(scanner))
    return SQLFromClause(tables=tables)


def check_lateral_view_clause(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否为 LATERAL VIEW 子句"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.search("LATERAL", "VIEW")


def parse_lateral_view_clause(scanner_or_string: Union[TokenScanner, str]) -> SQLLateralViewClause:
    """解析 LATERAL VIEW 子句"""
    scanner = _unify_input_scanner(scanner_or_string)
    scanner.match("LATERAL", "VIEW")
    function = parse_function_expression(scanner)
    view_name = scanner.pop_as_source()
    alias = parse_alias_expression(scanner)  # TODO 增加要求必须包含 AS
    return SQLLateralViewClause(function=function, view_name=view_name, alias=alias)


def check_join_clause(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否为 JOIN 子句"""
    scanner = _unify_input_scanner(scanner_or_string)
    return check_join_type(scanner)


def parse_join_clause(scanner_or_string: Union[TokenScanner, str]) -> SQLJoinClause:
    """解析 JOIN 子句"""
    scanner = _unify_input_scanner(scanner_or_string)
    join_type = parse_join_type(scanner)
    table_expression = parse_table_expression(scanner)
    if check_join_expression(scanner):
        join_rule = parse_join_expression(scanner)
    else:
        join_rule = None
    return SQLJoinClause(join_type=join_type, table=table_expression, join_rule=join_rule)


def check_where_clause(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否可能为 WHERE 子句"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.search("WHERE")


def parse_where_clause(scanner_or_string: Union[TokenScanner, str]) -> SQLWhereClause:
    """解析 WHERE 子句"""
    scanner = _unify_input_scanner(scanner_or_string)
    scanner.match("WHERE")
    return SQLWhereClause(condition=parse_condition_expression(scanner))


def check_group_by_clause(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否可能为 GROUP BY 子句"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.search("GROUP", "BY")


def parse_group_by_clause(scanner_or_string: Union[TokenScanner, str]) -> SQLGroupByClause:
    """解析 GROUP BY 子句"""
    scanner = _unify_input_scanner(scanner_or_string)
    scanner.match("GROUP", "BY")
    if scanner.search_and_move("GROUPING", "SETS"):
        # 处理 GROUPING SETS 的语法
        grouping_list = []
        for grouping_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            if grouping_scanner.now_is_parenthesis:
                parenthesis_scanner_list = grouping_scanner.pop_as_children_scanner_list_split_by(",")
                columns_list = [parse_general_expression(parenthesis_scanner)
                                for parenthesis_scanner in parenthesis_scanner_list]
                grouping_list.append(columns_list)
            else:
                grouping_list.append([parse_general_expression(grouping_scanner)])
        return SQLGroupingSetsGroupByClause(grouping_list=grouping_list)

    # 处理一般的 GROUP BY 的语法
    columns = [parse_general_expression(scanner)]
    while not scanner.is_finish and scanner.now.is_comma:
        scanner.pop()
        columns.append(parse_general_expression(scanner))
    with_rollup = False
    if scanner.search_and_move("WITH", "ROLLUP"):
        with_rollup = True
    return SQLNormalGroupByClause(columns=columns, with_rollup=with_rollup)


def check_having_clause(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """是否可能为 HAVING 子句"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.search("HAVING")


def parse_having_clause(scanner_or_string: Union[TokenScanner, str]) -> SQLHavingClause:
    """解析 HAVING 子句"""
    scanner = _unify_input_scanner(scanner_or_string)
    scanner.match("HAVING")
    return SQLHavingClause(condition=parse_condition_expression(scanner))


def check_order_by_clause(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """是否可能为 ORDER BY 子句"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.search("ORDER", "BY")


def parse_order_by_clause(scanner_or_string: Union[TokenScanner, str]) -> SQLOrderByClause:
    """解析 ORDER BY 子句"""
    scanner = _unify_input_scanner(scanner_or_string)

    def parse_single():
        column = parse_general_expression(scanner)
        order = parse_order_type(scanner)
        columns.append((column, order))

    scanner.match("ORDER", "BY")
    columns = []
    parse_single()
    while not scanner.is_finish and scanner.now.is_comma:
        scanner.pop()
        parse_single()

    return SQLOrderByClause(columns=columns)


def check_limit_clause(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """是否可能为 LIMIT 子句"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.search("LIMIT")


def parse_limit_clause(scanner_or_string: Union[TokenScanner, str]) -> SQLLimitClause:
    """解析 LIMIT 子句"""
    scanner = _unify_input_scanner(scanner_or_string)
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


def _parse_single_with_table(scanner_or_string: Union[TokenScanner, str]) -> Tuple[str, SQLSelectStatement]:
    """解析一个 WITH 临时表"""
    scanner = _unify_input_scanner(scanner_or_string)
    table_name = scanner.pop_as_source()
    scanner.match("AS")
    table_statement = parse_select_statement(scanner.pop_as_children_scanner(), with_clause=SQLWithClause.empty())
    return table_name, table_statement


def parse_with_clause(scanner_or_string: Union[TokenScanner, str]) -> Optional[SQLWithClause]:
    """解析 WITH 子句"""
    scanner = _unify_input_scanner(scanner_or_string)
    if scanner.search_and_move("WITH"):
        tables = [_parse_single_with_table(scanner)]
        while scanner.search_and_move(","):
            table_statement = _parse_single_with_table(scanner)
            tables.append(table_statement)  # 将前置的 WITH 作为当前解析临时表的 WITH 子句
        return SQLWithClause(tables=tables)
    return SQLWithClause.empty()


def check_select_statement(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否可能为 SELECT 语句"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.search("SELECT")


def parse_single_select_statement(scanner_or_string: Union[TokenScanner, str],
                                  with_clause: Optional[SQLWithClause] = None
                                  ) -> SQLSingleSelectStatement:
    """

    Parameters
    ----------
    scanner_or_string : Union[TokenScanner, str]
        扫描器
    with_clause : Optional[SQLWithClause], default = None
        前置 with 语句，如果该参数为 None 的话，则会尝试匹配 WITH 语句

    Returns
    -------

    """
    scanner = _unify_input_scanner(scanner_or_string)
    if with_clause is None:
        with_clause = parse_with_clause(scanner)
    select_clause = parse_select_clause(scanner)
    from_clause = parse_from_clause(scanner) if check_from_clause(scanner) else None
    lateral_view_clauses = []
    while check_lateral_view_clause(scanner):
        lateral_view_clauses.append(parse_lateral_view_clause(scanner))
    join_clause = []
    while check_join_clause(scanner):
        join_clause.append(parse_join_clause(scanner))
    where_clause = parse_where_clause(scanner) if check_where_clause(scanner) else None
    group_by_clause = parse_group_by_clause(scanner) if check_group_by_clause(scanner) else None
    having_clause = parse_having_clause(scanner) if check_having_clause(scanner) else None
    order_by_clause = parse_order_by_clause(scanner) if check_order_by_clause(scanner) else None
    limit_clause = parse_limit_clause(scanner) if check_limit_clause(scanner) else None
    return SQLSingleSelectStatement(
        with_clause=with_clause,
        select_clause=select_clause,
        from_clause=from_clause,
        lateral_view_clauses=lateral_view_clauses,
        join_clauses=join_clause,
        where_clause=where_clause,
        group_by_clause=group_by_clause,
        having_clause=having_clause,
        order_by_clause=order_by_clause,
        limit_clause=limit_clause
    )


def parse_select_statement(scanner_or_string: Union[TokenScanner, str],
                           with_clause: Optional[SQLWithClause] = None) -> SQLSelectStatement:
    """解析 SELECT 语句"""
    scanner = _unify_input_scanner(scanner_or_string)
    if with_clause is None:
        with_clause = parse_with_clause(scanner)
    result = [parse_single_select_statement(scanner, with_clause=with_clause)]
    while not scanner.is_finish and check_union_type(scanner):
        result.append(parse_union_type(scanner))
        result.append(parse_single_select_statement(scanner, with_clause=with_clause))
    scanner.search_and_move(";")
    if not scanner.is_finish:
        raise SqlParseError(f"没有解析完成: {scanner}")

    if len(result) == 1:
        return result[0]
    return SQLUnionSelectStatement(with_clause=with_clause, elements=result)


def check_insert_statement(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否为 INSERT 语句（已匹配过 WITH 语句才可以调用）"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.search("INSERT")


def parse_insert_statement(scanner_or_string: Union[TokenScanner, str],
                           with_clause: SQLWithClause) -> SQLInsertStatement:
    """解析 INSERT 表达式"""
    scanner = _unify_input_scanner(scanner_or_string)
    insert_type = parse_insert_type(scanner)

    # 匹配可能包含的 TABLE 关键字
    scanner.search_and_move("TABLE")

    # 匹配表名
    table_name = parse_table_name_expression(scanner)

    # 匹配分区表达式
    if check_partition_expression(scanner):
        partition = parse_partition_expression(scanner)
    else:
        partition = None

    # 匹配列名列表
    if scanner.now_is_parenthesis:
        columns = []
        for column_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            columns.append(parse_column_name_expression(column_scanner))
            if not column_scanner.is_finish:
                raise SqlParseError(f"未解析完成的列名: {column_scanner}")
    else:
        columns = None

    # 匹配 VALUES 类型
    if scanner.search_and_move("VALUES"):
        values = []
        while scanner.now_is_parenthesis:
            values.append(parse_value_expression(scanner))
            scanner.search_and_move(",")

        return SQLInsertValuesStatement(
            with_clause=with_clause,
            insert_type=insert_type,
            table_name=table_name,
            partition=partition,
            columns=columns,
            values=values
        )

    if scanner.search("SELECT"):
        select_statement = parse_select_statement(scanner, with_clause=SQLWithClause.empty())
        return SQLInsertSelectStatement(
            with_clause=with_clause,
            insert_type=insert_type,
            table_name=table_name,
            partition=partition,
            columns=columns,
            select_statement=select_statement
        )

    raise SqlParseError(f"未知的 INSERT 语句类型 {scanner}")


def check_set_statement(scanner_or_string: Union[TokenScanner, str]) -> bool:
    """判断是否为 SET 语句"""
    scanner = _unify_input_scanner(scanner_or_string)
    return scanner.search("SET")


def parse_set_statement(scanner_or_string: Union[TokenScanner, str]) -> SQLSetStatement:
    """解析 SET 语句"""
    scanner = _unify_input_scanner(scanner_or_string)
    scanner.match("SET")
    config_name = parse_config_name_expression(scanner)
    scanner.match("=")
    config_value = parse_config_value_expression(scanner)
    return SQLSetStatement(config_name=config_name, config_value=config_value)


def parse_create_table_statement(scanner_or_string: Union[TokenScanner, str]) -> SQLCreateTableStatement:
    """解析 CREATE TABLE 语句"""
    # 解析字段、索引括号前的部分
    scanner = _unify_input_scanner(scanner_or_string)
    scanner.match("CREATE", "TABLE")
    if_not_exists = scanner.search_and_move("IF", "NOT", "EXISTS")
    table_name_expression = parse_table_name_expression(scanner)

    # 解析字段和索引
    columns: List[SQLDefineColumnExpression] = []
    primary_key: Optional[SQLPrimaryIndexExpression] = None
    unique_key: List[SQLUniqueIndexExpression] = []
    key: List[SQLNormalIndexExpression] = []
    fulltext_key: List[SQLFulltextIndexExpression] = []
    foreign_key: List[SQLForeignKeyExpression] = []
    for group_scanner in scanner.pop_as_children_scanner_list_split_by(","):
        if check_primary_index_expression(group_scanner):
            primary_key = parse_primary_index_expression(group_scanner)
        elif check_unique_index_expression(group_scanner):
            unique_key.append(parse_unique_index_expression(group_scanner))
        elif check_normal_index_expression(group_scanner):
            key.append(parse_normal_index_expression(group_scanner))
        elif check_fulltext_expression(group_scanner):
            fulltext_key.append(parse_fulltext_expression(group_scanner))
        elif check_foreign_key_expression(group_scanner):
            foreign_key.append(parse_foreign_key_expression(group_scanner))
        else:
            columns.append(parse_define_column_expression(group_scanner))

    # 解析表属性
    comment: Optional[str] = None
    engine: Optional[str] = None
    auto_increment: Optional[int] = None
    default_charset: Optional[str] = None
    collate: Optional[str] = None
    row_format: Optional[str] = None
    states_persistent: Optional[str] = None
    while not scanner.is_finish:
        if scanner.search_and_move("ENGINE"):
            scanner.search_and_move("=")
            engine = scanner.pop_as_source()
        elif scanner.search_and_move("AUTO_INCREMENT"):
            scanner.match("=")
            auto_increment = int(scanner.pop_as_source())
        elif scanner.search_and_move("DEFAULT", "CHARSET"):
            scanner.match("=")
            default_charset = scanner.pop_as_source()
        elif scanner.search_and_move("ROW_FORMAT"):
            scanner.match("=")
            row_format = scanner.pop_as_source()
        elif scanner.search_and_move("COLLATE"):
            scanner.match("=")
            collate = scanner.pop_as_source()
        elif scanner.search_and_move("COMMENT"):
            scanner.match("=")
            comment = scanner.pop_as_source()
        elif scanner.search_and_move("STATS_PERSISTENT"):
            scanner.match("=")
            states_persistent = scanner.pop_as_source()
        else:
            raise SqlParseError(f"未知的 DDL 表属性: {scanner}")
    scanner.search_and_move(";")

    return SQLCreateTableStatement(
        table_name_expression=table_name_expression,
        comment=comment,
        if_not_exists=if_not_exists,
        columns=columns,
        primary_key=primary_key,
        unique_key=unique_key,
        key=key,
        fulltext_key=fulltext_key,
        foreign_key=foreign_key,
        engine=engine,
        auto_increment=auto_increment,
        default_charset=default_charset,
        collate=collate,
        row_format=row_format,
        states_persistent=states_persistent
    )


def parse_statements(scanner_or_string: Union[TokenScanner, str]) -> List[SQLStatement]:
    """解析一段 SQL 语句，返回表达式的列表"""
    scanner = _unify_input_scanner(scanner_or_string)
    statement_list = []
    for statement_scanner in scanner.split_by(";"):
        # 解析 SET 语句
        if check_set_statement(statement_scanner):
            statement_list.append(parse_set_statement(statement_scanner))
            continue

        # 先尝试解析 WITH 语句
        with_clause = parse_with_clause(statement_scanner)

        if check_select_statement(statement_scanner):
            statement_list.append(parse_select_statement(statement_scanner, with_clause=with_clause))
        elif check_insert_statement(statement_scanner):
            statement_list.append(parse_insert_statement(statement_scanner, with_clause=with_clause))
        else:
            raise SqlParseError(f"未知语句类型: {statement_scanner}")

    return statement_list
