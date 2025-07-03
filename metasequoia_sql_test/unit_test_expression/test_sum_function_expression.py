"""
聚集函数表达式（sum_function_expression）单元测试

测试 sum_function_expression.py 中的语义组：
- SUM_FUNCTION_EXPRESSION: 聚集函数表达式
- IN_SUM_EXPR: 聚集函数的参数
- OPT_DISTINCT: 可选的 DISTINCT 关键字
- OPT_SEPARATOR: 可选的 SEPARATOR 关键字引导的分隔符
"""

from unittest import TestCase

from metasequoia_sql import ast, parse_expression


class TestSumFunctionExpression(TestCase):
    """测试 sum_function_expression 语义组
    
    测试各种聚集函数表达式的解析，包括AVG、COUNT、SUM、MIN、MAX、GROUP_CONCAT等聚集函数
    """

    def test_avg_function_without_distinct(self):
        """测试 AVG 函数（无DISTINCT）"""
        node = parse_expression("AVG(column_name)")
        self.assertIsInstance(node, ast.FuncSumAvg)
        self.assertFalse(node.distinct)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.window_clause)

    def test_avg_function_with_distinct(self):
        """测试 AVG 函数（带DISTINCT）"""
        node = parse_expression("AVG(DISTINCT column_name)")
        self.assertIsInstance(node, ast.FuncSumAvg)
        self.assertTrue(node.distinct)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.window_clause)

    def test_bit_and_function(self):
        """测试 BIT_AND 函数"""
        node = parse_expression("BIT_AND(column_name)")
        self.assertIsInstance(node, ast.FuncSumBitAnd)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.window_clause)

    def test_bit_or_function(self):
        """测试 BIT_OR 函数"""
        node = parse_expression("BIT_OR(column_name)")
        self.assertIsInstance(node, ast.FuncSumBitOr)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.window_clause)

    def test_json_arrayagg_function(self):
        """测试 JSON_ARRAYAGG 函数"""
        node = parse_expression("JSON_ARRAYAGG(column_name)")
        self.assertIsInstance(node, ast.FuncSumJsonArrayAgg)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.window_clause)

    def test_json_objectagg_function(self):
        """测试 JSON_OBJECTAGG 函数"""
        node = parse_expression("JSON_OBJECTAGG(column_name_1, column_name_2)")
        self.assertIsInstance(node, ast.FuncSumJsonObjectAgg)
        self.assertIsNotNone(node.param1)
        self.assertIsNotNone(node.param2)
        self.assertIsNone(node.window_clause)

    def test_st_collect_function_without_distinct(self):
        """测试 ST_COLLECT 函数（无DISTINCT）"""
        node = parse_expression("ST_COLLECT(column_name)")
        self.assertIsInstance(node, ast.FuncSumStCollect)
        self.assertFalse(node.distinct)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.window_clause)

    def test_st_collect_function_with_distinct(self):
        """测试 ST_COLLECT 函数（带DISTINCT）"""
        node = parse_expression("ST_COLLECT(DISTINCT column_name)")
        self.assertIsInstance(node, ast.FuncSumStCollect)
        self.assertTrue(node.distinct)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.window_clause)

    def test_bit_xor_function(self):
        """测试 BIT_XOR 函数"""
        node = parse_expression("BIT_XOR(column_name)")
        self.assertIsInstance(node, ast.FuncSumBitXor)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.window_clause)

    def test_count_star_function(self):
        """测试 COUNT(*) 函数"""
        node = parse_expression("COUNT(*)")
        self.assertIsInstance(node, ast.FuncSumCountStar)
        self.assertIsNone(node.window_clause)

    def test_count_star_function_with_all(self):
        """测试 COUNT(ALL *) 函数"""
        node = parse_expression("COUNT(ALL *)")
        self.assertIsInstance(node, ast.FuncSumCountStar)
        self.assertIsNone(node.window_clause)

    def test_count_function_without_distinct(self):
        """测试 COUNT 函数（无DISTINCT）"""
        node = parse_expression("COUNT(column_name)")
        self.assertIsInstance(node, ast.FuncSumCount)
        self.assertFalse(node.distinct)
        self.assertIsNotNone(node.param_list)
        self.assertIsNone(node.window_clause)

    def test_count_function_with_distinct(self):
        """测试 COUNT 函数（带DISTINCT）"""
        node = parse_expression("COUNT(DISTINCT column_name)")
        self.assertIsInstance(node, ast.FuncSumCount)
        self.assertTrue(node.distinct)
        self.assertIsNotNone(node.param_list)
        self.assertIsNone(node.window_clause)

    def test_min_function_without_distinct(self):
        """测试 MIN 函数（无DISTINCT）"""
        node = parse_expression("MIN(column_name)")
        self.assertIsInstance(node, ast.FuncSumMin)
        self.assertFalse(node.distinct)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.window_clause)

    def test_min_function_with_distinct(self):
        """测试 MIN 函数（带DISTINCT）"""
        node = parse_expression("MIN(DISTINCT column_name)")
        self.assertIsInstance(node, ast.FuncSumMin)
        self.assertTrue(node.distinct)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.window_clause)

    def test_max_function_without_distinct(self):
        """测试 MAX 函数（无DISTINCT）"""
        node = parse_expression("MAX(column_name)")
        self.assertIsInstance(node, ast.FuncSumMax)
        self.assertFalse(node.distinct)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.window_clause)

    def test_max_function_with_distinct(self):
        """测试 MAX 函数（带DISTINCT）"""
        node = parse_expression("MAX(DISTINCT column_name)")
        self.assertIsInstance(node, ast.FuncSumMax)
        self.assertTrue(node.distinct)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.window_clause)

    def test_std_function(self):
        """测试 STD 函数"""
        node = parse_expression("STD(column_name)")
        self.assertIsInstance(node, ast.FuncSumStd)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.window_clause)

    def test_variance_function(self):
        """测试 VARIANCE 函数"""
        node = parse_expression("VARIANCE(column_name)")
        self.assertIsInstance(node, ast.FuncSumVariance)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.window_clause)

    def test_stddev_samp_function(self):
        """测试 STDDEV_SAMP 函数"""
        node = parse_expression("STDDEV_SAMP(column_name)")
        self.assertIsInstance(node, ast.FuncSumStddevSamp)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.window_clause)

    def test_var_samp_function(self):
        """测试 VAR_SAMP 函数"""
        node = parse_expression("VAR_SAMP(column_name)")
        self.assertIsInstance(node, ast.FuncSumVarSamp)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.window_clause)

    def test_sum_function_without_distinct(self):
        """测试 SUM 函数（无DISTINCT）"""
        node = parse_expression("SUM(column_name)")
        self.assertIsInstance(node, ast.FuncSumSum)
        self.assertFalse(node.distinct)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.window_clause)

    def test_sum_function_with_distinct(self):
        """测试 SUM 函数（带DISTINCT）"""
        node = parse_expression("SUM(DISTINCT column_name)")
        self.assertIsInstance(node, ast.FuncSumSum)
        self.assertTrue(node.distinct)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.window_clause)

    def test_group_concat_function_basic(self):
        """测试 GROUP_CONCAT 函数（基础形式）"""
        node = parse_expression("GROUP_CONCAT(column_name)")
        self.assertIsInstance(node, ast.FuncSumGroupConcat)
        self.assertFalse(node.distinct)
        self.assertEqual(len(node.param_list), 1)
        self.assertIsNone(node.order_by_clause)
        self.assertIsNone(node.separator)
        self.assertIsNone(node.window_clause)

    def test_group_concat_function_with_distinct(self):
        """测试 GROUP_CONCAT 函数（带DISTINCT）"""
        node = parse_expression("GROUP_CONCAT(DISTINCT column_name)")
        self.assertIsInstance(node, ast.FuncSumGroupConcat)
        self.assertTrue(node.distinct)
        self.assertEqual(len(node.param_list), 1)
        self.assertIsNone(node.order_by_clause)
        self.assertIsNone(node.separator)
        self.assertIsNone(node.window_clause)

    def test_group_concat_function_multiple_columns(self):
        """测试 GROUP_CONCAT 函数（多列）"""
        node = parse_expression("GROUP_CONCAT(column_name_1, column_name_2)")
        self.assertIsInstance(node, ast.FuncSumGroupConcat)
        self.assertFalse(node.distinct)
        self.assertEqual(len(node.param_list), 2)
        self.assertIsNone(node.order_by_clause)
        self.assertIsNone(node.separator)
        self.assertIsNone(node.window_clause)

    def test_group_concat_function_with_order_by(self):
        """测试 GROUP_CONCAT 函数（带ORDER BY）"""
        node = parse_expression("GROUP_CONCAT(column_name ORDER BY column_name)")
        self.assertIsInstance(node, ast.FuncSumGroupConcat)
        self.assertFalse(node.distinct)
        self.assertEqual(len(node.param_list), 1)
        self.assertIsNotNone(node.order_by_clause)
        self.assertIsNone(node.separator)
        self.assertIsNone(node.window_clause)

    def test_group_concat_function_with_separator(self):
        """测试 GROUP_CONCAT 函数（带SEPARATOR）"""
        node = parse_expression("GROUP_CONCAT(column_name SEPARATOR ', ')")
        self.assertIsInstance(node, ast.FuncSumGroupConcat)
        self.assertFalse(node.distinct)
        self.assertEqual(len(node.param_list), 1)
        self.assertIsNone(node.order_by_clause)
        self.assertIsNotNone(node.separator)
        self.assertIsNone(node.window_clause)

    def test_group_concat_function_with_order_by_and_separator(self):
        """测试 GROUP_CONCAT 函数（带ORDER BY和SEPARATOR）"""
        node = parse_expression("GROUP_CONCAT(column_name ORDER BY column_name SEPARATOR ', ')")
        self.assertIsInstance(node, ast.FuncSumGroupConcat)
        self.assertFalse(node.distinct)
        self.assertEqual(len(node.param_list), 1)
        self.assertIsNotNone(node.order_by_clause)
        self.assertIsNotNone(node.separator)
        self.assertIsNone(node.window_clause)

    def test_grouping_function(self):
        """测试 GROUPING 函数"""
        node = parse_expression("GROUPING(column_name)")
        self.assertIsInstance(node, ast.FunctionSumGrouping)
        self.assertEqual(len(node.param_list), 1)

    def test_grouping_function_multiple_columns(self):
        """测试 GROUPING 函数（多列）"""
        node = parse_expression("GROUPING(column_name_1, column_name_2)")
        self.assertIsInstance(node, ast.FunctionSumGrouping)
        self.assertEqual(len(node.param_list), 2)


class TestInSumExpr(TestCase):
    """测试 in_sum_expr 语义组
    
    测试聚集函数参数的解析，该语义组通过聚集函数进行间接测试
    注：此语义组只有一个备选规则，用于包装表达式，通过上述聚集函数测试已充分覆盖
    """

    def test_in_sum_expr_basic(self):
        """测试聚集函数参数（基础表达式）"""
        node = parse_expression("SUM(column_name)")
        self.assertIsInstance(node, ast.FuncSumSum)
        # in_sum_expr 的结果就是传入的表达式
        self.assertIsNotNone(node.param)

    def test_in_sum_expr_with_all(self):
        """测试聚集函数参数（带ALL关键字）"""
        node = parse_expression("SUM(ALL column_name)")
        self.assertIsInstance(node, ast.FuncSumSum)
        # in_sum_expr 的结果就是传入的表达式，ALL关键字被处理掉
        self.assertIsNotNone(node.param)


class TestOptDistinct(TestCase):
    """测试 opt_distinct 语义组
    
    测试可选的DISTINCT关键字的解析，该语义组通过支持DISTINCT的聚集函数进行间接测试
    注：此语义组通过上述聚集函数的DISTINCT测试已充分覆盖
    """

    def test_opt_distinct_present(self):
        """测试DISTINCT关键字存在时的解析"""
        node = parse_expression("SUM(DISTINCT column_name)")
        self.assertIsInstance(node, ast.FuncSumSum)
        self.assertTrue(node.distinct)

    def test_opt_distinct_absent(self):
        """测试DISTINCT关键字不存在时的解析"""
        node = parse_expression("SUM(column_name)")
        self.assertIsInstance(node, ast.FuncSumSum)
        self.assertFalse(node.distinct)


class TestOptSeparator(TestCase):
    """测试 opt_separator 语义组
    
    测试可选的SEPARATOR关键字引导的分隔符的解析，该语义组通过GROUP_CONCAT函数进行间接测试
    注：此语义组通过上述GROUP_CONCAT函数的SEPARATOR测试已充分覆盖
    """

    def test_opt_separator_present(self):
        """测试SEPARATOR子句存在时的解析"""
        node = parse_expression("GROUP_CONCAT(column_name SEPARATOR ', ')")
        self.assertIsInstance(node, ast.FuncSumGroupConcat)
        self.assertIsNotNone(node.separator)

    def test_opt_separator_absent(self):
        """测试SEPARATOR子句不存在时的解析"""
        node = parse_expression("GROUP_CONCAT(column_name)")
        self.assertIsInstance(node, ast.FuncSumGroupConcat)
        self.assertIsNone(node.separator)