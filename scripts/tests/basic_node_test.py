import unittest

from metasequoia_sql import *


class TestBasicNode(unittest.TestCase):
    def test_compare_operator(self):
        self.assertTrue(check_compare_operator(build_token_scanner("= 3")))
        self.assertTrue(check_compare_operator(build_token_scanner("< 3")))
        self.assertTrue(check_compare_operator(build_token_scanner("<= 3")))
        self.assertTrue(check_compare_operator(build_token_scanner("> 3")))
        self.assertTrue(check_compare_operator(build_token_scanner(">= 3")))
        self.assertTrue(check_compare_operator(build_token_scanner("!= 3")))
        self.assertTrue(check_compare_operator(build_token_scanner("<> 3")))
        self.assertFalse(check_compare_operator(build_token_scanner("3 + 3")))
        self.assertEqual(parse_compare_operator(build_token_scanner("= 3")).source(DataSource.MYSQL), "=")
        self.assertEqual(parse_compare_operator(build_token_scanner("< 3")).source(DataSource.MYSQL), "<")
        self.assertEqual(parse_compare_operator(build_token_scanner("<= 3")).source(DataSource.MYSQL), "<=")
        self.assertEqual(parse_compare_operator(build_token_scanner("> 3")).source(DataSource.MYSQL), ">")
        self.assertEqual(parse_compare_operator(build_token_scanner(">= 3")).source(DataSource.MYSQL), ">=")
        self.assertEqual(parse_compare_operator(build_token_scanner("!= 3")).source(DataSource.MYSQL), "!=")
        self.assertEqual(parse_compare_operator(build_token_scanner("<> 3")).source(DataSource.MYSQL), "!=")

    def test_compute_operator(self):
        self.assertTrue(check_compute_operator(build_token_scanner("+ 3")))
        self.assertTrue(check_compute_operator(build_token_scanner("- 3")))
        self.assertTrue(check_compute_operator(build_token_scanner("* 3")))
        self.assertTrue(check_compute_operator(build_token_scanner("/ 3")))
        self.assertTrue(check_compute_operator(build_token_scanner("% 3")))
        self.assertTrue(check_compute_operator(build_token_scanner("|| 3")))
        self.assertFalse(check_compute_operator(build_token_scanner("3 + 3")))
        self.assertEqual(parse_compute_operator(build_token_scanner("+ 3")).source(DataSource.MYSQL), "+")
        self.assertEqual(parse_compute_operator(build_token_scanner("- 3")).source(DataSource.MYSQL), "-")
        self.assertEqual(parse_compute_operator(build_token_scanner("* 3")).source(DataSource.MYSQL), "*")
        self.assertEqual(parse_compute_operator(build_token_scanner("/ 3")).source(DataSource.MYSQL), "/")
        self.assertEqual(parse_compute_operator(build_token_scanner("% 3")).source(DataSource.SQL_SERVER), "%")
        self.assertEqual(parse_compute_operator(build_token_scanner("|| 'A'")).source(DataSource.ORACLE), "||")

    def test_logical_operator(self):
        self.assertTrue(check_logical_operator(build_token_scanner("AND a > 1")))
        self.assertTrue(check_logical_operator(build_token_scanner("NOT a > 1")))
        self.assertTrue(check_logical_operator(build_token_scanner("OR a > 1")))
        self.assertFalse(check_logical_operator(build_token_scanner("a > 1")))
        self.assertEqual(parse_logical_operator(build_token_scanner("AND a > 1")).source(DataSource.MYSQL), "AND")
        self.assertEqual(parse_logical_operator(build_token_scanner("NOT a > 1")).source(DataSource.MYSQL), "NOT")
        self.assertEqual(parse_logical_operator(build_token_scanner("OR a > 1")).source(DataSource.MYSQL), "OR")
