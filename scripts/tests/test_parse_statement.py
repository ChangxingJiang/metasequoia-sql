"""
语句级解析样例
"""

import unittest

from metasequoia_sql import SQLParser


class TestDolphinSchedulerMysql(unittest.TestCase):
    """使用海豚调度元数据的测试用例"""

    def test_delete_statement(self):
        """测试 DELETE 语句解析"""
        SQLParser.parse_statements("DELETE FROM table_1 WHERE column1 = '3'")
