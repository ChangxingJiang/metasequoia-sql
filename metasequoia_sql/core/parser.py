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
from metasequoia_sql.core import node, static
from metasequoia_sql.core.sql_type import SQLType
from metasequoia_sql.errors import SqlParseError
from metasequoia_sql.lexical import AMTMark, AMTSingle, FSMMachine

__all__ = ["SQLParser"]

# 输入参数的类型别名
ScannerOrString = Union[TokenScanner, str]

# 两种 CREATE TABLE 语句的通用类型别名
AliasCreateTableStatement = Union[node.ASTCreateTableStatement, node.ASTCreateTableAsStatement]

# 两种 CASE 语句的通用类型别名
AliasCaseExpression = Union[node.ASTCaseConditionExpression, node.ASTCaseValueExpression]

# 表名表达式和子查询表达式
AliasTableExpression = Union[node.ASTTableName, node.ASTSubQueryExpression]

# ---------------------------------------- 一般表达式层级类型 ----------------------------------------

# 元素表达式层级
NodeElementLevel = Union[
    node.ASTColumnNameExpression, node.ASTLiteralExpression, node.ASTWildcardExpression, node.ASTFunctionExpressionBase,
    node.ASTWindowExpression, node.ASTCaseConditionExpression, node.ASTCaseValueExpression, node.ASTSubQueryExpression,
    node.ASTSubValueExpression]

# 下标表达式层级
NodeIndexLevel = Union[NodeElementLevel, node.ASTIndexExpression]

# 一元表达式层级
NodeUnaryLevel = Union[NodeIndexLevel, node.ASTUnaryExpression]

# 异或表达式层级
NodeXorLevel = Union[NodeUnaryLevel, node.ASTXorExpression]

# 单项表达式层级
NodeMonomialLevel = Union[NodeXorLevel, node.ASTMonomialExpression]

# 多项表达式层级
NodePolynomialLevel = Union[NodeMonomialLevel, node.ASTPolynomialExpression]

# 移位表达式层级
NodeShiftLevel = Union[NodePolynomialLevel, node.ASTShiftExpression]

# 按位与表达式层级
NodeBitwiseAndLevel = Union[NodeShiftLevel, node.ASTBitwiseAndExpression]

# 按位或表达式层级
NodeBitwiseOrLevel = Union[NodeBitwiseAndLevel, node.ASTBitwiseOrExpression]

# 关键字条件表达式层级
NodeKeywordConditionLevel = Union[
    NodeBitwiseOrLevel, node.ASTOperatorExpressionBase, node.ASTExistsExpression, node.ASTBetweenExpression]

# 运算符条件表达式层级
NodeOperatorConditionLevel = Union[NodeKeywordConditionLevel, node.ASTOperatorConditionExpression]

# 逻辑否表达式层级
NodeLogicalNotLevel = Union[NodeOperatorConditionLevel, node.ASTLogicalNotExpression]

# 逻辑与表达式层级
NodeLogicalAndLevel = Union[NodeLogicalNotLevel, node.ASTLogicalAndExpression]

# 逻辑异或表达式层级
NodeLogicalXorLevel = Union[NodeLogicalAndLevel, node.ASTLogicalXorExpression]

# 逻辑或表达式层级
NodeLogicalOrLevel = Union[NodeLogicalXorLevel, node.ASTLogicalOrExpression]


class SQLParser:
    # pylint: disable=R0904
    """SQL 语法解析器"""

    @classmethod
    def _build_token_scanner(cls, string: str) -> TokenScanner:
        """构造词法扫描器"""
        return TokenScanner(FSMMachine.parse(string), ignore_space=True, ignore_comment=True)

    @classmethod
    def _unify_input_scanner(cls, scanner_or_string: ScannerOrString,
                             sql_type: SQLType = SQLType.DEFAULT) -> TokenScanner:
        """格式化输入的参数，将字符串格式的 SQL 语句统一为词法扫描器 TokenScanner"""
        if isinstance(scanner_or_string, TokenScanner):
            return scanner_or_string
        if isinstance(scanner_or_string, str):
            if sql_type == SQLType.DB2:
                # 兼容 DB2 的 CURRENT DATE、CURRENT TIME、CURRENT TIMESTAMP 语法
                scanner_or_string = scanner_or_string.replace("CURRENT DATE", "CURRENT_DATE")
                scanner_or_string = scanner_or_string.replace("CURRENT TIME", "CURRENT_TIME")
                scanner_or_string = scanner_or_string.replace("CURRENT TIMESTAMP", "CURRENT_TIMESTAMP")

            if sql_type == SQLType.HIVE:
                # 兼容 HIVE 的 == 语法
                scanner_or_string = scanner_or_string.replace("==", "=")

            return cls._build_token_scanner(scanner_or_string)
        raise SqlParseError(f"未知的参数类型: {scanner_or_string} (type={type(scanner_or_string)})")

    # ------------------------------ 枚举类节点的解析方法 ------------------------------

    @classmethod
    def parse_insert_type(cls, scanner_or_string: ScannerOrString,
                          sql_type: SQLType = SQLType.DEFAULT) -> node.ASTInsertType:
        """解析插入类型"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if scanner.search_and_move("INSERT", "INTO"):
            return node.ASTInsertType(enum=static.EnumInsertType.INSERT_INTO)
        if scanner.search_and_move("INSERT", "IGNORE", "INTO"):
            return node.ASTInsertType(enum=static.EnumInsertType.INSERT_INTO)
        if scanner.search_and_move("INSERT", "OVERWRITE"):
            return node.ASTInsertType(enum=static.EnumInsertType.INSERT_OVERWRITE)
        raise SqlParseError(f"未知的 INSERT 类型: {scanner}")

    @classmethod
    def parse_join_type(cls, scanner_or_string: ScannerOrString,
                        sql_type: SQLType = SQLType.DEFAULT) -> node.ASTJoinType:
        """解析关联类型"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        for join_type in static.EnumJoinType:
            if scanner.search_and_move(*join_type.value):
                return node.ASTJoinType(enum=join_type)
        raise SqlParseError(f"无法解析的关联类型: {scanner}")

    @classmethod
    def parse_order_type(cls, scanner_or_string: ScannerOrString,
                         sql_type: SQLType = SQLType.DEFAULT) -> node.ASTOrderType:
        """解析排序类型"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if scanner.search_and_move("DESC"):
            return node.ASTOrderType(enum=static.EnumOrderType.DESC)
        if scanner.search_and_move("ASC"):
            return node.ASTOrderType(enum=static.EnumOrderType.ASC)
        return node.ASTOrderType(enum=static.EnumOrderType.ASC)

    @classmethod
    def parse_union_type(cls, scanner_or_string: ScannerOrString,
                         sql_type: SQLType = SQLType.DEFAULT) -> node.ASTUnionType:
        """解析组合类型"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        for union_type in static.EnumUnionType:
            if scanner.search_and_move(*union_type.value):
                return node.ASTUnionType(enum=union_type)
        raise SqlParseError(f"无法解析的组合类型: {scanner}")

    @classmethod
    def parse_compare_operator(cls, scanner_or_string: ScannerOrString,
                               sql_type: SQLType = SQLType.DEFAULT) -> node.ASTCompareOperator:
        """解析比较运算符"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        compare_operator = static.COMPARE_OPERATOR_HASH.get(scanner.pop_as_source())
        if compare_operator is None:
            raise SqlParseError(f"无法解析的比较运算符: {scanner}")
        return node.ASTCompareOperator(enum=compare_operator)

    @classmethod
    def parse_compute_operator(cls, scanner_or_string: ScannerOrString,
                               sql_type: SQLType = SQLType.DEFAULT) -> node.ASTComputeOperator:
        """解析计算运算符"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        compute_operator = static.COMPUTE_OPERATOR_HASH.get(scanner.pop_as_source())
        if compute_operator is None:
            raise SqlParseError(f"无法解析的计算运算符: {scanner}")
        return node.ASTComputeOperator(enum=compute_operator)

    @classmethod
    def parse_cast_data_type(cls, scanner_or_string: ScannerOrString,
                             sql_type: SQLType = SQLType.DEFAULT) -> static.EnumCastDataType:
        """解析 CAST 函数表达式中的类型"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        for cast_type in static.EnumCastDataType:
            if scanner.search_and_move(cast_type.value):
                return cast_type
        raise SqlParseError(f"无法解析的 CAST 函数表达式中的类型: {scanner}")

    # ------------------------------ 基础节点的解析方法 ------------------------------

    @classmethod
    def parse_column_name_expression(cls, scanner_or_string: ScannerOrString,
                                     sql_type: SQLType = SQLType.DEFAULT) -> node.ASTColumnNameExpression:
        """解析列名表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if (scanner.search(AMTMark.NAME, ".", AMTMark.NAME) and
                not scanner.search(AMTMark.NAME, ".", AMTMark.NAME, AMTMark.PARENTHESIS)):
            table_name = scanner.pop_as_source()
            scanner.match(".")
            column_name = scanner.pop_as_source()
            return node.ASTColumnNameExpression(
                table_name=unify_name(table_name),
                column_name=unify_name(column_name)
            )
        if (scanner.search(AMTMark.NAME)
                and not scanner.search(AMTMark.NAME, ".")
                and not scanner.search(AMTMark.NAME, AMTMark.PARENTHESIS)):
            return node.ASTColumnNameExpression(
                column_name=unify_name(scanner.pop_as_source())
            )
        raise SqlParseError(f"无法解析为表名表达式: {scanner}")

    @classmethod
    def parse_column_name_expression_maybe_with_array_index(cls, scanner_or_string: ScannerOrString,
                                                            sql_type: SQLType = SQLType.DEFAULT
                                                            ) -> Union[
        node.ASTColumnNameExpression, node.ASTIndexExpression]:
        """解析函数表达式，并解析函数表达式后可能包含的数组下标"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        column_name_expression = cls.parse_column_name_expression(scanner, sql_type=sql_type)
        if not scanner.search(AMTMark.ARRAY_INDEX):
            return column_name_expression  # 如果没有数组下标则直接返回
        # 解析数组下标
        children_scanner = scanner.pop_as_children_scanner()
        idx = cls.parse_bitwise_or_level_node(children_scanner, sql_type=sql_type)
        children_scanner.close()
        return node.ASTIndexExpression(
            array=column_name_expression,
            idx=idx
        )

    @classmethod
    def parse_table_name_expression(cls, scanner_or_string: ScannerOrString,
                                    sql_type: SQLType = SQLType.DEFAULT) -> node.ASTTableName:
        """解析表名表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
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
    def parse_function_name_expression(cls, scanner_or_string: ScannerOrString,
                                       sql_type: SQLType = SQLType.DEFAULT
                                       ) -> node.ASTFunctionName:
        """解析函数名表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
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
    def parse_literal_expression(cls, scanner_or_string: ScannerOrString,
                                 sql_type: SQLType = SQLType.DEFAULT) -> node.ASTLiteralExpression:
        """解析字面值：包含整型字面值、浮点型字面值、字符串型字面值、十六进制型字面值、布尔型字面值、位值型字面值、空值的字面值"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return node.ASTLiteralExpression(value=scanner.pop_as_source())

    @classmethod
    def parse_window_row_item(cls, scanner_or_string: ScannerOrString,
                              sql_type: SQLType = SQLType.DEFAULT) -> node.ASTWindowRowItem:
        """解析窗口函数行限制中的行"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if scanner.search_and_move("CURRENT", "ROW"):
            return node.ASTWindowRowItem(row_type=static.EnumWindowRowType.CURRENT_ROW)
        if scanner.search_and_move("UNBOUNDED"):
            if scanner.search_and_move("PRECEDING"):
                return node.ASTWindowRowItem(row_type=static.EnumWindowRowType.PRECEDING, is_unbounded=True)
            if scanner.search_and_move("FOLLOWING"):
                return node.ASTWindowRowItem(row_type=static.EnumWindowRowType.FOLLOWING, is_unbounded=True)
            raise SqlParseError(f"无法解析的窗口函数限制行: {scanner}")
        row_num = int(scanner.pop_as_source())
        if scanner.search_and_move("PRECEDING"):
            return node.ASTWindowRowItem(row_type=static.EnumWindowRowType.PRECEDING, row_num=row_num)
        if scanner.search_and_move("FOLLOWING"):
            return node.ASTWindowRowItem(row_type=static.EnumWindowRowType.FOLLOWING, row_num=row_num)
        raise SqlParseError(f"无法解析的窗口函数限制行: {scanner}")

    @classmethod
    def parse_window_row(cls, scanner_or_string: ScannerOrString,
                         sql_type: SQLType = SQLType.DEFAULT) -> node.ASTWindowRow:
        """解析窗口语句限制行的表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("ROWS", "BETWEEN")
        from_row = cls.parse_window_row_item(scanner, sql_type=sql_type)
        scanner.match("AND")
        to_row = cls.parse_window_row_item(scanner, sql_type=sql_type)
        return node.ASTWindowRow(from_row=from_row, to_row=to_row)

    @classmethod
    def parse_wildcard_expression(cls, scanner_or_string: ScannerOrString,
                                  sql_type: SQLType = SQLType.DEFAULT) -> node.ASTWildcardExpression:
        """解析通配符表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if scanner.search_and_move("*"):
            return node.ASTWildcardExpression()
        if scanner.search(AMTMark.NAME, ".", "*"):
            schema_name = scanner.pop_as_source()
            scanner.pop()
            scanner.pop()
            return node.ASTWildcardExpression(table_name=schema_name)
        raise SqlParseError("无法解析为通配符表达式")

    @classmethod
    def _get_name(cls, scanner: TokenScanner) -> str:
        """获取名称或别名：如果抽象词法树（AMT）没有 NAME 标记，则抛出异常 TODO 待移除"""
        if not scanner.search(AMTMark.NAME):
            raise SqlParseError(f"无法解析为名称: {scanner}")
        return unify_name(scanner.pop_as_source())

    @classmethod
    def parse_alias_expression(cls, scanner_or_string: ScannerOrString,
                               sql_type: SQLType = SQLType.DEFAULT) -> Optional[node.ASTAlisa]:
        """解析别名表达式：如果当前位置是别名表达式则返回别名表达式节点，否则返回 None"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if not scanner.search({"AS", AMTMark.NAME}):
            return None  # 当前位置不是别名表达式
        scanner.search_and_move("AS")
        return node.ASTAlisa(name=cls._get_name(scanner))

    @classmethod
    def parse_multi_alias_expression(cls, scanner_or_string: ScannerOrString,
                                     sql_type: SQLType = SQLType.DEFAULT) -> node.ASTMultiAlisa:
        """解析多个别名表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("AS")
        names = [cls._get_name(scanner)]
        while scanner.search_and_move(","):
            names.append(cls._get_name(scanner))
        return node.ASTMultiAlisa(names=tuple(names))

    # ------------------------------ SELECT 语句节点的解析方法 ------------------------------

    @classmethod
    def parse_extract_function_expression(cls, scanner_or_string: ScannerOrString,
                                          sql_type: SQLType = SQLType.DEFAULT
                                          ) -> node.ASTExtractFunctionExpression:
        """解析 EXTRACT 函数表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        extract_name = cls.parse_bitwise_or_level_node(scanner, sql_type=sql_type)
        scanner.match("FROM")
        column_expression = cls.parse_bitwise_or_level_node(scanner, sql_type=sql_type)
        scanner.close()
        return node.ASTExtractFunctionExpression(extract_name=extract_name, column_expression=column_expression)

    @classmethod
    def parse_cast_function_expression(cls, scanner_or_string: ScannerOrString,
                                       sql_type: SQLType = SQLType.DEFAULT
                                       ) -> node.ASTCastFunctionExpression:
        """解析 CAST 函数表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        column_expression = cls.parse_bitwise_or_level_node(scanner, sql_type=sql_type)
        scanner.match("AS")
        signed = scanner.search_and_move("SIGNED")
        cast_type = cls.parse_cast_data_type(scanner, sql_type=sql_type)
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
    def parse_if_function_expression(cls, scanner_or_string: ScannerOrString,
                                     sql_type: SQLType = SQLType.DEFAULT
                                     ) -> node.ASTNormalFunctionExpression:
        """解析 IF 函数表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        function_params: List[NodeLogicalOrLevel] = []
        first_param = True
        for param_scanner in scanner.split_by(","):
            if first_param is True:
                function_params.append(cls.parse_logical_or_level(param_scanner, sql_type=sql_type))
                first_param = False
            else:
                function_params.append(cls.parse_logical_or_level(param_scanner, sql_type=sql_type))
            param_scanner.close()
        return node.ASTNormalFunctionExpression(name=node.ASTFunctionName(function_name="IF"),
                                                params=tuple(function_params))

    @classmethod
    def parse_function_expression(cls, scanner_or_string: ScannerOrString, sql_type: SQLType = SQLType.DEFAULT
                                  ) -> Union[node.ASTFunctionExpressionBase]:
        """解析函数表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        function_name = cls.parse_function_name_expression(scanner, sql_type=sql_type)

        if function_name.function_name.upper() == "CAST":
            return cls.parse_cast_function_expression(scanner.pop_as_children_scanner(), sql_type=sql_type)
        if function_name.function_name.upper() == "EXTRACT":
            return cls.parse_extract_function_expression(scanner.pop_as_children_scanner(), sql_type=sql_type)
        if function_name.function_name.upper() == "IF":
            return cls.parse_if_function_expression(scanner.pop_as_children_scanner(), sql_type=sql_type)

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

        function_params: List[NodeLogicalOrLevel] = []
        for param_scanner in parenthesis_scanner.split_by(","):
            function_params.append(cls.parse_logical_or_level(param_scanner, sql_type=sql_type))
            if not param_scanner.is_finish:
                raise SqlParseError(f"无法解析函数参数: {param_scanner}")

        parenthesis_scanner.close()

        if (function_name.schema_name is None
                and function_name.function_name.upper() in name_set.AGGREGATION_FUNCTION_NAME_SET):
            return node.ASTAggregationFunction(
                name=function_name,
                params=tuple(function_params),
                is_distinct=is_distinct)
        return node.ASTNormalFunctionExpression(
            name=function_name,
            params=tuple(function_params))

    @classmethod
    def parse_function_expression_maybe_with_array_index(
            cls,
            scanner_or_string: ScannerOrString,
            sql_type: SQLType = SQLType.DEFAULT
    ) -> Union[node.ASTFunctionExpressionBase, node.ASTIndexExpression]:
        """解析函数表达式，并解析函数表达式后可能包含的数组下标"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        array_expression = cls.parse_function_expression(scanner, sql_type=sql_type)
        if not scanner.search(AMTMark.ARRAY_INDEX):
            return array_expression  # 如果没有数组下标则直接返回
        # 解析数组下标
        children_scanner = scanner.pop_as_children_scanner()
        idx = cls.parse_bitwise_or_level_node(children_scanner, sql_type=sql_type)
        children_scanner.close()
        return node.ASTIndexExpression(
            array=array_expression,
            idx=idx
        )

    @classmethod
    def parse_in_parenthesis(cls, scanner_or_string: ScannerOrString,
                             sql_type: SQLType = SQLType.DEFAULT) -> NodeElementLevel:
        """解析 IN 关键字后的插入语：插入语可能为子查询或值表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if scanner.get_as_children_scanner().search({"SELECT", "WITH"}):
            return cls.parse_sub_query_expression(scanner, sql_type=sql_type)
        return cls.parse_value_expression(scanner, sql_type=sql_type)

    @classmethod
    def parse_window_expression(cls, scanner_or_string: ScannerOrString,
                                sql_type: SQLType = SQLType.DEFAULT) -> node.ASTWindowExpression:
        """解析窗口函数"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        # 解析函数（因为这个函数可能是 UDF 函数，所以不作限制）
        window_function = cls.parse_function_expression_maybe_with_array_index(scanner, sql_type=sql_type)
        partition_by_columns = []
        order_by_columns = []
        row_expression = None
        scanner.match("OVER")
        parenthesis_scanner = scanner.pop_as_children_scanner()
        if parenthesis_scanner.search_and_move("PARTITION", "BY"):
            partition_by_columns = [cls.parse_bitwise_or_level_node(parenthesis_scanner,
                                                                    maybe_window=False, sql_type=sql_type)]
            while parenthesis_scanner.search_and_move(","):
                partition_by_columns.append(cls.parse_bitwise_or_level_node(parenthesis_scanner,
                                                                            maybe_window=False, sql_type=sql_type))
        if parenthesis_scanner.search_and_move("ORDER", "BY"):
            order_by_columns = [cls.parse_order_by_item(parenthesis_scanner, sql_type=sql_type)]
            while parenthesis_scanner.search_and_move(","):
                order_by_columns.append(cls.parse_order_by_item(parenthesis_scanner, sql_type=sql_type))
        if parenthesis_scanner.search("ROWS", "BETWEEN"):
            row_expression = cls.parse_window_row(parenthesis_scanner, sql_type=sql_type)
        parenthesis_scanner.close()
        return node.ASTWindowExpression(window_function=window_function,
                                        partition_by_columns=tuple(partition_by_columns),
                                        order_by_columns=tuple(order_by_columns),
                                        row_expression=row_expression)

    @classmethod
    def parse_case_expression(cls, scanner_or_string: ScannerOrString,
                              sql_type: SQLType = SQLType.DEFAULT
                              ) -> AliasCaseExpression:
        """解析 CASE 表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("CASE")
        if scanner.search("WHEN"):
            # 第 1 种格式的 CASE 表达式
            cases = []
            else_value = None
            while scanner.search_and_move("WHEN"):
                when_expression = cls.parse_logical_or_level(scanner, sql_type=sql_type)
                scanner.match("THEN")
                case_expression = cls.parse_logical_or_level(scanner, sql_type=sql_type)
                cases.append(node.ASTCaseConditionItem(when=when_expression, then=case_expression))
            if scanner.search_and_move("ELSE"):
                else_value = cls.parse_logical_or_level(scanner)
            scanner.match("END")
            return node.ASTCaseConditionExpression(
                cases=tuple(cases),
                else_value=else_value
            )

        # 第 2 种格式的 CASE 表达式
        case_value = cls.parse_logical_or_level(scanner, sql_type=sql_type)
        cases = []
        else_value = None
        while scanner.search_and_move("WHEN"):
            when_expression = cls.parse_logical_or_level(scanner, sql_type=sql_type)
            scanner.match("THEN")
            case_expression = cls.parse_logical_or_level(scanner, sql_type=sql_type)
            cases.append(node.ASTCaseValueItem(when=when_expression, then=case_expression))
        if scanner.search_and_move("ELSE"):
            else_value = cls.parse_logical_or_level(scanner, sql_type=sql_type)
        scanner.match("END")
        return node.ASTCaseValueExpression(
            case_value=case_value,
            cases=tuple(cases),
            else_value=else_value
        )

    @classmethod
    def parse_sub_query_expression(cls, scanner_or_string: ScannerOrString,
                                   sql_type: SQLType = SQLType.DEFAULT) -> node.ASTSubQueryExpression:
        """解析子查询表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        parenthesis_scanner = scanner.pop_as_children_scanner()
        result = node.ASTSubQueryExpression(
            statement=cls.parse_select_statement(parenthesis_scanner, sql_type=sql_type)
        )
        parenthesis_scanner.close()
        return result

    @classmethod
    def parse_value_expression(cls, scanner_or_string: ScannerOrString,
                               sql_type: SQLType = SQLType.DEFAULT) -> node.ASTSubValueExpression:
        """解析值表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        values = []
        for value_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            values.append(cls.parse_bitwise_or_level_node(value_scanner, sql_type=sql_type))
            value_scanner.close()
        return node.ASTSubValueExpression(values=tuple(values))

    @classmethod
    def parse_general_parenthesis_expression(cls, scanner_or_string: ScannerOrString,
                                             sql_type: SQLType = SQLType.DEFAULT) -> NodeLogicalOrLevel:
        """解析一般表达式中的插入语"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        # 处理插入语中是子查询的情况
        if scanner.get_as_children_scanner().search({"SELECT", "WITH"}):
            return cls.parse_sub_query_expression(scanner, sql_type=sql_type)
        # 处理插入语中是一般表达式的情况：如果有嵌套的插入语，那么会自动压缩为一层
        parenthesis_scanner = scanner.pop_as_children_scanner()
        result = cls.parse_logical_or_level(parenthesis_scanner, sql_type=sql_type)
        parenthesis_scanner.close()
        return result

    @classmethod
    def parse_element_level_node(cls, scanner_or_string: ScannerOrString,
                                 maybe_window: bool,
                                 sql_type: SQLType = SQLType.DEFAULT) -> NodeLogicalOrLevel:
        # pylint: disable=R0911
        """解析元素表达式层级（因为可能包含插入语，所以返回值类型是一般表达式）"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if scanner.search(AMTMark.PARENTHESIS):  # 处理包含插入语的情况
            return cls.parse_general_parenthesis_expression(scanner, sql_type=sql_type)
        if scanner.search("CASE"):
            return cls.parse_case_expression(scanner, sql_type=sql_type)
        if maybe_window and scanner.search(AMTMark.NAME, AMTMark.PARENTHESIS, "OVER", AMTMark.PARENTHESIS):
            return cls.parse_window_expression(scanner, sql_type=sql_type)
        if (scanner.search(AMTMark.NAME, AMTMark.PARENTHESIS) or
                scanner.search(AMTMark.NAME, ".", AMTMark.NAME, AMTMark.PARENTHESIS)):
            return cls.parse_function_expression_maybe_with_array_index(scanner, sql_type=sql_type)
        if scanner.search(AMTMark.LITERAL):
            return cls.parse_literal_expression(scanner, sql_type=sql_type)
        if ((scanner.search(AMTMark.NAME, ".", AMTMark.NAME)
             and not scanner.search(AMTMark.NAME, ".", AMTMark.NAME, AMTMark.PARENTHESIS))
                or (scanner.search(AMTMark.NAME)
                    and not scanner.search(AMTMark.NAME, ".")
                    and not scanner.search(AMTMark.NAME, AMTMark.PARENTHESIS))):
            return cls.parse_column_name_expression_maybe_with_array_index(scanner, sql_type=sql_type)
        if scanner.search("*") or scanner.search(AMTMark.NAME, ".", "*"):
            return cls.parse_wildcard_expression(scanner, sql_type=sql_type)
        raise SqlParseError(f"未知的元素表达式元素: {scanner}")

    @classmethod
    def parse_unary_level_node(cls, scanner_or_string: ScannerOrString,
                               maybe_window: bool,
                               sql_type: SQLType = SQLType.DEFAULT) -> NodeUnaryLevel:
        """解析一元表达式层级"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if scanner.get_as_source() in static.get_unary_operator_set(sql_type):
            unary_operator = cls.parse_compute_operator(scanner, sql_type=sql_type)
            return node.ASTUnaryExpression(
                operator=unary_operator,
                expression=cls.parse_unary_level_node(scanner, maybe_window=maybe_window, sql_type=sql_type)
            )
        return cls.parse_element_level_node(scanner, maybe_window=maybe_window, sql_type=sql_type)

    @classmethod
    def parse_xor_level_node(cls, scanner_or_string: ScannerOrString,
                             maybe_window: bool,
                             sql_type: SQLType = SQLType.DEFAULT) -> NodeXorLevel:
        """解析异或表达式层级"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        before_value = cls.parse_unary_level_node(scanner, maybe_window=maybe_window, sql_type=sql_type)
        while scanner.search_and_move("^"):
            # 在当前匹配结果的基础上，不断尝试匹配异或号，从而支持多个相连的异或号
            after_value = cls.parse_unary_level_node(scanner, maybe_window=maybe_window, sql_type=sql_type)
            before_value = node.ASTXorExpression(
                before_value=before_value,
                after_value=after_value
            )
        return before_value

    @classmethod
    def parse_monomial_level_node(cls, scanner_or_string: ScannerOrString,
                                  maybe_window: bool,
                                  sql_type: SQLType = SQLType.DEFAULT) -> NodeMonomialLevel:
        """解析单项表达式层级"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        before_value = cls.parse_xor_level_node(scanner, maybe_window=maybe_window, sql_type=sql_type)
        while scanner.get_as_source() in {"*", "/", "%", "MOD", "DIV"}:
            # 在当前匹配结果的基础上，不断尝试匹配乘号、除号和取模号，从而支持包含多个元素的乘积
            operator = cls.parse_compute_operator(scanner, sql_type=sql_type)
            after_value = cls.parse_xor_level_node(scanner, maybe_window=maybe_window, sql_type=sql_type)
            before_value = node.ASTMonomialExpression(
                before_value=before_value,
                operator=operator,
                after_value=after_value
            )
        return before_value

    @classmethod
    def parse_polynomial_level_node(cls, scanner_or_string: ScannerOrString,
                                    maybe_window: bool,
                                    sql_type: SQLType = SQLType.DEFAULT) -> NodePolynomialLevel:
        """解析多项式表达式层级"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        before_value = cls.parse_monomial_level_node(scanner, maybe_window=maybe_window, sql_type=sql_type)
        while scanner.search({"+", "-"}):
            operator = cls.parse_compute_operator(scanner, sql_type=sql_type)
            after_value = cls.parse_monomial_level_node(scanner, maybe_window=maybe_window, sql_type=sql_type)
            before_value = node.ASTPolynomialExpression(
                before_value=before_value,
                operator=operator,
                after_value=after_value
            )
        return before_value

    @classmethod
    def parse_shift_level_node(cls, scanner_or_string: ScannerOrString,
                               maybe_window: bool,
                               sql_type: SQLType = SQLType.DEFAULT) -> NodeShiftLevel:
        """解析移位表达式层级"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        before_value = cls.parse_polynomial_level_node(scanner, maybe_window=maybe_window, sql_type=sql_type)
        while scanner.get_as_source() in {"<<", ">>"}:
            operator = cls.parse_compute_operator(scanner, sql_type=sql_type)
            after_value = cls.parse_polynomial_level_node(scanner, maybe_window=maybe_window, sql_type=sql_type)
            before_value = node.ASTShiftExpression(
                before_value=before_value,
                operator=operator,
                after_value=after_value
            )
        return before_value

    @classmethod
    def parse_bitwise_and_level_node(cls, scanner_or_string: ScannerOrString,
                                     maybe_window: bool,
                                     sql_type: SQLType = SQLType.DEFAULT) -> NodeBitwiseAndLevel:
        """解析按位与层级表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        before_value = cls.parse_shift_level_node(scanner, maybe_window=maybe_window, sql_type=sql_type)
        while scanner.search_and_move("&"):
            after_value = cls.parse_shift_level_node(scanner, maybe_window=maybe_window, sql_type=sql_type)
            before_value = node.ASTBitwiseAndExpression(
                before_value=before_value,
                after_value=after_value
            )
        return before_value

    @classmethod
    def parse_bitwise_or_level_node(cls, scanner_or_string: ScannerOrString,
                                    sql_type: SQLType = SQLType.DEFAULT,
                                    maybe_window: bool = True) -> NodeBitwiseOrLevel:
        """解析按位或层级表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        before_value = cls.parse_bitwise_and_level_node(scanner, maybe_window=maybe_window, sql_type=sql_type)
        while scanner.search_and_move("|"):
            after_value = cls.parse_bitwise_and_level_node(scanner, maybe_window=maybe_window, sql_type=sql_type)
            before_value = node.ASTBitwiseOrExpression(
                before_value=before_value,
                after_value=after_value
            )
        return before_value

    @classmethod
    def parse_keyword_condition_level_node(cls, scanner_or_string: ScannerOrString,
                                           sql_type: SQLType = SQLType.DEFAULT,
                                           before_value: Optional[NodeKeywordConditionLevel] = None
                                           ) -> NodeKeywordConditionLevel:
        # pylint: disable=R0911
        """解析关键字条件表达式（不包含前置 NOT，但包含中间的 NOT）

        Parameters
        ----------
        scanner_or_string : ScannerOrString
            扫描器
        before_value : Optional[NodeKeywordConditionLevel], default = None
            已经遍历的上一个关键字条件表达式，用于递归，在第一次时置为 None 即可
        sql_type : SQLType
            SQL 类型
        """
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)

        # 首先尝试解析第一个关键字条件表达式
        if before_value is None and scanner.search_and_move("EXISTS"):
            # 正在解析第一个关键字表达式，且开头的关键字表达式为 EXISTS 语句
            value = cls.parse_sub_query_expression(scanner, sql_type=sql_type)
            result_value = node.ASTExistsExpression(value=value)
        else:
            if before_value is None:
                # 如果正在解析第一个关键字表达式，则解析按位或表达式或更低等级表达式作为关键字之前的部分
                before_value = cls.parse_bitwise_or_level_node(scanner, sql_type=sql_type)

            # 解析可能存在于关键字之间的 NOT
            is_not = scanner.search_and_move(static.get_not_operator_set(sql_type))

            if scanner.search_and_move("BETWEEN"):
                from_value = cls.parse_bitwise_or_level_node(scanner, sql_type=sql_type)
                scanner.match("AND")
                to_value = cls.parse_bitwise_or_level_node(scanner, sql_type=sql_type)
                result_value = node.ASTBetweenExpression(
                    is_not=is_not,
                    before_value=before_value,
                    from_value=from_value,
                    to_value=to_value
                )
            elif scanner.search_and_move("IS"):
                is_not = is_not or scanner.search_and_move("NOT")
                after_value = cls.parse_bitwise_or_level_node(scanner, sql_type=sql_type)
                result_value = node.ASTIsExpression(
                    is_not=is_not,
                    before_value=before_value,
                    after_value=after_value
                )
            elif scanner.search_and_move("IN"):
                after_value = cls.parse_in_parenthesis(scanner, sql_type=sql_type)
                result_value = node.ASTInExpression(
                    is_not=is_not,
                    before_value=before_value,
                    after_value=after_value
                )
            elif scanner.search_and_move("LIKE"):
                after_value = cls.parse_bitwise_or_level_node(scanner, sql_type=sql_type)
                result_value = node.ASTLikeExpression(
                    is_not=is_not,
                    before_value=before_value,
                    after_value=after_value
                )
            elif scanner.search_and_move("RLIKE"):
                after_value = cls.parse_bitwise_or_level_node(scanner, sql_type=sql_type)
                result_value = node.ASTRlikeExpression(
                    is_not=is_not,
                    before_value=before_value,
                    after_value=after_value
                )
            elif scanner.search_and_move("REGEXP"):
                after_value = cls.parse_bitwise_or_level_node(scanner, sql_type=sql_type)
                result_value = node.ASTRegexpExpression(
                    is_not=is_not,
                    before_value=before_value,
                    after_value=after_value
                )
            else:
                # 没有关键字表达式，直接返回按位或表达式或更低等级表达式
                return before_value

        # 如果后续是连续的关键字条件表达式的关键字，则将当前关键字表达式作为下一个关键字表达式的 before_value 继续解析
        if scanner.get_as_source() in {"NOT", "BETWEEN", "IS", "IN", "LIKE", "RLIKE", "REGEXP"}:
            return cls.parse_keyword_condition_level_node(scanner, before_value=result_value, sql_type=sql_type)

        # 如果后续不是关键字条件表达式的关键字，则直接返回当前的关键字条件表达式
        return result_value

    @classmethod
    def parse_operator_condition_level(cls, scanner_or_string: ScannerOrString,
                                       sql_type: SQLType = SQLType.DEFAULT) -> NodeOperatorConditionLevel:
        """解析运算符条件表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        before_value = cls.parse_keyword_condition_level_node(scanner, sql_type=sql_type)
        while scanner.search(static.COMPARE_OPERATOR_SET):
            compare_operator = cls.parse_compare_operator(scanner, sql_type=sql_type)
            after_value = cls.parse_keyword_condition_level_node(scanner, sql_type=sql_type)
            before_value = node.ASTOperatorConditionExpression(
                operator=compare_operator,
                before_value=before_value,
                after_value=after_value
            )
        return before_value

    @classmethod
    def parse_logical_not_level(cls, scanner_or_string: ScannerOrString,
                                sql_type: SQLType = SQLType.DEFAULT) -> NodeLogicalNotLevel:
        """解析逻辑否表达式层级"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if scanner.search_and_move(static.get_not_operator_set(sql_type)):
            return node.ASTLogicalNotExpression(
                expression=cls.parse_logical_not_level(scanner, sql_type=sql_type)
            )
        return cls.parse_operator_condition_level(scanner, sql_type=sql_type)

    @classmethod
    def parse_logical_and_level(cls, scanner_or_string: ScannerOrString,
                                sql_type: SQLType = SQLType.DEFAULT) -> NodeLogicalAndLevel:
        """解析逻辑与表达式层级"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        before_value = cls.parse_logical_not_level(scanner, sql_type=sql_type)
        while scanner.search_and_move({"AND", "&&"}):
            after_value = cls.parse_logical_not_level(scanner, sql_type=sql_type)
            before_value = node.ASTLogicalAndExpression(
                before_value=before_value,
                after_value=after_value
            )
        return before_value

    @classmethod
    def parse_logical_xor_level(cls, scanner_or_string: ScannerOrString,
                                sql_type: SQLType = SQLType.DEFAULT) -> NodeLogicalXorLevel:
        """解析逻辑异或表达式层级"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        before_value = cls.parse_logical_and_level(scanner, sql_type=sql_type)
        while scanner.search_and_move("XOR"):
            after_value = cls.parse_logical_and_level(scanner, sql_type=sql_type)
            before_value = node.ASTLogicalXorExpression(
                before_value=before_value,
                after_value=after_value
            )
        return before_value

    @classmethod
    def parse_logical_or_level(cls, scanner_or_string: ScannerOrString,
                               sql_type: SQLType = SQLType.DEFAULT) -> NodeLogicalOrLevel:
        """解析逻辑或表达式层级"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        before_value = cls.parse_logical_xor_level(scanner, sql_type=sql_type)
        while scanner.search_and_move({"OR", "||"}):
            after_value = cls.parse_logical_xor_level(scanner, sql_type=sql_type)
            before_value = node.ASTLogicalOrExpression(
                before_value=before_value,
                after_value=after_value
            )
        return before_value

    @classmethod
    def parse_join_on_expression(cls, scanner_or_string: ScannerOrString,
                                 sql_type: SQLType = SQLType.DEFAULT) -> node.ASTJoinOnExpression:
        """解析 ON 关联表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if not scanner.search_and_move("ON"):
            raise SqlParseError(f"无法解析为 ON 关联表达式: {scanner}")
        return node.ASTJoinOnExpression(condition=cls.parse_logical_or_level(scanner, sql_type=sql_type))

    @classmethod
    def parse_join_using_expression(cls, scanner_or_string: ScannerOrString,
                                    sql_type: SQLType = SQLType.DEFAULT) -> node.ASTJoinUsingExpression:
        """解析 USING 关联表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if not scanner.search("USING"):
            raise SqlParseError(f"无法解析为 USING 关联表达式: {scanner}")
        return node.ASTJoinUsingExpression(using_function=cls.parse_function_expression(scanner, sql_type=sql_type))

    @classmethod
    def parse_join_expression(cls, scanner_or_string: ScannerOrString,
                              sql_type: SQLType = SQLType.DEFAULT) -> node.ASTJoinExpression:
        """解析关联表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if scanner.search("ON"):
            return cls.parse_join_on_expression(scanner, sql_type=sql_type)
        if scanner.search("USING"):
            return cls.parse_join_using_expression(scanner, sql_type=sql_type)
        raise SqlParseError(f"无法解析为关联表达式: {scanner}")

    @classmethod
    def parse_type_table_expression(cls, scanner_or_string: ScannerOrString,
                                    sql_type: SQLType = SQLType.DEFAULT) -> AliasTableExpression:
        """解析表表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if scanner.get_as_children_scanner().search({"SELECT", "WITH"}):
            return cls.parse_sub_query_expression(scanner, sql_type=sql_type)
        if scanner.search(AMTMark.PARENTHESIS):  # 额外的插入语（因为只有一个元素，所以直接递归解析即可）
            return cls.parse_type_table_expression(scanner.pop_as_children_scanner(), sql_type=sql_type)
        return cls.parse_table_name_expression(scanner, sql_type=sql_type)

    @classmethod
    def parse_table_expression(cls, scanner_or_string: ScannerOrString,
                               sql_type: SQLType = SQLType.DEFAULT) -> node.ASTFromTable:
        """解析 FROM 和 JOIN 子句元素：包含别名的表表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        name_expression = cls.parse_type_table_expression(scanner, sql_type=sql_type)
        alias_expression = cls.parse_alias_expression(scanner, sql_type=sql_type)
        return node.ASTFromTable(name=name_expression, alias=alias_expression)

    @classmethod
    def parse_column_expression(cls, scanner_or_string: ScannerOrString,
                                sql_type: SQLType = SQLType.DEFAULT) -> node.ASTSelectColumn:
        """解析列名表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        general_expression = cls.parse_logical_or_level(scanner, sql_type=sql_type)
        alias_expression = cls.parse_alias_expression(scanner, sql_type=sql_type)
        return node.ASTSelectColumn(value=general_expression, alias=alias_expression)

    @classmethod
    def parse_select_clause(cls, scanner_or_string: ScannerOrString,
                            sql_type: SQLType = SQLType.DEFAULT) -> node.ASTSelectClause:
        """解析 SELECT 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("SELECT")
        distinct = scanner.search_and_move("DISTINCT")
        columns = [cls.parse_column_expression(scanner, sql_type=sql_type)]
        while scanner.search_and_move(","):
            columns.append(cls.parse_column_expression(scanner, sql_type=sql_type))
        return node.ASTSelectClause(distinct=distinct, columns=tuple(columns))

    @classmethod
    def parse_from_clause(cls, scanner_or_string: ScannerOrString,
                          sql_type: SQLType = SQLType.DEFAULT) -> node.ASTFromClause:
        """解析 FROM 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("FROM")
        tables = [cls.parse_table_expression(scanner, sql_type=sql_type)]
        while scanner.search_and_move(","):
            tables.append(cls.parse_table_expression(scanner, sql_type=sql_type))
        return node.ASTFromClause(tables=tuple(tables))

    @classmethod
    def parse_lateral_view_clause(cls, scanner_or_string: ScannerOrString,
                                  sql_type: SQLType = SQLType.DEFAULT) -> node.ASTLateralViewClause:
        """解析 LATERAL VIEW 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("LATERAL", "VIEW")
        outer = scanner.search_and_move("OUTER")
        function = cls.parse_function_expression(scanner, sql_type=sql_type)
        view_name = scanner.pop_as_source()
        alias = cls.parse_multi_alias_expression(scanner, sql_type=sql_type)
        return node.ASTLateralViewClause(outer=outer, function=function, view_name=view_name, alias=alias)

    @classmethod
    def parse_join_clause(cls, scanner_or_string: ScannerOrString,
                          sql_type: SQLType = SQLType.DEFAULT) -> node.ASTJoinClause:
        """解析 JOIN 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        join_type = cls.parse_join_type(scanner, sql_type=sql_type)
        table_expression = cls.parse_table_expression(scanner, sql_type=sql_type)
        if scanner.search({"ON", "USING"}):
            join_rule = cls.parse_join_expression(scanner, sql_type=sql_type)
        else:
            join_rule = None
        return node.ASTJoinClause(type=join_type, table=table_expression, rule=join_rule)

    @classmethod
    def parse_where_clause(cls, scanner_or_string: ScannerOrString,
                           sql_type: SQLType = SQLType.DEFAULT) -> node.ASTWhereClause:
        """解析 WHERE 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("WHERE")
        return node.ASTWhereClause(condition=cls.parse_logical_or_level(scanner, sql_type=sql_type))

    @classmethod
    def parse_grouping_sets(cls, scanner_or_string: ScannerOrString,
                            sql_type: SQLType = SQLType.DEFAULT) -> node.ASTGroupingSets:
        """解析 GROUP BY 子句的元素"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("GROUPING", "SETS")
        grouping_list = []
        for grouping_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            if grouping_scanner.search(AMTMark.PARENTHESIS):
                parenthesis_scanner_list = grouping_scanner.pop_as_children_scanner_list_split_by(",")
                columns_list = []
                for parenthesis_scanner in parenthesis_scanner_list:
                    columns_list.append(cls.parse_bitwise_or_level_node(parenthesis_scanner, sql_type=sql_type))
                    parenthesis_scanner.close()
                grouping_list.append(tuple(columns_list))
            else:
                grouping_list.append(
                    tuple([cls.parse_bitwise_or_level_node(grouping_scanner, sql_type=sql_type)]))
            grouping_scanner.close()
        return node.ASTGroupingSets(grouping_list=tuple(grouping_list))

    @classmethod
    def parse_group_by_clause(cls, scanner_or_string: ScannerOrString,
                              sql_type: SQLType = SQLType.DEFAULT) -> node.ASTGroupByClause:
        """解析 GROUP BY 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("GROUP", "BY")
        columns = []
        if not scanner.search("GROUPING", "SETS"):
            # 如果当 GROUP BY 子句中直接就是 GROUPING SETS 时，则不尝试解析字段
            columns.append(cls.parse_bitwise_or_level_node(scanner, sql_type=sql_type))
            while scanner.search_and_move(","):
                columns.append(cls.parse_bitwise_or_level_node(scanner, sql_type=sql_type))
        if scanner.search("GROUPING", "SETS"):
            grouping_sets = cls.parse_grouping_sets(scanner, sql_type=sql_type)
        else:
            grouping_sets = None
        with_cube = scanner.search_and_move("WITH", "CUBE")
        with_rollup = scanner.search_and_move("WITH", "ROLLUP")
        return node.ASTGroupByClause(
            columns=tuple(columns),
            grouping_sets=grouping_sets,
            with_cube=with_cube,
            with_rollup=with_rollup
        )

    @classmethod
    def parse_having_clause(cls, scanner_or_string: ScannerOrString,
                            sql_type: SQLType = SQLType.DEFAULT) -> node.ASTHavingClause:
        """解析 HAVING 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("HAVING")
        return node.ASTHavingClause(condition=cls.parse_logical_or_level(scanner, sql_type=sql_type))

    @classmethod
    def parse_order_by_item(cls, scanner: TokenScanner,
                            sql_type: SQLType = SQLType.DEFAULT) -> node.ASTOrderByColumn:
        """解析 ORDER BY 子句的元素"""
        column = cls.parse_bitwise_or_level_node(scanner, sql_type=sql_type)
        order = cls.parse_order_type(scanner, sql_type=sql_type)
        nulls_first = scanner.search_and_move("NULLS", "FIRST")
        nulls_last = scanner.search_and_move("NULLS", "LAST")
        if nulls_first is True and nulls_last is True:
            raise SqlParseError("同时定义了 NULLS FIRST 和 NULLS LAST")
        return node.ASTOrderByColumn(
            column=column,
            order=order,
            nulls_first=nulls_first,
            nulls_last=nulls_last
        )

    @classmethod
    def parse_order_by_clause(cls, scanner_or_string: ScannerOrString,
                              sql_type: SQLType = SQLType.DEFAULT) -> node.ASTOrderByClause:
        """解析 ORDER BY 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("ORDER", "BY")
        columns = [cls.parse_order_by_item(scanner, sql_type=sql_type)]
        while scanner.search_and_move(","):
            columns.append(cls.parse_order_by_item(scanner, sql_type=sql_type))
        return node.ASTOrderByClause(columns=tuple(columns))

    @classmethod
    def parse_sort_by_clause(cls, scanner_or_string: ScannerOrString,
                             sql_type: SQLType = SQLType.DEFAULT) -> node.ASTSortByClause:
        """解析 SORT BY 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("SORT", "BY")
        columns = [cls.parse_order_by_item(scanner, sql_type=sql_type)]
        while scanner.search_and_move(","):
            columns.append(cls.parse_order_by_item(scanner, sql_type=sql_type))
        return node.ASTSortByClause(columns=tuple(columns))

    @classmethod
    def parse_distribute_by_clause(cls, scanner_or_string: ScannerOrString,
                                   sql_type: SQLType = SQLType.DEFAULT) -> node.ASTDistributeByClause:
        """解析 DISTRIBUTE BY 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("DISTRIBUTE", "BY")
        columns = [cls.parse_bitwise_or_level_node(scanner, sql_type=sql_type)]
        while scanner.search_and_move(","):
            columns.append(cls.parse_bitwise_or_level_node(scanner, sql_type=sql_type))
        return node.ASTDistributeByClause(columns=tuple(columns))

    @classmethod
    def parse_cluster_by_clause(cls, scanner_or_string: ScannerOrString,
                                sql_type: SQLType = SQLType.DEFAULT) -> node.ASTClusterByClause:
        """解析 CLUSTER BY 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("DISTRIBUTE", "BY")
        columns = [cls.parse_bitwise_or_level_node(scanner, sql_type=sql_type)]
        while scanner.search_and_move(","):
            columns.append(cls.parse_bitwise_or_level_node(scanner, sql_type=sql_type))
        return node.ASTClusterByClause(columns=tuple(columns))

    @classmethod
    def parse_limit_clause(cls, scanner_or_string: ScannerOrString,
                           sql_type: SQLType = SQLType.DEFAULT) -> node.ASTLimitClause:
        """解析 LIMIT 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if not scanner.search_and_move("LIMIT"):
            raise SqlParseError("无法解析为 LIMIT 子句")
        cnt_1 = cls.parse_literal_expression(scanner, sql_type=sql_type).as_int()
        if scanner.search_and_move(","):
            offset_int = cnt_1
            limit_int = cls.parse_literal_expression(scanner, sql_type=sql_type).as_int()
        elif scanner.search_and_move("OFFSET"):
            offset_int = cls.parse_literal_expression(scanner, sql_type=sql_type).as_int()
            limit_int = cnt_1
        else:
            offset_int = None
            limit_int = cnt_1
        return node.ASTLimitClause(limit=limit_int, offset=offset_int)

    @classmethod
    def parse_with_table(cls, scanner_or_string: ScannerOrString,
                         sql_type: SQLType = SQLType.DEFAULT) -> node.ASTWithTable:
        """解析一个 WITH 临时表"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        table_name = unify_name(scanner.pop_as_source())
        scanner.match("AS")
        parenthesis_scanner = scanner.pop_as_children_scanner()
        table_statement = cls.parse_select_statement(parenthesis_scanner,
                                                     with_clause=node.ASTWithClause.empty(),
                                                     sql_type=sql_type)
        parenthesis_scanner.close()
        return node.ASTWithTable(name=table_name, statement=table_statement)

    @classmethod
    def parse_with_clause(cls,
                          scanner_or_string: ScannerOrString,
                          sql_type: SQLType = SQLType.DEFAULT) -> Optional[node.ASTWithClause]:
        """解析 WITH 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if scanner.search_and_move("WITH"):
            tables = [cls.parse_with_table(scanner, sql_type=sql_type)]
            while scanner.search_and_move(","):
                table_statement = cls.parse_with_table(scanner, sql_type=sql_type)
                tables.append(table_statement)  # 将前置的 WITH 作为当前解析临时表的 WITH 子句
            return node.ASTWithClause(tables=tuple(tables))
        return node.ASTWithClause.empty()

    @classmethod
    def parse_single_select_statement(cls, scanner_or_string: ScannerOrString,
                                      with_clause: Optional[node.ASTWithClause] = None,
                                      sql_type: SQLType = SQLType.DEFAULT
                                      ) -> node.ASTSingleSelectStatement:
        # pylint: disable=R0912
        # pylint: disable=R0914
        """

        Parameters
        ----------
        scanner_or_string : ScannerOrString
            扫描器
        with_clause : Optional[SQLWithClause], default = None
            前置 with 语句，如果该参数为 None 的话，则会尝试匹配 WITH 语句
        sql_type : SQLType
            SQL 类型
        """
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if with_clause is None:
            with_clause = cls.parse_with_clause(scanner, sql_type=sql_type)

        # 允许在外层添加任意数量的括号
        inner_scanner = scanner
        parenthesis_stack = []
        while inner_scanner.search(AMTMark.PARENTHESIS):
            inner_scanner = scanner.pop_as_children_scanner()
            parenthesis_stack.append(inner_scanner)

        select_clause = cls.parse_select_clause(inner_scanner, sql_type=sql_type)
        from_clause = (cls.parse_from_clause(inner_scanner, sql_type=sql_type)
                       if inner_scanner.search("FROM") else None)
        lateral_view_clauses = []
        while scanner.search("LATERAL", "VIEW"):
            lateral_view_clauses.append(cls.parse_lateral_view_clause(inner_scanner, sql_type=sql_type))
        join_clause = []
        while scanner.search({"JOIN", "INNER", "LEFT", "RIGHT", "FULL", "CROSS"}):
            join_clause.append(cls.parse_join_clause(inner_scanner, sql_type=sql_type))
        where_clause = (cls.parse_where_clause(inner_scanner, sql_type=sql_type)
                        if inner_scanner.search("WHERE") else None)
        group_by_clause = (cls.parse_group_by_clause(inner_scanner, sql_type=sql_type)
                           if inner_scanner.search("GROUP", "BY") else None)
        having_clause = (cls.parse_having_clause(inner_scanner, sql_type=sql_type)
                         if inner_scanner.search("HAVING") else None)
        order_by_clause = (cls.parse_order_by_clause(inner_scanner, sql_type=sql_type)
                           if inner_scanner.search("ORDER", "BY") else None)

        if sql_type == SQLType.HIVE and inner_scanner.search("SORT", "BY"):
            sort_by_clause = cls.parse_sort_by_clause(inner_scanner, sql_type=sql_type)
        else:
            sort_by_clause = None

        if sql_type == SQLType.HIVE and inner_scanner.search("DISTRIBUTE", "BY"):
            distribute_by_clause = cls.parse_distribute_by_clause(inner_scanner, sql_type=sql_type)
        else:
            distribute_by_clause = None

        if sql_type == SQLType.HIVE and inner_scanner.search("CLUSTER", "BY"):
            cluster_by_clause = cls.parse_cluster_by_clause(inner_scanner, sql_type=sql_type)
        else:
            cluster_by_clause = None

        if inner_scanner.search("LIMIT"):
            limit_clause = cls.parse_limit_clause(inner_scanner, sql_type=sql_type)
        else:
            limit_clause = None

        while parenthesis_stack:
            parenthesis_stack.pop().close()

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
            sort_by_clause=sort_by_clause,
            distribute_by_clause=distribute_by_clause,
            cluster_by_clause=cluster_by_clause,
            limit_clause=limit_clause
        )

    @classmethod
    def parse_select_statement(cls, scanner_or_string: ScannerOrString,
                               with_clause: Optional[node.ASTWithClause] = None,
                               sql_type: SQLType = SQLType.DEFAULT
                               ) -> node.ASTSelectStatement:
        """解析 SELECT 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if with_clause is None:
            with_clause = cls.parse_with_clause(scanner, sql_type=sql_type)
        result = [cls.parse_single_select_statement(scanner, with_clause=with_clause, sql_type=sql_type)]
        while scanner.search({"UNION", "EXCEPT", "INTERSECT", "MINUS"}):
            result.append(cls.parse_union_type(scanner, sql_type=sql_type))
            result.append(cls.parse_single_select_statement(scanner, with_clause=with_clause, sql_type=sql_type))
        if len(result) == 1:
            return result[0]
        return node.ASTUnionSelectStatement(with_clause=with_clause, elements=tuple(result))

    @classmethod
    def _parse_config_string(cls, scanner: TokenScanner) -> str:
        """解析配置名称或配置值：字符串中允许包含 . 符合和 - 符合"""
        column_string = [scanner.pop_as_source()]
        while True:
            if scanner.search_and_move("."):
                column_string.append(".")
                column_string.append(scanner.pop_as_source())
            elif scanner.search_and_move("-"):
                column_string.append("-")
                column_string.append(scanner.pop_as_source())
            else:
                break
        return "".join(column_string)

    @classmethod
    def parse_config_string_expression(cls, scanner_or_string: ScannerOrString,
                                       sql_type: SQLType = SQLType.DEFAULT
                                       ) -> node.ASTConfigStringExpression:
        """解析配置值为字符串的配置表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        config_name = cls._parse_config_string(scanner)
        scanner.match("=")
        config_value = cls._parse_config_string(scanner)
        return node.ASTConfigStringExpression(name=config_name, value=config_value)

    @classmethod
    def parse_column_type_expression(cls, scanner_or_string: ScannerOrString,
                                     sql_type: SQLType = SQLType.DEFAULT) -> node.ASTColumnTypeExpression:
        """解析 DDL 的字段类型：要求当前指针位置节点为函数名，下一个节点可能为函数参数也可能不是，解析为 SQLColumnType 对象"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)

        # 解析字段类型名称
        function_name: str = scanner.pop_as_source()

        # 解析字段类型参数
        if scanner.search(AMTMark.PARENTHESIS):
            function_params: List[node.ASTExpressionBase] = []
            for param_scanner in scanner.pop_as_children_scanner_list_split_by(","):
                function_params.append(cls.parse_bitwise_or_level_node(param_scanner, sql_type=sql_type))
                param_scanner.close()
            return node.ASTColumnTypeExpression(name=function_name, params=tuple(function_params))
        return node.ASTColumnTypeExpression(name=function_name)

    @classmethod
    def parse_partition_expression(cls, scanner_or_string: ScannerOrString,
                                   sql_type: SQLType = SQLType.DEFAULT) -> node.ASTPartitionExpression:
        """解析分区表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("PARTITION")
        partition_list = []
        is_dynamic_partition = False  # 是否有动态分区
        is_non_dynamic_partition = False  # 是否有非动态分区
        for partition_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            before_value = cls.parse_bitwise_or_level_node(partition_scanner, sql_type=sql_type)
            if partition_scanner.search(static.COMPARE_OPERATOR_SET):  # 非动态分区
                is_non_dynamic_partition = True
                operator = cls.parse_compare_operator(partition_scanner, sql_type=sql_type)
                after_value = cls.parse_bitwise_or_level_node(partition_scanner, sql_type=sql_type)
                partition_list.append(node.ASTOperatorConditionExpression(
                    before_value=before_value,
                    operator=operator,
                    after_value=after_value
                ))
            else:
                is_dynamic_partition = True
                partition_list.append(before_value)  # 动态分区
            partition_scanner.close()
        if is_dynamic_partition is True and is_non_dynamic_partition is True:
            raise SqlParseError("分区表达式同时包含动态分区和非动态分区")
        return node.ASTPartitionExpression(partitions=tuple(partition_list))

    @classmethod
    def parse_foreign_key_expression(cls, scanner_or_string: ScannerOrString,
                                     sql_type: SQLType = SQLType.DEFAULT) -> node.ASTForeignKeyExpression:
        """解析外键表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
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
    def parse_index_column(cls, scanner_or_string: ScannerOrString,
                           sql_type: SQLType = SQLType.DEFAULT) -> node.ASTIndexColumn:
        """解析索引声明表达式中的字段"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        name = unify_name(scanner.pop_as_source())
        max_length = None
        if scanner.search(AMTMark.PARENTHESIS):
            parenthesis_scanner = scanner.pop_as_children_scanner()
            max_length = int(parenthesis_scanner.pop_as_source())
            parenthesis_scanner.close()
        return node.ASTIndexColumn(name=name, max_length=max_length)

    @classmethod
    def _get_index_columns(cls, scanner: TokenScanner,
                           sql_type: SQLType = SQLType.DEFAULT
                           ) -> Tuple[node.ASTIndexColumn, ...]:
        """解析索引表达式中的索引字段"""
        columns = []
        for column_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            columns.append(cls.parse_index_column(column_scanner, sql_type=sql_type))
            column_scanner.close()
        return tuple(columns)

    @classmethod
    def parse_primary_index_expression(cls, scanner_or_string: ScannerOrString,
                                       sql_type: SQLType = SQLType.DEFAULT
                                       ) -> node.ASTPrimaryIndexExpression:
        """解析主键表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("PRIMARY", "KEY")
        columns = cls._get_index_columns(scanner, sql_type=sql_type)
        using = scanner.pop_as_source() if scanner.search_and_move("USING") else None
        comment = scanner.pop_as_source() if scanner.search_and_move("COMMENT") else None
        key_block_size = int(scanner.pop_as_source()) if scanner.search_and_move("KEY_BLOCK_SIZE", "=") else None
        return node.ASTPrimaryIndexExpression(columns=columns, using=using, comment=comment,
                                              key_block_size=key_block_size)

    @classmethod
    def parse_unique_index_expression(cls, scanner_or_string: ScannerOrString,
                                      sql_type: SQLType = SQLType.DEFAULT
                                      ) -> node.ASTUniqueIndexExpression:
        """解析唯一键表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("UNIQUE", "KEY")
        name = scanner.pop_as_source()
        columns = cls._get_index_columns(scanner, sql_type=sql_type)
        using = scanner.pop_as_source() if scanner.search_and_move("USING") else None
        comment = scanner.pop_as_source() if scanner.search_and_move("COMMENT") else None
        key_block_size = int(scanner.pop_as_source()) if scanner.search_and_move("KEY_BLOCK_SIZE", "=") else None
        return node.ASTUniqueIndexExpression(name=name, columns=columns, using=using, comment=comment,
                                             key_block_size=key_block_size)

    @classmethod
    def parse_normal_index_expression(cls, scanner_or_string: ScannerOrString,
                                      sql_type: SQLType = SQLType.DEFAULT
                                      ) -> node.ASTNormalIndexExpression:
        """解析一般索引表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("KEY")
        name = scanner.pop_as_source()
        columns = cls._get_index_columns(scanner, sql_type=sql_type)
        using = scanner.pop_as_source() if scanner.search_and_move("USING") else None
        comment = scanner.pop_as_source() if scanner.search_and_move("COMMENT") else None
        key_block_size = int(scanner.pop_as_source()) if scanner.search_and_move("KEY_BLOCK_SIZE", "=") else None
        return node.ASTNormalIndexExpression(name=name, columns=columns, using=using, comment=comment,
                                             key_block_size=key_block_size)

    @classmethod
    def parse_fulltext_expression(cls, scanner_or_string: ScannerOrString, sql_type: SQLType = SQLType.DEFAULT
                                  ) -> node.ASTFulltextIndexExpression:
        """解析全文索引表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("FULLTEXT", "KEY")
        name = scanner.pop_as_source()
        columns = cls._get_index_columns(scanner, sql_type=sql_type)
        using = scanner.pop_as_source() if scanner.search_and_move("USING") else None
        comment = scanner.pop_as_source() if scanner.search_and_move("COMMENT") else None
        key_block_size = int(scanner.pop_as_source()) if scanner.search_and_move("KEY_BLOCK_SIZE", "=") else None
        return node.ASTFulltextIndexExpression(name=name, columns=columns, using=using, comment=comment,
                                               key_block_size=key_block_size)

    @classmethod
    def parse_define_column_expression(cls, scanner_or_string: ScannerOrString,
                                       sql_type: SQLType = SQLType.DEFAULT
                                       ) -> node.ASTDefineColumnExpression:
        # pylint: disable=R0914

        """解析 DDL 的字段表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        # 解析顺序固定的信息
        column_name = scanner.pop_as_source()
        column_type = cls.parse_column_type_expression(scanner, sql_type=sql_type)

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
                default = cls.parse_bitwise_or_level_node(scanner, sql_type=sql_type)
            elif scanner.search_and_move("COMMENT"):
                comment = scanner.pop_as_source()
            elif scanner.search_and_move("ON", "UPDATE"):  # ON UPDATE
                on_update = cls.parse_bitwise_or_level_node(scanner, sql_type=sql_type)
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
    def parse_insert_statement(cls, scanner_or_string: ScannerOrString,
                               with_clause: Optional[node.ASTWithClause],
                               sql_type: SQLType = SQLType.DEFAULT,
                               ) -> node.ASTInsertStatement:
        """解析 INSERT 表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)

        if with_clause is None:
            with_clause = cls.parse_with_clause(scanner, sql_type=sql_type)

        insert_type = cls.parse_insert_type(scanner, sql_type=sql_type)

        # 匹配可能包含的 TABLE 关键字
        scanner.search_and_move("TABLE")

        # 匹配表名
        table_name = cls.parse_table_name_expression(scanner, sql_type=sql_type)

        # 匹配分区表达式
        if scanner.search("PARTITION"):
            partition = cls.parse_partition_expression(scanner, sql_type=sql_type)
        else:
            partition = None

        # 匹配列名列表
        if scanner.search(AMTMark.PARENTHESIS):
            columns = []
            for column_scanner in scanner.pop_as_children_scanner_list_split_by(","):
                columns.append(cls.parse_column_name_expression(column_scanner, sql_type=sql_type))
                column_scanner.close()
        else:
            columns = None

        # 匹配 VALUES 类型
        if scanner.search_and_move("VALUES"):
            values = []
            while scanner.search(AMTMark.PARENTHESIS):
                values.append(cls.parse_value_expression(scanner, sql_type=sql_type))
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
            select_statement = cls.parse_select_statement(scanner,
                                                          with_clause=node.ASTWithClause.empty(), sql_type=sql_type)
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
    def parse_set_statement(cls, scanner_or_string: ScannerOrString,
                            sql_type: SQLType = SQLType.DEFAULT) -> node.ASTSetStatement:
        """解析 SET 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("SET")
        config = cls.parse_config_string_expression(scanner, sql_type=sql_type)
        return node.ASTSetStatement(config=config)

    @classmethod
    def parse_create_table_statement(cls, scanner_or_string: ScannerOrString,
                                     sql_type: SQLType = SQLType.DEFAULT) -> AliasCreateTableStatement:
        # pylint: disable=R0912
        # pylint: disable=R0914
        # pylint: disable=R0915
        """解析 CREATE TABLE 语句"""
        # 解析字段、索引括号前的部分
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("CREATE", "TABLE")
        if_not_exists = scanner.search_and_move("IF", "NOT", "EXISTS")
        table_name = cls.parse_table_name_expression(scanner, sql_type=sql_type)

        # CREATE TABLE ... AS ... 语句
        if scanner.search_and_move("AS"):
            select_statement = cls.parse_select_statement(scanner, sql_type=sql_type)
            return node.ASTCreateTableAsStatement(
                table_name=table_name,
                select_statement=select_statement
            )

        # 解析字段和索引
        columns: List[node.ASTDefineColumnExpression] = []
        primary_key: Optional[node.ASTPrimaryIndexExpression] = None
        unique_key: List[node.ASTUniqueIndexExpression] = []
        key: List[node.ASTNormalIndexExpression] = []
        fulltext_key: List[node.ASTFulltextIndexExpression] = []
        foreign_key: List[node.ASTForeignKeyExpression] = []
        for group_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            if group_scanner.search("PRIMARY", "KEY"):
                primary_key = cls.parse_primary_index_expression(group_scanner, sql_type=sql_type)
            elif group_scanner.search("UNIQUE", "KEY"):
                unique_key.append(cls.parse_unique_index_expression(group_scanner, sql_type=sql_type))
            elif group_scanner.search("KEY"):
                key.append(cls.parse_normal_index_expression(group_scanner, sql_type=sql_type))
            elif group_scanner.search("FULLTEXT", "KEY"):
                fulltext_key.append(cls.parse_fulltext_expression(group_scanner, sql_type=sql_type))
            elif group_scanner.search("CONSTRAINT"):
                foreign_key.append(cls.parse_foreign_key_expression(group_scanner, sql_type=sql_type))
            else:
                columns.append(cls.parse_define_column_expression(group_scanner, sql_type=sql_type))
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
        row_format_delimited_fields_terminated_by: Optional[str] = None
        stored_as_inputformat: Optional[str] = None
        stored_as_textfile: bool = False
        outputformat: Optional[str] = None
        location: Optional[str] = None
        tblproperties: Optional[List[node.ASTConfigStringExpression]] = []
        while not scanner.is_finish and not scanner.search(";"):
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
                    partitioned_by.append(cls.parse_define_column_expression(group_scanner, sql_type=sql_type))
                    group_scanner.close()
            elif scanner.search_and_move("ROW", "FORMAT", "SERDE"):
                scanner.search_and_move("=")
                row_format_serde = scanner.pop_as_source()
            elif scanner.search_and_move("ROW", "FORMAT", "DELIMITED", "FIELDS", "TERMINATED", "BY"):
                scanner.search_and_move("=")
                row_format_delimited_fields_terminated_by = scanner.pop_as_source()
            elif scanner.search_and_move("STORED", "AS", "INPUTFORMAT"):
                scanner.search_and_move("=")
                stored_as_inputformat = scanner.pop_as_source()
            elif scanner.search_and_move("STORED", "AS", "TEXTFILE"):
                stored_as_textfile = True
            elif scanner.search_and_move("OUTPUTFORMAT"):
                scanner.search_and_move("=")
                outputformat = scanner.pop_as_source()
            elif scanner.search_and_move("LOCATION"):
                scanner.search_and_move("=")
                location = scanner.pop_as_source()
            elif scanner.search_and_move("TBLPROPERTIES"):
                for group_scanner in scanner.pop_as_children_scanner_list_split_by(","):
                    tblproperties.append(cls.parse_config_string_expression(group_scanner, sql_type=sql_type))
                    group_scanner.close()
            else:
                raise SqlParseError(f"未知的 DDL 表属性: {scanner}")
        scanner.search_and_move(";")

        return node.ASTCreateTableStatement(
            table_name=table_name,
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
            row_format_delimited_fields_terminated_by=row_format_delimited_fields_terminated_by,
            stored_as_inputformat=stored_as_inputformat,
            stored_as_textfile=stored_as_textfile,
            outputformat=outputformat,
            location=location,
            tblproperties=tuple(tblproperties)
        )

    @classmethod
    def parse_drop_table_statement(cls, scanner_or_string: ScannerOrString,
                                   sql_type: SQLType = SQLType.DEFAULT) -> node.ASTDropTableStatement:
        """解析 DROP TABLE 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("DROP", "TABLE")
        if_exists = scanner.search_and_move("IF", "EXISTS")
        table_name = cls.parse_table_name_expression(scanner, sql_type=sql_type)
        return node.ASTDropTableStatement(if_exists=if_exists, table_name=table_name)

    @classmethod
    def parse_analyze_table_statement(cls, scanner_or_string: ScannerOrString,
                                      sql_type: SQLType = SQLType.DEFAULT) -> node.ASTAnalyzeTableStatement:
        """解析 ANALYZE TABLE 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("ANALYZE", "TABLE")
        table_name = cls.parse_table_name_expression(scanner, sql_type=sql_type)

        if scanner.search("PARTITION"):
            partition = cls.parse_partition_expression(scanner, sql_type=sql_type)
        else:
            partition = None

        scanner.search_and_move("COMPUTE", "STATISTICS")  # [Hive]
        for_columns = scanner.search_and_move("FOR", "COLUMNS")  # [Hive]
        cache_metadata = scanner.search_and_move("CACHE", "METADATA")  # [Hive]
        noscan = scanner.search_and_move("NOSCAN")  # [Hive]

        return node.ASTAnalyzeTableStatement(
            table_name=table_name,
            partition=partition,
            for_columns=for_columns,
            cache_metadata=cache_metadata,
            noscan=noscan
        )

    @classmethod
    def parse_type_column_or_index(cls, scanner_or_string: ScannerOrString,
                                   sql_type: SQLType = SQLType.DEFAULT) -> node.AliasColumnOrIndex:
        """解析字段声明表达式或索引声明表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if scanner.search("PRIMARY", "KEY"):
            return cls.parse_primary_index_expression(scanner, sql_type=sql_type)
        if scanner.search("UNIQUE", "KEY"):
            return cls.parse_unique_index_expression(scanner, sql_type=sql_type)
        if scanner.search("KEY"):
            return cls.parse_normal_index_expression(scanner, sql_type=sql_type)
        if scanner.search("FULLTEXT", "KEY"):
            return cls.parse_fulltext_expression(scanner, sql_type=sql_type)
        if scanner.search("CONSTRAINT"):
            return cls.parse_foreign_key_expression(scanner, sql_type=sql_type)
        return cls.parse_define_column_expression(scanner, sql_type=sql_type)

    @classmethod
    def parse_alter_expression(cls, scanner_or_string: ScannerOrString,
                               sql_type: SQLType = SQLType.DEFAULT) -> node.ASTAlterExpressionBase:
        # pylint: disable=R0911
        """解析 ALTER TABLE 的子句表达式

        TODO 优化 PARTITION 的解析逻辑，将 search 和 match 合并为 1 个
        """
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        if scanner.search_and_move("ADD"):
            return node.ASTAlterAddExpression(
                expression=cls.parse_type_column_or_index(scanner, sql_type=sql_type)
            )
        if scanner.search_and_move("MODIFY"):
            return node.ASTAlterModifyExpression(
                expression=cls.parse_type_column_or_index(scanner, sql_type=sql_type)
            )
        if scanner.search_and_move("CHANGE"):
            from_column_name = unify_name(scanner.pop_as_source())
            to_expression = cls.parse_type_column_or_index(scanner, sql_type=sql_type)
            return node.ASTAlterChangeExpression(
                from_column_name=from_column_name,
                to_expression=to_expression
            )
        if scanner.search_and_move("RENAME", "COLUMN"):
            from_column_name = unify_name(scanner.pop_as_source())
            scanner.match("TO")
            to_column_name = unify_name(scanner.pop_as_source())
            return node.ASTAlterRenameColumnExpression(
                from_column_name=from_column_name,
                to_column_name=to_column_name
            )
        if scanner.search_and_move("DROP", "COLUMN"):
            return node.ASTAlterDropColumnExpression(
                column_name=unify_name(scanner.pop_as_source())
            )
        if scanner.search("DROP", "PARTITION"):
            scanner.match("DROP")
            return node.ASTAlterDropPartitionExpression(
                if_exists=False,
                partition=cls.parse_partition_expression(scanner, sql_type=sql_type)
            )
        if scanner.search("DROP", "IF", "EXISTS", "PARTITION"):
            scanner.match("DROP", "IF", "EXISTS")
            return node.ASTAlterDropPartitionExpression(
                if_exists=True,
                partition=cls.parse_partition_expression(scanner, sql_type=sql_type)
            )
        raise SqlParseError(f"未知的 ALTER TABLE 类型: {scanner}")

    @classmethod
    def parse_alter_table_statement(cls, scanner_or_string: ScannerOrString,
                                    sql_type: SQLType = SQLType.DEFAULT) -> node.ASTAlterTableStatement:
        """解析 ALTER TABLE 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("ALTER", "TABLE")
        table_name = cls.parse_table_name_expression(scanner, sql_type=sql_type)
        expressions = [cls.parse_alter_expression(scanner, sql_type=sql_type)]
        while scanner.search_and_move(","):
            expressions.append(cls.parse_alter_expression(scanner, sql_type=sql_type))
        return node.ASTAlterTableStatement(
            table_name=table_name,
            expressions=tuple(expressions)
        )

    @classmethod
    def parse_msck_repair_table_statement(cls, scanner_or_string: ScannerOrString,
                                          sql_type: SQLType = SQLType.DEFAULT) -> node.ASTMsckRepairTableStatement:
        """解析 MSCK REPAIR 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("MSCK", "REPAIR", "TABLE")
        table_name = cls.parse_table_name_expression(scanner, sql_type=sql_type)
        return node.ASTMsckRepairTableStatement(
            table_name=table_name
        )

    @classmethod
    def parse_use_statement(cls, scanner_or_string: ScannerOrString,
                            sql_type: SQLType = SQLType.DEFAULT) -> node.ASTUseStatement:
        """解析 USE 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("USE")
        return node.ASTUseStatement(
            schema_name=scanner.pop_as_source()
        )

    @classmethod
    def parse_truncate_table_statement(cls, scanner_or_string: ScannerOrString,
                                       sql_type: SQLType = SQLType.DEFAULT) -> node.ASTTruncateTable:
        """解析 TRUNCATE TABLE 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("TRUNCATE", "TABLE")
        table_name = cls.parse_table_name_expression(scanner)
        return node.ASTTruncateTable(
            table_name=table_name
        )

    @classmethod
    def parse_update_set_column(cls, scanner_or_string: ScannerOrString,
                                sql_type: SQLType = SQLType.DEFAULT) -> node.ASTUpdateSetColumn:
        """解析 UPDATE 语句中 SET 中的字段元素"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        column_name = scanner.pop_as_source()
        scanner.match("=")
        column_value = cls.parse_logical_or_level(scanner)
        return node.ASTUpdateSetColumn(
            column_name=column_name,
            column_value=column_value
        )

    @classmethod
    def parse_update_set_clause(cls, scanner_or_string: ScannerOrString,
                                sql_type: SQLType = SQLType.DEFAULT) -> node.ASTUpdateSetClause:
        """解析 UPDATE 语句的 SET 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("SET")
        columns = [cls.parse_update_set_column(scanner)]
        while scanner.search_and_move(","):
            columns.append(cls.parse_update_set_column(scanner))
        return node.ASTUpdateSetClause(
            columns=tuple(columns)
        )

    @classmethod
    def parse_update_statement(cls, scanner_or_string: ScannerOrString,
                               sql_type: SQLType = SQLType.DEFAULT) -> node.ASTUpdateStatement:
        """解析 UPDATE 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("UPDATE")
        table_name = cls.parse_table_name_expression(scanner)
        set_clause = cls.parse_update_set_clause(scanner)

        if scanner.search("WHERE"):
            where_clause = cls.parse_where_clause(scanner)
        else:
            where_clause = None

        if scanner.search("ORDER", "BY"):
            order_by_clause = cls.parse_order_by_clause(scanner)
        else:
            order_by_clause = None

        if scanner.search("LIMIT"):
            limit_clause = cls.parse_limit_clause(scanner)
        else:
            limit_clause = None

        return node.ASTUpdateStatement(
            table_name=table_name,
            set_clause=set_clause,
            where_clause=where_clause,
            order_by_clause=order_by_clause,
            limit_clause=limit_clause
        )

    @classmethod
    def parse_show_columns_statement(cls, scanner_or_string: ScannerOrString,
                                     sql_type: SQLType = SQLType.DEFAULT) -> node.ASTShowColumnsStatement:
        """解析 SHOW COLUMNS 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        scanner.match("SHOW", "COLUMNS")
        from_clause = cls.parse_from_clause(scanner, sql_type=sql_type)

        if scanner.search("WHERE"):
            where_clause = cls.parse_where_clause(scanner)
        else:
            where_clause = None

        return node.ASTShowColumnsStatement(
            from_clause=from_clause,
            where_clause=where_clause
        )

    @classmethod
    def parse_statements(cls, scanner_or_string: ScannerOrString,
                         sql_type: SQLType = SQLType.DEFAULT) -> List[node.ASTStatementBase]:
        # pylint: disable=R0912
        """解析一段 SQL 语句，返回表达式的列表"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        statement_list = []
        while not scanner.is_finish:
            # 解析 SET 语句
            if scanner.search("SET"):
                statement_list.append(cls.parse_set_statement(scanner, sql_type=sql_type))

            # 解析 DROP TABLE 语句
            elif scanner.search("DROP", "TABLE"):
                statement_list.append(cls.parse_drop_table_statement(scanner, sql_type=sql_type))

            # 解析 CREATE TABLE 语句
            elif scanner.search("CREATE", "TABLE"):
                statement_list.append(cls.parse_create_table_statement(scanner, sql_type=sql_type))

            # 解析 ANALYZE TABLE 语句
            elif scanner.search("ANALYZE", "TABLE"):
                statement_list.append(cls.parse_analyze_table_statement(scanner, sql_type=sql_type))

            # 解析 ALTER TABLE 语句
            elif scanner.search("ALTER", "TABLE"):
                statement_list.append(cls.parse_alter_table_statement(scanner, sql_type=sql_type))

            # 解析 MSCK REPAIR TABLE 语句
            elif scanner.search("MSCK", "REPAIR", "TABLE"):
                statement_list.append(cls.parse_msck_repair_table_statement(scanner, sql_type=sql_type))

            # 解析 USE 语句
            elif scanner.search("USE"):
                statement_list.append(cls.parse_use_statement(scanner, sql_type=sql_type))

            # 解析 TRUNCATE TABLE 语句
            elif scanner.search("TRUNCATE", "TABLE"):
                statement_list.append(cls.parse_truncate_table_statement(scanner, sql_type=sql_type))

            # 解析 SHOW DATABASES 语句
            elif scanner.search_and_move("SHOW", "DATABASES"):
                statement_list.append(node.ASTShowDatabasesStatement())

            # 解析 SHOW TABLES 语句
            elif scanner.search_and_move("SHOW", "TABLES"):
                statement_list.append(node.ASTShowTablesStatement())

            # 解析 SHOW COLUMNS 语句
            elif scanner.search_and_move("SHOW", "COLUMNS"):
                statement_list.append(cls.parse_show_columns_statement(scanner, sql_type=sql_type))

            # 解析 UPDATE 语句 TODO 增加支持 WITH 语句
            elif scanner.search("UPDATE"):
                statement_list.append(cls.parse_update_statement(scanner, sql_type=sql_type))

            else:
                # 解析可能包含 WITH 子句的语句类型
                with_clause = cls.parse_with_clause(scanner, sql_type=sql_type)

                if scanner.search("SELECT"):
                    statement_list.append(cls.parse_select_statement(scanner,
                                                                     with_clause=with_clause, sql_type=sql_type))
                elif scanner.search("INSERT"):
                    statement_list.append(cls.parse_insert_statement(scanner,
                                                                     with_clause=with_clause, sql_type=sql_type))
                else:
                    raise SqlParseError(f"未知语句类型: {scanner}")

            scanner.search_and_move(";")

        scanner.close()

        return statement_list


def unify_name(text: Optional[str]) -> Optional[str]:
    """格式化名称标识符：统一剔除当前引号并添加引号"""
    return text.strip("`") if text is not None else None

if __name__ == "__main__":
    demo_sql = "3 << 2 >> 1"
    ast_node = SQLParser.parse_shift_level_node(demo_sql, maybe_window=True)
    print(ast_node)