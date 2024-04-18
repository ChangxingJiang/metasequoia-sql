import unittest

from metasequoia_sql.core import objects


class TestObjectsHashable(unittest.TestCase):
    """检验对象可哈希的单元测试 TODO 补全对象"""

    def test_insert_type(self):
        hash(objects.SQLInsertType(insert_type=objects.EnumInsertType.INSERT_INTO))

    def test_normal_function_expression(self):
        hash(objects.SQLNormalFunctionExpression(function_name="TEST", function_params=tuple()))
