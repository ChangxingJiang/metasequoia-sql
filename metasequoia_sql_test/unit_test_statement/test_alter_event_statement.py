"""
ALTER EVENT 语句（alter_event_statement）单元测试

测试 alter_event_statement.py 中的语义组：
- alter_event_statement: ALTER EVENT 语句
"""

from unittest import TestCase

from metasequoia_sql import ast, parse_statement


class TestAlterEventStatement(TestCase):
    """测试 alter_event_statement 语义组
    
    测试 ALTER EVENT 语句的解析，包括各种可选选项的不同组合
    """

    def test_alter_event_basic(self):
        """测试基本的 ALTER EVENT 语句"""
        node = parse_statement("ALTER EVENT event_name")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsNone(node.definer)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertIsNone(node.schedule_time)
        self.assertEqual(node.completion_type, ast.EnumEventCompletionType.DEFAULT)
        self.assertIsNone(node.event_rename)
        self.assertEqual(node.event_status, ast.EnumEventStatusType.DEFAULT)
        self.assertIsNone(node.event_comment)
        self.assertIsNone(node.process_command)

    def test_alter_event_with_definer(self):
        """测试带有定义者的 ALTER EVENT 语句"""
        node = parse_statement("ALTER DEFINER = user@host EVENT event_name")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsNotNone(node.definer)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")

    def test_alter_event_with_schedule_every(self):
        """测试带有 EVERY 调度的 ALTER EVENT 语句"""
        node = parse_statement("ALTER EVENT event_name ON SCHEDULE EVERY 1 HOUR")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertIsInstance(node.schedule_time, ast.ScheduleTimeEvery)
        self.assertIsNotNone(node.schedule_time.interval_expression)
        self.assertIsNotNone(node.schedule_time.interval_type)

    def test_alter_event_with_schedule_at(self):
        """测试带有 AT 调度的 ALTER EVENT 语句"""
        node = parse_statement("ALTER EVENT event_name ON SCHEDULE AT '2023-01-01 12:00:00'")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertIsInstance(node.schedule_time, ast.ScheduleTimeAt)
        self.assertIsNotNone(node.schedule_time.execute_at_expression)

    def test_alter_event_with_schedule_every_with_starts_ends(self):
        """测试带有 EVERY 和 STARTS/ENDS 的调度"""
        node = parse_statement("ALTER EVENT event_name ON SCHEDULE EVERY 1 DAY STARTS '2023-01-01' ENDS '2023-12-31'")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertIsInstance(node.schedule_time, ast.ScheduleTimeEvery)
        self.assertIsNotNone(node.schedule_time.interval_expression)
        self.assertIsNotNone(node.schedule_time.interval_type)
        self.assertIsNotNone(node.schedule_time.starts_expression)
        self.assertIsNotNone(node.schedule_time.ends_expression)

    def test_alter_event_with_completion_preserve(self):
        """测试带有 ON COMPLETION PRESERVE 的 ALTER EVENT 语句"""
        node = parse_statement("ALTER EVENT event_name ON COMPLETION PRESERVE")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertEqual(node.completion_type, ast.EnumEventCompletionType.ON_COMPLETION_PRESERVE)

    def test_alter_event_with_completion_not_preserve(self):
        """测试带有 ON COMPLETION NOT PRESERVE 的 ALTER EVENT 语句"""
        node = parse_statement("ALTER EVENT event_name ON COMPLETION NOT PRESERVE")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertEqual(node.completion_type, ast.EnumEventCompletionType.ON_COMPLETION_NOT_PRESERVE)

    def test_alter_event_with_rename(self):
        """测试带有 RENAME TO 的 ALTER EVENT 语句"""
        node = parse_statement("ALTER EVENT event_name RENAME TO new_event_name")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertIsInstance(node.event_rename, ast.Identifier)
        self.assertEqual(node.event_rename.object_name, "new_event_name")

    def test_alter_event_with_enable_status(self):
        """测试带有 ENABLE 状态的 ALTER EVENT 语句"""
        node = parse_statement("ALTER EVENT event_name ENABLE")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertEqual(node.event_status, ast.EnumEventStatusType.ENABLE)

    def test_alter_event_with_disable_status(self):
        """测试带有 DISABLE 状态的 ALTER EVENT 语句"""
        node = parse_statement("ALTER EVENT event_name DISABLE")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertEqual(node.event_status, ast.EnumEventStatusType.DISABLE)

    def test_alter_event_with_disable_on_slave_status(self):
        """测试带有 DISABLE ON SLAVE 状态的 ALTER EVENT 语句"""
        node = parse_statement("ALTER EVENT event_name DISABLE ON SLAVE")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertEqual(node.event_status, ast.EnumEventStatusType.DISABLE_ON_SLAVE)

    def test_alter_event_with_disable_on_replica_status(self):
        """测试带有 DISABLE ON REPLICA 状态的 ALTER EVENT 语句"""
        node = parse_statement("ALTER EVENT event_name DISABLE ON REPLICA")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertEqual(node.event_status, ast.EnumEventStatusType.DISABLE_ON_REPLICA)

    def test_alter_event_with_comment(self):
        """测试带有 COMMENT 的 ALTER EVENT 语句"""
        node = parse_statement("ALTER EVENT event_name COMMENT 'This is a test event'")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertEqual(node.event_comment, "This is a test event")

    def test_alter_event_with_do_statement(self):
        """测试带有 DO 语句的 ALTER EVENT 语句"""
        node = parse_statement("ALTER EVENT event_name DO INSERT INTO table_name VALUES (1)")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertIsInstance(node.process_command, ast.ProcessCommandStatement)
        self.assertIsNotNone(node.process_command.statement)

    def test_alter_event_with_all_options(self):
        """测试包含所有选项的 ALTER EVENT 语句"""
        node = parse_statement(
            "ALTER DEFINER = user@host EVENT event_name "
            "ON SCHEDULE EVERY 1 HOUR "
            "ON COMPLETION PRESERVE "
            "RENAME TO new_event_name "
            "ENABLE "
            "COMMENT 'Complete event' "
            "DO SELECT NOW()"
        )
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsNotNone(node.definer)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertIsInstance(node.schedule_time, ast.ScheduleTimeEvery)
        self.assertEqual(node.completion_type, ast.EnumEventCompletionType.ON_COMPLETION_PRESERVE)
        self.assertIsInstance(node.event_rename, ast.Identifier)
        self.assertEqual(node.event_rename.object_name, "new_event_name")
        self.assertEqual(node.event_status, ast.EnumEventStatusType.ENABLE)
        self.assertEqual(node.event_comment, "Complete event")
        self.assertIsInstance(node.process_command, ast.ProcessCommandStatement)

    def test_alter_event_with_multiple_schedule_options(self):
        """测试带有多个调度选项的 ALTER EVENT 语句"""
        node = parse_statement("ALTER EVENT event_name ON SCHEDULE EVERY 2 MINUTE STARTS NOW() ENDS '2023-12-31 23:59:59'")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertIsInstance(node.schedule_time, ast.ScheduleTimeEvery)
        self.assertIsNotNone(node.schedule_time.interval_expression)
        self.assertIsNotNone(node.schedule_time.interval_type)
        self.assertIsNotNone(node.schedule_time.starts_expression)
        self.assertIsNotNone(node.schedule_time.ends_expression)

    def test_alter_event_with_different_time_units(self):
        """测试不同时间单位的 ALTER EVENT 语句"""
        # 测试秒
        node = parse_statement("ALTER EVENT event_name ON SCHEDULE EVERY 30 SECOND")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.schedule_time, ast.ScheduleTimeEvery)
        
        # 测试分钟
        node = parse_statement("ALTER EVENT event_name ON SCHEDULE EVERY 5 MINUTE")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.schedule_time, ast.ScheduleTimeEvery)
        
        # 测试小时
        node = parse_statement("ALTER EVENT event_name ON SCHEDULE EVERY 2 HOUR")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.schedule_time, ast.ScheduleTimeEvery)
        
        # 测试天
        node = parse_statement("ALTER EVENT event_name ON SCHEDULE EVERY 1 DAY")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.schedule_time, ast.ScheduleTimeEvery)

    def test_alter_event_with_schema_qualified_name(self):
        """测试使用模式限定名称的 ALTER EVENT 语句"""
        node = parse_statement("ALTER EVENT database_name.event_name")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.schema_name, "database_name")
        self.assertEqual(node.event_name.object_name, "event_name")

    def test_alter_event_with_quoted_names(self):
        """测试使用引号的事件名称"""
        node = parse_statement("ALTER EVENT `event_name` RENAME TO `new_event_name`")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertIsInstance(node.event_rename, ast.Identifier)
        self.assertEqual(node.event_rename.object_name, "new_event_name")

    def test_alter_event_with_complex_definer(self):
        """测试复杂的定义者格式"""
        node = parse_statement("ALTER DEFINER = 'user_name'@'localhost' EVENT event_name")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsNotNone(node.definer)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")

    def test_alter_event_with_expression_in_schedule(self):
        """测试调度中使用表达式"""
        node = parse_statement("ALTER EVENT event_name ON SCHEDULE AT NOW() + INTERVAL 1 DAY")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertIsInstance(node.schedule_time, ast.ScheduleTimeAt)
        self.assertIsNotNone(node.schedule_time.execute_at_expression)

    def test_alter_event_with_multiple_statements_in_do(self):
        """测试 DO 中包含多个语句的情况"""
        node = parse_statement("ALTER EVENT event_name DO INSERT INTO table_name VALUES (1)")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertIsNotNone(node.process_command)

    def test_alter_event_schedule_starts_only(self):
        """测试只有 STARTS 的调度"""
        node = parse_statement("ALTER EVENT event_name ON SCHEDULE EVERY 1 HOUR STARTS '2023-01-01 00:00:00'")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertIsInstance(node.schedule_time, ast.ScheduleTimeEvery)
        self.assertIsNotNone(node.schedule_time.starts_expression)
        self.assertIsNone(node.schedule_time.ends_expression)

    def test_alter_event_schedule_ends_only(self):
        """测试只有 ENDS 的调度"""
        node = parse_statement("ALTER EVENT event_name ON SCHEDULE EVERY 1 HOUR ENDS '2023-12-31 23:59:59'")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertIsInstance(node.schedule_time, ast.ScheduleTimeEvery)
        self.assertIsNone(node.schedule_time.starts_expression)
        self.assertIsNotNone(node.schedule_time.ends_expression)

    def test_alter_event_partial_options_combination(self):
        """测试部分选项组合的 ALTER EVENT 语句"""
        node = parse_statement("ALTER EVENT event_name ON SCHEDULE EVERY 1 DAY DISABLE COMMENT 'Disabled event'")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertIsInstance(node.schedule_time, ast.ScheduleTimeEvery)
        self.assertEqual(node.event_status, ast.EnumEventStatusType.DISABLE)
        self.assertEqual(node.event_comment, "Disabled event")
        self.assertIsNone(node.process_command)

    def test_alter_event_with_current_timestamp(self):
        """测试使用 CURRENT_TIMESTAMP 的调度"""
        node = parse_statement("ALTER EVENT event_name ON SCHEDULE AT INTERVAL 1 HOUR")
        self.assertIsInstance(node, ast.AlterEventStatement)
        self.assertIsInstance(node.event_name, ast.Identifier)
        self.assertEqual(node.event_name.object_name, "event_name")
        self.assertIsInstance(node.schedule_time, ast.ScheduleTimeAt)
        self.assertIsNotNone(node.schedule_time.execute_at_expression) 