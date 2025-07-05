"""
通用表达式（general_expression）单元测试

测试 general_expression.py 中的语义组：
- simple_expr: 简单表达式
"""

from unittest import TestCase

from metasequoia_sql import ast, parse_expression


class TestSimpleExpr(TestCase):
    """测试 simple_expr 语义组
    
    测试各种简单表达式的解析，包括标识符、函数、字面量、操作符等
    """

    def test_simple_ident(self):
        """测试简单标识符"""
        node = parse_expression("column_name")
        self.assertIsInstance(node, ast.Ident)
        self.assertEqual(node.get_str_value(), "column_name")

    def test_function_expression(self):
        """测试函数表达式"""
        node = parse_expression("NOW()")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "now")
        self.assertEqual(len(node.param_list), 0)

    def test_collate_operator(self):
        """测试 COLLATE 操作符"""
        node = parse_expression("column_name COLLATE utf8_general_ci")
        self.assertIsInstance(node, ast.OperatorCollate)
        self.assertIsInstance(node.collation_operand, ast.Ident)
        self.assertEqual(node.collation_name, "utf8_general_ci")

    def test_literal_or_null(self):
        """测试字面量或 NULL 值"""
        # 测试字符串字面量
        node = parse_expression("'hello'")
        self.assertIsInstance(node, ast.StringLiteral)

        # 测试 NULL 值
        node = parse_expression("NULL")
        self.assertIsInstance(node, ast.NullLiteral)

    def test_param_marker(self):
        """测试参数标记"""
        node = parse_expression("?")
        self.assertIsInstance(node, ast.Param)

    def test_system_or_user_variable(self):
        """测试系统变量或用户变量"""
        # 测试系统变量
        node = parse_expression("@@session.sql_mode")
        self.assertIsInstance(node, ast.SystemVariable)

        # 测试用户变量
        node = parse_expression("@user_var")
        self.assertIsInstance(node, ast.UserVariable)

    def test_user_variable_assignment(self):
        """测试用户变量赋值"""
        node = parse_expression("@user_var := 'value'")
        self.assertIsInstance(node, ast.UserVariableAssignment)

    def test_sum_function_expression(self):
        """测试聚合函数表达式"""
        node = parse_expression("SUM(column_name)")
        self.assertIsInstance(node, ast.FuncSumSum)
        self.assertEqual(node.distinct, False)
        self.assertIsNotNone(node.param)

    def test_window_function_expression(self):
        """测试窗口函数表达式"""
        node = parse_expression("ROW_NUMBER() OVER (ORDER BY column_name)")
        self.assertIsInstance(node, ast.FuncWindowRowNumber)
        self.assertIsNotNone(node.window_clause)

    def test_concat_operator(self):
        """测试字符串连接操作符 ||"""
        node = parse_expression("'hello' || 'world'")
        self.assertIsInstance(node, ast.OperatorConcat)
        self.assertIsInstance(node.left_operand, ast.StringLiteral)
        self.assertIsInstance(node.right_operand, ast.StringLiteral)

    def test_unary_plus_operator(self):
        """测试一元加号操作符"""
        node = parse_expression("+123")
        # 一元加号应该直接返回操作数
        self.assertIsInstance(node, ast.IntLiteral)

    def test_negative_operator(self):
        """测试负号操作符"""
        node = parse_expression("-123")
        self.assertIsInstance(node, ast.OperatorNegative)
        self.assertIsInstance(node.operand, ast.IntLiteral)

    def test_bit_not_operator(self):
        """测试按位取反操作符"""
        node = parse_expression("~123")
        self.assertIsInstance(node, ast.OperatorBitNot)
        self.assertIsInstance(node.operand, ast.IntLiteral)

    def test_truth_transform_operator(self):
        """测试真值转换操作符"""
        node = parse_expression("!column_name")
        self.assertIsInstance(node, ast.OperatorTruthTransform)
        self.assertIsInstance(node.operand, ast.Ident)

    def test_subquery(self):
        """测试子查询"""
        node = parse_expression("(SELECT column_name FROM table_name)")
        self.assertIsInstance(node, ast.SingleRowSubSelect)
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_parenthesized_expression(self):
        """测试括号表达式"""
        node = parse_expression("(column_name)")
        # 括号应该直接返回内部表达式
        self.assertIsInstance(node, ast.Ident)
        self.assertEqual(node.get_str_value(), "column_name")

    def test_row_value_constructor(self):
        """测试行值构造器"""
        node = parse_expression("(column_name_1, column_name_2)")
        self.assertIsInstance(node, ast.Row)
        self.assertEqual(len(node.value_list), 2)
        self.assertIsInstance(node.value_list[0], ast.Ident)
        self.assertIsInstance(node.value_list[1], ast.Ident)

    def test_row_keyword_constructor(self):
        """测试 ROW 关键字构造器"""
        node = parse_expression("ROW(column_name_1, column_name_2)")
        self.assertIsInstance(node, ast.Row)
        self.assertEqual(len(node.value_list), 2)
        self.assertIsInstance(node.value_list[0], ast.Ident)
        self.assertIsInstance(node.value_list[1], ast.Ident)

    def test_exists_subquery(self):
        """测试 EXISTS 子查询"""
        node = parse_expression("EXISTS (SELECT * FROM table_name)")
        self.assertIsInstance(node, ast.ExistsSubSelect)
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_odbc_date(self):
        """测试 ODBC 日期格式"""
        node = parse_expression("{d '2023-01-01'}")
        self.assertIsInstance(node, ast.OdbcDate)
        self.assertEqual(node.odbc_type, "d")
        self.assertIsInstance(node.odbc_value, ast.StringLiteral)

    def test_match_against_operator(self):
        """测试 MATCH AGAINST 操作符"""
        node = parse_expression("MATCH (column_name) AGAINST ('search_text')")
        self.assertIsInstance(node, ast.OperatorMatch)
        self.assertEqual(len(node.column_list), 1)
        self.assertIsInstance(node.column_list[0], ast.Ident)
        self.assertIsInstance(node.sub_string, ast.StringLiteral)

    def test_binary_operator(self):
        """测试 BINARY 操作符"""
        node = parse_expression("BINARY 'text'")
        self.assertIsInstance(node, ast.OperatorBinary)
        self.assertIsInstance(node.operand, ast.StringLiteral)

    def test_cast_function_basic(self):
        """测试 CAST 函数基本形式"""
        node = parse_expression("CAST(column_name AS CHAR(10))")
        self.assertIsInstance(node, ast.FunctionCast)
        self.assertIsInstance(node.expression, ast.Ident)
        self.assertFalse(node.at_local)
        self.assertFalse(node.is_array_cast)

    def test_cast_function_at_local(self):
        """测试 CAST 函数 AT LOCAL 形式"""
        node = parse_expression("CAST(column_name AT LOCAL AS CHAR(10))")
        self.assertIsInstance(node, ast.FunctionCast)
        self.assertIsInstance(node.expression, ast.Ident)
        self.assertTrue(node.at_local)
        self.assertFalse(node.is_array_cast)

    def test_cast_function_at_time_zone(self):
        """测试 CAST 函数 AT TIME ZONE 形式"""
        node = parse_expression("CAST(column_name AT TIME ZONE 'UTC' AS DATETIME(6))")
        self.assertIsInstance(node, ast.FunctionCastAtTimeZone)
        self.assertIsInstance(node.expression, ast.Ident)
        self.assertFalse(node.is_interval)
        self.assertEqual(node.time_zone, "UTC")

    def test_case_expression_simple(self):
        """测试 CASE 表达式（简单形式）"""
        node = parse_expression("CASE column_name WHEN 1 THEN 'one' ELSE 'other' END")
        self.assertIsInstance(node, ast.Case)
        self.assertIsInstance(node.case_expression, ast.Ident)
        self.assertEqual(len(node.when_list), 1)
        self.assertIsInstance(node.else_expression, ast.StringLiteral)

    def test_case_expression_searched(self):
        """测试 CASE 表达式（搜索形式）"""
        node = parse_expression("CASE WHEN column_name > 0 THEN 'positive' ELSE 'negative' END")
        self.assertIsInstance(node, ast.Case)
        self.assertIsNone(node.case_expression)
        self.assertEqual(len(node.when_list), 1)
        self.assertIsInstance(node.else_expression, ast.StringLiteral)

    def test_convert_function_basic(self):
        """测试 CONVERT 函数基本形式"""
        node = parse_expression("CONVERT(column_name, CHAR(10))")
        self.assertIsInstance(node, ast.FunctionConvert)
        self.assertIsInstance(node.expression, ast.Ident)
        self.assertIsNotNone(node.cast_type)

    def test_convert_function_using_charset(self):
        """测试 CONVERT 函数 USING 字符集形式"""
        node = parse_expression("CONVERT(column_name USING utf8)")
        self.assertIsInstance(node, ast.FunctionConvertCharset)
        self.assertIsInstance(node.expression, ast.Ident)
        self.assertIsNotNone(node.charset_name)

    def test_default_function(self):
        """测试 DEFAULT 函数"""
        node = parse_expression("DEFAULT(column_name)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "default")
        self.assertEqual(len(node.param_list), 1)
        self.assertIsInstance(node.param_list[0], ast.Ident)

    def test_values_function(self):
        """测试 VALUES 函数"""
        node = parse_expression("VALUES(column_name)")
        self.assertIsInstance(node, ast.FunctionExpression)
        self.assertEqual(node.function_name, "values")
        self.assertEqual(len(node.param_list), 1)
        self.assertIsInstance(node.param_list[0], ast.Ident)

    def test_time_interval_plus_expr(self):
        """测试时间间隔加表达式"""
        node = parse_expression("INTERVAL 1 DAY")
        self.assertIsInstance(node, ast.TimeInterval)
        self.assertIsInstance(node.time_unit, ast.TimeUnitEnum)
        self.assertIsInstance(node.time_value, ast.IntLiteral)

    def test_json_separator_operator(self):
        """测试 JSON 分隔符操作符"""
        node = parse_expression("column_name -> '$.path'")
        self.assertIsInstance(node, ast.OperatorJsonSeparator)
        self.assertIsInstance(node.expression, ast.Ident)
        self.assertEqual(node.path, "$.path")
        self.assertFalse(node.is_unquoted)

    def test_json_unquoted_separator_operator(self):
        """测试 JSON 非引号分隔符操作符"""
        node = parse_expression("column_name ->> '$.path'")
        self.assertIsInstance(node, ast.OperatorJsonSeparator)
        self.assertIsInstance(node.expression, ast.Ident)
        self.assertEqual(node.path, "$.path")
        self.assertTrue(node.is_unquoted)


class TestBinaryExpr(TestCase):
    """测试 binary_expr 语义组
    
    测试各种二元表达式的解析，包括算术操作符、位操作符、日期操作符等
    """

    def test_bit_or_operator(self):
        """测试按位或操作符 |"""
        node = parse_expression("column_name_1 | column_name_2")
        self.assertIsInstance(node, ast.OperatorBitOr)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)

    def test_bit_and_operator(self):
        """测试按位与操作符 &"""
        node = parse_expression("column_name_1 & column_name_2")
        self.assertIsInstance(node, ast.OperatorBitAnd)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)

    def test_shift_left_operator(self):
        """测试左移操作符 <<"""
        node = parse_expression("column_name_1 << column_name_2")
        self.assertIsInstance(node, ast.OperatorShiftLeft)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)

    def test_shift_right_operator(self):
        """测试右移操作符 >>"""
        node = parse_expression("column_name_1 >> column_name_2")
        self.assertIsInstance(node, ast.OperatorShiftRight)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)

    def test_plus_operator(self):
        """测试加法操作符 +"""
        node = parse_expression("column_name_1 + column_name_2")
        self.assertIsInstance(node, ast.OperatorPlus)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)

    def test_minus_operator(self):
        """测试减法操作符 -"""
        node = parse_expression("column_name_1 - column_name_2")
        self.assertIsInstance(node, ast.OperatorMinus)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)

    def test_plus_time_interval_operator(self):
        """测试日期加法操作符 + time_interval"""
        node = parse_expression("column_name + INTERVAL 1 DAY")
        self.assertIsInstance(node, ast.OperatorPlusDate)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.TimeInterval)

    def test_minus_time_interval_operator(self):
        """测试日期减法操作符 - time_interval"""
        node = parse_expression("column_name - INTERVAL 1 DAY")
        self.assertIsInstance(node, ast.OperatorMinusDate)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.TimeInterval)

    def test_multiply_operator(self):
        """测试乘法操作符 *"""
        node = parse_expression("column_name_1 * column_name_2")
        self.assertIsInstance(node, ast.OperatorMul)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)

    def test_divide_operator(self):
        """测试除法操作符 /"""
        node = parse_expression("column_name_1 / column_name_2")
        self.assertIsInstance(node, ast.OperatorDiv)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)

    def test_modulo_operator(self):
        """测试求模操作符 %"""
        node = parse_expression("column_name_1 % column_name_2")
        self.assertIsInstance(node, ast.OperatorMod)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)

    def test_div_keyword_operator(self):
        """测试整数除法操作符 DIV"""
        node = parse_expression("column_name_1 DIV column_name_2")
        self.assertIsInstance(node, ast.OperatorDivInt)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)

    def test_mod_keyword_operator(self):
        """测试求模操作符 MOD"""
        node = parse_expression("column_name_1 MOD column_name_2")
        self.assertIsInstance(node, ast.OperatorMod)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)

    def test_bit_xor_operator(self):
        """测试按位异或操作符 ^"""
        node = parse_expression("column_name_1 ^ column_name_2")
        self.assertIsInstance(node, ast.OperatorBitXor)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)

    def test_simple_expr_fallback(self):
        """测试 simple_expr 回退规则"""
        node = parse_expression("column_name")
        self.assertIsInstance(node, ast.Ident)
        self.assertEqual(node.get_str_value(), "column_name")

    def test_complex_binary_expression(self):
        """测试复杂的二元表达式组合"""
        node = parse_expression("column_name_1 + column_name_2 * column_name_3")
        self.assertIsInstance(node, ast.OperatorPlus)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.OperatorMul)

    def test_binary_expression_with_literals(self):
        """测试包含字面量的二元表达式"""
        node = parse_expression("123 + 456")
        self.assertIsInstance(node, ast.OperatorPlus)
        self.assertIsInstance(node.left_operand, ast.IntLiteral)
        self.assertIsInstance(node.right_operand, ast.IntLiteral)


class TestPredicateExpr(TestCase):
    """测试 predicate_expr 语义组
    
    测试各种谓词表达式的解析，包括 IN、BETWEEN、LIKE、REGEXP 等操作符
    """

    def test_in_subquery_operator(self):
        """测试 IN 子查询操作符"""
        node = parse_expression("column_name IN (SELECT column_name FROM table_name)")
        self.assertIsInstance(node, ast.OperatorInSubSelect)
        self.assertIsInstance(node.operand, ast.Ident)
        self.assertIsInstance(node.subquery_expression, ast.QueryExpression)

    def test_not_in_subquery_operator(self):
        """测试 NOT IN 子查询操作符"""
        node = parse_expression("column_name NOT IN (SELECT column_name FROM table_name)")
        self.assertIsInstance(node, ast.OperatorNotInSubSelect)
        self.assertIsInstance(node.operand, ast.Ident)
        self.assertIsInstance(node.subquery_expression, ast.QueryExpression)

    def test_in_single_value_operator(self):
        """测试 IN 单个值操作符"""
        node = parse_expression("column_name IN (123)")
        self.assertIsInstance(node, ast.OperatorInValues)
        self.assertIsInstance(node.operand, ast.Ident)
        self.assertEqual(len(node.value_list), 1)
        self.assertIsInstance(node.value_list[0], ast.IntLiteral)

    def test_in_multiple_values_operator(self):
        """测试 IN 多个值操作符"""
        node = parse_expression("column_name IN (123, 456)")
        self.assertIsInstance(node, ast.OperatorInValues)
        self.assertIsInstance(node.operand, ast.Ident)
        self.assertEqual(len(node.value_list), 2)
        self.assertIsInstance(node.value_list[0], ast.IntLiteral)
        self.assertIsInstance(node.value_list[1], ast.IntLiteral)

    def test_not_in_single_value_operator(self):
        """测试 NOT IN 单个值操作符"""
        node = parse_expression("column_name NOT IN (123)")
        self.assertIsInstance(node, ast.OperatorNotInValues)
        self.assertIsInstance(node.operand, ast.Ident)
        self.assertEqual(len(node.value_list), 1)
        self.assertIsInstance(node.value_list[0], ast.IntLiteral)

    def test_not_in_multiple_values_operator(self):
        """测试 NOT IN 多个值操作符"""
        node = parse_expression("column_name NOT IN (123, 456)")
        self.assertIsInstance(node, ast.OperatorNotInValues)
        self.assertIsInstance(node.operand, ast.Ident)
        self.assertEqual(len(node.value_list), 2)
        self.assertIsInstance(node.value_list[0], ast.IntLiteral)
        self.assertIsInstance(node.value_list[1], ast.IntLiteral)

    def test_member_of_operator(self):
        """测试 MEMBER OF 操作符"""
        node = parse_expression("column_name_1 MEMBER OF (column_name_2)")
        self.assertIsInstance(node, ast.OperatorMemberOf)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)

    def test_between_operator(self):
        """测试 BETWEEN 操作符"""
        node = parse_expression("column_name BETWEEN 1 AND 10")
        self.assertIsInstance(node, ast.OperatorBetween)
        self.assertIsInstance(node.first_operand, ast.Ident)
        self.assertIsInstance(node.second_operand, ast.IntLiteral)
        self.assertIsInstance(node.third_operand, ast.IntLiteral)

    def test_not_between_operator(self):
        """测试 NOT BETWEEN 操作符"""
        node = parse_expression("column_name NOT BETWEEN 1 AND 10")
        self.assertIsInstance(node, ast.OperatorNotBetween)
        self.assertIsInstance(node.first_operand, ast.Ident)
        self.assertIsInstance(node.second_operand, ast.IntLiteral)
        self.assertIsInstance(node.third_operand, ast.IntLiteral)

    def test_sounds_like_operator(self):
        """测试 SOUNDS LIKE 操作符"""
        node = parse_expression("column_name_1 SOUNDS LIKE column_name_2")
        self.assertIsInstance(node, ast.OperatorSoundsLike)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)

    def test_like_operator(self):
        """测试 LIKE 操作符"""
        node = parse_expression("column_name LIKE 'pattern%'")
        self.assertIsInstance(node, ast.OperatorLike)
        self.assertIsInstance(node.first_operand, ast.Ident)
        self.assertIsInstance(node.second_operand, ast.StringLiteral)
        self.assertIsNone(node.third_operand)

    def test_like_operator_with_escape(self):
        """测试 LIKE 操作符带转义字符"""
        node = parse_expression("column_name LIKE 'pattern\\%' ESCAPE '\\'")
        self.assertIsInstance(node, ast.OperatorLike)
        self.assertIsInstance(node.first_operand, ast.Ident)
        self.assertIsInstance(node.second_operand, ast.StringLiteral)
        self.assertIsInstance(node.third_operand, ast.StringLiteral)

    def test_not_like_operator(self):
        """测试 NOT LIKE 操作符"""
        node = parse_expression("column_name NOT LIKE 'pattern%'")
        self.assertIsInstance(node, ast.OperatorNotLike)
        self.assertIsInstance(node.first_operand, ast.Ident)
        self.assertIsInstance(node.second_operand, ast.StringLiteral)
        self.assertIsNone(node.third_operand)

    def test_not_like_operator_with_escape(self):
        """测试 NOT LIKE 操作符带转义字符"""
        node = parse_expression("column_name NOT LIKE 'pattern\\%' ESCAPE '\\'")
        self.assertIsInstance(node, ast.OperatorNotLike)
        self.assertIsInstance(node.first_operand, ast.Ident)
        self.assertIsInstance(node.second_operand, ast.StringLiteral)
        self.assertIsInstance(node.third_operand, ast.StringLiteral)

    def test_regexp_operator(self):
        """测试 REGEXP 操作符"""
        node = parse_expression("column_name REGEXP '^pattern.*$'")
        self.assertIsInstance(node, ast.OperatorRegexp)
        self.assertIsInstance(node.left_operand, ast.Ident)
        # 注意：这里根据代码实际情况，right_operand可能是x[1]而不是x[2]
        self.assertIsInstance(node.right_operand, ast.StringLiteral)

    def test_not_regexp_operator(self):
        """测试 NOT REGEXP 操作符"""
        node = parse_expression("column_name NOT REGEXP '^pattern.*$'")
        self.assertIsInstance(node, ast.OperatorNotRegexp)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.StringLiteral)

    def test_binary_expr_fallback(self):
        """测试 binary_expr 回退规则"""
        node = parse_expression("column_name_1 + column_name_2")
        self.assertIsInstance(node, ast.OperatorPlus)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)

    def test_complex_predicate_expression(self):
        """测试复杂的谓词表达式"""
        node = parse_expression("column_name BETWEEN 1 AND 10 OR column_name LIKE 'pattern%'")
        self.assertIsInstance(node, ast.OperatorOr)
        self.assertIsInstance(node.left_operand, ast.OperatorBetween)
        self.assertIsInstance(node.right_operand, ast.OperatorLike)

    def test_in_with_string_values(self):
        """测试 IN 操作符与字符串值"""
        node = parse_expression("column_name IN ('value1', 'value2')")
        self.assertIsInstance(node, ast.OperatorInValues)
        self.assertIsInstance(node.operand, ast.Ident)
        self.assertEqual(len(node.value_list), 2)
        self.assertIsInstance(node.value_list[0], ast.StringLiteral)
        self.assertIsInstance(node.value_list[1], ast.StringLiteral)


class TestBoolExpr(TestCase):
    """测试 bool_expr 语义组
    
    测试各种布尔表达式的解析，包括 IS NULL、IS NOT NULL、比较操作符、ALL/ANY 子查询等
    """

    def test_is_null_operator(self):
        """测试 IS NULL 操作符"""
        node = parse_expression("column_name IS NULL")
        self.assertIsInstance(node, ast.OperatorIsNull)
        self.assertIsInstance(node.operand, ast.Ident)
        self.assertEqual(node.operand.get_str_value(), "column_name")

    def test_is_not_null_operator(self):
        """测试 IS NOT NULL 操作符"""
        node = parse_expression("column_name IS NOT NULL")
        self.assertIsInstance(node, ast.OperatorIsNotNull)
        self.assertIsInstance(node.operand, ast.Ident)
        self.assertEqual(node.operand.get_str_value(), "column_name")

    def test_compare_operator_equal(self):
        """测试等于比较操作符"""
        node = parse_expression("column_name_1 = column_name_2")
        self.assertIsInstance(node, ast.OperatorCompare)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)
        self.assertEqual(node.operator, ast.EnumCompareOperator.EQ)

    def test_compare_operator_not_equal(self):
        """测试不等于比较操作符"""
        node = parse_expression("column_name_1 != column_name_2")
        self.assertIsInstance(node, ast.OperatorCompare)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)
        self.assertEqual(node.operator, ast.EnumCompareOperator.NE)

    def test_compare_operator_less_than(self):
        """测试小于比较操作符"""
        node = parse_expression("column_name_1 < column_name_2")
        self.assertIsInstance(node, ast.OperatorCompare)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)
        self.assertEqual(node.operator, ast.EnumCompareOperator.LT)

    def test_compare_operator_greater_than(self):
        """测试大于比较操作符"""
        node = parse_expression("column_name_1 > column_name_2")
        self.assertIsInstance(node, ast.OperatorCompare)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)
        self.assertEqual(node.operator, ast.EnumCompareOperator.GT)

    def test_compare_operator_less_equal(self):
        """测试小于等于比较操作符"""
        node = parse_expression("column_name_1 <= column_name_2")
        self.assertIsInstance(node, ast.OperatorCompare)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)
        self.assertEqual(node.operator, ast.EnumCompareOperator.LE)

    def test_compare_operator_greater_equal(self):
        """测试大于等于比较操作符"""
        node = parse_expression("column_name_1 >= column_name_2")
        self.assertIsInstance(node, ast.OperatorCompare)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.Ident)
        self.assertEqual(node.operator, ast.EnumCompareOperator.GE)

    def test_compare_all_subquery(self):
        """测试比较操作符与 ALL 子查询"""
        node = parse_expression("column_name > ALL (SELECT column_name FROM table_name)")
        self.assertIsInstance(node, ast.OperatorCompareAll)
        self.assertIsInstance(node.operand, ast.Ident)
        self.assertEqual(node.operator, ast.EnumCompareOperator.GT)
        self.assertIsInstance(node.subquery_expression, ast.QueryExpression)

    def test_compare_any_subquery(self):
        """测试比较操作符与 ANY 子查询"""
        node = parse_expression("column_name > ANY (SELECT column_name FROM table_name)")
        self.assertIsInstance(node, ast.OperatorCompareAny)
        self.assertIsInstance(node.operand, ast.Ident)
        self.assertEqual(node.operator, ast.EnumCompareOperator.GT)
        self.assertIsInstance(node.subquery_expression, ast.QueryExpression)

    def test_predicate_expr_fallback(self):
        """测试 predicate_expr 回退规则"""
        node = parse_expression("column_name IN (123, 456)")
        self.assertIsInstance(node, ast.OperatorInValues)
        self.assertIsInstance(node.operand, ast.Ident)
        self.assertEqual(len(node.value_list), 2)

    def test_complex_bool_expression(self):
        """测试复杂的布尔表达式"""
        node = parse_expression("column_name_1 = 123 AND column_name_2 IS NOT NULL")
        self.assertIsInstance(node, ast.OperatorAnd)
        self.assertIsInstance(node.left_operand, ast.OperatorCompare)
        self.assertIsInstance(node.right_operand, ast.OperatorIsNotNull)

    def test_bool_expr_with_literal_comparison(self):
        """测试布尔表达式与字面量比较"""
        node = parse_expression("column_name = 'test_value'")
        self.assertIsInstance(node, ast.OperatorCompare)
        self.assertIsInstance(node.left_operand, ast.Ident)
        self.assertIsInstance(node.right_operand, ast.StringLiteral)
        self.assertEqual(node.operator, ast.EnumCompareOperator.EQ)
