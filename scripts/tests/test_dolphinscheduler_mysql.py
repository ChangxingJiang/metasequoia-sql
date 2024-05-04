"""
使用海豚调度元数据的测试用例
"""

import os
import unittest

from metasequoia_sql import core


class TestDolphinSchedulerMysql(unittest.TestCase):
    """使用海豚调度元数据的测试用例"""

    def test_parse_statements(self):
        project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        demo_path = os.path.join(project_path, "demo", "dolphinscheduler_mysql.sql")
        with open(demo_path, encoding="UTF-8") as file:
            for statement in core.SQLParser.parse_statements(file.read()):
                statement.source(core.SQLType.MYSQL)
