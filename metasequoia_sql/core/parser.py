# pylint: disable=C0302

"""
基础元素的解析逻辑

因为不同解析函数之间需要相互调用，所以脚本文件不可避免地需要超过 1000 行，故忽略 pylint C0302。

TODO 使用 search 替代直接使用 now 判断
TODO 将 CAST_DATA_TYPE 提出作为一个基础类型节点
TODO 将 function_name 提出作为一个专有表达式
TODO 清理只调用一次的单行函数
TODO 将 CURRENT_TIMESTAMP、CURRENT_DATE、CURRENT_TIME 改为单独节点处理
"""

from typing import Optional, Tuple, List, Union

from metasequoia_sql.lexical import (AMTBase, AMTMark, AMTBaseSingle, AMTLiteralInteger, AMTLiteralFloat, AMTLiteralString,
                                     AMTLiteralHex, AMTLiteralBool, AMTLiteralBit, AMTLiteralNull, ASTParser)
from metasequoia_sql.common import TokenScanner
from metasequoia_sql.core.objects import *
from metasequoia_sql.core.static import AGGREGATION_FUNCTION_NAME_SET, WINDOW_FUNCTION_NAME_SET
from metasequoia_sql.errors import SqlParseError

__all__ = ["SQLParser"]


class SQLParser:
    # pylint: disable=R0904 忽略类中包含过多共有方法的问题

    """SQL语法解析器

    如需替换词法解析器，重写 build_token_scanner 方法即可
    """

    @classmethod
    def build_token_scanner(cls, string: str) -> TokenScanner:
        """构造词法扫描器"""
        context_automaton = ASTParser(string)
        context_automaton.parse()
        return TokenScanner(context_automaton.result(), ignore_space=True, ignore_comment=True)

    @classmethod
    def _unify_input_scanner(cls, scanner_or_string: Union[TokenScanner, str]) -> TokenScanner:
        """格式化输入的参数，将字符串格式的 SQL 语句统一为词法扫描器 TokenScanner"""
        if isinstance(scanner_or_string, TokenScanner):
            return scanner_or_string
        if isinstance(scanner_or_string, str):
            # 兼容 DB2 的 CURRENT DATE、CURRENT TIME、CURRENT TIMESTAMP 语法
            scanner_or_string = scanner_or_string.replace("CURRENT DATE", "CURRENT_DATE")
            scanner_or_string = scanner_or_string.replace("CURRENT TIME", "CURRENT_TIME")
            scanner_or_string = scanner_or_string.replace("CURRENT TIMESTAMP", "CURRENT_TIMESTAMP")
            return cls.build_token_scanner(scanner_or_string)
        raise SqlParseError(f"未知的参数类型: {scanner_or_string} (type={type(scanner_or_string)})")

    @classmethod
    def _unify_name(cls, string: Optional[str]) -> Optional[str]:
        """格式化名称标识符：统一剔除当前引号并添加引号"""
        if string is not None:
            return string.strip("`")
        return None

    @classmethod
    def check_insert_type(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为插入类型"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search_and_move("INSERT", "INTO") or scanner.search_and_move("INSERT", "OVERWRITE")

    @classmethod
    def parse_insert_type(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTInsertType:
        """解析插入类型"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if scanner.search_and_move("INSERT", "INTO"):
            return ASTInsertType(insert_type=EnumInsertType.INSERT_INTO)
        if scanner.search_and_move("INSERT", "OVERWRITE"):
            return ASTInsertType(insert_type=EnumInsertType.INSERT_OVERWRITE)
        raise SqlParseError(f"未知的 INSERT 类型: {scanner}")

    @classmethod
    def check_join_type(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为关联类型"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        for join_type in EnumJoinType:
            if scanner.search(*join_type.value):
                return True
        return False

    @classmethod
    def parse_join_type(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTJoinType:
        """解析关联类型"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        for join_type in EnumJoinType:
            if scanner.search_and_move(*join_type.value):
                return ASTJoinType(join_type=join_type)
        raise SqlParseError(f"无法解析的关联类型: {scanner}")

    @classmethod
    def check_order_type(cls) -> bool:
        """判断是否为排序类型：任何元素都可以是排序类型（省略升序），所以均返回 True"""
        return True

    @classmethod
    def parse_order_type(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTOrderType:
        """解析排序类型"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if scanner.search_and_move("DESC"):
            return ASTOrderType(order_type=EnumOrderType.DESC)
        if scanner.search_and_move("ASC"):
            return ASTOrderType(order_type=EnumOrderType.ASC)
        return ASTOrderType(order_type=EnumOrderType.ASC)

    @classmethod
    def check_union_type(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为组合类型"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        for union_type in EnumUnionType:
            if scanner.search(*union_type.value):
                return True
        return False

    @classmethod
    def parse_union_type(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTUnionType:
        """解析组合类型"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        for union_type in EnumUnionType:
            if scanner.search_and_move(*union_type.value):
                return ASTUnionType(union_type=union_type)
        raise SqlParseError(f"无法解析的组合类型: {scanner}")

    @classmethod
    def check_compare_operator(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为比较运算符"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.get_as_source() in {"=", "!=", "<>", "<", "<=", ">", ">="}

    @classmethod
    def parse_compare_operator(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTCompareOperator:
        """解析比较运算符"""
        scanner = cls._unify_input_scanner(scanner_or_string)
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
            return ASTCompareOperator(compare_operator=compare_operator)
        raise SqlParseError(f"无法解析的比较运算符: {scanner}")

    @classmethod
    def check_compute_operator(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为计算运算符"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        for compute_operator in EnumComputeOperator:
            if scanner.search(compute_operator.value):
                return True
        return False

    @classmethod
    def parse_compute_operator(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTComputeOperator:
        """解析计算运算符"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        for compute_operator in EnumComputeOperator:
            if scanner.search_and_move(compute_operator.value):
                return ASTComputeOperator(compute_operator=compute_operator)
        raise SqlParseError(f"无法解析的计算运算符: {scanner}")

    @classmethod
    def check_logical_operator(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为逻辑运算符"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.get_as_source() in {"AND", "OR"}

    @classmethod
    def parse_logical_operator(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTLogicalOperator:
        """解析逻辑运算符"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        for logical_operator in EnumLogicalOperator:
            if scanner.search_and_move(logical_operator.value):
                return ASTLogicalOperator(logical_operator=logical_operator)
        raise SqlParseError(f"无法解析的逻辑运算符: {scanner}")

    @classmethod
    def check_literal_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为字面值：包含整型字面值、浮点型字面值、字符串型字面值、十六进制型字面值、布尔型字面值、位值型字面值、空值的字面值"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search(AMTMark.LITERAL) or scanner.search("-")

    @classmethod
    def parse_literal_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTLiteralExpression:
        """解析字面值：包含整型字面值、浮点型字面值、字符串型字面值、十六进制型字面值、布尔型字面值、位值型字面值、空值的字面值"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        token: AMTBase = scanner.pop()
        if isinstance(token, AMTLiteralInteger):
            return ASTLiteralIntegerExpression(value=token.literal_value)
        if isinstance(token, AMTLiteralFloat):
            return ASTLiteralFloatExpression(value=token.literal_value)
        if isinstance(token, AMTLiteralString):
            return ASTLiteralStringExpression(value=token.literal_value)
        if isinstance(token, AMTLiteralHex):
            return ASTLiteralHexExpression(value=token.literal_value)
        if isinstance(token, AMTLiteralBool):
            return ASTLiteralBoolExpression(value=token.literal_value)
        if isinstance(token, AMTLiteralBit):
            return ASTLiteralBitExpression(value=token.literal_value)
        if isinstance(token, AMTLiteralNull):
            return ASTLiteralNullExpression()
        if token.equals("-") and isinstance(scanner.now, AMTLiteralInteger):
            next_token = scanner.pop()
            return ASTLiteralIntegerExpression(value=-next_token.literal_value)
        if token.equals("-") and isinstance(scanner.now, AMTLiteralFloat):
            next_token = scanner.pop()
            return ASTLiteralFloatExpression(value=-next_token.literal_value)
        raise SqlParseError(f"未知的字面值: {token}")

    @classmethod
    def check_column_name_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """是否可能为列名表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return not scanner.is_finish and (
                (scanner.now.equals(AMTMark.NAME) and
                 (scanner.next1 is None or (
                         not scanner.next1.equals(".") and not scanner.next1.equals(AMTMark.PARENTHESIS)))) or
                (scanner.now.equals(AMTMark.NAME) and
                 scanner.next1 is not None and scanner.next1.equals(".") and
                 scanner.next2 is not None and scanner.next2.equals(AMTMark.NAME) and
                 (scanner.next3 is None or not scanner.next3.equals(AMTMark.PARENTHESIS)))
        )

    @classmethod
    def parse_column_name_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTColumnNameExpression:
        """解析列名表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if (scanner.search(AMTMark.NAME, ".", AMTMark.NAME) and
                not scanner.search(AMTMark.NAME, ".", AMTMark.NAME, AMTMark.PARENTHESIS)):
            table_name = scanner.pop_as_source()
            scanner.pop()
            column_name = scanner.pop_as_source()
            return ASTColumnNameExpression(table=cls._unify_name(table_name), column=cls._unify_name(column_name))
        if scanner.search(AMTMark.NAME) and not scanner.search(AMTMark.NAME, AMTMark.PARENTHESIS):
            return ASTColumnNameExpression(column=cls._unify_name(scanner.pop_as_source()))
        raise SqlParseError(f"无法解析为表名表达式: {scanner}")

    @classmethod
    def check_function_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """是否可能为函数表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return (scanner.search(AMTMark.NAME, AMTMark.PARENTHESIS) or
                scanner.search(AMTMark.NAME, ".", AMTMark.NAME, AMTMark.PARENTHESIS))

    @classmethod
    def parse_cast_data_type(cls, scanner_or_string: Union[TokenScanner, str]) -> EnumCastDataType:
        """解析 CAST 函数表达式中的类型"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        for cast_type in EnumCastDataType:
            if scanner.search_and_move(cast_type.value):
                return cast_type
        raise SqlParseError(f"无法解析的 CAST 函数表达式中的类型: {scanner}")

    @classmethod
    def parse_cast_function_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTCastFunctionExpression:
        """解析 CAST 函数表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        column_expression = cls.parse_general_expression(scanner)
        scanner.match("AS")
        signed = scanner.search_and_move("SIGNED")
        cast_type = cls.parse_cast_data_type(scanner)
        if scanner.search(AMTMark.PARENTHESIS):
            parenthesis_scanner = scanner.pop_as_children_scanner()
            cast_params: Optional[List[ASTGeneralExpression] | Tuple[ASTGeneralExpression, ...]] = []
            for param_scanner in parenthesis_scanner.split_by(","):
                cast_params.append(cls.parse_general_expression(param_scanner))
                param_scanner.close()
            cast_params = tuple(cast_params)
        else:
            cast_params = None
        scanner.close()
        cast_data_type = ASTCastDataType(signed=signed, data_type=cast_type, params=cast_params)
        return ASTCastFunctionExpression(column_expression=column_expression, cast_type=cast_data_type)

    @classmethod
    def parse_extract_function_expression(cls,
                                          scanner_or_string: Union[TokenScanner, str]) -> ASTExtractFunctionExpression:
        """解析 EXTRACT 函数表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        extract_name = cls.parse_general_expression(scanner)
        scanner.match("FROM")
        column_expression = cls.parse_general_expression(scanner)
        scanner.close()
        return ASTExtractFunctionExpression(extract_name=extract_name, column_expression=column_expression)

    @classmethod
    def parse_if_function_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTNormalFunctionExpression:
        """解析 IF 函数表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        function_params: List[ASTGeneralExpression] = []
        first_param = True
        for param_scanner in scanner.split_by(","):
            if first_param is True:
                function_params.append(cls.parse_condition_expression(param_scanner))
                first_param = False
            else:
                function_params.append(cls.parse_general_expression(param_scanner))
            param_scanner.close()
        return ASTNormalFunctionExpression(function_name="IF", function_params=tuple(function_params))

    @classmethod
    def parse_function_name(cls, scanner_or_string: Union[TokenScanner, str]) -> Tuple[Optional[str], str]:
        """解析函数表达式函数的 schema 名和 function 名"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if scanner.search(AMTMark.NAME, AMTMark.PARENTHESIS):
            return None, scanner.pop_as_source()
        if scanner.search(AMTMark.NAME, ".", AMTMark.NAME, AMTMark.PARENTHESIS):
            schema_name = scanner.pop_as_source()
            scanner.pop()
            return cls._unify_name(schema_name), cls._unify_name(scanner.pop_as_source())
        raise SqlParseError(f"无法解析为函数表达式: {scanner}")

    @classmethod
    def parse_function_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> Union[ASTFunctionExpression]:
        """解析函数表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        schema_name, function_name = cls.parse_function_name(scanner)

        if function_name.upper() == "CAST":
            return cls.parse_cast_function_expression(scanner.pop_as_children_scanner())
        if function_name.upper() == "EXTRACT":
            return cls.parse_extract_function_expression(scanner.pop_as_children_scanner())
        if function_name.upper() == "IF":
            return cls.parse_if_function_expression(scanner.pop_as_children_scanner())

        parenthesis_scanner = scanner.pop_as_children_scanner()
        if function_name.upper() == "SUBSTRING":
            # 将 MySQL 和 PostgreSQL 中的 "SUBSTRING(str1 FROM 3 FOR 2)" 格式化为 "SUBSTRING(str1, 3, 2)"
            parenthesis_scanner = TokenScanner([
                element if not element.equals("FROM") and not element.equals("FOR") else AMTBaseSingle(",")
                for element in parenthesis_scanner.elements])

        is_distinct = False
        if function_name.upper() in AGGREGATION_FUNCTION_NAME_SET and parenthesis_scanner.search_and_move("DISTINCT"):
            is_distinct = True

        function_params: List[ASTGeneralExpression] = []
        for param_scanner in parenthesis_scanner.split_by(","):
            function_params.append(cls.parse_general_expression(param_scanner))
            if not param_scanner.is_finish:
                raise SqlParseError(f"无法解析函数参数: {param_scanner}")

        parenthesis_scanner.close()

        if schema_name is None and function_name.upper() in AGGREGATION_FUNCTION_NAME_SET:
            return ASTAggregationFunctionExpression(function_name=function_name,
                                                    function_params=tuple(function_params),
                                                    is_distinct=is_distinct)
        return ASTNormalFunctionExpression(schema_name=schema_name, function_name=function_name,
                                           function_params=tuple(function_params))

    @classmethod
    def parse_function_expression_maybe_with_array_index(
            cls, scanner_or_string: Union[TokenScanner, str]
    ) -> Union[ASTFunctionExpression, ASTArrayIndexExpression]:
        """解析函数表达式，并解析函数表达式后可能包含的数组下标"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        array_expression = cls.parse_function_expression(scanner)
        if scanner.is_finish or not scanner.search(AMTMark.ARRAY_INDEX):
            return array_expression
        idx = int(scanner.pop_as_source().lstrip("[").rstrip("]"))
        return ASTArrayIndexExpression(array_expression=array_expression, idx=idx)

    @classmethod
    def parse_bool_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTBoolExpression:
        """解析布尔值表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        is_not = scanner.search_and_move("NOT")
        if scanner.search_and_move("EXISTS"):
            after_value = cls.parse_sub_query_expression(scanner)
            return ASTBoolExistsExpression(is_not=is_not, after_value=after_value)
        before_value = cls.parse_general_expression(scanner)
        is_not = is_not or scanner.search_and_move("NOT")
        if scanner.search_and_move("BETWEEN"):  # "... BETWEEN ... AND ..."
            from_value = cls.parse_general_expression(scanner)
            scanner.match("AND")
            to_value = cls.parse_general_expression(scanner)
            return ASTBoolBetweenExpression(is_not=is_not, before_value=before_value, from_value=from_value,
                                            to_value=to_value)
        if scanner.search_and_move("IS"):  # ".... IS ...." 或 "... IS NOT ..."
            is_not = is_not or scanner.search_and_move("NOT")
            after_value = cls.parse_general_expression(scanner)
            return ASTBoolIsExpression(is_not=is_not, before_value=before_value, after_value=after_value)
        if scanner.search_and_move("IN"):  # "... IN (1, 2, 3)" 或 "... IN (SELECT ... )"
            after_value = cls._parse_in_parenthesis(scanner)
            return ASTBoolInExpression(is_not=is_not, before_value=before_value, after_value=after_value)
        if scanner.search_and_move("LIKE"):
            after_value = cls.parse_general_expression(scanner)
            return ASTBoolLikeExpression(is_not=is_not, before_value=before_value, after_value=after_value)
        if cls.check_compare_operator(scanner):  # "... > ..."
            compare_operator = cls.parse_compare_operator(scanner)
            after_value = cls.parse_general_expression(scanner)
            return ASTBoolCompareExpression(is_not=is_not, operator=compare_operator, before_value=before_value,
                                            after_value=after_value)
        raise SqlParseError(f"无法解析为布尔值表达式: {scanner}")

    @classmethod
    def check_window_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否可能为窗口函数"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return not scanner.is_finish and (
                scanner.now.equals(AMTMark.NAME) and scanner.now.source.upper() in WINDOW_FUNCTION_NAME_SET and
                scanner.next1 is not None and scanner.next1.equals(AMTMark.PARENTHESIS) and
                scanner.next2 is not None and scanner.next2.equals("OVER") and
                scanner.next3 is not None and scanner.next3.equals(AMTMark.PARENTHESIS))

    @classmethod
    def parse_window_row(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTWindowRow:
        """解析窗口函数行限制中的行"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if scanner.search_and_move("CURRENT", "ROW"):
            return ASTWindowRow(row_type=EnumWindowRowType.CURRENT_ROW)
        if scanner.search_and_move("UNBOUNDED"):
            if scanner.search_and_move("PRECEDING"):
                return ASTWindowRow(row_type=EnumWindowRowType.PRECEDING, is_unbounded=True)
            if scanner.search_and_move("FOLLOWING"):
                return ASTWindowRow(row_type=EnumWindowRowType.FOLLOWING, is_unbounded=True)
            raise SqlParseError(f"无法解析的窗口函数限制行: {scanner}")
        row_num = int(scanner.pop_as_source())
        if scanner.search_and_move("PRECEDING"):
            return ASTWindowRow(row_type=EnumWindowRowType.PRECEDING, row_num=row_num)
        if scanner.search_and_move("FOLLOWING"):
            return ASTWindowRow(row_type=EnumWindowRowType.FOLLOWING, row_num=row_num)
        raise SqlParseError(f"无法解析的窗口函数限制行: {scanner}")

    @classmethod
    def parse_window_row_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTWindowRowExpression:
        """解析窗口语句限制行的表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("ROWS", "BETWEEN")
        from_row = cls.parse_window_row(scanner)
        scanner.match("AND")
        to_row = cls.parse_window_row(scanner)
        return ASTWindowRowExpression(from_row=from_row, to_row=to_row)

    @classmethod
    def parse_window_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTWindowExpression:
        """解析窗口函数"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        window_function = cls.parse_function_expression_maybe_with_array_index(scanner)
        partition_by = None
        order_by = None
        row_expression = None
        scanner.match("OVER")
        parenthesis_scanner = scanner.pop_as_children_scanner()
        if parenthesis_scanner.search_and_move("PARTITION", "BY"):
            partition_by = cls.parse_general_expression(parenthesis_scanner, maybe_window=False)
        if parenthesis_scanner.search_and_move("ORDER", "BY"):
            order_by = cls.parse_general_expression(parenthesis_scanner, maybe_window=False)
        if parenthesis_scanner.search("ROWS", "BETWEEN"):
            row_expression = cls.parse_window_row_expression(parenthesis_scanner)
        parenthesis_scanner.close()
        return ASTWindowExpression(window_function=window_function,
                                   partition_by=partition_by,
                                   order_by=order_by,
                                   row_expression=row_expression)

    @classmethod
    def check_wildcard_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否可能为通配符表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("*") or scanner.search(AMTMark.NAME, ".", "*")

    @classmethod
    def parse_wildcard_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTWildcardExpression:
        """解析通配符表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if scanner.search_and_move("*"):
            return ASTWildcardExpression()
        if scanner.search(AMTMark.NAME, ".", "*"):
            schema_name = scanner.pop_as_source()
            scanner.pop()
            scanner.pop()
            return ASTWildcardExpression(schema=schema_name)
        raise SqlParseError("无法解析为通配符表达式")

    @classmethod
    def parse_condition_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTConditionExpression:
        """解析条件表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)

        def parse_single():
            if scanner.search(AMTMark.PARENTHESIS):
                parenthesis_scanner = scanner.pop_as_children_scanner()
                elements.append(cls.parse_condition_expression(parenthesis_scanner))  # 插入语，子句也应该是一个条件表达式
                parenthesis_scanner.close()
            else:
                elements.append(cls.parse_bool_expression(scanner))

        elements: List[Union["ASTConditionExpression", ASTBoolExpression, ASTLogicalOperator]] = []
        parse_single()  # 解析第 1 个表达式元素
        while not scanner.is_finish and scanner.now.source.upper() in {"AND", "OR"}:  # 如果是用 AND 和 OR 连接的多个表达式，则继续解析
            elements.append(cls.parse_logical_operator(scanner))
            parse_single()

        return ASTConditionExpression(elements=tuple(elements))

    @classmethod
    def check_case_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否可能为 CASE 表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("CASE")

    @classmethod
    def parse_case_expression(cls, scanner_or_string: Union[TokenScanner, str]
                              ) -> Union[ASTCaseExpression, ASTCaseValueExpression]:
        """解析 CASE 表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("CASE")
        if scanner.search("WHEN"):
            # 第 1 种格式的 CASE 表达式
            cases = []
            else_value = None
            while scanner.search_and_move("WHEN"):
                when_expression = cls.parse_condition_expression(scanner)
                scanner.match("THEN")
                case_expression = cls.parse_general_expression(scanner)
                cases.append((when_expression, case_expression))
            if scanner.search_and_move("ELSE"):
                else_value = cls.parse_general_expression(scanner)
            scanner.match("END")
            return ASTCaseExpression(cases=tuple(cases), else_value=else_value)
        # 第 2 种格式的 CASE 表达式
        case_value = cls.parse_general_expression(scanner)
        cases = []
        else_value = None
        while scanner.search_and_move("WHEN"):
            when_expression = cls.parse_general_expression(scanner)
            scanner.match("THEN")
            case_expression = cls.parse_general_expression(scanner)
            cases.append((when_expression, case_expression))
        if scanner.search_and_move("ELSE"):
            else_value = cls.parse_general_expression(scanner)
        scanner.match("END")
        return ASTCaseValueExpression(case_value=case_value, cases=tuple(cases), else_value=else_value)

    @classmethod
    def parse_value_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTValueExpression:
        """解析值表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        values = []
        for value_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            values.append(cls.parse_general_expression(value_scanner))
            value_scanner.close()
        return ASTValueExpression(values=tuple(values))

    @classmethod
    def check_sub_query_parenthesis(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为子查询的插入语"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return cls.check_select_statement(scanner.get_as_children_scanner())

    @classmethod
    def parse_sub_query_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTSubQueryExpression:
        """解析子查询表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        parenthesis_scanner = scanner.pop_as_children_scanner()
        result = ASTSubQueryExpression(select_statement=cls.parse_select_statement(parenthesis_scanner))
        parenthesis_scanner.close()
        return result

    @classmethod
    def _parse_in_parenthesis(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTGeneralExpression:
        """解析 IN 关键字后的插入语：插入语可能为子查询或值表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if cls.check_sub_query_parenthesis(scanner):
            return cls.parse_sub_query_expression(scanner)
        return cls.parse_value_expression(scanner)

    @classmethod
    def _parse_general_parenthesis(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTGeneralExpression:
        """解析一般表达式中的插入语：插入语可能为一般表达式或子查询"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if cls.check_sub_query_parenthesis(scanner):
            return cls.parse_sub_query_expression(scanner)
        parenthesis_scanner = scanner.pop_as_children_scanner()
        result = cls.parse_general_expression(parenthesis_scanner)
        parenthesis_scanner.close()
        return result

    @classmethod
    def parse_general_expression_element(cls, scanner_or_string: Union[TokenScanner, str],
                                         maybe_window: bool) -> ASTGeneralExpression:
        """解析一般表达式中的一个元素"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if cls.check_case_expression(scanner):
            return cls.parse_case_expression(scanner)
        if maybe_window is True and cls.check_window_expression(scanner):
            return cls.parse_window_expression(scanner)
        if cls.check_function_expression(scanner):
            return cls.parse_function_expression_maybe_with_array_index(scanner)
        if cls.check_literal_expression(scanner):
            return cls.parse_literal_expression(scanner)
        if cls.check_column_name_expression(scanner):
            return cls.parse_column_name_expression(scanner)
        if scanner.search(AMTMark.PARENTHESIS):
            return cls._parse_general_parenthesis(scanner)
        if cls.check_wildcard_expression(scanner):
            return cls.parse_wildcard_expression(scanner)
        raise SqlParseError(f"未知的一般表达式元素: {scanner}")

    @classmethod
    def parse_general_expression(cls, scanner_or_string: Union[TokenScanner, str],
                                 maybe_window: bool = True) -> ASTGeneralExpression:
        """解析一般表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        elements = [cls.parse_general_expression_element(scanner, maybe_window)]
        while cls.check_compute_operator(scanner):
            elements.append(cls.parse_compute_operator(scanner))
            elements.append(cls.parse_general_expression_element(scanner, maybe_window))
        if len(elements) == 1:
            return elements[0]  # 如果只有 1 个元素，则返回该元素的表达式
        return ASTComputeExpression(elements=tuple(elements))  # 如果超过 1 个元素，则返回计算表达式（多项式）

    @classmethod
    def parse_config_name_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTConfigNameExpression:
        """解析配置名称表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        config_name_list = [scanner.pop_as_source()]
        while scanner.search_and_move("."):
            config_name_list.append(scanner.pop_as_source())
        return ASTConfigNameExpression(config_name=".".join(config_name_list))

    @classmethod
    def parse_config_value_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTConfigValueExpression:
        """解析配置值表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return ASTConfigValueExpression(config_value=scanner.pop_as_source())

    @classmethod
    def parse_table_name_expression(cls, scanner_or_string: Union[TokenScanner, str]
                                    ) -> Union[ASTTableNameExpression, ASTSubQueryExpression]:
        """解析表名表达式或子查询表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if scanner.search(AMTMark.NAME, ".", AMTMark.NAME):
            schema_name = scanner.pop_as_source()
            scanner.pop()
            table_name = scanner.pop_as_source()
            return ASTTableNameExpression(schema=cls._unify_name(schema_name), table=cls._unify_name(table_name))
        if scanner.search(AMTMark.NAME):
            name_source = scanner.pop_as_source()
            if name_source.count(".") == 1:
                schema_name, table_name = name_source.strip("`").split(".")
            else:
                schema_name, table_name = None, name_source
            return ASTTableNameExpression(schema=cls._unify_name(schema_name), table=cls._unify_name(table_name))
        if cls.check_sub_query_parenthesis(scanner):
            return cls.parse_sub_query_expression(scanner)
        raise SqlParseError(f"无法解析为表名表达式: {scanner}")

    @classmethod
    def check_alias_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否可能为别名表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return not scanner.is_finish and (scanner.search("AS") or scanner.search(AMTMark.NAME))

    @classmethod
    def parse_alias_expression(cls, scanner_or_string: Union[TokenScanner, str],
                               must_has_as_keyword: bool = False) -> ASTAlisaExpression:
        """解析别名表达式

        Parameters
        ----------
        scanner_or_string : str
            词法扫描器或 SQL 字符串语句
        must_has_as_keyword : bool, default = False
            是否必须包含 AS 关键字
        """
        scanner = cls._unify_input_scanner(scanner_or_string)
        if must_has_as_keyword is True:
            scanner.match("AS")
        else:
            scanner.search_and_move("AS")
        if not scanner.search(AMTMark.NAME):
            raise SqlParseError(f"无法解析为别名表达式: {scanner}")
        return ASTAlisaExpression(name=cls._unify_name(scanner.pop_as_source()))

    @classmethod
    def check_join_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为关联表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("ON") or scanner.search("USING")

    @classmethod
    def parse_join_on_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTJoinOnExpression:
        """解析 ON 关联表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if not scanner.search_and_move("ON"):
            raise SqlParseError(f"无法解析为 ON 关联表达式: {scanner}")
        return ASTJoinOnExpression(condition=cls.parse_condition_expression(scanner))

    @classmethod
    def parse_join_using_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTJoinUsingExpression:
        """解析 USING 关联表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if not scanner.search("USING"):
            raise SqlParseError(f"无法解析为 USING 关联表达式: {scanner}")
        return ASTJoinUsingExpression(using_function=cls.parse_function_expression(scanner))

    @classmethod
    def parse_join_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTJoinExpression:
        """解析关联表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if scanner.search("ON"):
            return cls.parse_join_on_expression(scanner)
        if scanner.search("USING"):
            return cls.parse_join_using_expression(scanner)
        raise SqlParseError(f"无法解析为关联表达式: {scanner}")

    @classmethod
    def parse_column_type_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTColumnTypeExpression:
        """解析 DDL 的字段类型：要求当前指针位置节点为函数名，下一个节点可能为函数参数也可能不是，解析为 SQLColumnType 对象"""
        scanner = cls._unify_input_scanner(scanner_or_string)

        # 解析字段类型名称
        function_name: str = scanner.pop_as_source()

        # 解析字段类型参数
        if scanner.search(AMTMark.PARENTHESIS):
            function_params: List[ASTGeneralExpression] = []
            for param_scanner in scanner.pop_as_children_scanner_list_split_by(","):
                function_params.append(cls.parse_general_expression(param_scanner))
                param_scanner.close()
            return ASTColumnTypeExpression(name=function_name, params=tuple(function_params))
        return ASTColumnTypeExpression(name=function_name)

    @classmethod
    def parse_table_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTTableExpression:
        """解析表名表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        table_name_expression = cls.parse_table_name_expression(scanner)
        alias_expression = cls.parse_alias_expression(scanner) if cls.check_alias_expression(scanner) else None
        return ASTTableExpression(table=table_name_expression, alias=alias_expression)

    @classmethod
    def parse_column_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTColumnExpression:
        """解析列名表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        general_expression = cls.parse_general_expression(scanner)
        alias_expression = cls.parse_alias_expression(scanner) if cls.check_alias_expression(scanner) else None
        return ASTColumnExpression(column=general_expression, alias=alias_expression)

    @classmethod
    def parse_equal_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTEqualExpression:
        """解析等式表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        before_value = cls.parse_general_expression(scanner)
        scanner.match("=")
        after_value = cls.parse_general_expression(scanner)
        return ASTEqualExpression(before_value=before_value, after_value=after_value)

    @classmethod
    def check_partition_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否可能为分区表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("PARTITION")

    @classmethod
    def parse_partition_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTPartitionExpression:
        """解析分区表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("PARTITION")
        partition_list = []
        for partition_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            partition_list.append(cls.parse_equal_expression(partition_scanner))
            partition_scanner.close()
        return ASTPartitionExpression(partition_list=tuple(partition_list))

    @classmethod
    def check_foreign_key_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为外键表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("CONSTRAINT")

    @classmethod
    def parse_foreign_key_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTForeignKeyExpression:
        """解析外键表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("CONSTRAINT")
        constraint_name = scanner.pop_as_source()
        scanner.match("FOREIGN", "KEY")
        slave_columns = []
        for column_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            slave_columns.append(column_scanner.pop_as_source())
            column_scanner.close()
        scanner.match("REFERENCES")
        master_table_name = scanner.pop_as_source()
        master_columns = []
        for column_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            master_columns.append(column_scanner.pop_as_source())
            column_scanner.close()
        on_delete_cascade = scanner.search_and_move("ON", "DELETE", "CASCADE")
        return ASTForeignKeyExpression(
            constraint_name=constraint_name,
            slave_columns=tuple(slave_columns),
            master_table_name=master_table_name,
            master_columns=tuple(master_columns),
            on_delete_cascade=on_delete_cascade
        )

    @classmethod
    def parse_index_column(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTIndexColumn:
        """解析索引声明表达式中的字段"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        name = cls._unify_name(scanner.pop_as_source())
        max_length = None
        if scanner.search(AMTMark.PARENTHESIS):
            parenthesis_scanner = scanner.pop_as_children_scanner()
            max_length = int(parenthesis_scanner.pop_as_source())
            parenthesis_scanner.close()
        return ASTIndexColumn(name=name, max_length=max_length)

    @classmethod
    def check_primary_index_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为主键表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("PRIMARY", "KEY")

    @classmethod
    def parse_primary_index_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTPrimaryIndexExpression:
        """解析主键表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("PRIMARY", "KEY")
        columns = []
        for column_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            columns.append(cls.parse_index_column(column_scanner))
            column_scanner.close()
        using = scanner.pop_as_source() if scanner.search_and_move("USING") else None
        comment = scanner.pop_as_source() if scanner.search_and_move("COMMENT") else None
        if scanner.search_and_move("KEY_BLOCK_SIZE"):
            scanner.match("=")
            key_block_size = int(scanner.pop_as_source())
        else:
            key_block_size = None
        return ASTPrimaryIndexExpression(columns=tuple(columns), using=using, comment=comment,
                                         key_block_size=key_block_size)

    @classmethod
    def check_unique_index_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为唯一键表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("UNIQUE", "KEY")

    @classmethod
    def parse_unique_index_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTUniqueIndexExpression:
        """解析唯一键表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("UNIQUE", "KEY")
        name = scanner.pop_as_source()
        columns = []
        for column_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            columns.append(cls.parse_index_column(column_scanner))
            column_scanner.close()
        using = scanner.pop_as_source() if scanner.search_and_move("USING") else None
        comment = scanner.pop_as_source() if scanner.search_and_move("COMMENT") else None
        if scanner.search_and_move("KEY_BLOCK_SIZE"):
            scanner.match("=")
            key_block_size = int(scanner.pop_as_source())
        else:
            key_block_size = None
        return ASTUniqueIndexExpression(name=name, columns=tuple(columns), using=using, comment=comment,
                                        key_block_size=key_block_size)

    @classmethod
    def check_normal_index_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为一般索引表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("KEY")

    @classmethod
    def parse_normal_index_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTNormalIndexExpression:
        """解析一般索引表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("KEY")
        name = scanner.pop_as_source()
        columns = []
        for column_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            columns.append(cls.parse_index_column(column_scanner))
            column_scanner.close()
        using = scanner.pop_as_source() if scanner.search_and_move("USING") else None
        comment = scanner.pop_as_source() if scanner.search_and_move("COMMENT") else None
        if scanner.search_and_move("KEY_BLOCK_SIZE"):
            scanner.match("=")
            key_block_size = int(scanner.pop_as_source())
        else:
            key_block_size = None
        return ASTNormalIndexExpression(name=name, columns=tuple(columns), using=using, comment=comment,
                                        key_block_size=key_block_size)

    @classmethod
    def check_fulltext_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为全文索引表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("FULLTEXT", "KEY")

    @classmethod
    def parse_fulltext_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTFulltextIndexExpression:
        """解析全文索引表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("FULLTEXT", "KEY")
        name = scanner.pop_as_source()
        columns = []
        for column_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            columns.append(cls.parse_index_column(column_scanner))
            column_scanner.close()
        using = scanner.pop_as_source() if scanner.search_and_move("USING") else None
        comment = scanner.pop_as_source() if scanner.search_and_move("COMMENT") else None
        if scanner.search_and_move("KEY_BLOCK_SIZE"):
            scanner.match("=")
            key_block_size = int(scanner.pop_as_source())
        else:
            key_block_size = None
        return ASTFulltextIndexExpression(name=name, columns=tuple(columns), using=using, comment=comment,
                                          key_block_size=key_block_size)

    @classmethod
    def parse_define_column_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTDefineColumnExpression:
        """解析 DDL 的字段表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        # 解析顺序固定的信息
        column_name = scanner.pop_as_source()
        column_type = cls.parse_column_type_expression(scanner)

        # 解析顺序可能不定的字段信息
        comment: Optional[str] = None
        is_unsigned: bool = False
        is_zerofill: bool = False
        character_set: Optional[str] = None
        collate: Optional[str] = None
        is_allow_null: bool = False
        is_not_null: bool = False
        is_auto_increment: bool = False
        default: Optional[ASTGeneralExpression] = None
        on_update: Optional[ASTGeneralExpression] = None
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
                default = cls.parse_general_expression(scanner)
            elif scanner.search_and_move("COMMENT"):
                comment = scanner.pop_as_source()
            elif scanner.search_and_move("ON", "UPDATE"):  # ON UPDATE
                on_update = cls.parse_general_expression(scanner)
            elif scanner.search_and_move("AUTO_INCREMENT"):
                is_auto_increment = True
            elif scanner.search_and_move("UNSIGNED"):
                is_unsigned = True
            elif scanner.search_and_move("ZEROFILL"):
                is_zerofill = True
            else:
                raise SqlParseError(f"无法解析的 DDL 字段表达式的字段属性: {scanner}")

        # 构造 DDL 字段表达式对象
        return ASTDefineColumnExpression(
            column_name=cls._unify_name(column_name),
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

    @classmethod
    def check_select_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为 SELECT 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("SELECT")

    @classmethod
    def parse_select_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTSelectClause:
        """解析 SELECT 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("SELECT")
        distinct = scanner.search_and_move("DISTINCT")
        columns = [cls.parse_column_expression(scanner)]
        while scanner.search_and_move(","):
            columns.append(cls.parse_column_expression(scanner))
        return ASTSelectClause(distinct=distinct, columns=tuple(columns))

    @classmethod
    def check_from_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为 FROM 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("FROM")

    @classmethod
    def parse_from_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTFromClause:
        """解析 FROM 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("FROM")
        tables = [cls.parse_table_expression(scanner)]
        while scanner.search_and_move(","):
            tables.append(cls.parse_table_expression(scanner))
        return ASTFromClause(tables=tuple(tables))

    @classmethod
    def check_lateral_view_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为 LATERAL VIEW 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("LATERAL", "VIEW")

    @classmethod
    def parse_lateral_view_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTLateralViewClause:
        """解析 LATERAL VIEW 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("LATERAL", "VIEW")
        function = cls.parse_function_expression(scanner)
        view_name = scanner.pop_as_source()
        alias = cls.parse_alias_expression(scanner, must_has_as_keyword=True)
        return ASTLateralViewClause(function=function, view_name=view_name, alias=alias)

    @classmethod
    def check_join_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为 JOIN 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return cls.check_join_type(scanner)

    @classmethod
    def parse_join_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTJoinClause:
        """解析 JOIN 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        join_type = cls.parse_join_type(scanner)
        table_expression = cls.parse_table_expression(scanner)
        if cls.check_join_expression(scanner):
            join_rule = cls.parse_join_expression(scanner)
        else:
            join_rule = None
        return ASTJoinClause(join_type=join_type, table=table_expression, join_rule=join_rule)

    @classmethod
    def check_where_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否可能为 WHERE 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("WHERE")

    @classmethod
    def parse_where_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTWhereClause:
        """解析 WHERE 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("WHERE")
        return ASTWhereClause(condition=cls.parse_condition_expression(scanner))

    @classmethod
    def check_group_by_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否可能为 GROUP BY 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("GROUP", "BY")

    @classmethod
    def parse_group_by_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTGroupByClause:
        """解析 GROUP BY 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("GROUP", "BY")
        if scanner.search_and_move("GROUPING", "SETS"):
            # 处理 GROUPING SETS 的语法
            grouping_list = []
            for grouping_scanner in scanner.pop_as_children_scanner_list_split_by(","):
                if grouping_scanner.search(AMTMark.PARENTHESIS):
                    parenthesis_scanner_list = grouping_scanner.pop_as_children_scanner_list_split_by(",")
                    columns_list = []
                    for parenthesis_scanner in parenthesis_scanner_list:
                        cls.parse_general_expression(parenthesis_scanner)
                        parenthesis_scanner.close()
                    grouping_list.append(tuple(columns_list))
                else:
                    grouping_list.append(tuple([cls.parse_general_expression(grouping_scanner)]))
                grouping_scanner.close()
            return ASTGroupingSetsGroupByClause(grouping_list=tuple(grouping_list))

        # 处理一般的 GROUP BY 的语法
        columns = [cls.parse_general_expression(scanner)]
        while scanner.search_and_move(","):
            columns.append(cls.parse_general_expression(scanner))
        with_rollup = False
        if scanner.search_and_move("WITH", "ROLLUP"):
            with_rollup = True
        return ASTNormalGroupByClause(columns=tuple(columns), with_rollup=with_rollup)

    @classmethod
    def check_having_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """是否可能为 HAVING 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("HAVING")

    @classmethod
    def parse_having_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTHavingClause:
        """解析 HAVING 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("HAVING")
        return ASTHavingClause(condition=cls.parse_condition_expression(scanner))

    @classmethod
    def check_order_by_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """是否可能为 ORDER BY 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("ORDER", "BY")

    @classmethod
    def parse_order_by_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTOrderByClause:
        """解析 ORDER BY 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)

        def parse_single():
            column = cls.parse_general_expression(scanner)
            order = cls.parse_order_type(scanner)
            columns.append((column, order))

        scanner.match("ORDER", "BY")
        columns = []
        parse_single()
        while scanner.search_and_move(","):
            parse_single()

        return ASTOrderByClause(columns=tuple(columns))

    @classmethod
    def check_limit_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """是否可能为 LIMIT 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("LIMIT")

    @classmethod
    def parse_limit_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTLimitClause:
        """解析 LIMIT 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if not scanner.search_and_move("LIMIT"):
            raise SqlParseError("无法解析为 LIMIT 子句")
        cnt_1 = cls.parse_literal_expression(scanner).as_int()
        if scanner.search_and_move(","):
            offset_int = cnt_1
            limit_int = cls.parse_literal_expression(scanner).as_int()
        elif scanner.search_and_move("OFFSET"):
            offset_int = cls.parse_literal_expression(scanner).as_int()
            limit_int = cnt_1
        else:
            raise SqlParseError("无法解析为 LIMIT 子句")
        return ASTLimitClause(limit=limit_int, offset=offset_int)

    @classmethod
    def _parse_single_with_table(cls, scanner_or_string: Union[TokenScanner, str]) -> Tuple[str, ASTSelectStatement]:
        """解析一个 WITH 临时表"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        table_name = cls._unify_name(scanner.pop_as_source())
        scanner.match("AS")
        parenthesis_scanner = scanner.pop_as_children_scanner()
        table_statement = cls.parse_select_statement(parenthesis_scanner, with_clause=ASTWithClause.empty())
        parenthesis_scanner.close()
        return table_name, table_statement

    @classmethod
    def parse_with_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> Optional[ASTWithClause]:
        """解析 WITH 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if scanner.search_and_move("WITH"):
            tables = [cls._parse_single_with_table(scanner)]
            while scanner.search_and_move(","):
                table_statement = cls._parse_single_with_table(scanner)
                tables.append(table_statement)  # 将前置的 WITH 作为当前解析临时表的 WITH 子句
            return ASTWithClause(tables=tuple(tables))
        return ASTWithClause.empty()

    @classmethod
    def check_select_statement(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否可能为 SELECT 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("SELECT")

    @classmethod
    def parse_single_select_statement(cls, scanner_or_string: Union[TokenScanner, str],
                                      with_clause: Optional[ASTWithClause] = None
                                      ) -> ASTSingleSelectStatement:
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
        scanner = cls._unify_input_scanner(scanner_or_string)
        if with_clause is None:
            with_clause = cls.parse_with_clause(scanner)
        select_clause = cls.parse_select_clause(scanner)
        from_clause = cls.parse_from_clause(scanner) if cls.check_from_clause(scanner) else None
        lateral_view_clauses = []
        while cls.check_lateral_view_clause(scanner):
            lateral_view_clauses.append(cls.parse_lateral_view_clause(scanner))
        join_clause = []
        while cls.check_join_clause(scanner):
            join_clause.append(cls.parse_join_clause(scanner))
        where_clause = cls.parse_where_clause(scanner) if cls.check_where_clause(scanner) else None
        group_by_clause = cls.parse_group_by_clause(scanner) if cls.check_group_by_clause(scanner) else None
        having_clause = cls.parse_having_clause(scanner) if cls.check_having_clause(scanner) else None
        order_by_clause = cls.parse_order_by_clause(scanner) if cls.check_order_by_clause(scanner) else None
        limit_clause = cls.parse_limit_clause(scanner) if cls.check_limit_clause(scanner) else None
        return ASTSingleSelectStatement(
            with_clause=with_clause,
            select_clause=select_clause,
            from_clause=from_clause,
            lateral_view_clauses=tuple(lateral_view_clauses),
            join_clauses=tuple(join_clause),
            where_clause=where_clause,
            group_by_clause=group_by_clause,
            having_clause=having_clause,
            order_by_clause=order_by_clause,
            limit_clause=limit_clause
        )

    @classmethod
    def parse_select_statement(cls, scanner_or_string: Union[TokenScanner, str],
                               with_clause: Optional[ASTWithClause] = None) -> ASTSelectStatement:
        """解析 SELECT 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if with_clause is None:
            with_clause = cls.parse_with_clause(scanner)
        result = [cls.parse_single_select_statement(scanner, with_clause=with_clause)]
        while not scanner.is_finish and cls.check_union_type(scanner):
            result.append(cls.parse_union_type(scanner))
            result.append(cls.parse_single_select_statement(scanner, with_clause=with_clause))
        scanner.search_and_move(";")
        if not scanner.is_finish:
            raise SqlParseError(f"没有解析完成: {scanner}")

        if len(result) == 1:
            return result[0]
        return ASTUnionSelectStatement(with_clause=with_clause, elements=tuple(result))

    @classmethod
    def check_insert_statement(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为 INSERT 语句（已匹配过 WITH 语句才可以调用）"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("INSERT")

    @classmethod
    def parse_insert_statement(cls, scanner_or_string: Union[TokenScanner, str],
                               with_clause: Optional[ASTWithClause]) -> ASTInsertStatement:
        """解析 INSERT 表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)

        if with_clause is None:
            with_clause = cls.parse_with_clause(scanner)

        insert_type = cls.parse_insert_type(scanner)

        # 匹配可能包含的 TABLE 关键字
        scanner.search_and_move("TABLE")

        # 匹配表名
        table_name = cls.parse_table_name_expression(scanner)

        # 匹配分区表达式
        if cls.check_partition_expression(scanner):
            partition = cls.parse_partition_expression(scanner)
        else:
            partition = None

        # 匹配列名列表
        if scanner.search(AMTMark.PARENTHESIS):
            columns = []
            for column_scanner in scanner.pop_as_children_scanner_list_split_by(","):
                columns.append(cls.parse_column_name_expression(column_scanner))
                column_scanner.close()
        else:
            columns = None

        # 匹配 VALUES 类型
        if scanner.search_and_move("VALUES"):
            values = []
            while scanner.search(AMTMark.PARENTHESIS):
                values.append(cls.parse_value_expression(scanner))
                scanner.search_and_move(",")

            return ASTInsertValuesStatement(
                with_clause=with_clause,
                insert_type=insert_type,
                table_name=table_name,
                partition=partition,
                columns=tuple(columns) if columns is not None else None,
                values=tuple(values)
            )

        if scanner.search("SELECT"):
            select_statement = cls.parse_select_statement(scanner, with_clause=ASTWithClause.empty())
            return ASTInsertSelectStatement(
                with_clause=with_clause,
                insert_type=insert_type,
                table_name=table_name,
                partition=partition,
                columns=tuple(columns) if columns is not None else None,
                select_statement=select_statement
            )

        raise SqlParseError(f"未知的 INSERT 语句类型 {scanner}")

    @classmethod
    def check_set_statement(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为 SET 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("SET")

    @classmethod
    def parse_set_statement(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTSetStatement:
        """解析 SET 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("SET")
        config_name = cls.parse_config_name_expression(scanner)
        scanner.match("=")
        config_value = cls.parse_config_value_expression(scanner)
        return ASTSetStatement(config_name=config_name, config_value=config_value)

    @classmethod
    def parse_create_table_statement(cls, scanner_or_string: Union[TokenScanner, str]) -> ASTCreateTableStatement:
        """解析 CREATE TABLE 语句"""
        # 解析字段、索引括号前的部分
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("CREATE", "TABLE")
        if_not_exists = scanner.search_and_move("IF", "NOT", "EXISTS")
        table_name_expression = cls.parse_table_name_expression(scanner)

        # 解析字段和索引
        columns: List[ASTDefineColumnExpression] = []
        primary_key: Optional[ASTPrimaryIndexExpression] = None
        unique_key: List[ASTUniqueIndexExpression] = []
        key: List[ASTNormalIndexExpression] = []
        fulltext_key: List[ASTFulltextIndexExpression] = []
        foreign_key: List[ASTForeignKeyExpression] = []
        for group_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            if cls.check_primary_index_expression(group_scanner):
                primary_key = cls.parse_primary_index_expression(group_scanner)
            elif cls.check_unique_index_expression(group_scanner):
                unique_key.append(cls.parse_unique_index_expression(group_scanner))
            elif cls.check_normal_index_expression(group_scanner):
                key.append(cls.parse_normal_index_expression(group_scanner))
            elif cls.check_fulltext_expression(group_scanner):
                fulltext_key.append(cls.parse_fulltext_expression(group_scanner))
            elif cls.check_foreign_key_expression(group_scanner):
                foreign_key.append(cls.parse_foreign_key_expression(group_scanner))
            else:
                columns.append(cls.parse_define_column_expression(group_scanner))
            group_scanner.close()

        # 解析表属性
        partitioned_by: List[ASTDefineColumnExpression] = []
        comment: Optional[str] = None
        engine: Optional[str] = None
        auto_increment: Optional[int] = None
        default_charset: Optional[str] = None
        collate: Optional[str] = None
        row_format: Optional[str] = None
        states_persistent: Optional[str] = None
        row_format_serde: Optional[str] = None
        stored_as_inputformat: Optional[str] = None
        outputformat: Optional[str] = None
        location: Optional[str] = None
        tblproperties: Optional[List[Tuple[ASTConfigNameExpression, ASTConfigValueExpression]]] = []
        while not scanner.is_finish:
            if scanner.search_and_move("ENGINE"):
                scanner.search_and_move("=")
                engine = scanner.pop_as_source()
            elif scanner.search_and_move("AUTO_INCREMENT"):
                scanner.search_and_move("=")
                auto_increment = int(scanner.pop_as_source())
            elif scanner.search_and_move("DEFAULT", "CHARSET"):
                scanner.search_and_move("=")
                default_charset = scanner.pop_as_source()
            elif scanner.search_and_move("ROW_FORMAT"):
                scanner.search_and_move("=")
                row_format = scanner.pop_as_source()
            elif scanner.search_and_move("COLLATE"):
                scanner.search_and_move("=")
                collate = scanner.pop_as_source()
            elif scanner.search_and_move("COMMENT"):
                scanner.search_and_move("=")
                comment = scanner.pop_as_source()
            elif scanner.search_and_move("STATS_PERSISTENT"):
                scanner.search_and_move("=")
                states_persistent = scanner.pop_as_source()
            elif scanner.search_and_move("PARTITIONED", "BY"):
                for group_scanner in scanner.pop_as_children_scanner_list_split_by(","):
                    partitioned_by.append(cls.parse_define_column_expression(group_scanner))
                    group_scanner.close()
            elif scanner.search_and_move("ROW", "FORMAT", "SERDE"):
                scanner.search_and_move("=")
                row_format_serde = scanner.pop_as_source()
            elif scanner.search_and_move("STORED", "AS", "INPUTFORMAT"):
                scanner.search_and_move("=")
                stored_as_inputformat = scanner.pop_as_source()
            elif scanner.search_and_move("OUTPUTFORMAT"):
                scanner.search_and_move("=")
                outputformat = scanner.pop_as_source()
            elif scanner.search_and_move("LOCATION"):
                scanner.search_and_move("=")
                location = scanner.pop_as_source()
            elif scanner.search_and_move("TBLPROPERTIES"):
                for group_scanner in scanner.pop_as_children_scanner_list_split_by(","):
                    config_name = cls.parse_config_name_expression(group_scanner)
                    group_scanner.match("=")
                    config_value = cls.parse_config_value_expression(group_scanner)
                    tblproperties.append((config_name, config_value))
                    group_scanner.close()
            else:
                raise SqlParseError(f"未知的 DDL 表属性: {scanner}")
        scanner.search_and_move(";")

        return ASTCreateTableStatement(
            table_name_expression=table_name_expression,
            comment=comment,
            if_not_exists=if_not_exists,
            columns=tuple(columns),
            primary_key=primary_key,
            unique_key=tuple(unique_key),
            key=tuple(key),
            fulltext_key=tuple(fulltext_key),
            foreign_key=tuple(foreign_key),
            engine=engine,
            auto_increment=auto_increment,
            default_charset=default_charset,
            collate=collate,
            row_format=row_format,
            states_persistent=states_persistent,
            partitioned_by=tuple(partitioned_by),
            row_format_serde=row_format_serde,
            stored_as_inputformat=stored_as_inputformat,
            outputformat=outputformat,
            location=location,
            tblproperties=tuple(tblproperties)
        )

    @classmethod
    def parse_statements(cls, scanner_or_string: Union[TokenScanner, str]) -> List[ASTStatement]:
        """解析一段 SQL 语句，返回表达式的列表"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        statement_list = []
        for statement_scanner in scanner.split_by(";"):
            # 解析 SET 语句
            if cls.check_set_statement(statement_scanner):
                statement_list.append(cls.parse_set_statement(statement_scanner))
                continue

            # 先尝试解析 WITH 语句
            with_clause = cls.parse_with_clause(statement_scanner)

            if cls.check_select_statement(statement_scanner):
                statement_list.append(cls.parse_select_statement(statement_scanner, with_clause=with_clause))
            elif cls.check_insert_statement(statement_scanner):
                statement_list.append(cls.parse_insert_statement(statement_scanner, with_clause=with_clause))
            else:
                raise SqlParseError(f"未知语句类型: {statement_scanner}")

            statement_scanner.close()

        return statement_list
