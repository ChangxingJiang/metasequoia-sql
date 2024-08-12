"""
Issue 问题测试用例
"""

import unittest

from metasequoia_sql import SQLParser


class TestFunction(unittest.TestCase):
    """函数测试"""

    def test_func_char(self):
        """测试 char() 函数"""
        SQLParser.parse_function_expression("""CHAR('a', 'b')""")
        SQLParser.parse_function_expression("""CHAR('a', 'b' USING utf8)""")

    def test_func_current_user(self):
        """测试 current_user() 函数"""
        SQLParser.parse_function_expression("""CURRENT_USER""")
        SQLParser.parse_function_expression("""CURRENT_USER()""")

    def test_func_user(self):
        """测试 user() 函数"""
        SQLParser.parse_function_expression("""USER()""")

    def test_func_date(self):
        """测试 date() 函数"""
        SQLParser.parse_function_expression("""DATE('2024-08-12 13:28:05')""")

    def test_func_day(self):
        """测试 day() 函数"""
        SQLParser.parse_function_expression("""DAY('2024-08-12 13:28:05')""")

    def test_func_hour(self):
        """测试 hour() 函数"""
        SQLParser.parse_function_expression("""HOUR('2024-08-12 13:28:05')""")
