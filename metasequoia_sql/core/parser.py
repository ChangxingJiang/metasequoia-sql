# pylint: disable=C0302

"""
SQL 语法解析器

将所有解析方法合并到这个类中，以支持插件开发。
如需替换词法解析器，重写 build_token_scanner 方法即可。

TODO 将 CURRENT_TIMESTAMP、CURRENT_DATE、CURRENT_TIME 改为单独节点处理
"""

from typing import Optional, Tuple, List, Union

from metasequoia_sql.common import TokenScanner
from metasequoia_sql.common import name_set
from metasequoia_sql.core import node
from metasequoia_sql.errors import SqlParseError
from metasequoia_sql.lexical import AMTMark, AMTSingle, FSMMachine

__all__ = ["SQLParser"]


class SQLParser:
    # pylint: disable=R0904
    """SQL 语法解析器"""

    @classmethod
    def build_token_scanner(cls, string: str) -> TokenScanner:
        """构造词法扫描器"""
        return TokenScanner(FSMMachine.parse(string), ignore_space=True, ignore_comment=True)

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

    # ------------------------------ 枚举类节点的解析方法 ------------------------------

    @classmethod
    def check_insert_type(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为插入类型"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return (scanner.search_and_move("INSERT", "INTO") or
                scanner.search_and_move("INSERT", "OVERWRITE"))

    @classmethod
    def parse_insert_type(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTInsertType:
        """解析插入类型"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if scanner.search_and_move("INSERT", "INTO"):
            return node.ASTInsertType(enum=node.EnumInsertType.INSERT_INTO)
        if scanner.search_and_move("INSERT", "OVERWRITE"):
            return node.ASTInsertType(enum=node.EnumInsertType.INSERT_OVERWRITE)
        raise SqlParseError(f"未知的 INSERT 类型: {scanner}")

    @classmethod
    def check_join_type(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为关联类型"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        for join_type in node.EnumJoinType:
            if scanner.search(*join_type.value):
                return True
        return False

    @classmethod
    def parse_join_type(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTJoinType:
        """解析关联类型"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        for join_type in node.EnumJoinType:
            if scanner.search_and_move(*join_type.value):
                return node.ASTJoinType(enum=join_type)
        raise SqlParseError(f"无法解析的关联类型: {scanner}")

    @classmethod
    def parse_order_type(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTOrderType:
        """解析排序类型"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if scanner.search_and_move("DESC"):
            return node.ASTOrderType(enum=node.EnumOrderType.DESC)
        if scanner.search_and_move("ASC"):
            return node.ASTOrderType(enum=node.EnumOrderType.ASC)
        return node.ASTOrderType(enum=node.EnumOrderType.ASC)

    @classmethod
    def check_union_type(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为组合类型"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        for union_type in node.EnumUnionType:
            if scanner.search(*union_type.value):
                return True
        return False

    @classmethod
    def parse_union_type(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTUnionType:
        """解析组合类型"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        for union_type in node.EnumUnionType:
            if scanner.search_and_move(*union_type.value):
                return node.ASTUnionType(enum=union_type)
        raise SqlParseError(f"无法解析的组合类型: {scanner}")

    @classmethod
    def check_compare_operator(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为比较运算符"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.get_as_source() in {"=", "!=", "<>", "<", "<=", ">", ">="}

    @classmethod
    def parse_compare_operator(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTCompareOperator:
        """解析比较运算符"""
        scanner = cls._unify_input_scanner(scanner_or_string)
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

    @classmethod
    def check_compute_operator(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为计算运算符"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        for compute_operator in node.EnumComputeOperator:
            if scanner.search(*compute_operator.value):
                return True
        return False

    @classmethod
    def parse_compute_operator(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTComputeOperator:
        """解析计算运算符"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        for compute_operator in node.EnumComputeOperator:
            if scanner.search_and_move(*compute_operator.value):
                return node.ASTComputeOperator(enum=compute_operator)
        raise SqlParseError(f"无法解析的计算运算符: {scanner}")

    @classmethod
    def check_logical_operator(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为逻辑运算符"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.get_as_source() in {"AND", "OR"}

    @classmethod
    def parse_logical_operator(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTLogicalOperator:
        """解析逻辑运算符"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        for logical_operator in node.EnumLogicalOperator:
            if scanner.search_and_move(*logical_operator.value):
                return node.ASTLogicalOperator(enum=logical_operator)
        raise SqlParseError(f"无法解析的逻辑运算符: {scanner}")

    @classmethod
    def parse_cast_data_type(cls, scanner_or_string: Union[TokenScanner, str]) -> node.EnumCastDataType:
        """解析 CAST 函数表达式中的类型"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        for cast_type in node.EnumCastDataType:
            if scanner.search_and_move(cast_type.value):
                return cast_type
        raise SqlParseError(f"无法解析的 CAST 函数表达式中的类型: {scanner}")

    # ------------------------------ 基础节点的解析方法 ------------------------------

    @classmethod
    def check_column_name_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """是否可能为列名表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return ((scanner.search(AMTMark.NAME, ".", AMTMark.NAME)
                 and not scanner.search(AMTMark.NAME, ".", AMTMark.NAME, AMTMark.PARENTHESIS))
                or (scanner.search(AMTMark.NAME)
                    and not scanner.search(AMTMark.NAME, ".")
                    and not scanner.search(AMTMark.NAME, AMTMark.PARENTHESIS)))

    @classmethod
    def parse_column_name_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTColumnName:
        """解析列名表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if (scanner.search(AMTMark.NAME, ".", AMTMark.NAME) and
                not scanner.search(AMTMark.NAME, ".", AMTMark.NAME, AMTMark.PARENTHESIS)):
            table_name = scanner.pop_as_source()
            scanner.pop()
            column_name = scanner.pop_as_source()
            return node.ASTColumnName(table_name=unify_name(table_name),
                                      column_name=unify_name(column_name))
        if (scanner.search(AMTMark.NAME)
                and not scanner.search(AMTMark.NAME, ".")
                and not scanner.search(AMTMark.NAME, AMTMark.PARENTHESIS)):
            return node.ASTColumnName(column_name=unify_name(scanner.pop_as_source()))
        raise SqlParseError(f"无法解析为表名表达式: {scanner}")

    @classmethod
    def parse_table_name_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTTableName:
        """解析表名表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if scanner.search(AMTMark.NAME, ".", AMTMark.NAME):
            schema_name = scanner.pop_as_source()
            scanner.pop()
            table_name = scanner.pop_as_source()
            return node.ASTTableName(schema_name=unify_name(schema_name), table_name=unify_name(table_name))
        if scanner.search(AMTMark.NAME):
            name_source = scanner.pop_as_source()
            if name_source.count(".") == 1:
                schema_name, table_name = name_source.strip("`").split(".")
            else:
                schema_name, table_name = None, name_source
            return node.ASTTableName(schema_name=unify_name(schema_name), table_name=unify_name(table_name))
        raise SqlParseError(f"无法解析为表名表达式: {scanner}")

    @classmethod
    def parse_function_name_expression(cls, scanner_or_string: Union[TokenScanner, str]
                                       ) -> node.ASTFunctionName:
        """解析函数名表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if scanner.search(AMTMark.NAME, ".", AMTMark.NAME):
            schema_name = scanner.pop_as_source()
            scanner.pop()
            table_name = scanner.pop_as_source()
            return node.ASTFunctionName(schema_name=unify_name(schema_name),
                                        function_name=unify_name(table_name))
        if scanner.search(AMTMark.NAME):
            name_source = scanner.pop_as_source()
            if name_source.count(".") == 1:
                schema_name, table_name = name_source.strip("`").split(".")
            else:
                schema_name, table_name = None, name_source
            return node.ASTFunctionName(schema_name=unify_name(schema_name),
                                        function_name=unify_name(table_name))
        raise SqlParseError(f"无法解析为表名表达式: {scanner}")

    @classmethod
    def check_literal_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为字面值：包含整型字面值、浮点型字面值、字符串型字面值、十六进制型字面值、布尔型字面值、位值型字面值、空值的字面值"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search(AMTMark.LITERAL) or scanner.search("-")

    @classmethod
    def parse_literal_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTLiteralExpression:
        """解析字面值：包含整型字面值、浮点型字面值、字符串型字面值、十六进制型字面值、布尔型字面值、位值型字面值、空值的字面值"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        token = scanner.pop()
        if isinstance(token, AMTSingle):
            return node.ASTLiteralExpression(value=token.source)
        if token.equals("-") and (scanner.search(AMTMark.LITERAL_INT) or scanner.search(AMTMark.LITERAL_FLOAT)):
            next_token = scanner.pop()
            return node.ASTLiteralExpression(value=f"-{next_token.source}")
        raise SqlParseError(f"未知的字面值: {token}")

    @classmethod
    def parse_window_row_item(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTWindowRowItem:
        """解析窗口函数行限制中的行"""
        scanner = cls._unify_input_scanner(scanner_or_string)
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

    @classmethod
    def parse_window_row(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTWindowRow:
        """解析窗口语句限制行的表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("ROWS", "BETWEEN")
        from_row = cls.parse_window_row_item(scanner)
        scanner.match("AND")
        to_row = cls.parse_window_row_item(scanner)
        return node.ASTWindowRow(from_row=from_row, to_row=to_row)

    @classmethod
    def check_wildcard_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否可能为通配符表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("*") or scanner.search(AMTMark.NAME, ".", "*")

    @classmethod
    def parse_wildcard_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTWildcardExpression:
        """解析通配符表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if scanner.search_and_move("*"):
            return node.ASTWildcardExpression()
        if scanner.search(AMTMark.NAME, ".", "*"):
            schema_name = scanner.pop_as_source()
            scanner.pop()
            scanner.pop()
            return node.ASTWildcardExpression(table_name=schema_name)
        raise SqlParseError("无法解析为通配符表达式")

    @classmethod
    def check_alias_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否可能为别名表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("AS") or scanner.search(AMTMark.NAME)

    @classmethod
    def parse_alias_expression(cls, scanner_or_string: Union[TokenScanner, str],
                               must_has_as_keyword: bool = False) -> node.ASTAlisaExpression:
        """解析别名表达式

        Parameters
        ----------
        scanner_or_string : Union[TokenScanner, str]
            词法扫描器或字符串
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
        return node.ASTAlisaExpression(name=unify_name(scanner.pop_as_source()))

    # ------------------------------ SELECT 语句节点的解析方法 ------------------------------

    @classmethod
    def check_function_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """是否可能为函数表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return (scanner.search(AMTMark.NAME, AMTMark.PARENTHESIS) or
                scanner.search(AMTMark.NAME, ".", AMTMark.NAME, AMTMark.PARENTHESIS))

    @classmethod
    def parse_extract_function_expression(cls, scanner_or_string: Union[TokenScanner, str]
                                          ) -> node.ASTExtractFunctionExpression:
        """解析 EXTRACT 函数表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        extract_name = cls.parse_general_expression(scanner)
        scanner.match("FROM")
        column_expression = cls.parse_general_expression(scanner)
        scanner.close()
        return node.ASTExtractFunctionExpression(extract_name=extract_name, column_expression=column_expression)

    @classmethod
    def parse_cast_function_expression(cls, scanner_or_string: Union[TokenScanner, str]
                                       ) -> node.ASTCastFunctionExpression:
        """解析 CAST 函数表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        column_expression = cls.parse_general_expression(scanner)
        scanner.match("AS")
        signed = scanner.search_and_move("SIGNED")
        cast_type = cls.parse_cast_data_type(scanner)
        if scanner.search(AMTMark.PARENTHESIS):
            parenthesis_scanner = scanner.pop_as_children_scanner()
            cast_params: Optional[List[int] | Tuple[int, ...]] = []
            for param_scanner in parenthesis_scanner.split_by(","):
                cast_params.append(int(param_scanner.pop_as_source()))
                param_scanner.close()
            cast_params = tuple(cast_params)
        else:
            cast_params = None
        scanner.close()
        cast_data_type = node.ASTCastDataType(signed=signed, type=cast_type, params=cast_params)
        return node.ASTCastFunctionExpression(column_expression=column_expression, cast_type=cast_data_type)

    @classmethod
    def parse_if_function_expression(cls, scanner_or_string: Union[TokenScanner, str]
                                     ) -> node.ASTNormalFunctionExpression:
        """解析 IF 函数表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        function_params: List[node.ASTExpressionBase] = []
        first_param = True
        for param_scanner in scanner.split_by(","):
            if first_param is True:
                function_params.append(cls.parse_condition_expression(param_scanner))
                first_param = False
            else:
                function_params.append(cls.parse_general_expression(param_scanner))
            param_scanner.close()
        return node.ASTNormalFunctionExpression(name=node.ASTFunctionName(function_name="IF"),
                                                params=tuple(function_params))

    @classmethod
    def parse_function_expression(cls, scanner_or_string: Union[TokenScanner, str]
                                  ) -> Union[node.ASTFunctionExpression]:
        """解析函数表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        function_name = cls.parse_function_name_expression(scanner)

        if function_name.function_name.upper() == "CAST":
            return cls.parse_cast_function_expression(scanner.pop_as_children_scanner())
        if function_name.function_name.upper() == "EXTRACT":
            return cls.parse_extract_function_expression(scanner.pop_as_children_scanner())
        if function_name.function_name.upper() == "IF":
            return cls.parse_if_function_expression(scanner.pop_as_children_scanner())

        parenthesis_scanner = scanner.pop_as_children_scanner()
        if function_name.function_name.upper() == "SUBSTRING":
            # 将 MySQL 和 PostgreSQL 中的 "SUBSTRING(str1 FROM 3 FOR 2)" 格式化为 "SUBSTRING(str1, 3, 2)"
            parenthesis_scanner = TokenScanner([
                element if not element.equals("FROM") and not element.equals("FOR") else AMTSingle(",")
                for element in parenthesis_scanner.elements])

        is_distinct = False
        if (function_name.function_name.upper() in name_set.AGGREGATION_FUNCTION_NAME_SET
                and parenthesis_scanner.search_and_move("DISTINCT")):
            is_distinct = True

        function_params: List[node.ASTExpressionBase] = []
        for param_scanner in parenthesis_scanner.split_by(","):
            function_params.append(cls.parse_general_expression(param_scanner))
            if not param_scanner.is_finish:
                raise SqlParseError(f"无法解析函数参数: {param_scanner}")

        parenthesis_scanner.close()

        if (function_name.schema_name is None
                and function_name.function_name.upper() in name_set.AGGREGATION_FUNCTION_NAME_SET):
            return node.ASTAggregationFunctionExpression(
                name=function_name,
                params=tuple(function_params),
                is_distinct=is_distinct)
        return node.ASTNormalFunctionExpression(
            name=function_name,
            params=tuple(function_params))

    @classmethod
    def parse_function_expression_maybe_with_array_index(
            cls, scanner_or_string: Union[TokenScanner, str]
    ) -> Union[node.ASTFunctionExpression, node.ASTArrayIndexExpression]:
        """解析函数表达式，并解析函数表达式后可能包含的数组下标"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        array_expression = cls.parse_function_expression(scanner)
        if scanner.is_finish or not scanner.search(AMTMark.ARRAY_INDEX):
            return array_expression
        idx = int(scanner.pop_as_source().lstrip("[").rstrip("]"))
        return node.ASTArrayIndexExpression(array=array_expression, idx=idx)

    @classmethod
    def _parse_in_parenthesis(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTExpressionBase:
        """解析 IN 关键字后的插入语：插入语可能为子查询或值表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if cls.check_sub_query_parenthesis(scanner):
            return cls.parse_sub_query_expression(scanner)
        return cls.parse_value_expression(scanner)

    @classmethod
    def parse_bool_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTBoolExpression:
        # pylint: disable=R0911
        """解析布尔值表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        is_not = scanner.search_and_move("NOT")
        if scanner.search_and_move("EXISTS"):
            after_value = cls.parse_sub_query_expression(scanner)
            return node.ASTBoolExistsExpression(is_not=is_not, after_value=after_value)
        before_value = cls.parse_general_expression(scanner)
        is_not = is_not or scanner.search_and_move("NOT")
        if scanner.search_and_move("BETWEEN"):  # "... BETWEEN ... AND ..."
            from_value = cls.parse_general_expression(scanner)
            scanner.match("AND")
            to_value = cls.parse_general_expression(scanner)
            return node.ASTBoolBetweenExpression(is_not=is_not, before_value=before_value, from_value=from_value,
                                                 to_value=to_value)
        if scanner.search_and_move("IS"):  # ".... IS ...." 或 "... IS NOT ..."
            is_not = is_not or scanner.search_and_move("NOT")
            after_value = cls.parse_general_expression(scanner)
            return node.ASTBoolIsExpression(is_not=is_not, before_value=before_value, after_value=after_value)
        if scanner.search_and_move("IN"):  # "... IN (1, 2, 3)" 或 "... IN (SELECT ... )"
            after_value = cls._parse_in_parenthesis(scanner)
            return node.ASTBoolInExpression(is_not=is_not, before_value=before_value, after_value=after_value)
        if scanner.search_and_move("LIKE"):
            after_value = cls.parse_general_expression(scanner)
            return node.ASTBoolLikeExpression(is_not=is_not, before_value=before_value, after_value=after_value)
        if scanner.search_and_move("RLIKE"):
            after_value = cls.parse_general_expression(scanner)
            return node.ASTBoolRlikeExpression(is_not=is_not, before_value=before_value, after_value=after_value)
        if cls.check_compare_operator(scanner):  # "... > ..."
            compare_operator = cls.parse_compare_operator(scanner)
            after_value = cls.parse_general_expression(scanner)
            return node.ASTBoolCompareExpression(is_not=is_not, operator=compare_operator, before_value=before_value,
                                                 after_value=after_value)
        raise SqlParseError(f"无法解析为布尔值表达式: {scanner}")

    @classmethod
    def check_window_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否可能为窗口函数"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return (scanner.search(AMTMark.NAME, AMTMark.PARENTHESIS, "OVER", AMTMark.PARENTHESIS)
                and scanner.get_as_source() in name_set.WINDOW_FUNCTION_NAME_SET)

    @classmethod
    def parse_window_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTWindowExpression:
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
            row_expression = cls.parse_window_row(parenthesis_scanner)
        parenthesis_scanner.close()
        return node.ASTWindowExpression(window_function=window_function,
                                        partition_by=partition_by,
                                        order_by=order_by,
                                        row_expression=row_expression)

    @classmethod
    def parse_condition_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTConditionExpression:
        """解析条件表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)

        def parse_single():
            if scanner.search(AMTMark.PARENTHESIS):
                parenthesis_scanner = scanner.pop_as_children_scanner()
                elements.append(cls.parse_condition_expression(parenthesis_scanner))  # 插入语，子句也应该是一个条件表达式
                parenthesis_scanner.close()
            else:
                elements.append(cls.parse_bool_expression(scanner))

        elements: List[Union[node.ASTConditionExpression, node.ASTBoolExpression, node.ASTLogicalOperator]] = []
        parse_single()  # 解析第 1 个表达式元素
        while scanner.search("AND") or scanner.search("OR"):  # 如果是用 AND 和 OR 连接的多个表达式，则继续解析
            elements.append(cls.parse_logical_operator(scanner))
            parse_single()

        return node.ASTConditionExpression(elements=tuple(elements))

    @classmethod
    def check_case_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否可能为 CASE 表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("CASE")

    @classmethod
    def parse_case_expression(cls, scanner_or_string: Union[TokenScanner, str]
                              ) -> Union[node.ASTCaseConditionExpression, node.ASTCaseValueExpression]:
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
                cases.append(node.ASTCaseConditionItem(when=when_expression, then=case_expression))
            if scanner.search_and_move("ELSE"):
                else_value = cls.parse_general_expression(scanner)
            scanner.match("END")
            return node.ASTCaseConditionExpression(cases=tuple(cases), else_value=else_value)
        # 第 2 种格式的 CASE 表达式
        case_value = cls.parse_general_expression(scanner)
        cases = []
        else_value = None
        while scanner.search_and_move("WHEN"):
            when_expression = cls.parse_general_expression(scanner)
            scanner.match("THEN")
            case_expression = cls.parse_general_expression(scanner)
            cases.append(node.ASTCaseValueItem(when=when_expression, then=case_expression))
        if scanner.search_and_move("ELSE"):
            else_value = cls.parse_general_expression(scanner)
        scanner.match("END")
        return node.ASTCaseValueExpression(case_value=case_value, cases=tuple(cases), else_value=else_value)

    @classmethod
    def check_sub_query_parenthesis(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为子查询的插入语"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return cls.check_select_statement(scanner.get_as_children_scanner())

    @classmethod
    def parse_sub_query_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTSubQueryExpression:
        """解析子查询表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        parenthesis_scanner = scanner.pop_as_children_scanner()
        result = node.ASTSubQueryExpression(statement=cls.parse_select_statement(parenthesis_scanner))
        parenthesis_scanner.close()
        return result

    @classmethod
    def parse_value_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTValueExpression:
        """解析值表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        values = []
        for value_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            values.append(cls.parse_general_expression(value_scanner))
            value_scanner.close()
        return node.ASTValueExpression(values=tuple(values))

    @classmethod
    def _parse_general_parenthesis(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTExpressionBase:
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
                                         maybe_window: bool) -> node.ASTExpressionBase:
        # pylint: disable=R0911
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
                                 maybe_window: bool = True) -> node.ASTExpressionBase:
        """解析一般表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        elements = [cls.parse_general_expression_element(scanner, maybe_window)]
        while cls.check_compute_operator(scanner):
            elements.append(cls.parse_compute_operator(scanner))
            elements.append(cls.parse_general_expression_element(scanner, maybe_window))
        if len(elements) == 1:
            return elements[0]  # 如果只有 1 个元素，则返回该元素的表达式
        return node.ASTComputeExpression(elements=tuple(elements))  # 如果超过 1 个元素，则返回计算表达式（多项式）

    @classmethod
    def check_join_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为关联表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("ON") or scanner.search("USING")

    @classmethod
    def parse_join_on_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTJoinOnExpression:
        """解析 ON 关联表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if not scanner.search_and_move("ON"):
            raise SqlParseError(f"无法解析为 ON 关联表达式: {scanner}")
        return node.ASTJoinOnExpression(condition=cls.parse_condition_expression(scanner))

    @classmethod
    def parse_join_using_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTJoinUsingExpression:
        """解析 USING 关联表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if not scanner.search("USING"):
            raise SqlParseError(f"无法解析为 USING 关联表达式: {scanner}")
        return node.ASTJoinUsingExpression(using_function=cls.parse_function_expression(scanner))

    @classmethod
    def parse_join_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTJoinExpression:
        """解析关联表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if scanner.search("ON"):
            return cls.parse_join_on_expression(scanner)
        if scanner.search("USING"):
            return cls.parse_join_using_expression(scanner)
        raise SqlParseError(f"无法解析为关联表达式: {scanner}")

    @classmethod
    def parse_table_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTTableExpression:
        """解析表表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if cls.check_sub_query_parenthesis(scanner):
            table_name_expression = cls.parse_sub_query_expression(scanner)
        else:
            table_name_expression = cls.parse_table_name_expression(scanner)
        alias_expression = cls.parse_alias_expression(scanner) if cls.check_alias_expression(scanner) else None
        return node.ASTTableExpression(name=table_name_expression, alias=alias_expression)

    @classmethod
    def parse_column_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTColumnExpression:
        """解析列名表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        general_expression = cls.parse_general_expression(scanner)
        alias_expression = cls.parse_alias_expression(scanner) if cls.check_alias_expression(scanner) else None
        return node.ASTColumnExpression(value=general_expression, alias=alias_expression)

    @classmethod
    def check_select_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为 SELECT 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("SELECT")

    @classmethod
    def parse_select_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTSelectClause:
        """解析 SELECT 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("SELECT")
        distinct = scanner.search_and_move("DISTINCT")
        columns = [cls.parse_column_expression(scanner)]
        while scanner.search_and_move(","):
            columns.append(cls.parse_column_expression(scanner))
        return node.ASTSelectClause(distinct=distinct, columns=tuple(columns))

    @classmethod
    def check_from_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为 FROM 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("FROM")

    @classmethod
    def parse_from_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTFromClause:
        """解析 FROM 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("FROM")
        tables = [cls.parse_table_expression(scanner)]
        while scanner.search_and_move(","):
            tables.append(cls.parse_table_expression(scanner))
        return node.ASTFromClause(tables=tuple(tables))

    @classmethod
    def check_lateral_view_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为 LATERAL VIEW 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("LATERAL", "VIEW")

    @classmethod
    def parse_lateral_view_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTLateralViewClause:
        """解析 LATERAL VIEW 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("LATERAL", "VIEW")
        function = cls.parse_function_expression(scanner)
        view_name = scanner.pop_as_source()
        alias = cls.parse_alias_expression(scanner, must_has_as_keyword=True)
        return node.ASTLateralViewClause(function=function, view_name=view_name, alias=alias)

    @classmethod
    def check_join_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为 JOIN 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return cls.check_join_type(scanner)

    @classmethod
    def parse_join_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTJoinClause:
        """解析 JOIN 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        join_type = cls.parse_join_type(scanner)
        table_expression = cls.parse_table_expression(scanner)
        if cls.check_join_expression(scanner):
            join_rule = cls.parse_join_expression(scanner)
        else:
            join_rule = None
        return node.ASTJoinClause(type=join_type, table=table_expression, rule=join_rule)

    @classmethod
    def check_where_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否可能为 WHERE 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("WHERE")

    @classmethod
    def parse_where_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTWhereClause:
        """解析 WHERE 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("WHERE")
        return node.ASTWhereClause(condition=cls.parse_condition_expression(scanner))

    @classmethod
    def check_group_by_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否可能为 GROUP BY 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("GROUP", "BY")

    @classmethod
    def parse_group_by_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTGroupByClause:
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
            return node.ASTGroupingSetsGroupByClause(grouping_list=tuple(grouping_list))

        # 处理一般的 GROUP BY 的语法
        columns = [cls.parse_general_expression(scanner)]
        while scanner.search_and_move(","):
            columns.append(cls.parse_general_expression(scanner))
        with_rollup = False
        if scanner.search_and_move("WITH", "ROLLUP"):
            with_rollup = True
        return node.ASTNormalGroupByClause(columns=tuple(columns), with_rollup=with_rollup)

    @classmethod
    def check_having_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """是否可能为 HAVING 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("HAVING")

    @classmethod
    def parse_having_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTHavingClause:
        """解析 HAVING 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("HAVING")
        return node.ASTHavingClause(condition=cls.parse_condition_expression(scanner))

    @classmethod
    def check_order_by_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """是否可能为 ORDER BY 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("ORDER", "BY")

    @classmethod
    def parse_order_by_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTOrderByClause:
        """解析 ORDER BY 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)

        def parse_single():
            column = cls.parse_general_expression(scanner)
            order = cls.parse_order_type(scanner)
            return node.ASTOrderByItem(column=column, order=order)

        scanner.match("ORDER", "BY")
        columns = [parse_single()]
        while scanner.search_and_move(","):
            columns.append(parse_single())

        return node.ASTOrderByClause(columns=tuple(columns))

    @classmethod
    def check_limit_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """是否可能为 LIMIT 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("LIMIT")

    @classmethod
    def parse_limit_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTLimitClause:
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
        return node.ASTLimitClause(limit=limit_int, offset=offset_int)

    @classmethod
    def _parse_single_with_table(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTWithTable:
        """解析一个 WITH 临时表"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        table_name = unify_name(scanner.pop_as_source())
        scanner.match("AS")
        parenthesis_scanner = scanner.pop_as_children_scanner()
        table_statement = cls.parse_select_statement(parenthesis_scanner, with_clause=node.ASTWithClause.empty())
        parenthesis_scanner.close()
        return node.ASTWithTable(name=table_name, statement=table_statement)

    @classmethod
    def parse_with_clause(cls, scanner_or_string: Union[TokenScanner, str]) -> Optional[node.ASTWithClause]:
        """解析 WITH 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        if scanner.search_and_move("WITH"):
            tables = [cls._parse_single_with_table(scanner)]
            while scanner.search_and_move(","):
                table_statement = cls._parse_single_with_table(scanner)
                tables.append(table_statement)  # 将前置的 WITH 作为当前解析临时表的 WITH 子句
            return node.ASTWithClause(tables=tuple(tables))
        return node.ASTWithClause.empty()

    @classmethod
    def check_select_statement(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否可能为 SELECT 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("SELECT")

    @classmethod
    def parse_single_select_statement(cls, scanner_or_string: Union[TokenScanner, str],
                                      with_clause: Optional[node.ASTWithClause] = None
                                      ) -> node.ASTSingleSelectStatement:
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
        return node.ASTSingleSelectStatement(
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
                               with_clause: Optional[node.ASTWithClause] = None
                               ) -> node.ASTSelectStatement:
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
        return node.ASTUnionSelectStatement(with_clause=with_clause, elements=tuple(result))

    @classmethod
    def _get_config_name_expression(cls, scanner: TokenScanner) -> str:
        """解析配置名称表达式"""
        config_name_list = [scanner.pop_as_source()]
        while scanner.search_and_move("."):
            config_name_list.append(scanner.pop_as_source())
        return ".".join(config_name_list)

    @classmethod
    def parse_config_string_expression(cls, scanner_or_string: Union[TokenScanner, str]
                                       ) -> node.ASTConfigStringExpression:
        """解析配置值为字符串的配置表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        config_name = cls._get_config_name_expression(scanner)
        scanner.match("=")
        config_value = scanner.pop_as_source()
        return node.ASTConfigStringExpression(name=config_name, value=config_value)

    @classmethod
    def parse_column_type_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTColumnTypeExpression:
        """解析 DDL 的字段类型：要求当前指针位置节点为函数名，下一个节点可能为函数参数也可能不是，解析为 SQLColumnType 对象"""
        scanner = cls._unify_input_scanner(scanner_or_string)

        # 解析字段类型名称
        function_name: str = scanner.pop_as_source()

        # 解析字段类型参数
        if scanner.search(AMTMark.PARENTHESIS):
            function_params: List[node.ASTExpressionBase] = []
            for param_scanner in scanner.pop_as_children_scanner_list_split_by(","):
                function_params.append(cls.parse_general_expression(param_scanner))
                param_scanner.close()
            return node.ASTColumnTypeExpression(name=function_name, params=tuple(function_params))
        return node.ASTColumnTypeExpression(name=function_name)

    @classmethod
    def parse_equal_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTEqualExpression:
        """解析等式表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        before_value = cls.parse_general_expression(scanner)
        scanner.match("=")
        after_value = cls.parse_general_expression(scanner)
        return node.ASTEqualExpression(before_value=before_value, after_value=after_value)

    @classmethod
    def check_partition_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否可能为分区表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("PARTITION")

    @classmethod
    def parse_partition_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTPartitionExpression:
        """解析分区表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("PARTITION")
        partition_list = []
        for partition_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            partition_list.append(cls.parse_equal_expression(partition_scanner))
            partition_scanner.close()
        return node.ASTPartitionExpression(partitions=tuple(partition_list))

    @classmethod
    def check_foreign_key_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为外键表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("CONSTRAINT")

    @classmethod
    def parse_foreign_key_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTForeignKeyExpression:
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
        return node.ASTForeignKeyExpression(
            constraint_name=constraint_name,
            slave_columns=tuple(slave_columns),
            master_table_name=master_table_name,
            master_columns=tuple(master_columns),
            on_delete_cascade=on_delete_cascade
        )

    @classmethod
    def parse_index_column(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTIndexColumn:
        """解析索引声明表达式中的字段"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        name = unify_name(scanner.pop_as_source())
        max_length = None
        if scanner.search(AMTMark.PARENTHESIS):
            parenthesis_scanner = scanner.pop_as_children_scanner()
            max_length = int(parenthesis_scanner.pop_as_source())
            parenthesis_scanner.close()
        return node.ASTIndexColumn(name=name, max_length=max_length)

    @classmethod
    def _get_index_columns(cls, scanner: TokenScanner) -> Tuple[node.ASTIndexColumn, ...]:
        """解析索引表达式中的索引字段"""
        columns = []
        for column_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            columns.append(cls.parse_index_column(column_scanner))
            column_scanner.close()
        return tuple(columns)

    @classmethod
    def check_primary_index_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为主键表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("PRIMARY", "KEY")

    @classmethod
    def parse_primary_index_expression(cls, scanner_or_string: Union[TokenScanner, str]
                                       ) -> node.ASTPrimaryIndexExpression:
        """解析主键表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("PRIMARY", "KEY")
        columns = cls._get_index_columns(scanner)
        using = scanner.pop_as_source() if scanner.search_and_move("USING") else None
        comment = scanner.pop_as_source() if scanner.search_and_move("COMMENT") else None
        key_block_size = int(scanner.pop_as_source()) if scanner.search_and_move("KEY_BLOCK_SIZE", "=") else None
        return node.ASTPrimaryIndexExpression(columns=columns, using=using, comment=comment,
                                              key_block_size=key_block_size)

    @classmethod
    def check_unique_index_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为唯一键表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("UNIQUE", "KEY")

    @classmethod
    def parse_unique_index_expression(cls, scanner_or_string: Union[TokenScanner, str]
                                      ) -> node.ASTUniqueIndexExpression:
        """解析唯一键表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("UNIQUE", "KEY")
        name = scanner.pop_as_source()
        columns = cls._get_index_columns(scanner)
        using = scanner.pop_as_source() if scanner.search_and_move("USING") else None
        comment = scanner.pop_as_source() if scanner.search_and_move("COMMENT") else None
        key_block_size = int(scanner.pop_as_source()) if scanner.search_and_move("KEY_BLOCK_SIZE", "=") else None
        return node.ASTUniqueIndexExpression(name=name, columns=columns, using=using, comment=comment,
                                             key_block_size=key_block_size)

    @classmethod
    def check_normal_index_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为一般索引表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("KEY")

    @classmethod
    def parse_normal_index_expression(cls, scanner_or_string: Union[TokenScanner, str]
                                      ) -> node.ASTNormalIndexExpression:
        """解析一般索引表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("KEY")
        name = scanner.pop_as_source()
        columns = cls._get_index_columns(scanner)
        using = scanner.pop_as_source() if scanner.search_and_move("USING") else None
        comment = scanner.pop_as_source() if scanner.search_and_move("COMMENT") else None
        key_block_size = int(scanner.pop_as_source()) if scanner.search_and_move("KEY_BLOCK_SIZE", "=") else None
        return node.ASTNormalIndexExpression(name=name, columns=columns, using=using, comment=comment,
                                             key_block_size=key_block_size)

    @classmethod
    def check_fulltext_expression(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为全文索引表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("FULLTEXT", "KEY")

    @classmethod
    def parse_fulltext_expression(cls, scanner_or_string: Union[TokenScanner, str]
                                  ) -> node.ASTFulltextIndexExpression:
        """解析全文索引表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("FULLTEXT", "KEY")
        name = scanner.pop_as_source()
        columns = cls._get_index_columns(scanner)
        using = scanner.pop_as_source() if scanner.search_and_move("USING") else None
        comment = scanner.pop_as_source() if scanner.search_and_move("COMMENT") else None
        key_block_size = int(scanner.pop_as_source()) if scanner.search_and_move("KEY_BLOCK_SIZE", "=") else None
        return node.ASTFulltextIndexExpression(name=name, columns=columns, using=using, comment=comment,
                                               key_block_size=key_block_size)

    @classmethod
    def parse_define_column_expression(cls, scanner_or_string: Union[TokenScanner, str]
                                       ) -> node.ASTDefineColumnExpression:
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
        default: Optional[node.ASTExpressionBase] = None
        on_update: Optional[node.ASTExpressionBase] = None
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
        return node.ASTDefineColumnExpression(
            column_name=unify_name(column_name),
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
    def check_insert_statement(cls, scanner_or_string: Union[TokenScanner, str]) -> bool:
        """判断是否为 INSERT 语句（已匹配过 WITH 语句才可以调用）"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        return scanner.search("INSERT")

    @classmethod
    def parse_insert_statement(cls, scanner_or_string: Union[TokenScanner, str],
                               with_clause: Optional[node.ASTWithClause]
                               ) -> node.ASTInsertStatement:
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

            return node.ASTInsertValuesStatement(
                with_clause=with_clause,
                insert_type=insert_type,
                table_name=table_name,
                partition=partition,
                columns=tuple(columns) if columns is not None else None,
                values=tuple(values)
            )

        if scanner.search("SELECT"):
            select_statement = cls.parse_select_statement(scanner, with_clause=node.ASTWithClause.empty())
            return node.ASTInsertSelectStatement(
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
    def parse_set_statement(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTSetStatement:
        """解析 SET 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("SET")
        config_name_list = [scanner.pop_as_source()]
        while scanner.search_and_move("."):
            config_name_list.append(scanner.pop_as_source())
        config_name = ".".join(config_name_list)
        scanner.match("=")
        config_value = scanner.pop_as_source()
        return node.ASTSetStatement(config_name=config_name, config_value=config_value)

    @classmethod
    def parse_create_table_statement(cls, scanner_or_string: Union[TokenScanner, str]
                                     ) -> node.ASTCreateTableStatement:
        # pylint: disable=R0912
        # pylint: disable=R0914 忽略本地变量过多的问题
        # pylint: disable=R0915 忽略代码行数过多的问题
        """解析 CREATE TABLE 语句"""
        # 解析字段、索引括号前的部分
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("CREATE", "TABLE")
        if_not_exists = scanner.search_and_move("IF", "NOT", "EXISTS")
        table_name_expression = cls.parse_table_name_expression(scanner)

        # 解析字段和索引
        columns: List[node.ASTDefineColumnExpression] = []
        primary_key: Optional[node.ASTPrimaryIndexExpression] = None
        unique_key: List[node.ASTUniqueIndexExpression] = []
        key: List[node.ASTNormalIndexExpression] = []
        fulltext_key: List[node.ASTFulltextIndexExpression] = []
        foreign_key: List[node.ASTForeignKeyExpression] = []
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
        partitioned_by: List[node.ASTDefineColumnExpression] = []
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
        tblproperties: Optional[List[node.ASTConfigStringExpression]] = []
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
                    tblproperties.append(cls.parse_config_string_expression(group_scanner))
                    group_scanner.close()
            else:
                raise SqlParseError(f"未知的 DDL 表属性: {scanner}")
        scanner.search_and_move(";")

        return node.ASTCreateTableStatement(
            table_name=table_name_expression,
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
    def parse_drop_table_statement(cls, scanner_or_string: Union[TokenScanner, str]) -> node.ASTDropTableStatement:
        """解析 DROP TABLE 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        scanner.match("DROP", "TABLE")
        if_exists = scanner.search_and_move("IF", "EXISTS")
        table_name = cls.parse_table_name_expression(scanner)
        return node.ASTDropTableStatement(if_exists=if_exists, table_name=table_name)

    @classmethod
    def parse_statements(cls, scanner_or_string: Union[TokenScanner, str]) -> List[node.ASTStatementBase]:
        """解析一段 SQL 语句，返回表达式的列表"""
        scanner = cls._unify_input_scanner(scanner_or_string)
        statement_list = []
        for statement_scanner in scanner.split_by(";"):
            # 解析 SET 语句
            if statement_scanner.search("SET"):
                statement_list.append(cls.parse_set_statement(statement_scanner))
                statement_scanner.close()
                continue

            # 解析 DROP TABLE 语句
            if statement_scanner.search("DROP", "TABLE"):
                statement_list.append(cls.parse_drop_table_statement(statement_scanner))
                statement_scanner.close()
                continue

            # 解析 CREATE TABLE 语句
            if statement_scanner.search("CREATE", "TABLE"):
                statement_list.append(cls.parse_create_table_statement(statement_scanner))
                statement_scanner.close()
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


def unify_name(text: Optional[str]) -> Optional[str]:
    """格式化名称标识符：统一剔除当前引号并添加引号"""
    return text.strip("`") if text is not None else None
