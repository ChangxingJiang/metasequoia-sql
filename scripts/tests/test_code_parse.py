"""
metasequoia_sql.core.parser 的单元测试
"""

import unittest

from metasequoia_sql import *


class TestBasicNode(unittest.TestCase):
    def test_compare_operator(self):
        self.assertTrue(check_compare_operator("= 3"))
        self.assertTrue(check_compare_operator("< 3"))
        self.assertTrue(check_compare_operator("<= 3"))
        self.assertTrue(check_compare_operator("> 3"))
        self.assertTrue(check_compare_operator(">= 3"))
        self.assertTrue(check_compare_operator("!= 3"))
        self.assertTrue(check_compare_operator("<> 3"))
        self.assertFalse(check_compare_operator("3 + 3"))
        self.assertEqual(parse_compare_operator("= 3").source(DataSource.MYSQL), "=")
        self.assertEqual(parse_compare_operator("< 3").source(DataSource.MYSQL), "<")
        self.assertEqual(parse_compare_operator("<= 3").source(DataSource.MYSQL), "<=")
        self.assertEqual(parse_compare_operator("> 3").source(DataSource.MYSQL), ">")
        self.assertEqual(parse_compare_operator(">= 3").source(DataSource.MYSQL), ">=")
        self.assertEqual(parse_compare_operator("!= 3").source(DataSource.MYSQL), "!=")
        self.assertEqual(parse_compare_operator("<> 3").source(DataSource.MYSQL), "!=")

    def test_compute_operator(self):
        self.assertTrue(check_compute_operator("+ 3"))
        self.assertTrue(check_compute_operator("- 3"))
        self.assertTrue(check_compute_operator("* 3"))
        self.assertTrue(check_compute_operator("/ 3"))
        self.assertTrue(check_compute_operator("% 3"))
        self.assertTrue(check_compute_operator("|| 3"))
        self.assertFalse(check_compute_operator("3 + 3"))
        self.assertEqual(parse_compute_operator("+ 3").source(DataSource.MYSQL), "+")
        self.assertEqual(parse_compute_operator("- 3").source(DataSource.MYSQL), "-")
        self.assertEqual(parse_compute_operator("* 3").source(DataSource.MYSQL), "*")
        self.assertEqual(parse_compute_operator("/ 3").source(DataSource.MYSQL), "/")
        self.assertEqual(parse_compute_operator("% 3").source(DataSource.SQL_SERVER), "%")
        self.assertEqual(parse_compute_operator("|| 'A'").source(DataSource.ORACLE), "||")

    def test_logical_operator(self):
        self.assertTrue(check_logical_operator("AND a > 1"))
        self.assertTrue(check_logical_operator("NOT a > 1"))
        self.assertTrue(check_logical_operator("OR a > 1"))
        self.assertFalse(check_logical_operator("a > 1"))
        self.assertEqual(parse_logical_operator("AND a > 1").source(DataSource.MYSQL), "AND")
        self.assertEqual(parse_logical_operator("NOT a > 1").source(DataSource.MYSQL), "NOT")
        self.assertEqual(parse_logical_operator("OR a > 1").source(DataSource.MYSQL), "OR")
