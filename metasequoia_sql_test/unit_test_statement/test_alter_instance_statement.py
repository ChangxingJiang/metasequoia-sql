"""
ALTER INSTANCE 语句（alter_instance_statement）单元测试

测试 alter_instance_statement.py 中的语义组：
- alter_instance_statement: ALTER INSTANCE 语句
- alter_instance_action: ALTER INSTANCE 操作
"""

from unittest import TestCase

from metasequoia_sql import ast, parse_statement


class TestAlterInstanceStatement(TestCase):
    """测试 alter_instance_statement 语义组
    
    测试 ALTER INSTANCE 语句的解析，包括各种实例操作的不同场景
    """

    def test_alter_instance_rotate_innodb_master_key(self):
        """测试 ROTATE INNODB MASTER KEY 操作"""
        node = parse_statement("ALTER INSTANCE ROTATE INNODB MASTER KEY")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionRotateInnodbMasterKey)

    def test_alter_instance_rotate_innodb_master_key_with_quotes(self):
        """测试使用引号的 ROTATE INNODB MASTER KEY 操作"""
        node = parse_statement("ALTER INSTANCE ROTATE 'INNODB' MASTER KEY")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionRotateInnodbMasterKey)

    def test_alter_instance_rotate_binlog_master_key(self):
        """测试 ROTATE BINLOG MASTER KEY 操作"""
        node = parse_statement("ALTER INSTANCE ROTATE BINLOG MASTER KEY")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionRotateBinlogMasterKey)

    def test_alter_instance_rotate_binlog_master_key_with_quotes(self):
        """测试使用引号的 ROTATE BINLOG MASTER KEY 操作"""
        node = parse_statement("ALTER INSTANCE ROTATE 'BINLOG' MASTER KEY")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionRotateBinlogMasterKey)

    def test_alter_instance_reload_tls(self):
        """测试 RELOAD TLS 操作"""
        node = parse_statement("ALTER INSTANCE RELOAD TLS")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadTls)

    def test_alter_instance_reload_tls_no_rollback(self):
        """测试 RELOAD TLS NO ROLLBACK ON ERROR 操作"""
        node = parse_statement("ALTER INSTANCE RELOAD TLS NO ROLLBACK ON ERROR")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadTlsNoRollback)

    def test_alter_instance_reload_tls_for_channel(self):
        """测试 RELOAD TLS FOR CHANNEL 操作"""
        node = parse_statement("ALTER INSTANCE RELOAD TLS FOR CHANNEL channel_name")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadTlsForChannel)
        self.assertEqual(node.action.channel_name, "channel_name")

    def test_alter_instance_reload_tls_for_channel_no_rollback(self):
        """测试 RELOAD TLS FOR CHANNEL NO ROLLBACK ON ERROR 操作"""
        node = parse_statement("ALTER INSTANCE RELOAD TLS FOR CHANNEL channel_name NO ROLLBACK ON ERROR")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadTlsForChannelNoRollback)
        self.assertEqual(node.action.channel_name, "channel_name")

    def test_alter_instance_enable_innodb_redo_log(self):
        """测试 ENABLE INNODB REDO_LOG 操作"""
        node = parse_statement("ALTER INSTANCE ENABLE INNODB REDO_LOG")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionEnableInnodbRedo)

    def test_alter_instance_disable_innodb_redo_log(self):
        """测试 DISABLE INNODB REDO_LOG 操作"""
        node = parse_statement("ALTER INSTANCE DISABLE INNODB REDO_LOG")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionDisableInnodbRedo)

    def test_alter_instance_reload_keyring(self):
        """测试 RELOAD KEYRING 操作"""
        node = parse_statement("ALTER INSTANCE RELOAD KEYRING")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadKeyring)

    def test_alter_instance_rotate_with_case_variations(self):
        """测试不同大小写的 ROTATE 操作"""
        # 测试小写的 innodb
        node = parse_statement("ALTER INSTANCE ROTATE innodb MASTER KEY")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionRotateInnodbMasterKey)

        # 测试小写的 binlog
        node = parse_statement("ALTER INSTANCE ROTATE binlog MASTER KEY")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionRotateBinlogMasterKey)

        # 测试混合大小写的 InnoDB
        node = parse_statement("ALTER INSTANCE ROTATE InnoDB MASTER KEY")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionRotateInnodbMasterKey)

        # 测试混合大小写的 BinLog
        node = parse_statement("ALTER INSTANCE ROTATE BinLog MASTER KEY")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionRotateBinlogMasterKey)

    def test_alter_instance_enable_disable_with_case_variations(self):
        """测试不同大小写的 ENABLE/DISABLE 操作"""
        # 测试小写的 innodb 和 redo_log
        node = parse_statement("ALTER INSTANCE ENABLE innodb redo_log")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionEnableInnodbRedo)

        node = parse_statement("ALTER INSTANCE DISABLE innodb redo_log")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionDisableInnodbRedo)

        # 测试混合大小写
        node = parse_statement("ALTER INSTANCE ENABLE InnoDB Redo_Log")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionEnableInnodbRedo)

        node = parse_statement("ALTER INSTANCE DISABLE InnoDB Redo_Log")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionDisableInnodbRedo)

    def test_alter_instance_channel_with_quoted_names(self):
        """测试使用引号的通道名称"""
        node = parse_statement("ALTER INSTANCE RELOAD TLS FOR CHANNEL `channel_name`")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadTlsForChannel)
        self.assertEqual(node.action.channel_name, "channel_name")

        node = parse_statement("ALTER INSTANCE RELOAD TLS FOR CHANNEL `channel_name` NO ROLLBACK ON ERROR")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadTlsForChannelNoRollback)
        self.assertEqual(node.action.channel_name, "channel_name")

    def test_alter_instance_channel_with_special_names(self):
        """测试特殊字符的通道名称"""
        node = parse_statement("ALTER INSTANCE RELOAD TLS FOR CHANNEL replication_channel_1")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadTlsForChannel)
        self.assertEqual(node.action.channel_name, "replication_channel_1")

        node = parse_statement("ALTER INSTANCE RELOAD TLS FOR CHANNEL `group_replication_recovery`")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadTlsForChannel)
        self.assertEqual(node.action.channel_name, "group_replication_recovery")

    def test_alter_instance_rotate_with_double_quotes(self):
        """测试使用双引号的 ROTATE 操作"""
        node = parse_statement('ALTER INSTANCE ROTATE "INNODB" MASTER KEY')
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionRotateInnodbMasterKey)

        node = parse_statement('ALTER INSTANCE ROTATE "BINLOG" MASTER KEY')
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionRotateBinlogMasterKey)

    def test_alter_instance_tls_operations_completeness(self):
        """测试 TLS 相关操作的完整性"""
        # 基本的 RELOAD TLS
        node = parse_statement("ALTER INSTANCE RELOAD TLS")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadTls)

        # 带 NO ROLLBACK 的 RELOAD TLS
        node = parse_statement("ALTER INSTANCE RELOAD TLS NO ROLLBACK ON ERROR")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadTlsNoRollback)

        # 为特定通道的 RELOAD TLS
        node = parse_statement("ALTER INSTANCE RELOAD TLS FOR CHANNEL master_channel")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadTlsForChannel)
        self.assertEqual(node.action.channel_name, "master_channel")

        # 为特定通道带 NO ROLLBACK 的 RELOAD TLS
        node = parse_statement("ALTER INSTANCE RELOAD TLS FOR CHANNEL master_channel NO ROLLBACK ON ERROR")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadTlsForChannelNoRollback)
        self.assertEqual(node.action.channel_name, "master_channel")

    def test_alter_instance_redo_log_operations_completeness(self):
        """测试 REDO_LOG 相关操作的完整性"""
        # 启用 InnoDB REDO_LOG
        node = parse_statement("ALTER INSTANCE ENABLE INNODB REDO_LOG")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionEnableInnodbRedo)

        # 禁用 InnoDB REDO_LOG
        node = parse_statement("ALTER INSTANCE DISABLE INNODB REDO_LOG")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionDisableInnodbRedo)

    def test_alter_instance_keyring_operations(self):
        """测试 KEYRING 相关操作"""
        node = parse_statement("ALTER INSTANCE RELOAD KEYRING")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadKeyring)

    def test_alter_instance_master_key_operations_completeness(self):
        """测试 MASTER KEY 相关操作的完整性"""
        # InnoDB MASTER KEY
        node = parse_statement("ALTER INSTANCE ROTATE INNODB MASTER KEY")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionRotateInnodbMasterKey)

        # BINLOG MASTER KEY
        node = parse_statement("ALTER INSTANCE ROTATE BINLOG MASTER KEY")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionRotateBinlogMasterKey)

    def test_alter_instance_channel_names_with_numbers(self):
        """测试包含数字的通道名称"""
        node = parse_statement("ALTER INSTANCE RELOAD TLS FOR CHANNEL channel123")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadTlsForChannel)
        self.assertEqual(node.action.channel_name, "channel123")

        node = parse_statement("ALTER INSTANCE RELOAD TLS FOR CHANNEL channel123 NO ROLLBACK ON ERROR")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadTlsForChannelNoRollback)
        self.assertEqual(node.action.channel_name, "channel123")

    def test_alter_instance_channel_names_with_underscores(self):
        """测试包含下划线的通道名称"""
        node = parse_statement("ALTER INSTANCE RELOAD TLS FOR CHANNEL group_replication_applier")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadTlsForChannel)
        self.assertEqual(node.action.channel_name, "group_replication_applier")

        node = parse_statement("ALTER INSTANCE RELOAD TLS FOR CHANNEL group_replication_applier NO ROLLBACK ON ERROR")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadTlsForChannelNoRollback)
        self.assertEqual(node.action.channel_name, "group_replication_applier")

    def test_alter_instance_with_mixed_case_keywords(self):
        """测试混合大小写的关键字"""
        node = parse_statement("alter instance reload tls")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadTls)

        node = parse_statement("ALTER instance RELOAD keyring")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadKeyring)

    def test_alter_instance_comprehensive_scenarios(self):
        """测试综合场景"""
        # 测试所有主要操作类型
        test_cases = [
            ("ALTER INSTANCE ROTATE INNODB MASTER KEY", ast.AlterInstanceActionRotateInnodbMasterKey),
            ("ALTER INSTANCE ROTATE BINLOG MASTER KEY", ast.AlterInstanceActionRotateBinlogMasterKey),
            ("ALTER INSTANCE RELOAD TLS", ast.AlterInstanceActionReloadTls),
            ("ALTER INSTANCE RELOAD TLS NO ROLLBACK ON ERROR", ast.AlterInstanceActionReloadTlsNoRollback),
            ("ALTER INSTANCE RELOAD TLS FOR CHANNEL test_channel", ast.AlterInstanceActionReloadTlsForChannel),
            ("ALTER INSTANCE RELOAD TLS FOR CHANNEL test_channel NO ROLLBACK ON ERROR", ast.AlterInstanceActionReloadTlsForChannelNoRollback),
            ("ALTER INSTANCE ENABLE INNODB REDO_LOG", ast.AlterInstanceActionEnableInnodbRedo),
            ("ALTER INSTANCE DISABLE INNODB REDO_LOG", ast.AlterInstanceActionDisableInnodbRedo),
            ("ALTER INSTANCE RELOAD KEYRING", ast.AlterInstanceActionReloadKeyring),
        ]

        for sql, expected_action_type in test_cases:
            with self.subTest(sql=sql):
                node = parse_statement(sql)
                self.assertIsInstance(node, ast.AlterInstanceStatement)
                self.assertIsInstance(node.action, expected_action_type)

    def test_alter_instance_channel_edge_cases(self):
        """测试通道名称的边界情况"""
        # 最短通道名称
        node = parse_statement("ALTER INSTANCE RELOAD TLS FOR CHANNEL a")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadTlsForChannel)
        self.assertEqual(node.action.channel_name, "a")

        # 带特殊字符的通道名称（需要引号）
        node = parse_statement("ALTER INSTANCE RELOAD TLS FOR CHANNEL `channel-with-dash`")
        self.assertIsInstance(node, ast.AlterInstanceStatement)
        self.assertIsInstance(node.action, ast.AlterInstanceActionReloadTlsForChannel)
        self.assertEqual(node.action.channel_name, "channel-with-dash") 