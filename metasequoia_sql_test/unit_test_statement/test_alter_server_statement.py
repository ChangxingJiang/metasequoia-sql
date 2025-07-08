"""
ALTER SERVER 语句（alter_server_statement）单元测试

测试 alter_server_statement.py 中的语义组：
- alter_server_statement: ALTER SERVER 语句
"""

from unittest import TestCase

from metasequoia_sql import ast, parse_statement


class TestAlterServerStatement(TestCase):
    """测试 alter_server_statement 语义组
    
    测试 ALTER SERVER 语句的解析，包括服务器名称和各种服务器选项的组合
    """

    def test_alter_server_with_single_user_option(self):
        """测试包含单个 USER 选项的 ALTER SERVER 语句"""
        node = parse_statement("ALTER SERVER server_name OPTIONS (USER 'username')")
        self.assertIsInstance(node, ast.AlterServerStatement)
        self.assertEqual(node.server_name, "server_name")
        self.assertEqual(len(node.server_options), 1)
        self.assertIsInstance(node.server_options[0], ast.ServerUserOption)
        self.assertEqual(node.server_options[0].username, "username")

    def test_alter_server_with_single_host_option(self):
        """测试包含单个 HOST 选项的 ALTER SERVER 语句"""
        node = parse_statement("ALTER SERVER server_name OPTIONS (HOST 'localhost')")
        self.assertIsInstance(node, ast.AlterServerStatement)
        self.assertEqual(node.server_name, "server_name")
        self.assertEqual(len(node.server_options), 1)
        self.assertIsInstance(node.server_options[0], ast.ServerHostOption)
        self.assertEqual(node.server_options[0].host, "localhost")

    def test_alter_server_with_single_database_option(self):
        """测试包含单个 DATABASE 选项的 ALTER SERVER 语句"""
        node = parse_statement("ALTER SERVER server_name OPTIONS (DATABASE 'database_name')")
        self.assertIsInstance(node, ast.AlterServerStatement)
        self.assertEqual(node.server_name, "server_name")
        self.assertEqual(len(node.server_options), 1)
        self.assertIsInstance(node.server_options[0], ast.ServerDatabaseOption)
        self.assertEqual(node.server_options[0].database, "database_name")

    def test_alter_server_with_single_owner_option(self):
        """测试包含单个 OWNER 选项的 ALTER SERVER 语句"""
        node = parse_statement("ALTER SERVER server_name OPTIONS (OWNER 'owner_name')")
        self.assertIsInstance(node, ast.AlterServerStatement)
        self.assertEqual(node.server_name, "server_name")
        self.assertEqual(len(node.server_options), 1)
        self.assertIsInstance(node.server_options[0], ast.ServerOwnerOption)
        self.assertEqual(node.server_options[0].owner, "owner_name")

    def test_alter_server_with_single_password_option(self):
        """测试包含单个 PASSWORD 选项的 ALTER SERVER 语句"""
        node = parse_statement("ALTER SERVER server_name OPTIONS (PASSWORD 'password123')")
        self.assertIsInstance(node, ast.AlterServerStatement)
        self.assertEqual(node.server_name, "server_name")
        self.assertEqual(len(node.server_options), 1)
        self.assertIsInstance(node.server_options[0], ast.ServerPasswordOption)
        self.assertEqual(node.server_options[0].password, "password123")

    def test_alter_server_with_single_socket_option(self):
        """测试包含单个 SOCKET 选项的 ALTER SERVER 语句"""
        node = parse_statement("ALTER SERVER server_name OPTIONS (SOCKET '/tmp/mysql.sock')")
        self.assertIsInstance(node, ast.AlterServerStatement)
        self.assertEqual(node.server_name, "server_name")
        self.assertEqual(len(node.server_options), 1)
        self.assertIsInstance(node.server_options[0], ast.ServerSocketOption)
        self.assertEqual(node.server_options[0].socket, "/tmp/mysql.sock")

    def test_alter_server_with_single_port_option(self):
        """测试包含单个 PORT 选项的 ALTER SERVER 语句"""
        node = parse_statement("ALTER SERVER server_name OPTIONS (PORT 3306)")
        self.assertIsInstance(node, ast.AlterServerStatement)
        self.assertEqual(node.server_name, "server_name")
        self.assertEqual(len(node.server_options), 1)
        self.assertIsInstance(node.server_options[0], ast.ServerPortOption)
        self.assertEqual(node.server_options[0].port, 3306)

    def test_alter_server_with_multiple_options(self):
        """测试包含多个选项的 ALTER SERVER 语句"""
        node = parse_statement("ALTER SERVER server_name OPTIONS (USER 'username', HOST 'localhost', DATABASE 'database_name')")
        self.assertIsInstance(node, ast.AlterServerStatement)
        self.assertEqual(node.server_name, "server_name")
        self.assertEqual(len(node.server_options), 3)
        
        # 验证第一个选项
        self.assertIsInstance(node.server_options[0], ast.ServerUserOption)
        self.assertEqual(node.server_options[0].username, "username")
        
        # 验证第二个选项
        self.assertIsInstance(node.server_options[1], ast.ServerHostOption)
        self.assertEqual(node.server_options[1].host, "localhost")
        
        # 验证第三个选项
        self.assertIsInstance(node.server_options[2], ast.ServerDatabaseOption)
        self.assertEqual(node.server_options[2].database, "database_name")

    def test_alter_server_with_all_options(self):
        """测试包含所有选项的 ALTER SERVER 语句"""
        node = parse_statement("ALTER SERVER server_name OPTIONS (USER 'username', HOST 'localhost', DATABASE 'database_name', OWNER 'owner_name', PASSWORD 'password123', SOCKET '/tmp/mysql.sock', PORT 3306)")
        self.assertIsInstance(node, ast.AlterServerStatement)
        self.assertEqual(node.server_name, "server_name")
        self.assertEqual(len(node.server_options), 7)
        
        # 验证所有选项类型
        self.assertIsInstance(node.server_options[0], ast.ServerUserOption)
        self.assertEqual(node.server_options[0].username, "username")
        
        self.assertIsInstance(node.server_options[1], ast.ServerHostOption)
        self.assertEqual(node.server_options[1].host, "localhost")
        
        self.assertIsInstance(node.server_options[2], ast.ServerDatabaseOption)
        self.assertEqual(node.server_options[2].database, "database_name")
        
        self.assertIsInstance(node.server_options[3], ast.ServerOwnerOption)
        self.assertEqual(node.server_options[3].owner, "owner_name")
        
        self.assertIsInstance(node.server_options[4], ast.ServerPasswordOption)
        self.assertEqual(node.server_options[4].password, "password123")
        
        self.assertIsInstance(node.server_options[5], ast.ServerSocketOption)
        self.assertEqual(node.server_options[5].socket, "/tmp/mysql.sock")
        
        self.assertIsInstance(node.server_options[6], ast.ServerPortOption)
        self.assertEqual(node.server_options[6].port, 3306)

    def test_alter_server_with_quoted_server_name(self):
        """测试使用引号的服务器名称"""
        node = parse_statement("ALTER SERVER `server_name` OPTIONS (USER 'username')")
        self.assertIsInstance(node, ast.AlterServerStatement)
        self.assertEqual(node.server_name, "server_name")
        self.assertEqual(len(node.server_options), 1)
        self.assertIsInstance(node.server_options[0], ast.ServerUserOption)
        self.assertEqual(node.server_options[0].username, "username")

    def test_alter_server_with_hex_port(self):
        """测试使用十六进制端口号"""
        node = parse_statement("ALTER SERVER server_name OPTIONS (PORT 0x0CEA)")
        self.assertIsInstance(node, ast.AlterServerStatement)
        self.assertEqual(node.server_name, "server_name")
        self.assertEqual(len(node.server_options), 1)
        self.assertIsInstance(node.server_options[0], ast.ServerPortOption)
        self.assertEqual(node.server_options[0].port, 3306)  # 0x0CEA = 3306

    def test_alter_server_with_special_characters_in_options(self):
        """测试选项值中包含特殊字符"""
        node = parse_statement("ALTER SERVER server_name OPTIONS (PASSWORD 'p@ssw0rd!@#', SOCKET '/var/lib/mysql/mysql.sock')")
        self.assertIsInstance(node, ast.AlterServerStatement)
        self.assertEqual(node.server_name, "server_name")
        self.assertEqual(len(node.server_options), 2)
        
        self.assertIsInstance(node.server_options[0], ast.ServerPasswordOption)
        self.assertEqual(node.server_options[0].password, "p@ssw0rd!@#")
        
        self.assertIsInstance(node.server_options[1], ast.ServerSocketOption)
        self.assertEqual(node.server_options[1].socket, "/var/lib/mysql/mysql.sock") 