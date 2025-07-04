"""
测试窗口函数表达式的单元测试模块
"""

import unittest

from metasequoia_sql import parse_expression
from metasequoia_sql.ast.basic.literal import IntLiteral
from metasequoia_sql.ast.expression.window_function_expression import (
    EnumFromFirstOrLastOption,
    FuncWindowCumeDist,
    FuncWindowDenseRank,
    FuncWindowFirstValue,
    FuncWindowLag,
    FuncWindowLastValue,
    FuncWindowLead,
    FuncWindowNthValue,
    FuncWindowNtile,
    FuncWindowPercentRank,
    FuncWindowRank,
    FuncWindowRowNumber,
    EnumNullTreatmentOption
)


class TestWindowFunctionExpression(unittest.TestCase):
    """
    测试窗口函数表达式（window_function_expression）语义组
    """

    def test_row_number_function(self):
        """
        测试 ROW_NUMBER() OVER (...) 备选规则
        """
        node = parse_expression("ROW_NUMBER() OVER ()")
        self.assertIsInstance(node, FuncWindowRowNumber)
        self.assertIsNotNone(node.window_clause)

    def test_rank_function(self):
        """
        测试 RANK() OVER (...) 备选规则
        """
        node = parse_expression("RANK() OVER ()")
        self.assertIsInstance(node, FuncWindowRank)
        self.assertIsNotNone(node.window_clause)

    def test_dense_rank_function(self):
        """
        测试 DENSE_RANK() OVER (...) 备选规则
        """
        node = parse_expression("DENSE_RANK() OVER ()")
        self.assertIsInstance(node, FuncWindowDenseRank)
        self.assertIsNotNone(node.window_clause)

    def test_cume_dist_function(self):
        """
        测试 CUME_DIST() OVER (...) 备选规则
        """
        node = parse_expression("CUME_DIST() OVER ()")
        self.assertIsInstance(node, FuncWindowCumeDist)
        self.assertIsNotNone(node.window_clause)

    def test_percent_rank_function(self):
        """
        测试 PERCENT_RANK() OVER (...) 备选规则
        """
        node = parse_expression("PERCENT_RANK() OVER ()")
        self.assertIsInstance(node, FuncWindowPercentRank)
        self.assertIsNotNone(node.window_clause)

    def test_ntile_function_with_integer_literal(self):
        """
        测试 NTILE(stable_integer) OVER (...) 备选规则，使用整数字面值
        """
        node = parse_expression("NTILE(4) OVER ()")
        self.assertIsInstance(node, FuncWindowNtile)
        self.assertIsInstance(node.param, IntLiteral)
        self.assertEqual(node.param.value, 4)
        self.assertIsNotNone(node.window_clause)

    def test_lead_function_basic(self):
        """
        测试 LEAD(expr) OVER (...) 备选规则，不包含偏移量和默认值
        """
        node = parse_expression("LEAD(column_name) OVER ()")
        self.assertIsInstance(node, FuncWindowLead)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.offset)
        self.assertIsNone(node.default_value)
        self.assertEqual(node.null_treatment, EnumNullTreatmentOption.NONE)
        self.assertIsNotNone(node.window_clause)

    def test_lead_function_with_offset(self):
        """
        测试 LEAD(expr, offset) OVER (...) 备选规则，包含偏移量
        """
        node = parse_expression("LEAD(column_name, 1) OVER ()")
        self.assertIsInstance(node, FuncWindowLead)
        self.assertIsNotNone(node.param)
        self.assertIsNotNone(node.offset)
        self.assertIsInstance(node.offset, IntLiteral)
        self.assertEqual(node.offset.value, 1)
        self.assertIsNone(node.default_value)
        self.assertEqual(node.null_treatment, EnumNullTreatmentOption.NONE)
        self.assertIsNotNone(node.window_clause)

    def test_lead_function_with_offset_and_default(self):
        """
        测试 LEAD(expr, offset, default) OVER (...) 备选规则，包含偏移量和默认值
        """
        node = parse_expression("LEAD(column_name, 1, 0) OVER ()")
        self.assertIsInstance(node, FuncWindowLead)
        self.assertIsNotNone(node.param)
        self.assertIsNotNone(node.offset)
        self.assertIsInstance(node.offset, IntLiteral)
        self.assertEqual(node.offset.value, 1)
        self.assertIsNotNone(node.default_value)
        self.assertIsInstance(node.default_value, IntLiteral)
        self.assertEqual(node.default_value.value, 0)
        self.assertEqual(node.null_treatment, EnumNullTreatmentOption.NONE)
        self.assertIsNotNone(node.window_clause)

    def test_lead_function_with_respect_nulls(self):
        """
        测试 LEAD(expr) RESPECT NULLS OVER (...) 备选规则，包含 NULL 处理策略
        """
        node = parse_expression("LEAD(column_name) RESPECT NULLS OVER ()")
        self.assertIsInstance(node, FuncWindowLead)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.offset)
        self.assertIsNone(node.default_value)
        self.assertEqual(node.null_treatment, EnumNullTreatmentOption.RESPECT_NULLS)
        self.assertIsNotNone(node.window_clause)

    def test_lead_function_with_ignore_nulls(self):
        """
        测试 LEAD(expr) IGNORE NULLS OVER (...) 备选规则，包含 NULL 处理策略
        """
        node = parse_expression("LEAD(column_name) IGNORE NULLS OVER ()")
        self.assertIsInstance(node, FuncWindowLead)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.offset)
        self.assertIsNone(node.default_value)
        self.assertEqual(node.null_treatment, EnumNullTreatmentOption.IGNORE_NULLS)
        self.assertIsNotNone(node.window_clause)

    def test_lag_function_basic(self):
        """
        测试 LAG(expr) OVER (...) 备选规则，不包含偏移量和默认值
        """
        node = parse_expression("LAG(column_name) OVER ()")
        self.assertIsInstance(node, FuncWindowLag)
        self.assertIsNotNone(node.param)
        self.assertIsNone(node.offset)
        self.assertIsNone(node.default_value)
        self.assertEqual(node.null_treatment, EnumNullTreatmentOption.NONE)
        self.assertIsNotNone(node.window_clause)

    def test_lag_function_with_offset(self):
        """
        测试 LAG(expr, offset) OVER (...) 备选规则，包含偏移量
        """
        node = parse_expression("LAG(column_name, 2) OVER ()")
        self.assertIsInstance(node, FuncWindowLag)
        self.assertIsNotNone(node.param)
        self.assertIsNotNone(node.offset)
        self.assertIsInstance(node.offset, IntLiteral)
        self.assertEqual(node.offset.value, 2)
        self.assertIsNone(node.default_value)
        self.assertEqual(node.null_treatment, EnumNullTreatmentOption.NONE)
        self.assertIsNotNone(node.window_clause)

    def test_lag_function_with_offset_and_default(self):
        """
        测试 LAG(expr, offset, default) OVER (...) 备选规则，包含偏移量和默认值
        """
        node = parse_expression("LAG(column_name, 2, 1) OVER ()")
        self.assertIsInstance(node, FuncWindowLag)
        self.assertIsNotNone(node.param)
        self.assertIsNotNone(node.offset)
        self.assertIsInstance(node.offset, IntLiteral)
        self.assertEqual(node.offset.value, 2)
        self.assertIsNotNone(node.default_value)
        self.assertIsInstance(node.default_value, IntLiteral)
        self.assertEqual(node.default_value.value, 1)
        self.assertEqual(node.null_treatment, EnumNullTreatmentOption.NONE)
        self.assertIsNotNone(node.window_clause)

    def test_first_value_function_basic(self):
        """
        测试 FIRST_VALUE(expr) OVER (...) 备选规则，不包含 NULL 处理策略
        """
        node = parse_expression("FIRST_VALUE(column_name) OVER ()")
        self.assertIsInstance(node, FuncWindowFirstValue)
        self.assertIsNotNone(node.param)
        self.assertEqual(node.null_treatment, EnumNullTreatmentOption.NONE)
        self.assertIsNotNone(node.window_clause)

    def test_first_value_function_with_respect_nulls(self):
        """
        测试 FIRST_VALUE(expr) RESPECT NULLS OVER (...) 备选规则，包含 NULL 处理策略
        """
        node = parse_expression("FIRST_VALUE(column_name) RESPECT NULLS OVER ()")
        self.assertIsInstance(node, FuncWindowFirstValue)
        self.assertIsNotNone(node.param)
        self.assertEqual(node.null_treatment, EnumNullTreatmentOption.RESPECT_NULLS)
        self.assertIsNotNone(node.window_clause)

    def test_first_value_function_with_ignore_nulls(self):
        """
        测试 FIRST_VALUE(expr) IGNORE NULLS OVER (...) 备选规则，包含 NULL 处理策略
        """
        node = parse_expression("FIRST_VALUE(column_name) IGNORE NULLS OVER ()")
        self.assertIsInstance(node, FuncWindowFirstValue)
        self.assertIsNotNone(node.param)
        self.assertEqual(node.null_treatment, EnumNullTreatmentOption.IGNORE_NULLS)
        self.assertIsNotNone(node.window_clause)

    def test_last_value_function_basic(self):
        """
        测试 LAST_VALUE(expr) OVER (...) 备选规则，不包含 NULL 处理策略
        """
        node = parse_expression("LAST_VALUE(column_name) OVER ()")
        self.assertIsInstance(node, FuncWindowLastValue)
        self.assertIsNotNone(node.param)
        self.assertEqual(node.null_treatment, EnumNullTreatmentOption.NONE)
        self.assertIsNotNone(node.window_clause)

    def test_last_value_function_with_respect_nulls(self):
        """
        测试 LAST_VALUE(expr) RESPECT NULLS OVER (...) 备选规则，包含 NULL 处理策略
        """
        node = parse_expression("LAST_VALUE(column_name) RESPECT NULLS OVER ()")
        self.assertIsInstance(node, FuncWindowLastValue)
        self.assertIsNotNone(node.param)
        self.assertEqual(node.null_treatment, EnumNullTreatmentOption.RESPECT_NULLS)
        self.assertIsNotNone(node.window_clause)

    def test_last_value_function_with_ignore_nulls(self):
        """
        测试 LAST_VALUE(expr) IGNORE NULLS OVER (...) 备选规则，包含 NULL 处理策略
        """
        node = parse_expression("LAST_VALUE(column_name) IGNORE NULLS OVER ()")
        self.assertIsInstance(node, FuncWindowLastValue)
        self.assertIsNotNone(node.param)
        self.assertEqual(node.null_treatment, EnumNullTreatmentOption.IGNORE_NULLS)
        self.assertIsNotNone(node.window_clause)

    def test_nth_value_function_basic(self):
        """
        测试 NTH_VALUE(expr, simple_expr) OVER (...) 备选规则，不包含 FROM 子句和 NULL 处理策略
        """
        node = parse_expression("NTH_VALUE(column_name, 2) OVER ()")
        self.assertIsInstance(node, FuncWindowNthValue)
        self.assertIsNotNone(node.param1)
        self.assertIsNotNone(node.param2)
        self.assertIsInstance(node.param2, IntLiteral)
        self.assertEqual(node.param2.value, 2)
        self.assertEqual(node.from_first_or_last, EnumFromFirstOrLastOption.NONE)
        self.assertEqual(node.null_treatment, EnumNullTreatmentOption.NONE)
        self.assertIsNotNone(node.window_clause)

    def test_nth_value_function_with_from_first(self):
        """
        测试 NTH_VALUE(expr, simple_expr) FROM FIRST OVER (...) 备选规则，包含 FROM FIRST 子句
        """
        node = parse_expression("NTH_VALUE(column_name, 3) FROM FIRST OVER ()")
        self.assertIsInstance(node, FuncWindowNthValue)
        self.assertIsNotNone(node.param1)
        self.assertIsNotNone(node.param2)
        self.assertIsInstance(node.param2, IntLiteral)
        self.assertEqual(node.param2.value, 3)
        self.assertEqual(node.from_first_or_last, EnumFromFirstOrLastOption.FROM_FIRST)
        self.assertEqual(node.null_treatment, EnumNullTreatmentOption.NONE)
        self.assertIsNotNone(node.window_clause)

    def test_nth_value_function_with_from_last(self):
        """
        测试 NTH_VALUE(expr, simple_expr) FROM LAST OVER (...) 备选规则，包含 FROM LAST 子句
        """
        node = parse_expression("NTH_VALUE(column_name, 1) FROM LAST OVER ()")
        self.assertIsInstance(node, FuncWindowNthValue)
        self.assertIsNotNone(node.param1)
        self.assertIsNotNone(node.param2)
        self.assertIsInstance(node.param2, IntLiteral)
        self.assertEqual(node.param2.value, 1)
        self.assertEqual(node.from_first_or_last, EnumFromFirstOrLastOption.FROM_LAST)
        self.assertEqual(node.null_treatment, EnumNullTreatmentOption.NONE)
        self.assertIsNotNone(node.window_clause)

    def test_nth_value_function_with_from_first_and_respect_nulls(self):
        """
        测试 NTH_VALUE(expr, simple_expr) FROM FIRST RESPECT NULLS OVER (...) 备选规则，
        包含 FROM FIRST 子句和 NULL 处理策略
        """
        node = parse_expression("NTH_VALUE(column_name, 2) FROM FIRST RESPECT NULLS OVER ()")
        self.assertIsInstance(node, FuncWindowNthValue)
        self.assertIsNotNone(node.param1)
        self.assertIsNotNone(node.param2)
        self.assertIsInstance(node.param2, IntLiteral)
        self.assertEqual(node.param2.value, 2)
        self.assertEqual(node.from_first_or_last, EnumFromFirstOrLastOption.FROM_FIRST)
        self.assertEqual(node.null_treatment, EnumNullTreatmentOption.RESPECT_NULLS)
        self.assertIsNotNone(node.window_clause)

    def test_nth_value_function_with_from_last_and_ignore_nulls(self):
        """
        测试 NTH_VALUE(expr, simple_expr) FROM LAST IGNORE NULLS OVER (...) 备选规则，
        包含 FROM LAST 子句和 NULL 处理策略
        """
        node = parse_expression("NTH_VALUE(column_name, 1) FROM LAST IGNORE NULLS OVER ()")
        self.assertIsInstance(node, FuncWindowNthValue)
        self.assertIsNotNone(node.param1)
        self.assertIsNotNone(node.param2)
        self.assertIsInstance(node.param2, IntLiteral)
        self.assertEqual(node.param2.value, 1)
        self.assertEqual(node.from_first_or_last, EnumFromFirstOrLastOption.FROM_LAST)
        self.assertEqual(node.null_treatment, EnumNullTreatmentOption.IGNORE_NULLS)
        self.assertIsNotNone(node.window_clause)
