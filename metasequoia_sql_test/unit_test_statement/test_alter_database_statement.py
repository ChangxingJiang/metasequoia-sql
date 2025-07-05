"""
ALTER DATABASE 语句（alter_database_statement）单元测试

测试 alter_database_statement.py 中的语义组：
- alter_database_statement: ALTER DATABASE 语句
"""

from unittest import TestCase

from metasequoia_sql import ast, parse_statement


class TestAlterDatabaseStatement(TestCase):
    """测试 alter_database_statement 语义组
    
    测试 ALTER DATABASE 语句的解析，包括数据库名称和各种选项的不同组合
    """

    def test_alter_database_with_name_and_charset(self):
        """测试指定数据库名称和字符集的 ALTER DATABASE 语句"""
        node = parse_statement("ALTER DATABASE database_name DEFAULT CHAR SET utf8mb4")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertEqual(node.database_name, "database_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionDefaultCharset)
        self.assertEqual(node.option_list[0].value.charset_name, "utf8mb4")

    def test_alter_database_with_name_and_collate(self):
        """测试指定数据库名称和排序规则的 ALTER DATABASE 语句"""
        node = parse_statement("ALTER DATABASE database_name DEFAULT COLLATE = utf8mb4_unicode_ci")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertEqual(node.database_name, "database_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionDefaultCollate)
        self.assertEqual(node.option_list[0].value.charset_name, "utf8mb4_unicode_ci")

    def test_alter_database_with_name_and_encryption(self):
        """测试指定数据库名称和加密的 ALTER DATABASE 语句"""
        node = parse_statement("ALTER DATABASE database_name DEFAULT ENCRYPTION = 'Y'")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertEqual(node.database_name, "database_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionDefaultEncryption)
        self.assertEqual(node.option_list[0].value, "Y")

    def test_alter_database_with_name_and_read_only(self):
        """测试指定数据库名称和只读选项的 ALTER DATABASE 语句"""
        node = parse_statement("ALTER DATABASE database_name READ ONLY = 1")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertEqual(node.database_name, "database_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionReadOnly)
        self.assertIsNotNone(node.option_list[0].value)

    def test_alter_database_without_name_and_charset(self):
        """测试不指定数据库名称和字符集的 ALTER DATABASE 语句"""
        node = parse_statement("ALTER DATABASE CHAR SET utf8mb4")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertIsNone(node.database_name)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionDefaultCharset)
        self.assertEqual(node.option_list[0].value.charset_name, "utf8mb4")

    def test_alter_database_without_name_and_collate(self):
        """测试不指定数据库名称和排序规则的 ALTER DATABASE 语句"""
        node = parse_statement("ALTER DATABASE COLLATE utf8mb4_unicode_ci")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertIsNone(node.database_name)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionDefaultCollate)
        self.assertEqual(node.option_list[0].value.charset_name, "utf8mb4_unicode_ci")

    def test_alter_database_without_name_and_encryption(self):
        """测试不指定数据库名称和加密的 ALTER DATABASE 语句"""
        node = parse_statement("ALTER DATABASE ENCRYPTION = 'N'")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertIsNone(node.database_name)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionDefaultEncryption)
        self.assertEqual(node.option_list[0].value, "N")

    def test_alter_database_without_name_and_read_only(self):
        """测试不指定数据库名称和只读选项的 ALTER DATABASE 语句"""
        node = parse_statement("ALTER DATABASE READ ONLY = 0")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertIsNone(node.database_name)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionReadOnly)
        self.assertIsNotNone(node.option_list[0].value)

    def test_alter_database_with_multiple_options(self):
        """测试包含多个选项的 ALTER DATABASE 语句"""
        node = parse_statement(
            "ALTER DATABASE database_name DEFAULT CHAR SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertEqual(node.database_name, "database_name")
        self.assertEqual(len(node.option_list), 2)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionDefaultCharset)
        self.assertEqual(node.option_list[0].value.charset_name, "utf8mb4")
        self.assertIsInstance(node.option_list[1], ast.DdlOptionDefaultCollate)
        self.assertEqual(node.option_list[1].value.charset_name, "utf8mb4_unicode_ci")

    def test_alter_database_with_all_options(self):
        """测试包含所有选项的 ALTER DATABASE 语句"""
        node = parse_statement(
            "ALTER DATABASE database_name DEFAULT CHAR SET utf8mb4 DEFAULT COLLATE utf8mb4_unicode_ci DEFAULT ENCRYPTION = 'Y' READ ONLY = 1")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertEqual(node.database_name, "database_name")
        self.assertEqual(len(node.option_list), 4)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionDefaultCharset)
        self.assertEqual(node.option_list[0].value.charset_name, "utf8mb4")
        self.assertIsInstance(node.option_list[1], ast.DdlOptionDefaultCollate)
        self.assertEqual(node.option_list[1].value.charset_name, "utf8mb4_unicode_ci")
        self.assertIsInstance(node.option_list[2], ast.DdlOptionDefaultEncryption)
        self.assertEqual(node.option_list[2].value, "Y")
        self.assertIsInstance(node.option_list[3], ast.DdlOptionReadOnly)
        self.assertIsNotNone(node.option_list[3].value)

    def test_alter_database_charset_with_equal_sign(self):
        """测试使用等号的字符集选项"""
        node = parse_statement("ALTER DATABASE database_name DEFAULT CHAR SET = utf8mb4")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertEqual(node.database_name, "database_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionDefaultCharset)
        self.assertEqual(node.option_list[0].value.charset_name, "utf8mb4")

    def test_alter_database_collate_with_equal_sign(self):
        """测试使用等号的排序规则选项"""
        node = parse_statement("ALTER DATABASE database_name DEFAULT COLLATE = utf8mb4_unicode_ci")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertEqual(node.database_name, "database_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionDefaultCollate)
        self.assertEqual(node.option_list[0].value.charset_name, "utf8mb4_unicode_ci")

    def test_alter_database_read_only_with_default_value(self):
        """测试只读选项使用 DEFAULT 值"""
        node = parse_statement("ALTER DATABASE database_name READ ONLY = DEFAULT")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertEqual(node.database_name, "database_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionReadOnly)
        self.assertIsInstance(node.option_list[0].value, ast.DefaultValue)

    def test_alter_database_without_default_keyword(self):
        """测试不使用 DEFAULT 关键字的选项"""
        node = parse_statement("ALTER DATABASE database_name CHAR SET utf8mb4")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertEqual(node.database_name, "database_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionDefaultCharset)
        self.assertEqual(node.option_list[0].value.charset_name, "utf8mb4")

    def test_alter_database_charset_variations(self):
        """测试字符集选项的不同变体"""
        # 测试 CHARSET 关键字
        node = parse_statement("ALTER DATABASE database_name DEFAULT CHARSET utf8mb4")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertEqual(node.database_name, "database_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionDefaultCharset)
        self.assertEqual(node.option_list[0].value.charset_name, "utf8mb4")

    def test_alter_database_with_quoted_database_name(self):
        """测试使用引号的数据库名称"""
        node = parse_statement("ALTER DATABASE `database_name` DEFAULT CHAR SET utf8mb4")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertEqual(node.database_name, "database_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionDefaultCharset)
        self.assertEqual(node.option_list[0].value.charset_name, "utf8mb4")

    def test_alter_database_with_special_charset_names(self):
        """测试特殊字符集名称"""
        node = parse_statement("ALTER DATABASE database_name DEFAULT CHAR SET latin1")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertEqual(node.database_name, "database_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionDefaultCharset)
        self.assertEqual(node.option_list[0].value.charset_name, "latin1")

    def test_alter_database_with_special_collate_names(self):
        """测试特殊排序规则名称"""
        node = parse_statement("ALTER DATABASE database_name DEFAULT COLLATE latin1_swedish_ci")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertEqual(node.database_name, "database_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionDefaultCollate)
        self.assertEqual(node.option_list[0].value.charset_name, "latin1_swedish_ci")

    def test_alter_database_encryption_with_boolean_values(self):
        """测试加密选项使用布尔值"""
        # 测试 'Y' 值
        node = parse_statement("ALTER DATABASE database_name DEFAULT ENCRYPTION = 'Y'")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertEqual(node.database_name, "database_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionDefaultEncryption)
        self.assertEqual(node.option_list[0].value, "Y")

        # 测试 'N' 值
        node = parse_statement("ALTER DATABASE database_name DEFAULT ENCRYPTION = 'N'")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertEqual(node.database_name, "database_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionDefaultEncryption)
        self.assertEqual(node.option_list[0].value, "N")

    def test_alter_database_read_only_with_numeric_values(self):
        """测试只读选项使用数字值"""
        # 测试 1 值
        node = parse_statement("ALTER DATABASE database_name READ ONLY = 1")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertEqual(node.database_name, "database_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionReadOnly)
        self.assertIsNotNone(node.option_list[0].value)

        # 测试 0 值
        node = parse_statement("ALTER DATABASE database_name READ ONLY = 0")
        self.assertIsInstance(node, ast.AlterDatabaseStatement)
        self.assertEqual(node.database_name, "database_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.DdlOptionReadOnly)
        self.assertIsNotNone(node.option_list[0].value)
