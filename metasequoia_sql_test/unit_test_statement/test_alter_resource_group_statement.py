"""
ALTER RESOURCE GROUP 语句单元测试

测试语义组：alter_resource_group_statement
"""

import unittest

from metasequoia_sql import parse_statement
from metasequoia_sql.ast.basic.fixed_enum import EnumEnableDisable
from metasequoia_sql.ast.phrase.cpu_range import CpuRange
from metasequoia_sql.ast.phrase.thread_priority import ThreadPriority
from metasequoia_sql.ast.statement.alter_resource_group_statement import AlterResourceGroupStatement


class TestAlterResourceGroupStatement(unittest.TestCase):
    """测试 ALTER RESOURCE GROUP 语句解析"""

    def test_basic_alter_resource_group(self):
        """测试基本的 ALTER RESOURCE GROUP 语句（仅包含必需的参数）"""
        sql = "ALTER RESOURCE GROUP group_name"
        node = parse_statement(sql)

        self.assertIsInstance(node, AlterResourceGroupStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.vcpu_list, [])
        self.assertIsNone(node.priority)
        self.assertEqual(node.enable_disable, EnumEnableDisable.DEFAULT)
        self.assertFalse(node.force)

    def test_with_vcpu_list_single_cpu(self):
        """测试包含单个 CPU 的 VCPU 列表"""
        sql = "ALTER RESOURCE GROUP group_name VCPU = 1"
        node = parse_statement(sql)

        self.assertIsInstance(node, AlterResourceGroupStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertIsInstance(node.vcpu_list, list)
        self.assertEqual(len(node.vcpu_list), 1)
        self.assertIsInstance(node.vcpu_list[0], CpuRange)
        self.assertEqual(node.vcpu_list[0].start, 1)
        self.assertIsNone(node.vcpu_list[0].end)

    def test_with_vcpu_list_cpu_range(self):
        """测试包含 CPU 范围的 VCPU 列表"""
        sql = "ALTER RESOURCE GROUP group_name VCPU = 1-4"
        node = parse_statement(sql)

        self.assertIsInstance(node, AlterResourceGroupStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertIsInstance(node.vcpu_list, list)
        self.assertEqual(len(node.vcpu_list), 1)
        self.assertIsInstance(node.vcpu_list[0], CpuRange)
        self.assertEqual(node.vcpu_list[0].start, 1)
        self.assertEqual(node.vcpu_list[0].end, 4)

    def test_with_vcpu_list_multiple_cpus(self):
        """测试包含多个 CPU 的 VCPU 列表"""
        sql = "ALTER RESOURCE GROUP group_name VCPU = 1, 3, 5"
        node = parse_statement(sql)

        self.assertIsInstance(node, AlterResourceGroupStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertIsInstance(node.vcpu_list, list)
        self.assertEqual(len(node.vcpu_list), 3)
        self.assertEqual(node.vcpu_list[0].start, 1)
        self.assertEqual(node.vcpu_list[1].start, 3)
        self.assertEqual(node.vcpu_list[2].start, 5)

    def test_with_vcpu_list_mixed_cpus_and_ranges(self):
        """测试包含 CPU 和 CPU 范围混合的 VCPU 列表"""
        sql = "ALTER RESOURCE GROUP group_name VCPU = 1, 3-5, 7"
        node = parse_statement(sql)

        self.assertIsInstance(node, AlterResourceGroupStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertIsInstance(node.vcpu_list, list)
        self.assertEqual(len(node.vcpu_list), 3)
        self.assertEqual(node.vcpu_list[0].start, 1)
        self.assertIsNone(node.vcpu_list[0].end)
        self.assertEqual(node.vcpu_list[1].start, 3)
        self.assertEqual(node.vcpu_list[1].end, 5)
        self.assertEqual(node.vcpu_list[2].start, 7)
        self.assertIsNone(node.vcpu_list[2].end)

    def test_with_thread_priority_positive(self):
        """测试包含正数线程优先级"""
        sql = "ALTER RESOURCE GROUP group_name THREAD_PRIORITY = 10"
        node = parse_statement(sql)

        self.assertIsInstance(node, AlterResourceGroupStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertIsInstance(node.priority, ThreadPriority)
        self.assertEqual(node.priority.value, 10)

    def test_with_thread_priority_negative(self):
        """测试包含负数线程优先级"""
        sql = "ALTER RESOURCE GROUP group_name THREAD_PRIORITY = -5"
        node = parse_statement(sql)

        self.assertIsInstance(node, AlterResourceGroupStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertIsInstance(node.priority, ThreadPriority)
        self.assertEqual(node.priority.value, -5)

    def test_with_enable(self):
        """测试包含 ENABLE 选项"""
        sql = "ALTER RESOURCE GROUP group_name ENABLE"
        node = parse_statement(sql)

        self.assertIsInstance(node, AlterResourceGroupStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.enable_disable, EnumEnableDisable.ENABLE)

    def test_with_disable(self):
        """测试包含 DISABLE 选项"""
        sql = "ALTER RESOURCE GROUP group_name DISABLE"
        node = parse_statement(sql)

        self.assertIsInstance(node, AlterResourceGroupStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.enable_disable, EnumEnableDisable.DISABLE)

    def test_with_force(self):
        """测试包含 FORCE 选项"""
        sql = "ALTER RESOURCE GROUP group_name FORCE"
        node = parse_statement(sql)

        self.assertIsInstance(node, AlterResourceGroupStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertTrue(node.force)

    def test_with_vcpu_and_thread_priority(self):
        """测试同时包含 VCPU 和线程优先级"""
        sql = "ALTER RESOURCE GROUP group_name VCPU = 1-4 THREAD_PRIORITY = 5"
        node = parse_statement(sql)

        self.assertIsInstance(node, AlterResourceGroupStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertIsInstance(node.vcpu_list, list)
        self.assertEqual(len(node.vcpu_list), 1)
        self.assertEqual(node.vcpu_list[0].start, 1)
        self.assertEqual(node.vcpu_list[0].end, 4)
        self.assertIsInstance(node.priority, ThreadPriority)
        self.assertEqual(node.priority.value, 5)

    def test_with_vcpu_and_enable(self):
        """测试同时包含 VCPU 和 ENABLE 选项"""
        sql = "ALTER RESOURCE GROUP group_name VCPU = 1, 2, 3 ENABLE"
        node = parse_statement(sql)

        self.assertIsInstance(node, AlterResourceGroupStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertIsInstance(node.vcpu_list, list)
        self.assertEqual(len(node.vcpu_list), 3)
        self.assertEqual(node.enable_disable, EnumEnableDisable.ENABLE)

    def test_with_thread_priority_and_disable(self):
        """测试同时包含线程优先级和 DISABLE 选项"""
        sql = "ALTER RESOURCE GROUP group_name THREAD_PRIORITY = -3 DISABLE"
        node = parse_statement(sql)

        self.assertIsInstance(node, AlterResourceGroupStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertIsInstance(node.priority, ThreadPriority)
        self.assertEqual(node.priority.value, -3)
        self.assertEqual(node.enable_disable, EnumEnableDisable.DISABLE)

    def test_with_vcpu_thread_priority_and_force(self):
        """测试同时包含 VCPU、线程优先级和 FORCE 选项"""
        sql = "ALTER RESOURCE GROUP group_name VCPU = 1-8 THREAD_PRIORITY = 10 FORCE"
        node = parse_statement(sql)

        self.assertIsInstance(node, AlterResourceGroupStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertIsInstance(node.vcpu_list, list)
        self.assertEqual(len(node.vcpu_list), 1)
        self.assertEqual(node.vcpu_list[0].start, 1)
        self.assertEqual(node.vcpu_list[0].end, 8)
        self.assertIsInstance(node.priority, ThreadPriority)
        self.assertEqual(node.priority.value, 10)
        self.assertTrue(node.force)

    def test_with_all_options(self):
        """测试包含所有可选选项"""
        sql = "ALTER RESOURCE GROUP group_name VCPU = 1, 3-5, 7 THREAD_PRIORITY = -5 ENABLE FORCE"
        node = parse_statement(sql)

        self.assertIsInstance(node, AlterResourceGroupStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertIsInstance(node.vcpu_list, list)
        self.assertEqual(len(node.vcpu_list), 3)
        self.assertIsInstance(node.priority, ThreadPriority)
        self.assertEqual(node.priority.value, -5)
        self.assertEqual(node.enable_disable, EnumEnableDisable.ENABLE)
        self.assertTrue(node.force)

    def test_with_vcpu_equal_sign(self):
        """测试 VCPU 选项包含等号"""
        sql = "ALTER RESOURCE GROUP group_name VCPU = 1"
        node = parse_statement(sql)

        self.assertIsInstance(node, AlterResourceGroupStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertIsInstance(node.vcpu_list, list)
        self.assertEqual(len(node.vcpu_list), 1)

    def test_with_thread_priority_equal_sign(self):
        """测试线程优先级选项包含等号"""
        sql = "ALTER RESOURCE GROUP group_name THREAD_PRIORITY = 5"
        node = parse_statement(sql)

        self.assertIsInstance(node, AlterResourceGroupStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertIsInstance(node.priority, ThreadPriority)
        self.assertEqual(node.priority.value, 5)


if __name__ == "__main__":
    unittest.main()
