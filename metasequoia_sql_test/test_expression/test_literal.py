"""
语法逻辑测试：标识符
"""

from unittest import TestCase

from metasequoia_sql import ast, parse_expression


class TestSimpleIdent(TestCase):
    """测试 simple_ident 语义组

    通过 SELECT 表达式的方式测试 simple_ident 语义组的各种形式
    """

    def test_simple_ident_single(self):
        """测试单个标识符"""
        node = parse_expression("column_name")
        self.assertTrue(isinstance(node, ast.Ident))
        self.assertEqual(node.value, "column_name")

    def test_simple_ident_2d(self):
        """测试两个点分隔的标识符"""
        node = parse_expression("table_name.column_name")
        self.assertTrue(isinstance(node, ast.Ident2D))
        self.assertEqual(node.value1, "table_name")
        self.assertEqual(node.value2, "column_name")

    def test_simple_ident_3d(self):
        """测试三个点分隔的标识符"""
        node = parse_expression("database_name.table_name.column_name")
        self.assertTrue(isinstance(node, ast.Ident3D))
        self.assertEqual(node.value1, "database_name")
        self.assertEqual(node.value2, "table_name")
        self.assertEqual(node.value3, "column_name")
