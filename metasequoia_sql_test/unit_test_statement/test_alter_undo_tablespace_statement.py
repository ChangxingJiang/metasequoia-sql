"""
ALTER UNDO TABLESPACE 语句单元测试

测试语义组：alter_undo_tablespace_statement 及其相关语义组
"""

import unittest

from metasequoia_sql import parse_statement
from metasequoia_sql.ast.statement.alter_undo_tablespace_statement import AlterUndoTablespaceStatement
from metasequoia_sql.ast.basic.fixed_enum import EnumUndoTablespaceState
from metasequoia_sql.ast.phrase.ddl_option import DdlOptionStorageEngine


class TestAlterUndoTablespaceStatement(unittest.TestCase):
    """测试 ALTER UNDO TABLESPACE 语句解析"""

    def test_alter_undo_tablespace_set_active(self):
        """测试 ALTER UNDO TABLESPACE SET ACTIVE 语句"""
        sql = "ALTER UNDO TABLESPACE undo_tablespace_name SET ACTIVE"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterUndoTablespaceStatement)
        self.assertEqual(node.tablespace_name, "undo_tablespace_name")
        self.assertEqual(node.state, EnumUndoTablespaceState.ACTIVE)
        self.assertEqual(len(node.option_list), 0)

    def test_alter_undo_tablespace_set_inactive(self):
        """测试 ALTER UNDO TABLESPACE SET INACTIVE 语句"""
        sql = "ALTER UNDO TABLESPACE undo_tablespace_name SET INACTIVE"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterUndoTablespaceStatement)
        self.assertEqual(node.tablespace_name, "undo_tablespace_name")
        self.assertEqual(node.state, EnumUndoTablespaceState.INACTIVE)
        self.assertEqual(len(node.option_list), 0)

    def test_alter_undo_tablespace_set_active_with_engine(self):
        """测试 ALTER UNDO TABLESPACE SET ACTIVE 带 ENGINE 选项"""
        sql = "ALTER UNDO TABLESPACE undo_tablespace_name SET ACTIVE ENGINE = 'InnoDB'"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterUndoTablespaceStatement)
        self.assertEqual(node.tablespace_name, "undo_tablespace_name")
        self.assertEqual(node.state, EnumUndoTablespaceState.ACTIVE)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionStorageEngine)
        self.assertEqual(node.option_list[0].value, "InnoDB")

    def test_alter_undo_tablespace_set_inactive_with_engine(self):
        """测试 ALTER UNDO TABLESPACE SET INACTIVE 带 ENGINE 选项"""
        sql = "ALTER UNDO TABLESPACE undo_tablespace_name SET INACTIVE ENGINE = 'InnoDB'"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterUndoTablespaceStatement)
        self.assertEqual(node.tablespace_name, "undo_tablespace_name")
        self.assertEqual(node.state, EnumUndoTablespaceState.INACTIVE)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionStorageEngine)
        self.assertEqual(node.option_list[0].value, "InnoDB")

    def test_alter_undo_tablespace_with_quoted_tablespace_name(self):
        """测试 ALTER UNDO TABLESPACE 带引号的表空间名称"""
        sql = "ALTER UNDO TABLESPACE `undo_tablespace_name` SET ACTIVE"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterUndoTablespaceStatement)
        self.assertEqual(node.tablespace_name, "undo_tablespace_name")
        self.assertEqual(node.state, EnumUndoTablespaceState.ACTIVE)
        self.assertEqual(len(node.option_list), 0)

    def test_alter_undo_tablespace_with_engine_without_equal(self):
        """测试 ALTER UNDO TABLESPACE 带 ENGINE 选项（不使用等号）"""
        sql = "ALTER UNDO TABLESPACE undo_tablespace_name SET ACTIVE ENGINE 'InnoDB'"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterUndoTablespaceStatement)
        self.assertEqual(node.tablespace_name, "undo_tablespace_name")
        self.assertEqual(node.state, EnumUndoTablespaceState.ACTIVE)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionStorageEngine)
        self.assertEqual(node.option_list[0].value, "InnoDB")

    def test_alter_undo_tablespace_with_different_engine_types(self):
        """测试 ALTER UNDO TABLESPACE 带不同存储引擎类型"""
        # 测试 InnoDB 引擎
        sql = "ALTER UNDO TABLESPACE undo_tablespace_name SET ACTIVE ENGINE = 'InnoDB'"
        node = parse_statement(sql)
        self.assertIsInstance(node, AlterUndoTablespaceStatement)
        self.assertEqual(node.state, EnumUndoTablespaceState.ACTIVE)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionStorageEngine)
        self.assertEqual(node.option_list[0].value, "InnoDB")

        # 测试 MyISAM 引擎
        sql = "ALTER UNDO TABLESPACE undo_tablespace_name SET INACTIVE ENGINE = 'MyISAM'"
        node = parse_statement(sql)
        self.assertIsInstance(node, AlterUndoTablespaceStatement)
        self.assertEqual(node.state, EnumUndoTablespaceState.INACTIVE)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionStorageEngine)
        self.assertEqual(node.option_list[0].value, "MyISAM")

    def test_alter_undo_tablespace_with_double_quoted_engine(self):
        """测试 ALTER UNDO TABLESPACE 带双引号的存储引擎"""
        sql = 'ALTER UNDO TABLESPACE undo_tablespace_name SET ACTIVE ENGINE = "InnoDB"'
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterUndoTablespaceStatement)
        self.assertEqual(node.tablespace_name, "undo_tablespace_name")
        self.assertEqual(node.state, EnumUndoTablespaceState.ACTIVE)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionStorageEngine)
        self.assertEqual(node.option_list[0].value, "InnoDB")

    def test_alter_undo_tablespace_with_complex_tablespace_name(self):
        """测试 ALTER UNDO TABLESPACE 带复杂表空间名称"""
        sql = "ALTER UNDO TABLESPACE `my_undo_tablespace_123` SET INACTIVE"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterUndoTablespaceStatement)
        self.assertEqual(node.tablespace_name, "my_undo_tablespace_123")
        self.assertEqual(node.state, EnumUndoTablespaceState.INACTIVE)
        self.assertEqual(len(node.option_list), 0)

    def test_alter_undo_tablespace_case_insensitive_keywords(self):
        """测试 ALTER UNDO TABLESPACE 关键字大小写不敏感"""
        sql = "alter undo tablespace undo_tablespace_name set active"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterUndoTablespaceStatement)
        self.assertEqual(node.tablespace_name, "undo_tablespace_name")
        self.assertEqual(node.state, EnumUndoTablespaceState.ACTIVE)
        self.assertEqual(len(node.option_list), 0)

    def test_alter_undo_tablespace_mixed_case_keywords(self):
        """测试 ALTER UNDO TABLESPACE 混合大小写关键字"""
        sql = "ALTER undo TABLESPACE undo_tablespace_name SET inactive"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterUndoTablespaceStatement)
        self.assertEqual(node.tablespace_name, "undo_tablespace_name")
        self.assertEqual(node.state, EnumUndoTablespaceState.INACTIVE)
        self.assertEqual(len(node.option_list), 0)

    def test_alter_undo_tablespace_with_engine_mixed_case(self):
        """测试 ALTER UNDO TABLESPACE 带混合大小写的 ENGINE 选项"""
        sql = "ALTER UNDO TABLESPACE undo_tablespace_name SET ACTIVE engine = 'innodb'"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterUndoTablespaceStatement)
        self.assertEqual(node.tablespace_name, "undo_tablespace_name")
        self.assertEqual(node.state, EnumUndoTablespaceState.ACTIVE)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionStorageEngine)
        self.assertEqual(node.option_list[0].value, "innodb")

    def test_alter_undo_tablespace_with_whitespace(self):
        """测试 ALTER UNDO TABLESPACE 带额外空白字符"""
        sql = """
        ALTER    UNDO    TABLESPACE    undo_tablespace_name    
        SET    ACTIVE    
        ENGINE    =    'InnoDB'
        """
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterUndoTablespaceStatement)
        self.assertEqual(node.tablespace_name, "undo_tablespace_name")
        self.assertEqual(node.state, EnumUndoTablespaceState.ACTIVE)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionStorageEngine)
        self.assertEqual(node.option_list[0].value, "InnoDB")

    def test_alter_undo_tablespace_enum_state_values(self):
        """测试 ALTER UNDO TABLESPACE 状态枚举值"""
        # 测试 ACTIVE 状态
        sql = "ALTER UNDO TABLESPACE undo_tablespace_name SET ACTIVE"
        node = parse_statement(sql)
        self.assertEqual(node.state, EnumUndoTablespaceState.ACTIVE)
        self.assertEqual(node.state.value, 1)

        # 测试 INACTIVE 状态
        sql = "ALTER UNDO TABLESPACE undo_tablespace_name SET INACTIVE"
        node = parse_statement(sql)
        self.assertEqual(node.state, EnumUndoTablespaceState.INACTIVE)
        self.assertEqual(node.state.value, 2)

    def test_alter_undo_tablespace_option_list_empty(self):
        """测试 ALTER UNDO TABLESPACE 选项列表为空的情况"""
        sql = "ALTER UNDO TABLESPACE undo_tablespace_name SET ACTIVE"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterUndoTablespaceStatement)
        self.assertEqual(node.tablespace_name, "undo_tablespace_name")
        self.assertEqual(node.state, EnumUndoTablespaceState.ACTIVE)
        self.assertIsInstance(node.option_list, list)
        self.assertEqual(len(node.option_list), 0)

    def test_alter_undo_tablespace_option_list_with_engine(self):
        """测试 ALTER UNDO TABLESPACE 选项列表包含 ENGINE 的情况"""
        sql = "ALTER UNDO TABLESPACE undo_tablespace_name SET INACTIVE ENGINE = 'InnoDB'"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterUndoTablespaceStatement)
        self.assertEqual(node.tablespace_name, "undo_tablespace_name")
        self.assertEqual(node.state, EnumUndoTablespaceState.INACTIVE)
        self.assertIsInstance(node.option_list, list)
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], DdlOptionStorageEngine)

    def test_alter_undo_tablespace_property_access(self):
        """测试 ALTER UNDO TABLESPACE 属性访问"""
        sql = "ALTER UNDO TABLESPACE test_undo_tablespace SET ACTIVE ENGINE = 'InnoDB'"
        node = parse_statement(sql)
        
        # 测试所有属性访问
        self.assertEqual(node.tablespace_name, "test_undo_tablespace")
        self.assertEqual(node.state, EnumUndoTablespaceState.ACTIVE)
        self.assertIsInstance(node.option_list, list)
        self.assertEqual(len(node.option_list), 1)
        
        # 测试选项属性
        engine_option = node.option_list[0]
        self.assertIsInstance(engine_option, DdlOptionStorageEngine)
        self.assertEqual(engine_option.value, "InnoDB")

    def test_alter_undo_tablespace_minimal_case(self):
        """测试 ALTER UNDO TABLESPACE 最小化用例"""
        sql = "ALTER UNDO TABLESPACE t SET ACTIVE"
        node = parse_statement(sql)
        
        self.assertIsInstance(node, AlterUndoTablespaceStatement)
        self.assertEqual(node.tablespace_name, "t")
        self.assertEqual(node.state, EnumUndoTablespaceState.ACTIVE)
        self.assertEqual(len(node.option_list), 0)


if __name__ == "__main__":
    unittest.main() 