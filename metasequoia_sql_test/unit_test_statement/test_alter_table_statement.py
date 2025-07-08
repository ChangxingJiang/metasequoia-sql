"""
ALTER TABLE 语句（alter_table_statement）单元测试

测试 alter_table_statement.py 中的语义组：
- alter_table_statement: ALTER TABLE 语句
"""

from unittest import TestCase

from metasequoia_sql import ast, parse_statement


class TestAlterTableStatement(TestCase):
    """测试 alter_table_statement 语义组
    
    测试 ALTER TABLE 语句的解析，包括各种修改命令和选项的不同组合
    """

    def test_alter_table_add_column(self):
        """测试添加单列的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name ADD COLUMN column_name INT")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterAddColumn)
        self.assertEqual(node.command_list[0].column_name, "column_name")

    def test_alter_table_add_column_without_column_keyword(self):
        """测试不使用 COLUMN 关键字添加列的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name ADD column_name VARCHAR(255)")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterAddColumn)
        self.assertEqual(node.command_list[0].column_name, "column_name")

    def test_alter_table_add_multiple_columns(self):
        """测试添加多列的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name ADD COLUMN (column_name_1 INT, column_name_2 VARCHAR(255))")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterAddColumns)
        self.assertIsNotNone(node.command_list[0].table_element_list)

    def test_alter_table_drop_column(self):
        """测试删除列的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name DROP COLUMN column_name")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterDropColumn)
        self.assertEqual(node.command_list[0].column_name, "column_name")

    def test_alter_table_drop_column_without_column_keyword(self):
        """测试不使用 COLUMN 关键字删除列的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name DROP column_name")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterDropColumn)
        self.assertEqual(node.command_list[0].column_name, "column_name")

    def test_alter_table_modify_column(self):
        """测试修改列的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name MODIFY COLUMN column_name VARCHAR(500)")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterModifyColumn)
        self.assertEqual(node.command_list[0].column_name, "column_name")

    def test_alter_table_change_column(self):
        """测试更改列名和定义的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name CHANGE COLUMN old_column_name new_column_name INT")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterChangeColumn)
        self.assertEqual(node.command_list[0].old_column_name, "old_column_name")
        self.assertEqual(node.command_list[0].new_column_name, "new_column_name")

    def test_alter_table_rename_table(self):
        """测试重命名表的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name RENAME TO new_table_name")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterRenameTable)
        self.assertIsInstance(node.command_list[0].new_table_name, ast.Identifier)

    def test_alter_table_add_index(self):
        """测试添加索引的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name ADD INDEX index_name (column_name)")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterAddConstraint)

    def test_alter_table_drop_index(self):
        """测试删除索引的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name DROP INDEX index_name")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterDropKey)
        self.assertEqual(node.command_list[0].key_name, "index_name")

    def test_alter_table_drop_primary_key(self):
        """测试删除主键的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name DROP PRIMARY KEY")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterDropPrimaryKey)

    def test_alter_table_drop_foreign_key(self):
        """测试删除外键的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name DROP FOREIGN KEY fk_name")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterDropForeignKey)
        self.assertEqual(node.command_list[0].key_name, "fk_name")

    def test_alter_table_enable_keys(self):
        """测试启用键的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name ENABLE KEYS")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterEnableKeys)

    def test_alter_table_disable_keys(self):
        """测试禁用键的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name DISABLE KEYS")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterDisableKeys)

    def test_alter_table_set_default_value(self):
        """测试设置默认值的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name ALTER COLUMN column_name SET DEFAULT 'default_value'")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterSetDefaultValue)
        self.assertEqual(node.command_list[0].column_name, "column_name")

    def test_alter_table_drop_default_value(self):
        """测试删除默认值的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name ALTER COLUMN column_name DROP DEFAULT")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterDropDefault)
        self.assertEqual(node.command_list[0].column_name, "column_name")

    def test_alter_table_convert_to_charset(self):
        """测试转换字符集的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name CONVERT TO CHAR SET utf8mb4")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterConvertToCharset)

    def test_alter_table_order_by(self):
        """测试按列排序的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name ORDER BY column_name")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterOrderBy)

    def test_alter_table_force(self):
        """测试强制重建表的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name FORCE")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterForce)

    def test_alter_table_multiple_commands(self):
        """测试包含多个命令的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name ADD COLUMN column_name_1 INT, DROP COLUMN column_name_2")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 2)
        self.assertIsInstance(node.command_list[0], ast.AlterAddColumn)
        self.assertEqual(node.command_list[0].column_name, "column_name_1")
        self.assertIsInstance(node.command_list[1], ast.AlterDropColumn)
        self.assertEqual(node.command_list[1].column_name, "column_name_2")

    def test_alter_table_add_partition(self):
        """测试添加分区的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name ADD PARTITION")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterAddPartition)

    def test_alter_table_drop_partition(self):
        """测试删除分区的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name DROP PARTITION partition_name")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterDropPartition)

    def test_alter_table_truncate_partition(self):
        """测试清空分区的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name TRUNCATE PARTITION partition_name")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterTruncatePartition)

    def test_alter_table_discard_tablespace(self):
        """测试丢弃表空间的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name DISCARD TABLESPACE")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterDiscardTablespace)

    def test_alter_table_import_tablespace(self):
        """测试导入表空间的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name IMPORT TABLESPACE")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterImportTablespace)

    def test_alter_table_with_schema_qualified_name(self):
        """测试使用模式限定名称的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE database_name.table_name ADD COLUMN column_name INT")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.schema_name, "database_name")
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterAddColumn)

    def test_alter_table_with_quoted_names(self):
        """测试使用引号名称的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE `table_name` ADD COLUMN `column_name` INT")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterAddColumn)
        self.assertEqual(node.command_list[0].column_name, "column_name")

    def test_alter_table_rename_column(self):
        """测试重命名列的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name RENAME COLUMN old_column_name TO new_column_name")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterRenameColumn)
        self.assertEqual(node.command_list[0].old_column_name, "old_column_name")
        self.assertEqual(node.command_list[0].new_column_name, "new_column_name")

    def test_alter_table_rename_key(self):
        """测试重命名键的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name RENAME KEY old_key_name TO new_key_name")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterRenameKey)
        self.assertEqual(node.command_list[0].old_key_name, "old_key_name")
        self.assertEqual(node.command_list[0].new_key_name, "new_key_name")

    def test_alter_table_with_column_position(self):
        """测试指定列位置的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name ADD COLUMN column_name INT FIRST")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterAddColumn)
        self.assertEqual(node.command_list[0].column_name, "column_name")
        self.assertIsNotNone(node.command_list[0].place)

    def test_alter_table_with_column_after(self):
        """测试指定列在某列之后的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name ADD COLUMN column_name INT AFTER existing_column")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterAddColumn)
        self.assertEqual(node.command_list[0].column_name, "column_name")
        self.assertIsNotNone(node.command_list[0].place)

    def test_alter_table_partition_by(self):
        """测试添加分区的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name PARTITION BY HASH(column_name) PARTITIONS 4")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterPartitionBy)

    def test_alter_table_remove_partitioning(self):
        """测试移除分区的 ALTER TABLE 语句"""
        node = parse_statement("ALTER TABLE table_name REMOVE PARTITIONING")
        self.assertIsInstance(node, ast.AlterTableStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertEqual(node.table_ident.object_name, "table_name")
        self.assertEqual(len(node.command_list), 1)
        self.assertIsInstance(node.command_list[0], ast.AlterRemovePartitioning) 