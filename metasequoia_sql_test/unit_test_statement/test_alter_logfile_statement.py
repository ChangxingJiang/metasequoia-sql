"""
ALTER LOGFILE GROUP 语句（alter_logfile_statement）单元测试

测试 alter_logfile_statement.py 中的语义组：
- alter_logfile_statement: ALTER LOGFILE GROUP 语句
"""

from unittest import TestCase

from metasequoia_sql import ast, parse_statement


class TestAlterLogfileStatement(TestCase):
    """测试 alter_logfile_statement 语义组
    
    测试 ALTER LOGFILE GROUP 语句的解析，包括日志文件组名称、撤销文件和各种选项的不同组合
    """

    def test_alter_logfile_basic(self):
        """测试基本的 ALTER LOGFILE GROUP 语句"""
        node = parse_statement("ALTER LOGFILE GROUP group_name ADD UNDOFILE 'undofile.log'")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "undofile.log")
        self.assertEqual(len(node.option_list), 0)

    def test_alter_logfile_with_initial_size(self):
        """测试带有初始大小选项的 ALTER LOGFILE GROUP 语句"""
        node = parse_statement("ALTER LOGFILE GROUP group_name ADD UNDOFILE 'undofile.log' INITIAL_SIZE = 16M")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "undofile.log")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionInitialSize)

    def test_alter_logfile_with_storage_engine(self):
        """测试带有存储引擎选项的 ALTER LOGFILE GROUP 语句"""
        node = parse_statement("ALTER LOGFILE GROUP group_name ADD UNDOFILE 'undofile.log' ENGINE = NDB")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "undofile.log")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionStorageEngine)
        self.assertEqual(node.option_list[0].value, "NDB")

    def test_alter_logfile_with_wait_option(self):
        """测试带有等待选项的 ALTER LOGFILE GROUP 语句"""
        node = parse_statement("ALTER LOGFILE GROUP group_name ADD UNDOFILE 'undofile.log' WAIT")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "undofile.log")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionWait)
        self.assertTrue(node.option_list[0].value)

    def test_alter_logfile_with_no_wait_option(self):
        """测试带有不等待选项的 ALTER LOGFILE GROUP 语句"""
        node = parse_statement("ALTER LOGFILE GROUP group_name ADD UNDOFILE 'undofile.log' NO_WAIT")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "undofile.log")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionWait)
        self.assertFalse(node.option_list[0].value)

    def test_alter_logfile_with_multiple_options(self):
        """测试包含多个选项的 ALTER LOGFILE GROUP 语句"""
        node = parse_statement("ALTER LOGFILE GROUP group_name ADD UNDOFILE 'undofile.log' INITIAL_SIZE = 32M, ENGINE = NDB")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "undofile.log")
        self.assertEqual(len(node.option_list), 2)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionInitialSize)
        self.assertIsInstance(node.option_list[1], ast.DdlOptionStorageEngine)
        self.assertEqual(node.option_list[1].value, "NDB")

    def test_alter_logfile_with_all_options(self):
        """测试包含所有选项的 ALTER LOGFILE GROUP 语句"""
        node = parse_statement("ALTER LOGFILE GROUP group_name ADD UNDOFILE 'undofile.log' INITIAL_SIZE = 64M, ENGINE = NDB, WAIT")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "undofile.log")
        self.assertEqual(len(node.option_list), 3)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionInitialSize)
        self.assertIsInstance(node.option_list[1], ast.DdlOptionStorageEngine)
        self.assertEqual(node.option_list[1].value, "NDB")
        self.assertIsInstance(node.option_list[2], ast.DdlOptionWait)
        self.assertTrue(node.option_list[2].value)

    def test_alter_logfile_with_quoted_group_name(self):
        """测试使用引号的日志文件组名称"""
        node = parse_statement("ALTER LOGFILE GROUP `log_group_name` ADD UNDOFILE 'undofile.log'")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "log_group_name")
        self.assertEqual(node.undofile, "undofile.log")
        self.assertEqual(len(node.option_list), 0)

    def test_alter_logfile_with_different_undofile_paths(self):
        """测试不同的撤销文件路径格式"""
        # 测试相对路径
        node = parse_statement("ALTER LOGFILE GROUP group_name ADD UNDOFILE 'logs/undofile.log'")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "logs/undofile.log")

        # 测试绝对路径
        node = parse_statement("ALTER LOGFILE GROUP group_name ADD UNDOFILE '/var/lib/mysql/undofile.log'")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "/var/lib/mysql/undofile.log")

        # 测试 Windows 路径
        node = parse_statement("ALTER LOGFILE GROUP group_name ADD UNDOFILE 'C:\\\\mysql\\\\data\\\\undofile.log'")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "C:\\mysql\\data\\undofile.log")

    def test_alter_logfile_with_double_quoted_undofile(self):
        """测试使用双引号的撤销文件路径"""
        node = parse_statement('ALTER LOGFILE GROUP group_name ADD UNDOFILE "undofile.log"')
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "undofile.log")
        self.assertEqual(len(node.option_list), 0)

    def test_alter_logfile_with_special_group_names(self):
        """测试特殊字符的日志文件组名称"""
        # 测试包含数字的组名
        node = parse_statement("ALTER LOGFILE GROUP log_group_123 ADD UNDOFILE 'undofile.log'")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "log_group_123")
        self.assertEqual(node.undofile, "undofile.log")

        # 测试包含下划线的组名
        node = parse_statement("ALTER LOGFILE GROUP log_file_group ADD UNDOFILE 'undofile.log'")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "log_file_group")
        self.assertEqual(node.undofile, "undofile.log")

    def test_alter_logfile_with_initial_size_variations(self):
        """测试不同的初始大小值格式"""
        # 测试 MB 单位
        node = parse_statement("ALTER LOGFILE GROUP group_name ADD UNDOFILE 'undofile.log' INITIAL_SIZE = 128M")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "undofile.log")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionInitialSize)

        # 测试 GB 单位
        node = parse_statement("ALTER LOGFILE GROUP group_name ADD UNDOFILE 'undofile.log' INITIAL_SIZE = 1G")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "undofile.log")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionInitialSize)

        # 测试字节数
        node = parse_statement("ALTER LOGFILE GROUP group_name ADD UNDOFILE 'undofile.log' INITIAL_SIZE = 1073741824")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "undofile.log")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionInitialSize)

    def test_alter_logfile_with_storage_engine_variations(self):
        """测试不同的存储引擎选项"""
        # 测试 NDB 引擎
        node = parse_statement("ALTER LOGFILE GROUP group_name ADD UNDOFILE 'undofile.log' ENGINE = NDB")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "undofile.log")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionStorageEngine)
        self.assertEqual(node.option_list[0].value, "NDB")

        # 测试带 STORAGE 关键字的引擎
        node = parse_statement("ALTER LOGFILE GROUP group_name ADD UNDOFILE 'undofile.log' STORAGE ENGINE = NDB")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "undofile.log")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionStorageEngine)
        self.assertEqual(node.option_list[0].value, "NDB")

    def test_alter_logfile_without_equal_signs(self):
        """测试不使用等号的选项格式"""
        node = parse_statement("ALTER LOGFILE GROUP group_name ADD UNDOFILE 'undofile.log' INITIAL_SIZE 64M")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "undofile.log")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionInitialSize)

    def test_alter_logfile_options_different_order(self):
        """测试不同顺序的选项组合"""
        node = parse_statement("ALTER LOGFILE GROUP group_name ADD UNDOFILE 'undofile.log' WAIT, INITIAL_SIZE = 32M, ENGINE = NDB")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "undofile.log")
        self.assertEqual(len(node.option_list), 3)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionWait)
        self.assertTrue(node.option_list[0].value)
        self.assertIsInstance(node.option_list[1], ast.DdlOptionInitialSize)
        self.assertIsInstance(node.option_list[2], ast.DdlOptionStorageEngine)
        self.assertEqual(node.option_list[2].value, "NDB")

    def test_alter_logfile_with_complex_undofile_names(self):
        """测试复杂的撤销文件名称"""
        # 测试包含特殊字符的文件名
        node = parse_statement("ALTER LOGFILE GROUP group_name ADD UNDOFILE 'undo-file_01.log'")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "undo-file_01.log")

        # 测试长路径名称
        node = parse_statement("ALTER LOGFILE GROUP group_name ADD UNDOFILE '/very/long/path/to/mysql/data/logs/undofile_backup_2023.log'")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "/very/long/path/to/mysql/data/logs/undofile_backup_2023.log")

    def test_alter_logfile_case_insensitive_keywords(self):
        """测试关键字的大小写不敏感性"""
        node = parse_statement("alter logfile group group_name add undofile 'undofile.log' initial_size = 16M")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "undofile.log")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionInitialSize)

    def test_alter_logfile_with_options_no_comma(self):
        """测试选项之间不使用逗号的情况"""
        node = parse_statement("ALTER LOGFILE GROUP group_name ADD UNDOFILE 'undofile.log' INITIAL_SIZE = 32M ENGINE = NDB")
        self.assertIsInstance(node, ast.AlterLogfileStatement)
        self.assertEqual(node.group_name, "group_name")
        self.assertEqual(node.undofile, "undofile.log")
        self.assertEqual(len(node.option_list), 2)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionInitialSize)
        self.assertIsInstance(node.option_list[1], ast.DdlOptionStorageEngine)
        self.assertEqual(node.option_list[1].value, "NDB")

    def test_alter_logfile_comprehensive_scenarios(self):
        """测试综合场景"""
        # 测试所有主要选项类型
        test_cases = [
            ("ALTER LOGFILE GROUP lg1 ADD UNDOFILE 'undo1.log'", 0),
            ("ALTER LOGFILE GROUP lg1 ADD UNDOFILE 'undo1.log' INITIAL_SIZE = 16M", 1),
            ("ALTER LOGFILE GROUP lg1 ADD UNDOFILE 'undo1.log' ENGINE = NDB", 1),
            ("ALTER LOGFILE GROUP lg1 ADD UNDOFILE 'undo1.log' WAIT", 1),
            ("ALTER LOGFILE GROUP lg1 ADD UNDOFILE 'undo1.log' NO_WAIT", 1),
            ("ALTER LOGFILE GROUP lg1 ADD UNDOFILE 'undo1.log' INITIAL_SIZE = 32M, ENGINE = NDB, WAIT", 3),
        ]

        for sql, expected_option_count in test_cases:
            with self.subTest(sql=sql):
                node = parse_statement(sql)
                self.assertIsInstance(node, ast.AlterLogfileStatement)
                self.assertEqual(len(node.option_list), expected_option_count) 