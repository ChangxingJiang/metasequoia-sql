# pylint: disable=C0302

"""
SQL 语法解析器

将所有解析方法合并到这个类中，以支持插件开发。
如需替换词法解析器，重写 build_token_scanner 方法即可。
"""

from typing import List, Optional, Tuple, Union

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

# 表名表达式和子查询表达式的通用类型别名
AliasTableExpression = Union[node.ASTTableNameExpression, node.ASTSubQueryExpression]

# 两种 JOIN 表达式的通用类型别名
AliasJoinExpression = Union[node.ASTJoinOnExpression, node.ASTJoinUsingExpression]

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

# 按位或表达式层级
NodeBitwiseOrLevel = Union[NodeUnaryLevel, node.ASTComputeExpression]

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

# 逻辑或表达式层级（通用表达式）
GeneralExpression = Union[NodeLogicalXorLevel, node.ASTLogicalOrExpression]


class SQLParser:
    # pylint: disable=R0904
    """SQL 语法解析器"""

    # ------------------------------ 词法扫描器构造方法 ------------------------------

    @classmethod
    def _build_token_scanner(cls, string: str) -> TokenScanner:
        """构造词法扫描器"""
        return TokenScanner(FSMMachine.parse(string))

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

    # ------------------------------ 通用工具方法 ------------------------------

    @classmethod
    def _unify_name(cls, text: Optional[str]) -> Optional[str]:
        """格式化名称标识符：剔除名称前后的引号"""
        return text.strip("`") if text is not None else None

    @classmethod
    def _get_alias_name(cls, scanner: TokenScanner) -> str:
        """获取别名：如果抽象词法树（AMT）没有 NAME 标记，则抛出异常"""
        if not scanner.search_one_type_mark(AMTMark.NAME):
            raise SqlParseError(f"无法解析为名称: {scanner}")
        return cls._unify_name(scanner.pop_as_source())

    @classmethod
    def _parse_config_string(cls, scanner: TokenScanner) -> str:
        """解析配置名称或配置值：字符串中允许包含 . 符合和 - 符合"""
        column_string = [scanner.pop_as_source()]
        while True:
            if scanner.search_and_move_one_type_str("."):
                column_string.append(".")
                column_string.append(scanner.pop_as_source())
            elif scanner.search_and_move_one_type_str("-"):
                column_string.append("-")
                column_string.append(scanner.pop_as_source())
            else:
                break
        return "".join(column_string)

    # ------------------------------ 枚举类节点的解析方法 ------------------------------

    @classmethod
    def parse_insert_type(cls, scanner_or_string: ScannerOrString,
                          sql_type: SQLType = SQLType.DEFAULT) -> node.ASTInsertType:
        """解析插入类型"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_insert_type(scanner)

    @classmethod
    def _parse_insert_type(cls, scanner: TokenScanner) -> node.ASTInsertType:
        if scanner.search_and_move_two_type_str_use_upper("INSERT", "INTO"):
            return node.ASTInsertType(enum=static.EnumInsertType.INSERT_INTO)
        if scanner.search_and_move_three_type_str_use_upper("INSERT", "IGNORE", "INTO"):
            return node.ASTInsertType(enum=static.EnumInsertType.INSERT_INTO)
        if scanner.search_and_move_two_type_str_use_upper("INSERT", "OVERWRITE"):
            return node.ASTInsertType(enum=static.EnumInsertType.INSERT_OVERWRITE)
        raise SqlParseError(f"未知的 INSERT 类型: {scanner}")

    @classmethod
    def parse_join_type(cls, scanner_or_string: ScannerOrString,
                        sql_type: SQLType = SQLType.DEFAULT) -> node.ASTJoinType:
        """解析关联类型"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_join_type(scanner)

    @classmethod
    def _parse_join_type(cls, scanner: TokenScanner) -> node.ASTJoinType:
        for join_type in static.EnumJoinType:
            if scanner.search_and_move(*join_type.value):
                return node.ASTJoinType(enum=join_type)
        raise SqlParseError(f"无法解析的关联类型: {scanner}")

    @classmethod
    def parse_order_type(cls, scanner_or_string: ScannerOrString,
                         sql_type: SQLType = SQLType.DEFAULT) -> node.ASTOrderType:
        """解析排序类型"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_order_type(scanner)

    @classmethod
    def _parse_order_type(cls, scanner: TokenScanner) -> node.ASTOrderType:
        if scanner.search_and_move_one_type_str_use_upper("DESC"):
            return node.ASTOrderType(enum=static.EnumOrderType.DESC)
        if scanner.search_and_move_one_type_str_use_upper("ASC"):
            return node.ASTOrderType(enum=static.EnumOrderType.ASC)
        return node.ASTOrderType(enum=static.EnumOrderType.ASC)

    @classmethod
    def parse_union_type(cls, scanner_or_string: ScannerOrString,
                         sql_type: SQLType = SQLType.DEFAULT) -> node.ASTUnionType:
        """解析组合类型"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_union_type(scanner)

    @classmethod
    def _parse_union_type(cls, scanner: TokenScanner) -> node.ASTUnionType:
        for union_type in static.EnumUnionType:
            if scanner.search_and_move(*union_type.value):
                return node.ASTUnionType(enum=union_type)
        raise SqlParseError(f"无法解析的组合类型: {scanner}")

    @classmethod
    def parse_compare_operator(cls, scanner_or_string: ScannerOrString,
                               sql_type: SQLType = SQLType.DEFAULT) -> node.ASTCompareOperator:
        """解析比较运算符"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_compare_operator(scanner)

    @classmethod
    def _parse_compare_operator(cls, scanner: TokenScanner) -> node.ASTCompareOperator:
        compare_operator = static.COMPARE_OPERATOR_HASH.get(scanner.pop_as_source())
        if compare_operator is None:
            raise SqlParseError(f"无法解析的比较运算符: {scanner}")
        return node.ASTCompareOperator(enum=compare_operator)

    @classmethod
    def parse_compute_operator(cls, scanner_or_string: ScannerOrString,
                               sql_type: SQLType = SQLType.DEFAULT) -> node.ASTComputeOperator:
        """解析计算运算符"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_compute_operator(scanner)

    @classmethod
    def _parse_compute_operator(cls, scanner: TokenScanner) -> node.ASTComputeOperator:
        compute_operator = static.COMPUTE_OPERATOR_HASH.get(scanner.pop_as_source())
        if compute_operator is None:
            raise SqlParseError(f"无法解析的计算运算符: {scanner}")
        return node.ASTComputeOperator(enum=compute_operator)

    @classmethod
    def parse_cast_data_type(cls, scanner_or_string: ScannerOrString,
                             sql_type: SQLType = SQLType.DEFAULT) -> static.EnumCastDataType:
        """解析 CAST 函数表达式中的类型"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_cast_data_type(scanner)

    @classmethod
    def _parse_cast_data_type(cls, scanner: TokenScanner) -> static.EnumCastDataType:
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
        return cls._parse_column_name_expression(scanner)

    @classmethod
    def _parse_column_name_expression(cls, scanner: TokenScanner) -> node.ASTColumnNameExpression:
        if not scanner.search_one_type_mark(AMTMark.NAME):
            raise SqlParseError(f"无法解析为表名表达式: {scanner}")
        first_name = scanner.pop_as_source()
        if scanner.search_and_move_one_type_str("."):  # table.name 的形式
            if not scanner.search_one_type_mark(AMTMark.NAME):
                raise SqlParseError(f"无法解析为表名表达式: {scanner}")
            table_name = first_name
            column_name = scanner.pop_as_source()
        else:
            table_name = None
            column_name = first_name
        return node.ASTColumnNameExpression(
            table_name=cls._unify_name(table_name),
            column_name=cls._unify_name(column_name)
        )

    @classmethod
    def _parse_column_name_expression_with_table(cls, scanner: TokenScanner) -> node.ASTColumnNameExpression:
        """解析已确定包含表名的列名表达式"""
        table_name = scanner.pop_as_source()
        scanner.match(".")
        column_name = scanner.pop_as_source()
        return node.ASTColumnNameExpression(
            table_name=cls._unify_name(table_name),
            column_name=cls._unify_name(column_name)
        )

    @classmethod
    def _parse_column_name_expression_without_table(cls, scanner: TokenScanner) -> node.ASTColumnNameExpression:
        """解析已确定不包含表名的列名表达式"""
        column_name = scanner.pop_as_source()
        return node.ASTColumnNameExpression(
            column_name=cls._unify_name(column_name)
        )

    @classmethod
    def parse_table_name_expression(cls, scanner_or_string: ScannerOrString,
                                    sql_type: SQLType = SQLType.DEFAULT) -> node.ASTTableNameExpression:
        """解析表名表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_table_name_expression(scanner)

    @classmethod
    def _parse_table_name_expression(cls, scanner: TokenScanner) -> node.ASTTableNameExpression:
        node_0 = scanner.pop()
        if not node_0.has_mark(AMTMark.NAME):
            raise SqlParseError(f"无法解析为表名表达式: {scanner}")

        if scanner.search_and_move_one_type_str("."):
            # 解析包含 schema 的表名
            node_2 = scanner.pop()
            if not node_0.has_mark(AMTMark.NAME):
                raise SqlParseError(f"无法解析为表名表达式: {scanner}")
            return node.ASTTableNameExpression(
                schema_name=cls._unify_name(node_0.source),
                table_name=cls._unify_name(node_2.source)
            )

        # 解析没有 schema 或 `schema.table` 格式的表名
        name_source = node_0.source
        if name_source.count(".") == 1:
            schema_name, table_name = name_source.strip("`").split(".")
        else:
            schema_name, table_name = None, name_source
        return node.ASTTableNameExpression(
            schema_name=cls._unify_name(schema_name),
            table_name=cls._unify_name(table_name)
        )

    @classmethod
    def parse_function_name_expression(cls, scanner_or_string: ScannerOrString,
                                       sql_type: SQLType = SQLType.DEFAULT
                                       ) -> node.ASTFunctionNameExpression:
        """解析函数名表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_function_name_expression(scanner)

    @classmethod
    def _parse_function_name_expression(cls, scanner: TokenScanner) -> node.ASTFunctionNameExpression:
        if scanner.search(AMTMark.NAME, ".", AMTMark.NAME):
            schema_name = scanner.pop_as_source()
            scanner.move()
            table_name = scanner.pop_as_source()
            return node.ASTFunctionNameExpression(
                schema_name=cls._unify_name(schema_name),
                function_name=cls._unify_name(table_name)
            )
        if scanner.search_one_type_mark(AMTMark.NAME):
            name_source = scanner.pop_as_source()
            if name_source.count(".") == 1:
                schema_name, table_name = name_source.strip("`").split(".")
            else:
                schema_name, table_name = None, name_source
            return node.ASTFunctionNameExpression(
                schema_name=cls._unify_name(schema_name),
                function_name=cls._unify_name(table_name)
            )
        raise SqlParseError(f"无法解析为表名表达式: {scanner}")

    @classmethod
    def parse_literal_expression(cls, scanner_or_string: ScannerOrString,
                                 sql_type: SQLType = SQLType.DEFAULT) -> node.ASTLiteralExpression:
        """解析字面值：包含整型字面值、浮点型字面值、字符串型字面值、十六进制型字面值、布尔型字面值、位值型字面值、空值的字面值"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_literal_expression(scanner)

    @classmethod
    def _parse_literal_expression(cls, scanner: TokenScanner) -> node.ASTLiteralExpression:
        return node.ASTLiteralExpression(value=scanner.pop_as_source())

    @classmethod
    def parse_window_row_item(cls, scanner_or_string: ScannerOrString,
                              sql_type: SQLType = SQLType.DEFAULT) -> node.ASTWindowRowItem:
        """解析窗口函数行限制中的行"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_window_row_item(scanner)

    @classmethod
    def _parse_window_row_item(cls, scanner: TokenScanner) -> node.ASTWindowRowItem:
        if scanner.search_and_move_two_type_str_use_upper("CURRENT", "ROW"):
            return node.ASTWindowRowItem(row_type=static.EnumWindowRowType.CURRENT_ROW)
        if scanner.search_and_move_one_type_str_use_upper("UNBOUNDED"):
            if scanner.search_and_move_one_type_str_use_upper("PRECEDING"):
                return node.ASTWindowRowItem(row_type=static.EnumWindowRowType.PRECEDING, is_unbounded=True)
            if scanner.search_and_move_one_type_str_use_upper("FOLLOWING"):
                return node.ASTWindowRowItem(row_type=static.EnumWindowRowType.FOLLOWING, is_unbounded=True)
            raise SqlParseError(f"无法解析的窗口函数限制行: {scanner}")
        row_num = int(scanner.pop_as_source())
        if scanner.search_and_move_one_type_str_use_upper("PRECEDING"):
            return node.ASTWindowRowItem(row_type=static.EnumWindowRowType.PRECEDING, row_num=row_num)
        if scanner.search_and_move_one_type_str_use_upper("FOLLOWING"):
            return node.ASTWindowRowItem(row_type=static.EnumWindowRowType.FOLLOWING, row_num=row_num)
        raise SqlParseError(f"无法解析的窗口函数限制行: {scanner}")

    @classmethod
    def parse_window_row(cls, scanner_or_string: ScannerOrString,
                         sql_type: SQLType = SQLType.DEFAULT) -> node.ASTWindowRow:
        """解析窗口语句限制行的表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_window_row(scanner)

    @classmethod
    def _parse_window_row(cls, scanner: TokenScanner) -> node.ASTWindowRow:
        scanner.match("ROWS", "BETWEEN")
        from_row = cls._parse_window_row_item(scanner)
        scanner.match("AND")
        to_row = cls._parse_window_row_item(scanner)
        return node.ASTWindowRow(from_row=from_row, to_row=to_row)

    @classmethod
    def parse_wildcard_expression(cls, scanner_or_string: ScannerOrString,
                                  sql_type: SQLType = SQLType.DEFAULT) -> node.ASTWildcardExpression:
        """解析通配符表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_wildcard_expression(scanner)

    @classmethod
    def _parse_wildcard_expression(cls, scanner: TokenScanner) -> node.ASTWildcardExpression:
        if scanner.search_and_move_one_type_str("*"):
            return node.ASTWildcardExpression()
        if scanner.search(AMTMark.NAME, ".", "*"):
            schema_name = scanner.pop_as_source()
            scanner.move(2)
            return node.ASTWildcardExpression(table_name=schema_name)
        raise SqlParseError("无法解析为通配符表达式")

    @classmethod
    def _parse_wildcard_expression_with_table(cls, scanner: TokenScanner) -> node.ASTWildcardExpression:
        """直接解析为包含 schema 的通配符格式"""
        schema_name = scanner.pop_as_source()
        scanner.move(2)
        return node.ASTWildcardExpression(table_name=schema_name)

    @classmethod
    def _parse_wildcard_expression_without_table(cls, scanner: TokenScanner) -> node.ASTWildcardExpression:
        """直接解析为包含 schema 的通配符格式"""
        scanner.move()
        return node.ASTWildcardExpression()

    @classmethod
    def parse_alias_expression(cls, scanner_or_string: ScannerOrString,
                               sql_type: SQLType = SQLType.DEFAULT) -> Optional[node.ASTAlisaExpression]:
        """解析别名表达式：如果当前位置是别名表达式则返回别名表达式节点，否则返回 None"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_alias_expression(scanner)

    @classmethod
    def _parse_alias_expression(cls, scanner: TokenScanner) -> Optional[node.ASTAlisaExpression]:
        if scanner.search_and_move_one_type_str_use_upper("AS"):
            return node.ASTAlisaExpression(name=cls._get_alias_name(scanner))
        if scanner.search_one_type_mark(AMTMark.NAME):
            return node.ASTAlisaExpression(name=cls._unify_name(scanner.pop_as_source()))
        return None

    @classmethod
    def parse_multi_alias_expression(cls, scanner_or_string: ScannerOrString,
                                     sql_type: SQLType = SQLType.DEFAULT) -> node.ASTMultiAlisaExpression:
        """解析多个别名表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_multi_alias_expression(scanner)

    @classmethod
    def _parse_multi_alias_expression(cls, scanner: TokenScanner) -> node.ASTMultiAlisaExpression:
        scanner.match("AS")
        names = [cls._get_alias_name(scanner)]
        while scanner.search_and_move_one_type_str(","):
            names.append(cls._get_alias_name(scanner))
        return node.ASTMultiAlisaExpression(names=tuple(names))

    # ------------------------------ SELECT 语句节点的解析方法 ------------------------------

    @classmethod
    def parse_extract_function_expression(cls, scanner_or_string: ScannerOrString,
                                          sql_type: SQLType = SQLType.DEFAULT
                                          ) -> node.ASTExtractFunctionExpression:
        """解析 EXTRACT 函数表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_extract_function_expression(scanner, sql_type)

    @classmethod
    def _parse_extract_function_expression(cls, scanner: TokenScanner, sql_type: SQLType
                                           ) -> node.ASTExtractFunctionExpression:
        inner_scanner = scanner.pop_as_children_scanner()
        extract_name = cls._parse_compute_expression(inner_scanner, sql_type)
        inner_scanner.match("FROM")
        column_expression = cls._parse_compute_expression(inner_scanner, sql_type)
        inner_scanner.close()
        return node.ASTExtractFunctionExpression(
            extract_name=extract_name,
            column_expression=column_expression
        )

    @classmethod
    def parse_cast_function_expression(cls, scanner_or_string: ScannerOrString,
                                       sql_type: SQLType = SQLType.DEFAULT
                                       ) -> node.ASTCastFunctionExpression:
        """解析 CAST 函数表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_cast_function_expression(scanner, sql_type)

    @classmethod
    def _parse_cast_function_expression(cls, scanner: TokenScanner, sql_type: SQLType):
        inner_scanner = scanner.pop_as_children_scanner()
        column_expression = cls._parse_compute_expression(inner_scanner, sql_type)
        inner_scanner.match("AS")
        signed = inner_scanner.search_and_move_one_type_str_use_upper("SIGNED")
        cast_type = cls._parse_cast_data_type(inner_scanner)
        if inner_scanner.search_one_type_mark(AMTMark.PARENTHESIS):
            parenthesis_scanner = inner_scanner.pop_as_children_scanner()
            cast_params: Optional[List[int] | Tuple[int, ...]] = []
            if not parenthesis_scanner.is_finish:
                cast_params.append(int(parenthesis_scanner.pop_as_source()))
            while parenthesis_scanner.search_and_move_one_type_str(","):
                cast_params.append(int(parenthesis_scanner.pop_as_source()))
            cast_params = tuple(cast_params)
        else:
            cast_params = None
        inner_scanner.close()
        cast_data_type = node.ASTCastDataType(signed=signed, type=cast_type, params=cast_params)
        return node.ASTCastFunctionExpression(
            column_expression=column_expression,
            cast_type=cast_data_type
        )

    @classmethod
    def parse_if_function_expression(cls, scanner_or_string: ScannerOrString,
                                     sql_type: SQLType = SQLType.DEFAULT
                                     ) -> node.ASTNormalFunctionExpression:
        """解析 IF 函数表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_if_function_expression(scanner, sql_type)

    @classmethod
    def _parse_if_function_expression(cls, scanner: TokenScanner,
                                      sql_type: SQLType) -> node.ASTNormalFunctionExpression:
        inner_scanner = scanner.pop_as_children_scanner()
        function_params: List[GeneralExpression] = []
        if not inner_scanner.is_finish:
            cls._parse_logical_or_level_expression(inner_scanner, sql_type=sql_type)
        while inner_scanner.search_and_move_one_type_str(","):
            function_params.append(cls._parse_logical_or_level_expression(inner_scanner, sql_type=sql_type))
        inner_scanner.close()
        return node.ASTNormalFunctionExpression(
            name=node.ASTFunctionNameExpression(function_name="IF"),
            params=tuple(function_params)
        )

    @classmethod
    def parse_function_expression(cls, scanner_or_string: ScannerOrString, sql_type: SQLType = SQLType.DEFAULT
                                  ) -> node.ASTFunctionExpressionBase:
        """解析函数表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_function_expression(scanner, sql_type=sql_type)

    @classmethod
    def _parse_function_expression(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTFunctionExpressionBase:
        function_name_expression = cls._parse_function_name_expression(scanner)
        function_name_upper = function_name_expression.function_name.upper()

        if function_name_upper == "CAST":
            return cls._parse_cast_function_expression(scanner, sql_type)
        if function_name_upper == "EXTRACT":
            return cls._parse_extract_function_expression(scanner, sql_type)
        if function_name_upper == "IF":
            return cls._parse_if_function_expression(scanner, sql_type)
        if function_name_upper == "CHAR":
            return cls._parse_func_char(scanner, sql_type)
        if function_name_upper == "CURRENT_USER":
            return cls._parse_func_current_user(scanner)
        if function_name_upper == "USER":
            return cls._parse_func_user(scanner)
        if function_name_upper == "DATE":
            return cls._parse_func_date(scanner, sql_type)

        parenthesis_scanner = scanner.pop_as_children_scanner()
        if function_name_upper == "SUBSTRING":
            # 将 MySQL 和 PostgreSQL 中的 "SUBSTRING(str1 FROM 3 FOR 2)" 格式化为 "SUBSTRING(str1, 3, 2)"
            parenthesis_scanner = TokenScanner([
                element if not element.source_in_set_use_upper({"FROM", "FOR"}) else AMTSingle(",")
                for element in parenthesis_scanner.elements])

        is_distinct = False
        if (function_name_upper in name_set.AGGREGATION_FUNCTION_NAME_SET
                and parenthesis_scanner.search_and_move_one_type_str_use_upper("DISTINCT")):
            is_distinct = True

        function_params: List[GeneralExpression] = []
        if not parenthesis_scanner.is_finish:
            function_params.append(cls._parse_logical_or_level_expression(parenthesis_scanner, sql_type))
        while parenthesis_scanner.search_and_move_one_type_str(","):
            function_params.append(cls._parse_logical_or_level_expression(parenthesis_scanner, sql_type))

        parenthesis_scanner.close()

        if (function_name_expression.schema_name is None
                and function_name_upper in name_set.AGGREGATION_FUNCTION_NAME_SET):
            return node.ASTAggregationFunction(
                name=function_name_expression,
                params=tuple(function_params),
                is_distinct=is_distinct)
        return node.ASTNormalFunctionExpression(
            name=function_name_expression,
            params=tuple(function_params)
        )

    @classmethod
    def _parse_func_char(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTFuncChar:
        """解析 CHAR() 函数"""
        # 获取函数参数部分的迭代器
        parenthesis_scanner = scanner.pop_as_children_scanner()

        # 解析表达式列表
        expr_list: List[GeneralExpression] = []
        if not parenthesis_scanner.is_finish:
            expr_list.append(cls._parse_logical_or_level_expression(parenthesis_scanner, sql_type))
        while parenthesis_scanner.search_and_move_one_type_str(","):
            expr_list.append(cls._parse_logical_or_level_expression(parenthesis_scanner, sql_type))

        # 解析字符集名称
        charset_name: Optional[str] = None
        if parenthesis_scanner.search_and_move_one_type_str("USING"):
            charset_name = parenthesis_scanner.pop_as_source()

        # 关闭迭代器，确保其中元素已迭代完成
        parenthesis_scanner.close()

        return node.ASTFuncChar(
            name=node.ASTFunctionNameExpression(function_name="char"),
            expr_list=tuple(expr_list),
            charset_name=charset_name
        )

    @classmethod
    def _parse_func_current_user(cls, scanner: TokenScanner) -> node.ASTFuncCurrentUser:
        """解析 CURRENT_USER() 函数"""
        if scanner.search_one_type_mark(AMTMark.PARENTHESIS):
            parenthesis_scanner = scanner.pop_as_children_scanner()
            parenthesis_scanner.close()

        return node.ASTFuncCurrentUser(
            name=node.ASTFunctionNameExpression(function_name="current_user"),
        )

    @classmethod
    def _parse_func_user(cls, scanner: TokenScanner) -> node.ASTFuncUser:
        """解析 USER() 函数"""
        parenthesis_scanner = scanner.pop_as_children_scanner()
        parenthesis_scanner.close()
        return node.ASTFuncUser(
            name=node.ASTFunctionNameExpression(function_name="user"),
        )


    @classmethod
    def _parse_func_date(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTFuncDate:
        """解析 USER() 函数"""
        parenthesis_scanner = scanner.pop_as_children_scanner()
        expr = cls._parse_logical_or_level_expression(parenthesis_scanner, sql_type)
        parenthesis_scanner.close()
        return node.ASTFuncDate(
            name=node.ASTFunctionNameExpression(function_name="date"),
            expr=expr
        )


    @classmethod
    def parse_function_expression_and_index(cls, scanner_or_string: ScannerOrString,
                                            sql_type: SQLType = SQLType.DEFAULT
                                            ) -> Union[node.ASTFunctionExpressionBase, node.ASTIndexExpression]:
        """解析函数表达式，并解析函数表达式后可能包含的数组下标"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_function_expression_and_index(scanner, sql_type=sql_type)

    @classmethod
    def _parse_function_expression_and_index(cls, scanner: TokenScanner, sql_type: SQLType
                                             ) -> Union[node.ASTFunctionExpressionBase, node.ASTIndexExpression]:
        before_expression = cls._parse_function_expression(scanner, sql_type=sql_type)
        return cls._parse_array_index_expression(scanner, before_expression, sql_type)

    @classmethod
    def _parse_in_parenthesis(cls, scanner: TokenScanner, sql_type: SQLType) -> NodeElementLevel:
        """解析 IN 关键字后的插入语：插入语可能为子查询或值表达式"""
        if scanner.get_as_children_scanner().search_one_type_set_use_upper({"SELECT", "WITH"}):
            return cls._parse_sub_query_expression(scanner, sql_type=sql_type)
        return cls._parse_sub_value_expression(scanner, sql_type=sql_type)

    @classmethod
    def parse_window_expression(cls, scanner_or_string: ScannerOrString,
                                sql_type: SQLType = SQLType.DEFAULT) -> node.ASTWindowExpression:
        """解析窗口函数"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_window_expression(scanner, sql_type=sql_type)

    @classmethod
    def _parse_window_expression(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTWindowExpression:
        # 解析函数（因为这个函数可能是 UDF 函数，所以不作限制）
        window_function = cls._parse_function_expression_and_index(scanner, sql_type=sql_type)
        partition_by_columns = []
        order_by_columns = []
        row_expression = None
        scanner.match("OVER")
        parenthesis_scanner = scanner.pop_as_children_scanner()
        if parenthesis_scanner.search_and_move_two_type_str_use_upper("PARTITION", "BY"):
            partition_by_columns = [cls._parse_compute_expression(parenthesis_scanner, sql_type)]
            while parenthesis_scanner.search_and_move_one_type_str(","):
                partition_by_columns.append(cls._parse_compute_expression(parenthesis_scanner, sql_type))
        if parenthesis_scanner.search_and_move_two_type_str_use_upper("ORDER", "BY"):
            order_by_columns = [cls._parse_order_by_column(parenthesis_scanner, sql_type)]
            while parenthesis_scanner.search_and_move_one_type_str(","):
                order_by_columns.append(cls._parse_order_by_column(parenthesis_scanner, sql_type))
        if parenthesis_scanner.search_two_type_str_use_upper("ROWS", "BETWEEN"):
            row_expression = cls._parse_window_row(parenthesis_scanner)
        parenthesis_scanner.close()
        return node.ASTWindowExpression(
            window_function=window_function,
            partition_by_columns=tuple(partition_by_columns),
            order_by_columns=tuple(order_by_columns),
            row_expression=row_expression
        )

    @classmethod
    def parse_case_expression(cls, scanner_or_string: ScannerOrString,
                              sql_type: SQLType = SQLType.DEFAULT
                              ) -> AliasCaseExpression:
        """解析 CASE 表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_case_expression(scanner, sql_type=sql_type)

    @classmethod
    def _parse_case_expression(cls, scanner: TokenScanner, sql_type: SQLType):
        scanner.match("CASE")
        if scanner.search_one_type_str_use_upper("WHEN"):
            # 第 1 种格式的 CASE 表达式
            cases = []
            else_value = None
            while scanner.search_and_move_one_type_str_use_upper("WHEN"):
                when_expression = cls._parse_logical_or_level_expression(scanner, sql_type=sql_type)
                scanner.match("THEN")
                case_expression = cls._parse_logical_or_level_expression(scanner, sql_type=sql_type)
                cases.append(node.ASTCaseConditionItem(when=when_expression, then=case_expression))
            if scanner.search_and_move_one_type_str_use_upper("ELSE"):
                else_value = cls._parse_logical_or_level_expression(scanner, sql_type)
            scanner.match("END")
            return node.ASTCaseConditionExpression(
                cases=tuple(cases),
                else_value=else_value
            )

        # 第 2 种格式的 CASE 表达式
        case_value = cls._parse_logical_or_level_expression(scanner, sql_type=sql_type)
        cases = []
        else_value = None
        while scanner.search_and_move_one_type_str_use_upper("WHEN"):
            when_expression = cls._parse_logical_or_level_expression(scanner, sql_type=sql_type)
            scanner.match("THEN")
            case_expression = cls._parse_logical_or_level_expression(scanner, sql_type=sql_type)
            cases.append(node.ASTCaseValueItem(when=when_expression, then=case_expression))
        if scanner.search_and_move_one_type_str_use_upper("ELSE"):
            else_value = cls._parse_logical_or_level_expression(scanner, sql_type=sql_type)
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
        return cls._parse_sub_query_expression(scanner, sql_type=sql_type)

    @classmethod
    def _parse_sub_query_expression(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTSubQueryExpression:
        parenthesis_scanner = scanner.pop_as_children_scanner()
        result = node.ASTSubQueryExpression(
            statement=cls._parse_select_statement(parenthesis_scanner, None, sql_type=sql_type)
        )
        parenthesis_scanner.close()
        return result

    @classmethod
    def parse_sub_value_expression(cls, scanner_or_string: ScannerOrString,
                                   sql_type: SQLType = SQLType.DEFAULT) -> node.ASTSubValueExpression:
        """解析值表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_sub_value_expression(scanner, sql_type=sql_type)

    @classmethod
    def _parse_sub_value_expression(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTSubValueExpression:
        values = []
        for value_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            values.append(cls._parse_compute_expression(value_scanner, sql_type))
            value_scanner.close()
        return node.ASTSubValueExpression(values=tuple(values))

    @classmethod
    def _parse_general_parenthesis(cls, scanner: TokenScanner, sql_type: SQLType) -> GeneralExpression:
        """解析一般表达式中的插入语"""
        # 处理插入语中是子查询的情况
        if scanner.get_as_children_scanner().search_one_type_set_use_upper({"SELECT", "WITH"}):
            return cls._parse_sub_query_expression(scanner, sql_type=sql_type)
        # 处理插入语中是一般表达式的情况：如果有嵌套的插入语，那么会自动压缩为一层
        parenthesis_scanner = scanner.pop_as_children_scanner()
        result = cls._parse_logical_or_level_expression(parenthesis_scanner, sql_type=sql_type)
        parenthesis_scanner.close()
        return result

    @classmethod
    def _parse_array_index_expression(cls, scanner: TokenScanner, before_expression: GeneralExpression,
                                      sql_type: SQLType) -> GeneralExpression:
        """解析下标表达式

        Parameters
        ----------
        scanner : TokenScanner
        before_expression : NodeLogicalOrLevel
            下标表达式之前的表达式
        sql_type : SQLType
        """
        if not scanner.search_one_type_mark(AMTMark.ARRAY_INDEX):
            return before_expression  # 如果没有下标则直接返回
        # 解析数组下标
        children_scanner = scanner.pop_as_children_scanner()
        idx = cls._parse_compute_expression(children_scanner, sql_type)
        children_scanner.close()
        return node.ASTIndexExpression(
            array=before_expression,
            idx=idx
        )

    @classmethod
    def parse_element_level_expression(cls, scanner_or_string: ScannerOrString,
                                       sql_type: SQLType = SQLType.DEFAULT) -> GeneralExpression:
        # pylint: disable=R0911
        """解析元素表达式层级"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_element_level_expression(scanner, sql_type=sql_type)

    @classmethod
    def _parse_element_level_expression(cls, scanner: TokenScanner, sql_type: SQLType
                                        ) -> GeneralExpression:
        # pylint: disable=R0911
        # pylint: disable=R0912
        """已进行性能优化，使用专有解析逻辑而非通用解析逻辑"""
        node_0 = scanner.get_offset()
        if node_0.has_mark(AMTMark.LITERAL):
            return cls._parse_literal_expression(scanner)
        if node_0.has_mark(AMTMark.PARENTHESIS):  # 处理包含插入语的情况
            return cls._parse_general_parenthesis(scanner, sql_type=sql_type)
        if node_0.source_equal_use_upper("CASE"):
            return cls._parse_case_expression(scanner, sql_type=sql_type)
        if node_0.source_equal("*"):
            return cls._parse_wildcard_expression_without_table(scanner)

        node_1 = scanner.get_offset_or_null(1)
        if node_1 is not None and node_1.has_mark(AMTMark.PARENTHESIS):
            node_2 = scanner.get_offset_or_null(2)
            if node_2 is None or not node_2.source_equal_use_upper("OVER"):
                return cls._parse_function_expression_and_index(scanner, sql_type=sql_type)
            return cls._parse_window_expression(scanner, sql_type=sql_type)
        if node_1 is not None and node_1.source_equal("."):
            node_2 = scanner.get_offset(2)
            if node_2.has_mark(AMTMark.NAME):
                node_3 = scanner.get_offset_or_null(3)
                if node_3 is None or not node_3.has_mark(AMTMark.PARENTHESIS):
                    column_name_expression = cls._parse_column_name_expression_with_table(scanner)
                    return cls._parse_array_index_expression(scanner, column_name_expression, sql_type)
                return cls._parse_function_expression_and_index(scanner, sql_type=sql_type)
            if node_2.source_equal("*"):
                return cls._parse_wildcard_expression_with_table(scanner)
            raise SqlParseError(f"{node_1.source}. 之后不是名称或通配符")
        column_name_expression = cls._parse_column_name_expression_without_table(scanner)
        return cls._parse_array_index_expression(scanner, column_name_expression, sql_type)

    @classmethod
    def parse_unary_level_expression(cls, scanner_or_string: ScannerOrString,
                                     sql_type: SQLType = SQLType.DEFAULT) -> GeneralExpression:
        """解析一元表达式层级"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_unary_level_expression(scanner, sql_type=sql_type)

    @classmethod
    def _parse_unary_level_expression(cls, scanner: TokenScanner, sql_type: SQLType
                                      ) -> GeneralExpression:
        if scanner.search_one_type_set(static.get_unary_operator_set(sql_type)):
            unary_operator = cls._parse_compute_operator(scanner)
            return node.ASTUnaryExpression(
                operator=unary_operator,
                expression=cls._parse_unary_level_expression(scanner, sql_type)
            )
        return cls._parse_element_level_expression(scanner, sql_type=sql_type)

    @classmethod
    def parse_compute_expression(cls, scanner_or_string: ScannerOrString,
                                 sql_type: SQLType = SQLType.DEFAULT) -> GeneralExpression:
        """解析按位或层级表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_compute_expression(scanner, sql_type)

    @classmethod
    def _parse_compute_expression(cls, scanner: TokenScanner, sql_type: SQLType) -> GeneralExpression:
        stack: List[Union[GeneralExpression, static.EnumComputeOperator]]
        stack = [cls._parse_unary_level_expression(scanner, sql_type)]
        while compute_operator := static.COMPUTE_OPERATOR_HASH.get(scanner.get_as_source_or_null()):
            while len(stack) >= 3 and compute_operator.level >= stack[-2].level:
                after_value: GeneralExpression = stack.pop()
                last_compute_operator = stack.pop()
                before_value: GeneralExpression = stack.pop()
                stack.append(node.ASTComputeExpression(
                    before_value=before_value,
                    operator=node.ASTComputeOperator(enum=last_compute_operator),
                    after_value=after_value
                ))
            scanner.move()
            stack.append(compute_operator)
            stack.append(cls._parse_unary_level_expression(scanner, sql_type))
        while len(stack) >= 3:
            after_value: GeneralExpression = stack.pop()
            last_compute_operator = stack.pop()
            before_value: GeneralExpression = stack.pop()
            stack.append(node.ASTComputeExpression(
                before_value=before_value,
                operator=node.ASTComputeOperator(enum=last_compute_operator),
                after_value=after_value
            ))

        return stack[0]

    @classmethod
    def parse_keyword_condition_level_expression(cls, scanner_or_string: ScannerOrString,
                                                 sql_type: SQLType = SQLType.DEFAULT) -> GeneralExpression:
        # pylint: disable=R0911
        """解析关键字条件表达式（不包含前置 NOT，但包含中间的 NOT）

        Parameters
        ----------
        scanner_or_string : ScannerOrString
            扫描器
        sql_type : SQLType
            SQL 类型
        """
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_keyword_condition_level_expression(scanner, None, sql_type=sql_type)

    @classmethod
    def _parse_keyword_condition_level_expression(cls, scanner: TokenScanner,
                                                  before_value: Optional[NodeKeywordConditionLevel],
                                                  sql_type: SQLType = SQLType.DEFAULT) -> GeneralExpression:
        """解析关键字条件表达式

        Parameters
        ----------
        scanner
        before_value : Optional[NodeKeywordConditionLevel], default = None
            已经遍历的上一个关键字条件表达式，用于递归，在第一次时置为 None 即可
        sql_type
        """
        # 首先尝试解析第一个关键字条件表达式
        if before_value is None and scanner.search_and_move_one_type_str_use_upper("EXISTS"):
            # 正在解析第一个关键字表达式，且开头的关键字表达式为 EXISTS 语句
            value = cls._parse_sub_query_expression(scanner, sql_type=sql_type)
            result_value = node.ASTExistsExpression(value=value)
        else:
            if before_value is None:
                # 如果正在解析第一个关键字表达式，则解析按位或表达式或更低等级表达式作为关键字之前的部分
                before_value = cls._parse_compute_expression(scanner, sql_type)

            # 解析可能存在于关键字之间的 NOT
            is_not = scanner.search_and_move_one_type_set_use_upper(static.get_not_operator_set(sql_type))

            if scanner.is_finish:
                return before_value  # 如果已经匹配结果，则直接返回

            next_ch = scanner.get_as_source_or_null().upper()
            if next_ch == "BETWEEN":
                scanner.move()
                from_value = cls._parse_compute_expression(scanner, sql_type)
                scanner.match("AND")
                to_value = cls._parse_compute_expression(scanner, sql_type)
                result_value = node.ASTBetweenExpression(
                    is_not=is_not,
                    before_value=before_value,
                    from_value=from_value,
                    to_value=to_value
                )
            elif next_ch == "IS":
                scanner.move()
                is_not = is_not or scanner.search_and_move_one_type_str_use_upper("NOT")
                after_value = cls._parse_compute_expression(scanner, sql_type)
                result_value = node.ASTIsExpression(
                    is_not=is_not,
                    before_value=before_value,
                    after_value=after_value
                )
            elif next_ch == "IN":
                scanner.move()
                after_value = cls._parse_in_parenthesis(scanner, sql_type=sql_type)
                result_value = node.ASTInExpression(
                    is_not=is_not,
                    before_value=before_value,
                    after_value=after_value
                )
            elif next_ch == "LIKE":
                scanner.move()
                after_value = cls._parse_compute_expression(scanner, sql_type)
                result_value = node.ASTLikeExpression(
                    is_not=is_not,
                    before_value=before_value,
                    after_value=after_value
                )
            elif next_ch == "RLIKE":
                scanner.move()
                after_value = cls._parse_compute_expression(scanner, sql_type)
                result_value = node.ASTRlikeExpression(
                    is_not=is_not,
                    before_value=before_value,
                    after_value=after_value
                )
            elif next_ch == "REGEXP":
                scanner.move()
                after_value = cls._parse_compute_expression(scanner, sql_type)
                result_value = node.ASTRegexpExpression(
                    is_not=is_not,
                    before_value=before_value,
                    after_value=after_value
                )
            else:
                # 没有关键字表达式，直接返回按位或表达式或更低等级表达式
                return before_value

        # 如果后续是连续的关键字条件表达式的关键字，则将当前关键字表达式作为下一个关键字表达式的 before_value 继续解析
        if scanner.get_as_source_or_null() in {"NOT", "BETWEEN", "IS", "IN", "LIKE", "RLIKE", "REGEXP"}:
            return cls._parse_keyword_condition_level_expression(scanner, result_value, sql_type=sql_type)

        # 如果后续不是关键字条件表达式的关键字，则直接返回当前的关键字条件表达式
        return result_value

    @classmethod
    def parse_operator_condition_level_expression(cls, scanner_or_string: ScannerOrString,
                                                  sql_type: SQLType = SQLType.DEFAULT) -> GeneralExpression:
        """解析运算符条件表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_operator_condition_level_expression(scanner, sql_type=sql_type)

    @classmethod
    def _parse_operator_condition_level_expression(cls, scanner: TokenScanner,
                                                   sql_type: SQLType) -> GeneralExpression:
        before_value = cls._parse_keyword_condition_level_expression(scanner, None, sql_type=sql_type)
        while scanner.search_one_type_set(static.COMPARE_OPERATOR_SET):
            compare_operator = cls._parse_compare_operator(scanner)
            after_value = cls._parse_keyword_condition_level_expression(scanner, None, sql_type=sql_type)
            before_value = node.ASTOperatorConditionExpression(
                operator=compare_operator,
                before_value=before_value,
                after_value=after_value
            )
        return before_value

    @classmethod
    def parse_logical_not_level_expression(cls, scanner_or_string: ScannerOrString,
                                           sql_type: SQLType = SQLType.DEFAULT) -> GeneralExpression:
        """解析逻辑否表达式层级"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_logical_not_level_expression(scanner, sql_type=sql_type)

    @classmethod
    def _parse_logical_not_level_expression(cls, scanner: TokenScanner, sql_type: SQLType) -> GeneralExpression:
        if scanner.search_and_move_one_type_set_use_upper(static.get_not_operator_set(sql_type)):
            return node.ASTLogicalNotExpression(
                expression=cls._parse_logical_not_level_expression(scanner, sql_type=sql_type)
            )
        return cls._parse_operator_condition_level_expression(scanner, sql_type=sql_type)

    @classmethod
    def parse_logical_and_level_expression(cls, scanner_or_string: ScannerOrString,
                                           sql_type: SQLType = SQLType.DEFAULT) -> GeneralExpression:
        """解析逻辑与表达式层级"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_logical_and_level_expression(scanner, sql_type)

    @classmethod
    def _parse_logical_and_level_expression(cls, scanner: TokenScanner, sql_type: SQLType) -> GeneralExpression:
        before_value = cls._parse_logical_not_level_expression(scanner, sql_type=sql_type)
        while scanner.search_and_move_one_type_set_use_upper({"AND", "&&"}):
            after_value = cls._parse_logical_not_level_expression(scanner, sql_type=sql_type)
            before_value = node.ASTLogicalAndExpression(
                before_value=before_value,
                after_value=after_value
            )
        return before_value

    @classmethod
    def parse_logical_xor_level_expression(cls, scanner_or_string: ScannerOrString,
                                           sql_type: SQLType = SQLType.DEFAULT) -> GeneralExpression:
        """解析逻辑异或表达式层级"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_logical_xor_level_expression(scanner, sql_type)

    @classmethod
    def _parse_logical_xor_level_expression(cls, scanner: TokenScanner, sql_type: SQLType) -> GeneralExpression:
        before_value = cls._parse_logical_and_level_expression(scanner, sql_type=sql_type)
        while scanner.search_and_move_one_type_str_use_upper("XOR"):
            after_value = cls._parse_logical_and_level_expression(scanner, sql_type=sql_type)
            before_value = node.ASTLogicalXorExpression(
                before_value=before_value,
                after_value=after_value
            )
        return before_value

    @classmethod
    def parse_logical_or_level_expression(cls, scanner_or_string: ScannerOrString,
                                          sql_type: SQLType = SQLType.DEFAULT) -> GeneralExpression:
        """解析逻辑或表达式层级"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_logical_or_level_expression(scanner, sql_type)

    @classmethod
    def _parse_logical_or_level_expression(cls, scanner: TokenScanner, sql_type: SQLType) -> GeneralExpression:
        before_value = cls._parse_logical_xor_level_expression(scanner, sql_type=sql_type)
        while scanner.search_and_move_one_type_set_use_upper({"OR", "||"}):
            after_value = cls._parse_logical_xor_level_expression(scanner, sql_type=sql_type)
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
        return cls._parse_join_on_expression(scanner, sql_type)

    @classmethod
    def _parse_join_on_expression(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTJoinOnExpression:
        scanner.match("ON")
        return node.ASTJoinOnExpression(condition=cls._parse_logical_or_level_expression(scanner, sql_type=sql_type))

    @classmethod
    def parse_join_using_expression(cls, scanner_or_string: ScannerOrString,
                                    sql_type: SQLType = SQLType.DEFAULT) -> node.ASTJoinUsingExpression:
        """解析 USING 关联表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_join_using_expression(scanner, sql_type)

    @classmethod
    def _parse_join_using_expression(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTJoinUsingExpression:
        return node.ASTJoinUsingExpression(using_function=cls._parse_function_expression(scanner, sql_type=sql_type))

    @classmethod
    def parse_join_expression(cls, scanner_or_string: ScannerOrString,
                              sql_type: SQLType = SQLType.DEFAULT) -> AliasJoinExpression:
        """解析关联表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_join_expression(scanner, sql_type)

    @classmethod
    def _parse_join_expression(cls, scanner: TokenScanner, sql_type: SQLType) -> AliasJoinExpression:
        if scanner.search_one_type_str_use_upper("ON"):
            return cls._parse_join_on_expression(scanner, sql_type)
        if scanner.search_one_type_str_use_upper("USING"):
            return cls._parse_join_using_expression(scanner, sql_type)
        raise SqlParseError(f"无法解析为关联表达式: {scanner}")

    @classmethod
    def parse_table_expression(cls, scanner_or_string: ScannerOrString,
                               sql_type: SQLType = SQLType.DEFAULT) -> AliasTableExpression:
        """解析表表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_table_expression(scanner, sql_type)

    @classmethod
    def _parse_table_expression(cls, scanner: TokenScanner, sql_type: SQLType) -> AliasTableExpression:
        if scanner.get_as_children_scanner().search_one_type_set_use_upper({"SELECT", "WITH"}):
            return cls._parse_sub_query_expression(scanner, sql_type=sql_type)
        if scanner.search_one_type_mark(AMTMark.PARENTHESIS):  # 额外的插入语（因为只有一个元素，所以直接递归解析即可）
            return cls._parse_table_expression(scanner.pop_as_children_scanner(), sql_type=sql_type)
        return cls._parse_table_name_expression(scanner)

    @classmethod
    def parse_from_table(cls, scanner_or_string: ScannerOrString,
                         sql_type: SQLType = SQLType.DEFAULT) -> node.ASTFromTable:
        """解析 FROM 和 JOIN 子句元素：包含别名的表表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_from_table(scanner, sql_type)

    @classmethod
    def _parse_from_table(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTFromTable:
        name_expression = cls._parse_table_expression(scanner, sql_type=sql_type)
        alias_expression = cls._parse_alias_expression(scanner)
        return node.ASTFromTable(name=name_expression, alias=alias_expression)

    @classmethod
    def parse_select_column(cls, scanner_or_string: ScannerOrString,
                            sql_type: SQLType = SQLType.DEFAULT) -> node.ASTSelectColumn:
        """解析列名表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_select_column(scanner, sql_type)

    @classmethod
    def _parse_select_column(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTSelectColumn:
        general_expression = cls._parse_logical_or_level_expression(scanner, sql_type)
        alias_expression = cls._parse_alias_expression(scanner)
        return node.ASTSelectColumn(value=general_expression, alias=alias_expression)

    @classmethod
    def parse_select_clause(cls, scanner_or_string: ScannerOrString,
                            sql_type: SQLType = SQLType.DEFAULT) -> node.ASTSelectClause:
        """解析 SELECT 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_select_clause(scanner, sql_type)

    @classmethod
    def _parse_select_clause(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTSelectClause:
        scanner.match("SELECT")
        distinct = scanner.search_and_move_one_type_str_use_upper("DISTINCT")
        columns = [cls._parse_select_column(scanner, sql_type)]
        while scanner.search_and_move_one_type_str(","):
            columns.append(cls._parse_select_column(scanner, sql_type))
        return node.ASTSelectClause(distinct=distinct, columns=tuple(columns))

    @classmethod
    def parse_from_clause(cls, scanner_or_string: ScannerOrString,
                          sql_type: SQLType = SQLType.DEFAULT) -> node.ASTFromClause:
        """解析 FROM 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_from_clause(scanner, sql_type)

    @classmethod
    def _parse_from_clause(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTFromClause:
        scanner.match("FROM")
        tables = [cls._parse_from_table(scanner, sql_type=sql_type)]
        while scanner.search_and_move_one_type_str(","):
            tables.append(cls._parse_from_table(scanner, sql_type=sql_type))
        return node.ASTFromClause(tables=tuple(tables))

    @classmethod
    def parse_lateral_view_clause(cls, scanner_or_string: ScannerOrString,
                                  sql_type: SQLType = SQLType.DEFAULT) -> node.ASTLateralViewClause:
        """解析 LATERAL VIEW 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_lateral_view_clause(scanner, sql_type)

    @classmethod
    def _parse_lateral_view_clause(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTLateralViewClause:
        scanner.match("LATERAL", "VIEW")
        outer = scanner.search_and_move_one_type_str_use_upper("OUTER")
        function = cls._parse_function_expression(scanner, sql_type=sql_type)
        view_name = scanner.pop_as_source()
        alias = cls._parse_multi_alias_expression(scanner)
        return node.ASTLateralViewClause(outer=outer, function=function, view_name=view_name, alias=alias)

    @classmethod
    def parse_join_clause(cls, scanner_or_string: ScannerOrString,
                          sql_type: SQLType = SQLType.DEFAULT) -> node.ASTJoinClause:
        """解析 JOIN 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_join_clause(scanner, sql_type)

    @classmethod
    def _parse_join_clause(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTJoinClause:
        join_type = cls._parse_join_type(scanner)
        table_expression = cls._parse_from_table(scanner, sql_type=sql_type)
        if scanner.search_one_type_set_use_upper({"ON", "USING"}):
            join_rule = cls._parse_join_expression(scanner, sql_type=sql_type)
        else:
            join_rule = None
        return node.ASTJoinClause(type=join_type, table=table_expression, rule=join_rule)

    @classmethod
    def parse_where_clause(cls, scanner_or_string: ScannerOrString,
                           sql_type: SQLType = SQLType.DEFAULT) -> Optional[node.ASTWhereClause]:
        """解析 WHERE 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_where_clause(scanner, sql_type)

    @classmethod
    def _parse_where_clause(cls, scanner: TokenScanner, sql_type: SQLType) -> Optional[node.ASTWhereClause]:
        if not scanner.search_and_move_one_type_str_use_upper("WHERE"):
            return None
        return node.ASTWhereClause(condition=cls._parse_logical_or_level_expression(scanner, sql_type=sql_type))

    @classmethod
    def parse_grouping_sets(cls, scanner_or_string: ScannerOrString,
                            sql_type: SQLType = SQLType.DEFAULT) -> node.ASTGroupingSets:
        """解析 GROUP BY 子句的元素"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_grouping_sets(scanner, sql_type)

    @classmethod
    def _parse_grouping_sets(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTGroupingSets:
        scanner.match("GROUPING", "SETS")
        grouping_list = []
        for grouping_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            if grouping_scanner.search_one_type_mark(AMTMark.PARENTHESIS):
                parenthesis_scanner_list = grouping_scanner.pop_as_children_scanner_list_split_by(",")
                columns_list = []
                for parenthesis_scanner in parenthesis_scanner_list:
                    columns_list.append(cls._parse_compute_expression(parenthesis_scanner, sql_type))
                    parenthesis_scanner.close()
                grouping_list.append(tuple(columns_list))
            else:
                grouping_list.append(
                    tuple([cls._parse_compute_expression(grouping_scanner, sql_type)]))
            grouping_scanner.close()
        return node.ASTGroupingSets(grouping_list=tuple(grouping_list))

    @classmethod
    def parse_group_by_clause(cls, scanner_or_string: ScannerOrString,
                              sql_type: SQLType = SQLType.DEFAULT) -> Optional[node.ASTGroupByClause]:
        """解析 GROUP BY 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_group_by_clause(scanner, sql_type)

    @classmethod
    def _parse_group_by_clause(cls, scanner: TokenScanner, sql_type: SQLType) -> Optional[node.ASTGroupByClause]:
        if not scanner.search_and_move_two_type_str_use_upper("GROUP", "BY"):
            return None
        columns = []
        if not scanner.search_two_type_str_use_upper("GROUPING", "SETS"):
            # 如果当 GROUP BY 子句中直接就是 GROUPING SETS 时，则不尝试解析字段
            columns.append(cls._parse_compute_expression(scanner, sql_type))
            while scanner.search_and_move_one_type_str(","):
                columns.append(cls._parse_compute_expression(scanner, sql_type))
        if scanner.search_two_type_str_use_upper("GROUPING", "SETS"):
            grouping_sets = cls._parse_grouping_sets(scanner, sql_type)
        else:
            grouping_sets = None
        with_cube = scanner.search_and_move_two_type_str_use_upper("WITH", "CUBE")
        with_rollup = scanner.search_and_move_two_type_str_use_upper("WITH", "ROLLUP")
        return node.ASTGroupByClause(
            columns=tuple(columns),
            grouping_sets=grouping_sets,
            with_cube=with_cube,
            with_rollup=with_rollup
        )

    @classmethod
    def parse_having_clause(cls, scanner_or_string: ScannerOrString,
                            sql_type: SQLType = SQLType.DEFAULT) -> Optional[node.ASTHavingClause]:
        """解析 HAVING 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_having_clause(scanner, sql_type)

    @classmethod
    def _parse_having_clause(cls, scanner: TokenScanner, sql_type: SQLType) -> Optional[node.ASTHavingClause]:
        if not scanner.search_and_move_one_type_str_use_upper("HAVING"):
            return None
        return node.ASTHavingClause(condition=cls._parse_logical_or_level_expression(scanner, sql_type=sql_type))

    @classmethod
    def _parse_order_by_column(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTOrderByColumn:
        """解析 ORDER BY 子句的元素"""
        column = cls._parse_compute_expression(scanner, sql_type)
        order = cls._parse_order_type(scanner)
        nulls_first = scanner.search_and_move_two_type_str_use_upper("NULLS", "FIRST")
        nulls_last = scanner.search_and_move_two_type_str_use_upper("NULLS", "LAST")
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
                              sql_type: SQLType = SQLType.DEFAULT) -> Optional[node.ASTOrderByClause]:
        """解析 ORDER BY 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_order_by_clause(scanner, sql_type)

    @classmethod
    def _parse_order_by_clause(cls, scanner: TokenScanner, sql_type: SQLType) -> Optional[node.ASTOrderByClause]:
        if not scanner.search_and_move_two_type_str_use_upper("ORDER", "BY"):
            return None
        columns = [cls._parse_order_by_column(scanner, sql_type)]
        while scanner.search_and_move_one_type_str(","):
            columns.append(cls._parse_order_by_column(scanner, sql_type))
        return node.ASTOrderByClause(columns=tuple(columns))

    @classmethod
    def parse_sort_by_clause(cls, scanner_or_string: ScannerOrString,
                             sql_type: SQLType = SQLType.DEFAULT) -> Optional[node.ASTSortByClause]:
        """解析 SORT BY 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_sort_by_clause(scanner, sql_type)

    @classmethod
    def _parse_sort_by_clause(cls, scanner: TokenScanner, sql_type: SQLType) -> Optional[node.ASTSortByClause]:
        if not scanner.search_and_move_two_type_str_use_upper("SORT", "BY"):
            return None
        columns = [cls._parse_order_by_column(scanner, sql_type)]
        while scanner.search_and_move_one_type_str(","):
            columns.append(cls._parse_order_by_column(scanner, sql_type))
        return node.ASTSortByClause(columns=tuple(columns))

    @classmethod
    def parse_distribute_by_clause(cls, scanner_or_string: ScannerOrString,
                                   sql_type: SQLType = SQLType.DEFAULT) -> Optional[node.ASTDistributeByClause]:
        """解析 DISTRIBUTE BY 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_distribute_by_clause(scanner, sql_type)

    @classmethod
    def _parse_distribute_by_clause(cls, scanner: TokenScanner,
                                    sql_type: SQLType) -> Optional[node.ASTDistributeByClause]:
        if not scanner.search_and_move_two_type_str_use_upper("DISTRIBUTE", "BY"):
            return None
        columns = [cls._parse_compute_expression(scanner, sql_type)]
        while scanner.search_and_move_one_type_str(","):
            columns.append(cls._parse_compute_expression(scanner, sql_type))
        return node.ASTDistributeByClause(columns=tuple(columns))

    @classmethod
    def parse_cluster_by_clause(cls, scanner_or_string: ScannerOrString,
                                sql_type: SQLType = SQLType.DEFAULT) -> Optional[node.ASTClusterByClause]:
        """解析 CLUSTER BY 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_cluster_by_clause(scanner, sql_type)

    @classmethod
    def _parse_cluster_by_clause(cls, scanner: TokenScanner, sql_type: SQLType) -> Optional[node.ASTClusterByClause]:
        if not scanner.search_and_move_two_type_str_use_upper("CLUSTER", "BY"):
            return None
        columns = [cls._parse_compute_expression(scanner, sql_type)]
        while scanner.search_and_move_one_type_str(","):
            columns.append(cls._parse_compute_expression(scanner, sql_type))
        return node.ASTClusterByClause(columns=tuple(columns))

    @classmethod
    def parse_limit_clause(cls, scanner_or_string: ScannerOrString,
                           sql_type: SQLType = SQLType.DEFAULT) -> Optional[node.ASTLimitClause]:
        """解析 LIMIT 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_limit_clause(scanner)

    @classmethod
    def _parse_limit_clause(cls, scanner: TokenScanner) -> Optional[node.ASTLimitClause]:
        if not scanner.search_and_move_one_type_str_use_upper("LIMIT"):
            return None
        cnt_1 = cls._parse_literal_expression(scanner).as_int()
        if scanner.search_and_move_one_type_str(","):
            offset_int = cnt_1
            limit_int = cls._parse_literal_expression(scanner).as_int()
        elif scanner.search_and_move_one_type_str_use_upper("OFFSET"):
            offset_int = cls._parse_literal_expression(scanner).as_int()
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
        return cls._parse_with_table(scanner, sql_type)

    @classmethod
    def _parse_with_table(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTWithTable:
        table_name = cls._unify_name(scanner.pop_as_source())
        scanner.match("AS")
        parenthesis_scanner = scanner.pop_as_children_scanner()
        table_statement = cls._parse_select_statement(parenthesis_scanner, node.ASTWithClause.empty(), sql_type)
        parenthesis_scanner.close()
        return node.ASTWithTable(name=table_name, statement=table_statement)

    @classmethod
    def parse_with_clause(cls,
                          scanner_or_string: ScannerOrString,
                          sql_type: SQLType = SQLType.DEFAULT) -> Optional[node.ASTWithClause]:
        """解析 WITH 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_with_clause(scanner, sql_type)

    @classmethod
    def _parse_with_clause(cls, scanner: TokenScanner, sql_type: SQLType) -> Optional[node.ASTWithClause]:
        if scanner.search_and_move_one_type_str_use_upper("WITH"):
            tables = [cls._parse_with_table(scanner, sql_type)]
            while scanner.search_and_move_one_type_str(","):
                table_statement = cls._parse_with_table(scanner, sql_type)
                tables.append(table_statement)  # 将前置的 WITH 作为当前解析临时表的 WITH 子句
            return node.ASTWithClause(tables=tuple(tables))
        return node.ASTWithClause.empty()

    @classmethod
    def parse_single_select_statement(cls, scanner_or_string: ScannerOrString,
                                      with_clause: Optional[node.ASTWithClause] = None,
                                      sql_type: SQLType = SQLType.DEFAULT
                                      ) -> node.ASTSingleSelectStatement:
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
        return cls._parse_single_select_statement(scanner, with_clause, sql_type)

    @classmethod
    def _parse_single_select_statement(cls, scanner: TokenScanner,
                                       with_clause: Optional[node.ASTWithClause],
                                       sql_type: SQLType) -> node.ASTSingleSelectStatement:
        # pylint: disable=R0912
        # pylint: disable=R0914
        if with_clause is None:
            with_clause = cls._parse_with_clause(scanner, sql_type)

        # 允许在外层添加任意数量的括号
        inner_scanner = scanner
        parenthesis_stack = []
        while inner_scanner.search_one_type_mark(AMTMark.PARENTHESIS):
            inner_scanner = scanner.pop_as_children_scanner()
            parenthesis_stack.append(inner_scanner)

        select_clause = cls._parse_select_clause(inner_scanner, sql_type)
        from_clause = (cls._parse_from_clause(inner_scanner, sql_type)
                       if inner_scanner.search_one_type_str_use_upper("FROM") else None)
        lateral_view_clauses = []
        while scanner.search_two_type_str_use_upper("LATERAL", "VIEW"):
            lateral_view_clauses.append(cls._parse_lateral_view_clause(inner_scanner, sql_type))
        join_clause = []
        while scanner.search_one_type_set_use_upper({"JOIN", "INNER", "LEFT", "RIGHT", "FULL", "CROSS"}):
            join_clause.append(cls._parse_join_clause(inner_scanner, sql_type))
        where_clause = cls._parse_where_clause(inner_scanner, sql_type)
        group_by_clause = cls._parse_group_by_clause(inner_scanner, sql_type)
        having_clause = cls._parse_having_clause(inner_scanner, sql_type)
        order_by_clause = cls._parse_order_by_clause(inner_scanner, sql_type)
        sort_by_clause = cls._parse_sort_by_clause(inner_scanner, sql_type)
        distribute_by_clause = cls._parse_distribute_by_clause(inner_scanner, sql_type)
        cluster_by_clause = cls._parse_cluster_by_clause(inner_scanner, sql_type)
        limit_clause = cls._parse_limit_clause(inner_scanner)

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
        return cls._parse_select_statement(scanner, with_clause, sql_type)

    @classmethod
    def _parse_select_statement(cls, scanner: TokenScanner,
                                with_clause: Optional[node.ASTWithClause],
                                sql_type: SQLType) -> node.ASTSelectStatement:
        if with_clause is None:
            with_clause = cls._parse_with_clause(scanner, sql_type)
        result = [cls._parse_single_select_statement(scanner, with_clause, sql_type)]
        while scanner.search_one_type_set_use_upper({"UNION", "EXCEPT", "INTERSECT", "MINUS"}):
            result.append(cls._parse_union_type(scanner))
            result.append(cls._parse_single_select_statement(scanner, with_clause, sql_type))
        if len(result) == 1:
            return result[0]
        return node.ASTUnionSelectStatement(with_clause=with_clause, elements=tuple(result))

    @classmethod
    def parse_config_string_expression(cls, scanner_or_string: ScannerOrString,
                                       sql_type: SQLType = SQLType.DEFAULT
                                       ) -> node.ASTConfigStringExpression:
        """解析配置值为字符串的配置表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_config_string_expression(scanner)

    @classmethod
    def _parse_config_string_expression(cls, scanner: TokenScanner) -> node.ASTConfigStringExpression:
        config_name = cls._parse_config_string(scanner)
        scanner.match("=")
        config_value = cls._parse_config_string(scanner)
        return node.ASTConfigStringExpression(name=config_name, value=config_value)

    @classmethod
    def parse_column_type_expression(cls, scanner_or_string: ScannerOrString,
                                     sql_type: SQLType = SQLType.DEFAULT) -> node.ASTColumnTypeExpression:
        """解析 DDL 的字段类型：要求当前指针位置节点为函数名，下一个节点可能为函数参数也可能不是，解析为 SQLColumnType 对象"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_column_type_expression(scanner, sql_type)

    @classmethod
    def _parse_column_type_expression(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTColumnTypeExpression:
        # 解析字段类型名称
        function_name: str = scanner.pop_as_source()

        # 解析字段类型参数
        if scanner.search_one_type_mark(AMTMark.PARENTHESIS):
            function_params: List[node.ASTExpressionBase] = []
            for param_scanner in scanner.pop_as_children_scanner_list_split_by(","):
                function_params.append(cls._parse_compute_expression(param_scanner, sql_type))
                param_scanner.close()
            return node.ASTColumnTypeExpression(name=function_name, params=tuple(function_params))
        return node.ASTColumnTypeExpression(name=function_name)

    @classmethod
    def parse_partition_expression(cls, scanner_or_string: ScannerOrString,
                                   already_match_partition: bool = False,
                                   sql_type: SQLType = SQLType.DEFAULT) -> node.ASTPartitionExpression:
        """解析分区表达式

        already_match_partition : bool, default = False
            是否已匹配 PARTITION 关键字
        """
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_partition_expression(scanner, already_match_partition, sql_type)

    @classmethod
    def _parse_partition_expression(cls, scanner: TokenScanner, already_match_partition: bool,
                                    sql_type: SQLType) -> node.ASTPartitionExpression:
        if not already_match_partition:
            scanner.match("PARTITION")
        partition_list = []
        is_dynamic_partition = False  # 是否有动态分区
        is_non_dynamic_partition = False  # 是否有非动态分区
        for partition_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            before_value = cls._parse_compute_expression(partition_scanner, sql_type)
            if partition_scanner.search_one_type_set(static.COMPARE_OPERATOR_SET):  # 非动态分区
                is_non_dynamic_partition = True
                operator = cls._parse_compare_operator(partition_scanner)
                after_value = cls._parse_compute_expression(partition_scanner, sql_type)
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
        return cls._parse_foreign_key_expression(scanner)

    @classmethod
    def _parse_foreign_key_expression(cls, scanner: TokenScanner) -> node.ASTForeignKeyExpression:
        """解析外键表达式"""
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
        on_delete = None
        on_update = None
        if scanner.search_and_move_two_type_str_use_upper("ON", "DELETE"):
            on_delete = cls._parse_foreign_key_action(scanner=scanner)
        if scanner.search_and_move_two_type_str_use_upper("ON", "UPDATE"):
            on_update = cls._parse_foreign_key_action(scanner=scanner)
        return node.ASTForeignKeyExpression(
            constraint_name=constraint_name,
            slave_columns=tuple(slave_columns),
            master_table_name=master_table_name,
            master_columns=tuple(master_columns),
            on_delete=on_delete,
            on_update=on_update
        )

    @classmethod
    def _parse_foreign_key_action(cls, scanner: TokenScanner) -> str:
        """解析外键表达式中的 ACTION 表达式"""
        if scanner.search_and_move_two_type_str_use_upper("NO", "ACTION"):
            return "NO ACTION"
        if scanner.search_and_move_two_type_str_use_upper("SET", "NULL"):
            return "SET NULL"
        if scanner.search_and_move_one_type_str_use_upper("CASCADE"):
            return "CASCADE"
        if scanner.search_and_move_one_type_str_use_upper("RESTRICT"):
            return "RESTRICT"
        raise SqlParseError(f"无法解析的外键 ACTION: {scanner}")

    @classmethod
    def parse_index_column(cls, scanner_or_string: ScannerOrString,
                           sql_type: SQLType = SQLType.DEFAULT) -> node.ASTIndexColumn:
        """解析索引声明表达式中的字段"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_index_column(scanner)

    @classmethod
    def _parse_index_column(cls, scanner: TokenScanner) -> node.ASTIndexColumn:
        name = cls._unify_name(scanner.pop_as_source())
        max_length = None
        if scanner.search_one_type_mark(AMTMark.PARENTHESIS):
            parenthesis_scanner = scanner.pop_as_children_scanner()
            max_length = int(parenthesis_scanner.pop_as_source())
            parenthesis_scanner.close()
        return node.ASTIndexColumn(name=name, max_length=max_length)

    @classmethod
    def _get_index_columns(cls, scanner: TokenScanner) -> Tuple[node.ASTIndexColumn, ...]:
        """解析索引表达式中的索引字段"""
        columns = []
        for column_scanner in scanner.pop_as_children_scanner_list_split_by(","):
            columns.append(cls._parse_index_column(column_scanner))
            column_scanner.close()
        return tuple(columns)

    @classmethod
    def parse_primary_index_expression(cls, scanner_or_string: ScannerOrString,
                                       sql_type: SQLType = SQLType.DEFAULT
                                       ) -> node.ASTPrimaryIndexExpression:
        """解析主键表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_primary_index_expression(scanner)

    @classmethod
    def _parse_primary_index_expression(cls, scanner: TokenScanner) -> node.ASTPrimaryIndexExpression:
        scanner.match("PRIMARY", "KEY")
        columns = cls._get_index_columns(scanner)
        using = scanner.pop_as_source() if scanner.search_and_move_one_type_str_use_upper("USING") else None
        comment = scanner.pop_as_source() if scanner.search_and_move_one_type_str_use_upper("COMMENT") else None
        key_block_size = (int(scanner.pop_as_source())
                          if scanner.search_and_move_two_type_str_use_upper("KEY_BLOCK_SIZE", "=") else None)
        return node.ASTPrimaryIndexExpression(columns=columns, using=using, comment=comment,
                                              key_block_size=key_block_size)

    @classmethod
    def parse_unique_index_expression(cls, scanner_or_string: ScannerOrString,
                                      sql_type: SQLType = SQLType.DEFAULT
                                      ) -> node.ASTUniqueIndexExpression:
        """解析唯一键表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_unique_index_expression(scanner)

    @classmethod
    def _parse_unique_index_expression(cls, scanner: TokenScanner) -> node.ASTUniqueIndexExpression:
        scanner.match("UNIQUE", "KEY")
        name = scanner.pop_as_source()
        columns = cls._get_index_columns(scanner)
        using = scanner.pop_as_source() if scanner.search_and_move_one_type_str_use_upper("USING") else None
        comment = scanner.pop_as_source() if scanner.search_and_move_one_type_str_use_upper("COMMENT") else None
        key_block_size = (int(scanner.pop_as_source())
                          if scanner.search_and_move_two_type_str_use_upper("KEY_BLOCK_SIZE", "=") else None)
        return node.ASTUniqueIndexExpression(name=name, columns=columns, using=using, comment=comment,
                                             key_block_size=key_block_size)

    @classmethod
    def parse_normal_index_expression(cls, scanner_or_string: ScannerOrString,
                                      sql_type: SQLType = SQLType.DEFAULT
                                      ) -> node.ASTNormalIndexExpression:
        """解析一般索引表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_normal_index_expression(scanner)

    @classmethod
    def _parse_normal_index_expression(cls, scanner: TokenScanner) -> node.ASTNormalIndexExpression:
        scanner.match("KEY")
        name = scanner.pop_as_source()
        columns = cls._get_index_columns(scanner)
        using = scanner.pop_as_source() if scanner.search_and_move_one_type_str_use_upper("USING") else None
        comment = scanner.pop_as_source() if scanner.search_and_move_one_type_str_use_upper("COMMENT") else None
        key_block_size = (int(scanner.pop_as_source())
                          if scanner.search_and_move_two_type_str_use_upper("KEY_BLOCK_SIZE", "=") else None)
        return node.ASTNormalIndexExpression(name=name, columns=columns, using=using, comment=comment,
                                             key_block_size=key_block_size)

    @classmethod
    def parse_fulltext_expression(cls, scanner_or_string: ScannerOrString, sql_type: SQLType = SQLType.DEFAULT
                                  ) -> node.ASTFulltextIndexExpression:
        """解析全文索引表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_fulltext_expression(scanner)

    @classmethod
    def _parse_fulltext_expression(cls, scanner: TokenScanner) -> node.ASTFulltextIndexExpression:
        scanner.match("FULLTEXT", "KEY")
        name = scanner.pop_as_source()
        columns = cls._get_index_columns(scanner)
        using = scanner.pop_as_source() if scanner.search_and_move_one_type_str_use_upper("USING") else None
        comment = scanner.pop_as_source() if scanner.search_and_move_one_type_str_use_upper("COMMENT") else None
        key_block_size = (int(scanner.pop_as_source())
                          if scanner.search_and_move_two_type_str_use_upper("KEY_BLOCK_SIZE", "=") else None)
        return node.ASTFulltextIndexExpression(name=name, columns=columns, using=using, comment=comment,
                                               key_block_size=key_block_size)

    @classmethod
    def parse_define_column_expression(cls, scanner_or_string: ScannerOrString,
                                       sql_type: SQLType = SQLType.DEFAULT
                                       ) -> node.ASTDefineColumnExpression:
        # pylint: disable=R0914
        """解析 DDL 的字段表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_define_column_expression(scanner, sql_type)

    @classmethod
    def _parse_generated_column(cls, scanner: TokenScanner, sql_type: SQLType) -> Optional[node.ASTGeneratedColumn]:
        """解析字段定义表达式中的计算字段"""
        if scanner.search_and_move_three_type_str_use_upper("GENERATED", "ALWAYS", "AS"):
            children_scanner = scanner.pop_as_children_scanner()
            compute_expression = cls._parse_compute_expression(children_scanner, sql_type)  # 解析
            children_scanner.close()
            save_mode = static.GENERATE_COLUMN_SAVE_MODE_HASH.get(scanner.pop_as_source())
            return node.ASTGeneratedColumn(
                expression=compute_expression,
                save_mode=save_mode
            )
        return None

    @classmethod
    def _parse_define_column_expression(cls, scanner: TokenScanner, sql_type: SQLType
                                        ) -> node.ASTDefineColumnExpression:
        # pylint: disable=R0912
        # pylint: disable=R0914
        # 解析顺序固定的信息
        column_name = scanner.pop_as_source()
        column_type = cls._parse_column_type_expression(scanner, sql_type)

        # 解析顺序可能不定的字段信息
        comment: Optional[str] = None
        is_unsigned: bool = False
        is_zerofill: bool = False
        character_set: Optional[str] = None
        collate: Optional[str] = None
        generated_always_as: Optional[node.ASTGeneratedColumn] = None
        is_allow_null: bool = False
        is_not_null: bool = False
        is_auto_increment: bool = False
        default: Optional[node.ASTExpressionBase] = None
        on_update: Optional[node.ASTExpressionBase] = None
        while not scanner.is_finish:
            if scanner.search_and_move_two_type_str_use_upper("NOT", "NULL"):
                is_not_null = True
            elif scanner.search_and_move_one_type_str_use_upper("NULL"):
                is_allow_null = True
            elif scanner.search_and_move_two_type_str_use_upper("CHARACTER", "SET"):
                character_set = scanner.pop_as_source()
            elif scanner.search_and_move_one_type_str_use_upper("COLLATE"):
                collate = scanner.pop_as_source()
            elif scanner.search_and_move_one_type_str_use_upper("DEFAULT"):
                default = cls._parse_compute_expression(scanner, sql_type)
            elif scanner.search_and_move_one_type_str_use_upper("COMMENT"):
                comment = scanner.pop_as_source()
            elif scanner.search_and_move_two_type_str_use_upper("ON", "UPDATE"):
                on_update = cls._parse_compute_expression(scanner, sql_type)
            elif scanner.search_and_move_one_type_str_use_upper("AUTO_INCREMENT"):
                is_auto_increment = True
            elif scanner.search_and_move_one_type_str_use_upper("UNSIGNED"):
                is_unsigned = True
            elif scanner.search_and_move_one_type_str_use_upper("ZEROFILL"):
                is_zerofill = True
            elif scanner.search_one_type_str_use_upper("GENERATED"):  # GENERATED ALWAYS AS
                generated_always_as = cls._parse_generated_column(scanner, sql_type)
            else:
                raise SqlParseError(f"无法解析的 DDL 字段表达式的字段属性: {scanner}")

        # 构造 DDL 字段表达式对象
        return node.ASTDefineColumnExpression(
            column_name=cls._unify_name(column_name),
            column_type=column_type,
            comment=comment,
            is_unsigned=is_unsigned,
            is_zerofill=is_zerofill,
            character_set=character_set,
            collate=collate,
            generated_always_as=generated_always_as,
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
        return cls._parse_insert_statement(scanner, with_clause, sql_type)

    @classmethod
    def _parse_insert_statement(cls, scanner: TokenScanner,
                                with_clause: Optional[node.ASTWithClause],
                                sql_type: SQLType
                                ) -> node.ASTInsertStatement:
        if with_clause is None:
            with_clause = cls._parse_with_clause(scanner, sql_type)

        insert_type = cls._parse_insert_type(scanner)

        # 匹配可能包含的 TABLE 关键字
        scanner.search_and_move_one_type_str_use_upper("TABLE")

        # 匹配表名
        table_name = cls._parse_table_name_expression(scanner)

        # 匹配分区表达式
        if scanner.search_one_type_str_use_upper("PARTITION"):
            partition = cls._parse_partition_expression(scanner, False, sql_type)
        else:
            partition = None

        # 匹配列名列表
        if scanner.search_one_type_mark(AMTMark.PARENTHESIS):
            columns = []
            for column_scanner in scanner.pop_as_children_scanner_list_split_by(","):
                columns.append(cls._parse_column_name_expression(column_scanner))
                column_scanner.close()
        else:
            columns = None

        # 匹配 VALUES 类型
        if scanner.search_and_move_one_type_str_use_upper("VALUES"):
            values = []
            while scanner.search_one_type_mark(AMTMark.PARENTHESIS):
                values.append(cls._parse_sub_value_expression(scanner, sql_type=sql_type))
                scanner.search_and_move_one_type_str(",")

            return node.ASTInsertValuesStatement(
                with_clause=with_clause,
                insert_type=insert_type,
                table_name=table_name,
                partition=partition,
                columns=tuple(columns) if columns is not None else None,
                values=tuple(values)
            )

        if scanner.search_one_type_str_use_upper("SELECT"):
            select_statement = cls._parse_select_statement(scanner, node.ASTWithClause.empty(), sql_type)
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
        return cls._parse_set_statement(scanner)

    @classmethod
    def _parse_set_statement(cls, scanner: TokenScanner) -> node.ASTSetStatement:
        scanner.match("SET")
        config = cls._parse_config_string_expression(scanner)
        return node.ASTSetStatement(config=config)

    @classmethod
    def parse_create_table_statement(cls, scanner_or_string: ScannerOrString,
                                     sql_type: SQLType = SQLType.DEFAULT) -> AliasCreateTableStatement:
        """解析 CREATE TABLE 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_create_table_statement(scanner, sql_type)

    @classmethod
    def _parse_create_table_statement(cls, scanner: TokenScanner, sql_type: SQLType) -> AliasCreateTableStatement:
        # pylint: disable=R0912
        # pylint: disable=R0914
        # pylint: disable=R0915
        # 解析字段、索引括号前的部分
        scanner.match("CREATE", "TABLE")
        if_not_exists = scanner.search_and_move_three_type_str_use_upper("IF", "NOT", "EXISTS")
        table_name = cls._parse_table_name_expression(scanner)

        # CREATE TABLE ... AS ... 语句
        if scanner.search_and_move_one_type_str_use_upper("AS"):
            select_statement = cls._parse_select_statement(scanner, None, sql_type)
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
            if group_scanner.search_two_type_str_use_upper("PRIMARY", "KEY"):
                primary_key = cls._parse_primary_index_expression(group_scanner)
            elif group_scanner.search_two_type_str_use_upper("UNIQUE", "KEY"):
                unique_key.append(cls._parse_unique_index_expression(group_scanner))
            elif group_scanner.search_one_type_str_use_upper("KEY"):
                key.append(cls._parse_normal_index_expression(group_scanner))
            elif group_scanner.search_two_type_str_use_upper("FULLTEXT", "KEY"):
                fulltext_key.append(cls._parse_fulltext_expression(group_scanner))
            elif group_scanner.search_one_type_str_use_upper("CONSTRAINT"):
                foreign_key.append(cls._parse_foreign_key_expression(group_scanner))
            else:
                columns.append(cls._parse_define_column_expression(group_scanner, sql_type))
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
        while not scanner.is_finish and not scanner.search_one_type_str(";"):
            if scanner.search_and_move_one_type_str_use_upper("ENGINE"):
                scanner.search_and_move_one_type_str("=")
                engine = scanner.pop_as_source()
            elif scanner.search_and_move_one_type_str_use_upper("AUTO_INCREMENT"):
                scanner.search_and_move_one_type_str("=")
                auto_increment = int(scanner.pop_as_source())
            elif scanner.search_and_move_two_type_str_use_upper("DEFAULT", "CHARSET"):
                scanner.search_and_move_one_type_str("=")
                default_charset = scanner.pop_as_source()
            elif scanner.search_and_move_one_type_str_use_upper("ROW_FORMAT"):
                scanner.search_and_move_one_type_str("=")
                row_format = scanner.pop_as_source()
            elif scanner.search_and_move_one_type_str_use_upper("COLLATE"):
                scanner.search_and_move_one_type_str("=")
                collate = scanner.pop_as_source()
            elif scanner.search_and_move_one_type_str_use_upper("COMMENT"):
                scanner.search_and_move_one_type_str("=")
                comment = scanner.pop_as_source()
            elif scanner.search_and_move_one_type_str_use_upper("STATS_PERSISTENT"):
                scanner.search_and_move_one_type_str("=")
                states_persistent = scanner.pop_as_source()
            elif scanner.search_and_move_two_type_str_use_upper("PARTITIONED", "BY"):
                for group_scanner in scanner.pop_as_children_scanner_list_split_by(","):
                    partitioned_by.append(cls._parse_define_column_expression(group_scanner, sql_type))
                    group_scanner.close()
            elif scanner.search_and_move_three_type_str_use_upper("ROW", "FORMAT", "SERDE"):
                scanner.search_and_move_one_type_str("=")
                row_format_serde = scanner.pop_as_source()
            elif scanner.search_and_move("ROW", "FORMAT", "DELIMITED", "FIELDS", "TERMINATED", "BY"):
                scanner.search_and_move_one_type_str("=")
                row_format_delimited_fields_terminated_by = scanner.pop_as_source()
            elif scanner.search_and_move_three_type_str_use_upper("STORED", "AS", "INPUTFORMAT"):
                scanner.search_and_move_one_type_str("=")
                stored_as_inputformat = scanner.pop_as_source()
            elif scanner.search_and_move_three_type_str_use_upper("STORED", "AS", "TEXTFILE"):
                stored_as_textfile = True
            elif scanner.search_and_move_one_type_str_use_upper("OUTPUTFORMAT"):
                scanner.search_and_move_one_type_str("=")
                outputformat = scanner.pop_as_source()
            elif scanner.search_and_move_one_type_str_use_upper("LOCATION"):
                scanner.search_and_move_one_type_str("=")
                location = scanner.pop_as_source()
            elif scanner.search_and_move_one_type_str_use_upper("TBLPROPERTIES"):
                for group_scanner in scanner.pop_as_children_scanner_list_split_by(","):
                    tblproperties.append(cls._parse_config_string_expression(group_scanner))
                    group_scanner.close()
            else:
                raise SqlParseError(f"未知的 DDL 表属性: {scanner}")
        scanner.search_and_move_one_type_str(";")

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
        return cls._parse_drop_table_statement(scanner)

    @classmethod
    def _parse_drop_table_statement(cls, scanner: TokenScanner) -> node.ASTDropTableStatement:
        scanner.match("DROP", "TABLE")
        if_exists = scanner.search_and_move_two_type_str_use_upper("IF", "EXISTS")
        table_name = cls._parse_table_name_expression(scanner)
        return node.ASTDropTableStatement(if_exists=if_exists, table_name=table_name)

    @classmethod
    def parse_analyze_table_statement(cls, scanner_or_string: ScannerOrString,
                                      sql_type: SQLType = SQLType.DEFAULT) -> node.ASTAnalyzeTableStatement:
        """解析 ANALYZE TABLE 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_analyze_table_statement(scanner, sql_type)

    @classmethod
    def _parse_analyze_table_statement(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTAnalyzeTableStatement:
        scanner.match("ANALYZE", "TABLE")
        table_name = cls._parse_table_name_expression(scanner)

        if scanner.search_one_type_str_use_upper("PARTITION"):
            partition = cls._parse_partition_expression(scanner, False, sql_type)
        else:
            partition = None

        scanner.search_and_move_two_type_str_use_upper("COMPUTE", "STATISTICS")  # [Hive]
        for_columns = scanner.search_and_move_two_type_str_use_upper("FOR", "COLUMNS")  # [Hive]
        cache_metadata = scanner.search_and_move_two_type_str_use_upper("CACHE", "METADATA")  # [Hive]
        noscan = scanner.search_and_move_one_type_str_use_upper("NOSCAN")  # [Hive]

        return node.ASTAnalyzeTableStatement(
            table_name=table_name,
            partition=partition,
            for_columns=for_columns,
            cache_metadata=cache_metadata,
            noscan=noscan
        )

    @classmethod
    def parse_column_or_index(cls, scanner_or_string: ScannerOrString,
                              sql_type: SQLType = SQLType.DEFAULT) -> node.AliasColumnOrIndex:
        """解析字段声明表达式或索引声明表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_column_or_index(scanner, sql_type)

    @classmethod
    def _parse_column_or_index(cls, scanner: TokenScanner, sql_type: SQLType) -> node.AliasColumnOrIndex:
        if scanner.search_two_type_str_use_upper("PRIMARY", "KEY"):
            return cls._parse_primary_index_expression(scanner)
        if scanner.search_two_type_str_use_upper("UNIQUE", "KEY"):
            return cls._parse_unique_index_expression(scanner)
        if scanner.search_one_type_str_use_upper("KEY"):
            return cls._parse_normal_index_expression(scanner)
        if scanner.search_two_type_str_use_upper("FULLTEXT", "KEY"):
            return cls._parse_fulltext_expression(scanner)
        if scanner.search_one_type_str_use_upper("CONSTRAINT"):
            return cls._parse_foreign_key_expression(scanner)
        return cls._parse_define_column_expression(scanner, sql_type)

    @classmethod
    def parse_alter_expression(cls, scanner_or_string: ScannerOrString,
                               sql_type: SQLType = SQLType.DEFAULT) -> node.ASTAlterExpressionBase:
        """解析 ALTER TABLE 的子句表达式"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_alter_expression(scanner, sql_type)

    @classmethod
    def _parse_alter_expression(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTAlterExpressionBase:
        # pylint: disable=R0911
        # pylint: disable=W0511
        if scanner.search_and_move_two_type_str_use_upper("ADD", "PARTITION"):
            return node.ASTAlterAddPartitionExpression(
                if_not_exists=False,
                partition=cls._parse_partition_expression(scanner, True, sql_type)
            )
        if scanner.search_and_move("ADD", "IF", "NOT", "EXISTS", "PARTITION"):
            return node.ASTAlterAddPartitionExpression(
                if_not_exists=True,
                partition=cls._parse_partition_expression(scanner, True, sql_type)
            )
        if scanner.search_and_move_one_type_str_use_upper("ADD"):  # TODO 待拆分
            return node.ASTAlterAddExpression(
                expression=cls._parse_column_or_index(scanner, sql_type)
            )
        if scanner.search_and_move_one_type_str_use_upper("MODIFY"):
            return node.ASTAlterModifyExpression(
                expression=cls._parse_column_or_index(scanner, sql_type)
            )
        if scanner.search_and_move_one_type_str_use_upper("CHANGE"):
            from_column_name = cls._unify_name(scanner.pop_as_source())
            to_expression = cls._parse_column_or_index(scanner, sql_type)
            return node.ASTAlterChangeExpression(
                from_column_name=from_column_name,
                to_expression=to_expression
            )
        if scanner.search_and_move_two_type_str_use_upper("RENAME", "COLUMN"):
            from_column_name = cls._unify_name(scanner.pop_as_source())
            scanner.match("TO")
            to_column_name = cls._unify_name(scanner.pop_as_source())
            return node.ASTAlterRenameColumnExpression(
                from_column_name=from_column_name,
                to_column_name=to_column_name
            )
        if scanner.search_and_move_two_type_str_use_upper("DROP", "COLUMN"):
            return node.ASTAlterDropColumnExpression(
                column_name=cls._unify_name(scanner.pop_as_source())
            )
        if scanner.search_and_move_two_type_str_use_upper("DROP", "PARTITION"):
            return node.ASTAlterDropPartitionExpression(
                if_exists=False,
                partition=cls._parse_partition_expression(scanner, True, sql_type)
            )
        if scanner.search_and_move("DROP", "IF", "EXISTS", "PARTITION"):
            return node.ASTAlterDropPartitionExpression(
                if_exists=True,
                partition=cls._parse_partition_expression(scanner, True, sql_type)
            )
        raise SqlParseError(f"未知的 ALTER TABLE 类型: {scanner}")

    @classmethod
    def parse_alter_table_statement(cls, scanner_or_string: ScannerOrString,
                                    sql_type: SQLType = SQLType.DEFAULT) -> node.ASTAlterTableStatement:
        """解析 ALTER TABLE 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_alter_table_statement(scanner, sql_type)

    @classmethod
    def _parse_alter_table_statement(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTAlterTableStatement:
        scanner.match("ALTER", "TABLE")
        table_name = cls._parse_table_name_expression(scanner)
        expressions = [cls._parse_alter_expression(scanner, sql_type)]
        while scanner.search_and_move_one_type_str(","):
            expressions.append(cls._parse_alter_expression(scanner, sql_type))
        return node.ASTAlterTableStatement(
            table_name=table_name,
            expressions=tuple(expressions)
        )

    @classmethod
    def parse_msck_repair_table_statement(cls, scanner_or_string: ScannerOrString,
                                          sql_type: SQLType = SQLType.DEFAULT) -> node.ASTMsckRepairTableStatement:
        """解析 MSCK REPAIR 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_msck_repair_table_statement(scanner)

    @classmethod
    def _parse_msck_repair_table_statement(cls, scanner: TokenScanner) -> node.ASTMsckRepairTableStatement:
        scanner.match("MSCK", "REPAIR", "TABLE")
        table_name = cls._parse_table_name_expression(scanner)
        return node.ASTMsckRepairTableStatement(
            table_name=table_name
        )

    @classmethod
    def parse_use_statement(cls, scanner_or_string: ScannerOrString,
                            sql_type: SQLType = SQLType.DEFAULT) -> node.ASTUseStatement:
        """解析 USE 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_use_statement(scanner)

    @classmethod
    def _parse_use_statement(cls, scanner: TokenScanner) -> node.ASTUseStatement:
        scanner.match("USE")
        return node.ASTUseStatement(
            schema_name=scanner.pop_as_source()
        )

    @classmethod
    def parse_truncate_table_statement(cls, scanner_or_string: ScannerOrString,
                                       sql_type: SQLType = SQLType.DEFAULT) -> node.ASTTruncateTable:
        """解析 TRUNCATE TABLE 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_truncate_table_statement(scanner)

    @classmethod
    def _parse_truncate_table_statement(cls, scanner: TokenScanner) -> node.ASTTruncateTable:
        scanner.match("TRUNCATE", "TABLE")
        table_name = cls._parse_table_name_expression(scanner)
        return node.ASTTruncateTable(
            table_name=table_name
        )

    @classmethod
    def parse_update_set_column(cls, scanner_or_string: ScannerOrString,
                                sql_type: SQLType = SQLType.DEFAULT) -> node.ASTUpdateSetColumn:
        """解析 UPDATE 语句中 SET 中的字段元素"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_update_set_column(scanner, sql_type)

    @classmethod
    def _parse_update_set_column(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTUpdateSetColumn:
        column_name = scanner.pop_as_source()
        scanner.match("=")
        column_value = cls._parse_logical_or_level_expression(scanner, sql_type)
        return node.ASTUpdateSetColumn(
            column_name=column_name,
            column_value=column_value
        )

    @classmethod
    def parse_update_set_clause(cls, scanner_or_string: ScannerOrString,
                                sql_type: SQLType = SQLType.DEFAULT) -> node.ASTUpdateSetClause:
        """解析 UPDATE 语句的 SET 子句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_update_set_clause(scanner, sql_type)

    @classmethod
    def _parse_update_set_clause(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTUpdateSetClause:
        scanner.match("SET")
        columns = [cls._parse_update_set_column(scanner, sql_type)]
        while scanner.search_and_move_one_type_str(","):
            columns.append(cls._parse_update_set_column(scanner, sql_type))
        return node.ASTUpdateSetClause(
            columns=tuple(columns)
        )

    @classmethod
    def parse_update_statement(cls, scanner_or_string: ScannerOrString,
                               with_clause: Optional[node.ASTWithClause],
                               sql_type: SQLType = SQLType.DEFAULT) -> node.ASTUpdateStatement:
        """解析 UPDATE 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_update_statement(scanner, with_clause, sql_type)

    @classmethod
    def _parse_update_statement(cls, scanner: TokenScanner,
                                with_clause: Optional[node.ASTWithClause],
                                sql_type: SQLType) -> node.ASTUpdateStatement:
        scanner.match("UPDATE")
        table_name = cls._parse_table_name_expression(scanner)
        set_clause = cls._parse_update_set_clause(scanner, sql_type)
        where_clause = cls._parse_where_clause(scanner, sql_type)
        order_by_clause = cls._parse_order_by_clause(scanner, sql_type)
        limit_clause = cls._parse_limit_clause(scanner)
        return node.ASTUpdateStatement(
            with_clause=with_clause,
            table_name=table_name,
            set_clause=set_clause,
            where_clause=where_clause,
            order_by_clause=order_by_clause,
            limit_clause=limit_clause
        )

    @classmethod
    def parse_delete_statement(cls, scanner_or_string: ScannerOrString,
                               sql_type: SQLType = SQLType.DEFAULT) -> node.ASTDeleteStatement:
        """解析 UPDATE 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_delete_statement(scanner, sql_type)

    @classmethod
    def _parse_delete_statement(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTDeleteStatement:
        scanner.match("DELETE", "FROM")
        table_name = cls._parse_table_name_expression(scanner)
        where_clause = cls._parse_where_clause(scanner, sql_type)
        order_by_clause = cls._parse_order_by_clause(scanner, sql_type)
        limit_clause = cls._parse_limit_clause(scanner)
        return node.ASTDeleteStatement(
            table_name=table_name,
            where_clause=where_clause,
            order_by_clause=order_by_clause,
            limit_clause=limit_clause
        )

    @classmethod
    def parse_show_columns_statement(cls, scanner_or_string: ScannerOrString,
                                     sql_type: SQLType = SQLType.DEFAULT) -> node.ASTShowColumnsStatement:
        """解析 SHOW COLUMNS 语句"""
        scanner = cls._unify_input_scanner(scanner_or_string, sql_type=sql_type)
        return cls._parse_show_columns_statement(scanner, sql_type)

    @classmethod
    def _parse_show_columns_statement(cls, scanner: TokenScanner, sql_type: SQLType) -> node.ASTShowColumnsStatement:
        scanner.match("SHOW", "COLUMNS")
        from_clause = cls._parse_from_clause(scanner, sql_type)
        where_clause = cls._parse_where_clause(scanner, sql_type)
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
            if scanner.search_one_type_str_use_upper("SET"):
                statement_list.append(cls._parse_set_statement(scanner))

            # 解析 DELETE 语句
            elif scanner.search_two_type_str_use_upper("DELETE", "FROM"):
                statement_list.append(cls._parse_delete_statement(scanner, sql_type))

            # 解析 DROP TABLE 语句
            elif scanner.search_two_type_str_use_upper("DROP", "TABLE"):
                statement_list.append(cls._parse_drop_table_statement(scanner))

            # 解析 CREATE TABLE 语句
            elif scanner.search_two_type_str_use_upper("CREATE", "TABLE"):
                statement_list.append(cls._parse_create_table_statement(scanner, sql_type))

            # 解析 ANALYZE TABLE 语句
            elif scanner.search_two_type_str_use_upper("ANALYZE", "TABLE"):
                statement_list.append(cls._parse_analyze_table_statement(scanner, sql_type))

            # 解析 ALTER TABLE 语句
            elif scanner.search_two_type_str_use_upper("ALTER", "TABLE"):
                statement_list.append(cls._parse_alter_table_statement(scanner, sql_type))

            # 解析 MSCK REPAIR TABLE 语句
            elif scanner.search_three_type_str_use_upper("MSCK", "REPAIR", "TABLE"):
                statement_list.append(cls._parse_msck_repair_table_statement(scanner))

            # 解析 USE 语句
            elif scanner.search_one_type_str_use_upper("USE"):
                statement_list.append(cls._parse_use_statement(scanner))

            # 解析 TRUNCATE TABLE 语句
            elif scanner.search_two_type_str_use_upper("TRUNCATE", "TABLE"):
                statement_list.append(cls._parse_truncate_table_statement(scanner))

            # 解析 SHOW DATABASES 语句
            elif scanner.search_and_move_two_type_str_use_upper("SHOW", "DATABASES"):
                statement_list.append(node.ASTShowDatabasesStatement())

            # 解析 SHOW TABLES 语句
            elif scanner.search_and_move_two_type_str_use_upper("SHOW", "TABLES"):
                statement_list.append(node.ASTShowTablesStatement())

            # 解析 SHOW COLUMNS 语句
            elif scanner.search_and_move_two_type_str_use_upper("SHOW", "COLUMNS"):
                statement_list.append(cls._parse_show_columns_statement(scanner, sql_type))

            else:
                # 解析可能包含 WITH 子句的语句类型
                with_clause = cls._parse_with_clause(scanner, sql_type)

                # 解析 SELECT 语句
                if scanner.search_one_type_str_use_upper("SELECT"):
                    statement_list.append(cls._parse_select_statement(scanner, with_clause, sql_type))

                # 解析 INSERT 语句
                elif scanner.search_one_type_str_use_upper("INSERT"):
                    statement_list.append(cls._parse_insert_statement(scanner, with_clause, sql_type))

                # 解析 UPDATE 语句
                elif scanner.search_one_type_str_use_upper("UPDATE"):
                    statement_list.append(cls._parse_update_statement(scanner, with_clause, sql_type))

                else:
                    raise SqlParseError(f"未知语句类型: {scanner}")

            scanner.search_and_move_one_type_str(";")

        scanner.close()

        return statement_list
