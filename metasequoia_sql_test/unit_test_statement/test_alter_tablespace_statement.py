"""
ALTER TABLESPACE 语句单元测试

测试语义组：alter_tablespace_statement 及其相关语义组
"""

import unittest

from metasequoia_sql import parse_statement
from metasequoia_sql.ast.statement.alter_tablespace_statement import (
    AlterTablespaceStatement, EnumAlterTablespaceActionType
)
from metasequoia_sql.ast.phrase.ddl_option import (
    DdlOptionInitialSize, DdlOptionAutoextendSize, DdlOptionMaxSize,
    DdlOptionStorageEngine, DdlOptionWait, DdlOptionTablespaceEncryption,
    DdlOptionTablespaceEngineAttribute
)


class TestAlterTablespaceStatement(unittest.TestCase):
    """测试 ALTER TABLESPACE 语句解析"""

    def test_alter_tablespace_add_datafile(self):
        """测试 ALTER TABLESPACE ADD DATAFILE 语句"""
        sql = "ALTER TABLESPACE tablespace_name ADD DATAFILE '/path/to/datafile.ibd'"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.ADD)
        self.assertEqual(node.datafile, "/path/to/datafile.ibd")
        self.assertIsNone(node.target_name)
        self.assertEqual(len(node.option_list), 0)

    def test_alter_tablespace_drop_datafile(self):
        """测试 ALTER TABLESPACE DROP DATAFILE 语句"""
        sql = "ALTER TABLESPACE tablespace_name DROP DATAFILE '/path/to/datafile.ibd'"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.DROP)
        self.assertEqual(node.datafile, "/path/to/datafile.ibd")
        self.assertIsNone(node.target_name)
        self.assertEqual(len(node.option_list), 0)

    def test_alter_tablespace_rename_to(self):
        """测试 ALTER TABLESPACE RENAME TO 语句"""
        sql = "ALTER TABLESPACE tablespace_name RENAME TO new_tablespace_name"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.RENAME)
        self.assertIsNone(node.datafile)
        self.assertEqual(node.target_name, "new_tablespace_name")
        self.assertEqual(len(node.option_list), 0)

    def test_alter_tablespace_with_initial_size(self):
        """测试 ALTER TABLESPACE 带 INITIAL_SIZE 选项"""
        sql = "ALTER TABLESPACE tablespace_name INITIAL_SIZE = 100M"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.ALTER)
        self.assertIsNone(node.datafile)
        self.assertIsNone(node.target_name)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionInitialSize)

    def test_alter_tablespace_with_autoextend_size(self):
        """测试 ALTER TABLESPACE 带 AUTOEXTEND_SIZE 选项"""
        sql = "ALTER TABLESPACE tablespace_name AUTOEXTEND_SIZE = 50M"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.ALTER)
        self.assertIsNone(node.datafile)
        self.assertIsNone(node.target_name)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionAutoextendSize)

    def test_alter_tablespace_with_max_size(self):
        """测试 ALTER TABLESPACE 带 MAX_SIZE 选项"""
        sql = "ALTER TABLESPACE tablespace_name MAX_SIZE = 1G"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.ALTER)
        self.assertIsNone(node.datafile)
        self.assertIsNone(node.target_name)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionMaxSize)

    def test_alter_tablespace_with_storage_engine(self):
        """测试 ALTER TABLESPACE 带 ENGINE 选项"""
        sql = "ALTER TABLESPACE tablespace_name ENGINE = 'InnoDB'"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.ALTER)
        self.assertIsNone(node.datafile)
        self.assertIsNone(node.target_name)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionStorageEngine)

    def test_alter_tablespace_with_wait(self):
        """测试 ALTER TABLESPACE 带 WAIT 选项"""
        sql = "ALTER TABLESPACE tablespace_name WAIT"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.ALTER)
        self.assertIsNone(node.datafile)
        self.assertIsNone(node.target_name)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionWait)

    def test_alter_tablespace_with_encryption(self):
        """测试 ALTER TABLESPACE 带 ENCRYPTION 选项"""
        sql = "ALTER TABLESPACE tablespace_name ENCRYPTION = 'Y'"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.ALTER)
        self.assertIsNone(node.datafile)
        self.assertIsNone(node.target_name)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionTablespaceEncryption)

    def test_alter_tablespace_with_engine_attribute(self):
        """测试 ALTER TABLESPACE 带 ENGINE_ATTRIBUTE 选项"""
        sql = "ALTER TABLESPACE tablespace_name ENGINE_ATTRIBUTE = 'attribute_value'"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.ALTER)
        self.assertIsNone(node.datafile)
        self.assertIsNone(node.target_name)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionTablespaceEngineAttribute)

    def test_alter_tablespace_with_multiple_options(self):
        """测试 ALTER TABLESPACE 带多个选项"""
        sql = "ALTER TABLESPACE tablespace_name INITIAL_SIZE = 100M, MAX_SIZE = 1G, ENGINE = 'InnoDB'"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.ALTER)
        self.assertIsNone(node.datafile)
        self.assertIsNone(node.target_name)
        self.assertEqual(len(node.option_list), 3)
        self.assertIsInstance(node.option_list[0], DdlOptionInitialSize)
        self.assertIsInstance(node.option_list[1], DdlOptionMaxSize)
        self.assertIsInstance(node.option_list[2], DdlOptionStorageEngine)

    def test_alter_tablespace_add_datafile_with_options(self):
        """测试 ALTER TABLESPACE ADD DATAFILE 带选项"""
        sql = "ALTER TABLESPACE tablespace_name ADD DATAFILE '/path/to/datafile.ibd' INITIAL_SIZE = 100M"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.ADD)
        self.assertEqual(node.datafile, "/path/to/datafile.ibd")
        self.assertIsNone(node.target_name)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionInitialSize)

    def test_alter_tablespace_drop_datafile_with_options(self):
        """测试 ALTER TABLESPACE DROP DATAFILE 带选项"""
        sql = "ALTER TABLESPACE tablespace_name DROP DATAFILE '/path/to/datafile.ibd' WAIT"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.DROP)
        self.assertEqual(node.datafile, "/path/to/datafile.ibd")
        self.assertIsNone(node.target_name)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionWait)

    def test_alter_tablespace_add_datafile_with_multiple_options(self):
        """测试 ALTER TABLESPACE ADD DATAFILE 带多个选项"""
        sql = """
        ALTER TABLESPACE tablespace_name 
        ADD DATAFILE '/path/to/datafile.ibd' 
        INITIAL_SIZE = 100M, 
        AUTOEXTEND_SIZE = 50M, 
        MAX_SIZE = 1G
        """
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.ADD)
        self.assertEqual(node.datafile, "/path/to/datafile.ibd")
        self.assertIsNone(node.target_name)
        self.assertEqual(len(node.option_list), 3)
        self.assertIsInstance(node.option_list[0], DdlOptionInitialSize)
        self.assertIsInstance(node.option_list[1], DdlOptionAutoextendSize)
        self.assertIsInstance(node.option_list[2], DdlOptionMaxSize)

    def test_alter_tablespace_with_size_units(self):
        """测试 ALTER TABLESPACE 带不同大小单位"""
        # 测试 K 单位
        sql = "ALTER TABLESPACE tablespace_name INITIAL_SIZE = 1024K"
        node = parse_statement(sql)
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionInitialSize)

        # 测试 M 单位
        sql = "ALTER TABLESPACE tablespace_name INITIAL_SIZE = 100M"
        node = parse_statement(sql)
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionInitialSize)

        # 测试 G 单位
        sql = "ALTER TABLESPACE tablespace_name INITIAL_SIZE = 1G"
        node = parse_statement(sql)
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionInitialSize)

    def test_alter_tablespace_with_quoted_strings(self):
        """测试 ALTER TABLESPACE 带引号字符串"""
        sql = "ALTER TABLESPACE tablespace_name ADD DATAFILE '/path/with spaces/datafile.ibd'"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.ADD)
        self.assertEqual(node.datafile, "/path/with spaces/datafile.ibd")

    def test_alter_tablespace_with_double_quoted_strings(self):
        """测试 ALTER TABLESPACE 带双引号字符串"""
        sql = 'ALTER TABLESPACE tablespace_name ADD DATAFILE "/path/to/datafile.ibd"'
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.ADD)
        self.assertEqual(node.datafile, "/path/to/datafile.ibd")

    def test_alter_tablespace_with_backtick_identifiers(self):
        """测试 ALTER TABLESPACE 带反引号标识符"""
        sql = "ALTER TABLESPACE `tablespace_name` ADD DATAFILE '/path/to/datafile.ibd'"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.ADD)
        self.assertEqual(node.datafile, "/path/to/datafile.ibd")

    def test_alter_tablespace_rename_with_backtick_identifiers(self):
        """测试 ALTER TABLESPACE RENAME TO 带反引号标识符"""
        sql = "ALTER TABLESPACE `old_tablespace_name` RENAME TO `new_tablespace_name`"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "old_tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.RENAME)
        self.assertEqual(node.target_name, "new_tablespace_name")

    def test_alter_tablespace_with_no_wait(self):
        """测试 ALTER TABLESPACE 带 NO_WAIT 选项"""
        sql = "ALTER TABLESPACE tablespace_name NO_WAIT"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.ALTER)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionWait)

    def test_alter_tablespace_with_encryption_off(self):
        """测试 ALTER TABLESPACE 带 ENCRYPTION = 'N' 选项"""
        sql = "ALTER TABLESPACE tablespace_name ENCRYPTION = 'N'"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.ALTER)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionTablespaceEncryption)
        self.assertEqual(node.option_list[0].value, "N")

    def test_alter_tablespace_complex_scenario(self):
        """测试复杂的 ALTER TABLESPACE 场景"""
        sql = """
        ALTER TABLESPACE `my_tablespace` 
        ADD DATAFILE '/var/lib/mysql/data/my_tablespace.ibd' 
        INITIAL_SIZE = 512M,
        AUTOEXTEND_SIZE = 64M,
        MAX_SIZE = 2G,
        ENGINE = 'InnoDB',
        ENCRYPTION = 'Y',
        ENGINE_ATTRIBUTE = '{"key": "value"}',
        WAIT
        """
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "my_tablespace")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.ADD)
        self.assertEqual(node.datafile, "/var/lib/mysql/data/my_tablespace.ibd")
        self.assertIsNone(node.target_name)
        self.assertEqual(len(node.option_list), 7)
        
        # 验证选项类型
        option_types = [type(opt) for opt in node.option_list]
        self.assertIn(DdlOptionInitialSize, option_types)
        self.assertIn(DdlOptionAutoextendSize, option_types)
        self.assertIn(DdlOptionMaxSize, option_types)
        self.assertIn(DdlOptionStorageEngine, option_types)
        self.assertIn(DdlOptionTablespaceEncryption, option_types)
        self.assertIn(DdlOptionTablespaceEngineAttribute, option_types)
        self.assertIn(DdlOptionWait, option_types)

    def test_alter_tablespace_without_equal_sign(self):
        """测试 ALTER TABLESPACE 不带等号的选项"""
        sql = "ALTER TABLESPACE tablespace_name INITIAL_SIZE 100M"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.ALTER)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionInitialSize)

    def test_alter_tablespace_with_numeric_values(self):
        """测试 ALTER TABLESPACE 带数值选项"""
        sql = "ALTER TABLESPACE tablespace_name INITIAL_SIZE = 1073741824"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterTablespaceStatement)
        self.assertEqual(node.tablespace_name, "tablespace_name")
        self.assertEqual(node.action_type, EnumAlterTablespaceActionType.ALTER)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionInitialSize)


if __name__ == "__main__":
    unittest.main() 