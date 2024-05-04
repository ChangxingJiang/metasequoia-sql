import unittest

from metasequoia_sql.core import node


class TestObjectsHashable(unittest.TestCase):
    """检验对象可哈希的单元测试 TODO 补全对象"""

    def test_null_field(self):
        """测试存在为 None 值的字段时，哈希值和等于状态是否生效"""
        node1 = node.ASTColumnName(table_name=None, column_name="column_name")
        node2 = node.ASTColumnName(table_name=None, column_name="column_name")
        node3 = node.ASTColumnName(table_name=None, column_name="column_name2")
        self.assertTrue(hash(node1) == hash(node2))
        self.assertTrue(node1 == node2)
        self.assertFalse(hash(node1) == hash(node3))
        self.assertFalse(node1 == node3)
        test_dict = {node1: "node1"}
        test_dict[node2] = "node2"
        test_dict[node3] = "node3"
        self.assertEqual(2, len(test_dict))
        self.assertEqual("node2", test_dict[node1])
        self.assertEqual("node2", test_dict[node2])
        self.assertEqual("node3", test_dict[node3])

    def test_insert_type(self):
        hash(node.ASTInsertType(enum=node.EnumInsertType.INSERT_INTO))

    def test_normal_function_expression(self):
        hash(node.ASTNormalFunctionExpression(name=node.ASTFunctionName(function_name="TEST"),
                                              params=tuple()))
