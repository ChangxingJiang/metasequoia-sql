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
