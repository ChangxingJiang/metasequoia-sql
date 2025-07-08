"""
ALTER USER 语句（alter_user_statement）单元测试

测试 alter_user_statement.py 中的语义组：
- alter_user_statement: ALTER USER 语句
- opt_replace_password: 可选的替换密码
"""

from unittest import TestCase

from metasequoia_sql import ast, parse_statement
from metasequoia_sql.ast.phrase.identification import IdentificationType


class TestAlterUserStatement(TestCase):
    """测试 alter_user_statement 语义组
    
    测试 ALTER USER 语句的解析，包括各种用户操作和认证方式的不同组合
    """

    def test_alter_user_standard_with_password(self):
        """测试标准 ALTER USER 语句，使用密码认证"""
        node = parse_statement("ALTER USER user_name IDENTIFIED BY 'password123'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertFalse(node.if_exists)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserIdentifiedByPassword)
        self.assertEqual(node.user_list[0].user.user_name.value, "user_name")
        self.assertIsInstance(node.user_list[0].identification, ast.IdentifiedByPassword)
        self.assertEqual(node.user_list[0].identification.password, "password123")
        self.assertFalse(node.user_list[0].retain_current_password)

    def test_alter_user_standard_with_random_password(self):
        """测试标准 ALTER USER 语句，使用随机密码认证"""
        node = parse_statement("ALTER USER user_name IDENTIFIED BY RANDOM PASSWORD")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertFalse(node.if_exists)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserIdentifiedByRandomPassword)
        self.assertEqual(node.user_list[0].user.user_name.value, "user_name")
        self.assertIsInstance(node.user_list[0].identification, ast.IdentifiedByRandomPassword)
        self.assertEqual(node.user_list[0].identification.identification_type, IdentificationType.BY_RANDOM_PASSWORD)
        self.assertFalse(node.user_list[0].retain_current_password)

    def test_alter_user_standard_with_plugin(self):
        """测试标准 ALTER USER 语句，使用插件认证"""
        node = parse_statement("ALTER USER user_name IDENTIFIED WITH mysql_native_password")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertFalse(node.if_exists)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserIdentifiedWithPlugin)
        self.assertEqual(node.user_list[0].user.user_name.value, "user_name")
        self.assertIsInstance(node.user_list[0].identification, ast.IdentifiedWithPlugin)
        self.assertEqual(node.user_list[0].identification.plugin, "mysql_native_password")

    def test_alter_user_standard_with_plugin_by_password(self):
        """测试标准 ALTER USER 语句，使用插件和密码认证"""
        node = parse_statement("ALTER USER user_name IDENTIFIED WITH mysql_native_password BY 'password123'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertFalse(node.if_exists)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserIdentifiedWithPluginByPassword)
        self.assertEqual(node.user_list[0].user.user_name.value, "user_name")
        self.assertIsInstance(node.user_list[0].identification, ast.IdentifiedWithPluginByPassword)
        self.assertEqual(node.user_list[0].identification.plugin, "mysql_native_password")
        self.assertEqual(node.user_list[0].identification.password, "password123")
        self.assertFalse(node.user_list[0].retain_current_password)

    def test_alter_user_standard_with_plugin_by_random_password(self):
        """测试标准 ALTER USER 语句，使用插件和随机密码认证"""
        node = parse_statement("ALTER USER user_name IDENTIFIED WITH mysql_native_password BY RANDOM PASSWORD")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertFalse(node.if_exists)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserIdentifiedWithPluginByRandomPassword)
        self.assertEqual(node.user_list[0].user.user_name.value, "user_name")
        self.assertIsInstance(node.user_list[0].identification, ast.IdentifiedWithPluginByRandomPassword)
        self.assertEqual(node.user_list[0].identification.plugin, "mysql_native_password")
        self.assertFalse(node.user_list[0].retain_current_password)

    def test_alter_user_standard_with_plugin_as_auth(self):
        """测试标准 ALTER USER 语句，使用插件和认证字符串"""
        node = parse_statement("ALTER USER user_name IDENTIFIED WITH mysql_native_password AS '*6BB4837EB74329105EE4568DDA7DC67ED2CA2AD9'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertFalse(node.if_exists)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserIdentifiedWithPluginAsAuth)
        self.assertEqual(node.user_list[0].user.user_name.value, "user_name")
        self.assertIsInstance(node.user_list[0].identification, ast.IdentifiedWithPluginAsAuth)
        self.assertEqual(node.user_list[0].identification.plugin, "mysql_native_password")
        self.assertEqual(node.user_list[0].identification.auth_string, "*6BB4837EB74329105EE4568DDA7DC67ED2CA2AD9")
        self.assertFalse(node.user_list[0].retain_current_password)

    def test_alter_user_standard_with_retain_current_password(self):
        """测试标准 ALTER USER 语句，保留当前密码"""
        node = parse_statement("ALTER USER user_name IDENTIFIED BY 'password123' RETAIN CURRENT PASSWORD")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertFalse(node.if_exists)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserIdentifiedByPassword)
        self.assertEqual(node.user_list[0].user.user_name.value, "user_name")
        self.assertIsInstance(node.user_list[0].identification, ast.IdentifiedByPassword)
        self.assertEqual(node.user_list[0].identification.password, "password123")
        self.assertTrue(node.user_list[0].retain_current_password)

    def test_alter_user_standard_with_replace_password(self):
        """测试标准 ALTER USER 语句，替换当前密码"""
        node = parse_statement("ALTER USER user_name IDENTIFIED BY 'newpassword' REPLACE 'oldpassword'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertFalse(node.if_exists)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserIdentifiedByPasswordReplace)
        self.assertEqual(node.user_list[0].user.user_name.value, "user_name")
        self.assertIsInstance(node.user_list[0].identification, ast.IdentifiedByPassword)
        self.assertEqual(node.user_list[0].identification.password, "newpassword")
        self.assertEqual(node.user_list[0].current_password, "oldpassword")
        self.assertFalse(node.user_list[0].retain_current_password)

    def test_alter_user_standard_with_replace_and_retain_password(self):
        """测试标准 ALTER USER 语句，替换并保留当前密码"""
        node = parse_statement("ALTER USER user_name IDENTIFIED BY 'newpassword' REPLACE 'oldpassword' RETAIN CURRENT PASSWORD")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertFalse(node.if_exists)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserIdentifiedByPasswordReplace)
        self.assertEqual(node.user_list[0].user.user_name.value, "user_name")
        self.assertIsInstance(node.user_list[0].identification, ast.IdentifiedByPassword)
        self.assertEqual(node.user_list[0].identification.password, "newpassword")
        self.assertEqual(node.user_list[0].current_password, "oldpassword")
        self.assertTrue(node.user_list[0].retain_current_password)

    def test_alter_user_standard_with_discard_old_password(self):
        """测试标准 ALTER USER 语句，丢弃旧密码"""
        node = parse_statement("ALTER USER user_name DISCARD OLD PASSWORD")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertFalse(node.if_exists)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserDiscardOldPassword)
        self.assertEqual(node.user_list[0].user.user_name.value, "user_name")
        self.assertTrue(node.user_list[0].discard_old_password)

    def test_alter_user_standard_with_add_factor(self):
        """测试标准 ALTER USER 语句，添加认证因子"""
        node = parse_statement("ALTER USER user_name ADD 2 FACTOR IDENTIFIED BY 'factor_password'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertFalse(node.if_exists)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserAddFactor)
        self.assertEqual(node.user_list[0].user.user_name.value, "user_name")
        self.assertEqual(node.user_list[0].factor, 2)
        self.assertIsInstance(node.user_list[0].identification, ast.IdentifiedByPassword)
        self.assertEqual(node.user_list[0].identification.password, "factor_password")

    def test_alter_user_standard_with_add_two_factors(self):
        """测试标准 ALTER USER 语句，添加两个认证因子"""
        node = parse_statement("ALTER USER user_name ADD 2 FACTOR IDENTIFIED BY 'factor2_password' ADD 3 FACTOR IDENTIFIED BY 'factor3_password'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertFalse(node.if_exists)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserAddTwoFactors)
        self.assertEqual(node.user_list[0].user.user_name.value, "user_name")
        self.assertEqual(node.user_list[0].first_factor, 2)
        self.assertIsInstance(node.user_list[0].first_identification, ast.IdentifiedByPassword)
        self.assertEqual(node.user_list[0].first_identification.password, "factor2_password")
        self.assertEqual(node.user_list[0].second_factor, 3)
        self.assertIsInstance(node.user_list[0].second_identification, ast.IdentifiedByPassword)
        self.assertEqual(node.user_list[0].second_identification.password, "factor3_password")

    def test_alter_user_standard_with_modify_factor(self):
        """测试标准 ALTER USER 语句，修改认证因子"""
        node = parse_statement("ALTER USER user_name MODIFY 2 FACTOR IDENTIFIED BY 'new_factor_password'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertFalse(node.if_exists)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserModifyFactor)
        self.assertEqual(node.user_list[0].user.user_name.value, "user_name")
        self.assertEqual(node.user_list[0].factor, 2)
        self.assertIsInstance(node.user_list[0].identification, ast.IdentifiedByPassword)
        self.assertEqual(node.user_list[0].identification.password, "new_factor_password")

    def test_alter_user_standard_with_drop_factor(self):
        """测试标准 ALTER USER 语句，删除认证因子"""
        node = parse_statement("ALTER USER user_name DROP 2 FACTOR")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertFalse(node.if_exists)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserDropFactor)
        self.assertEqual(node.user_list[0].user.user_name.value, "user_name")
        self.assertEqual(node.user_list[0].factor, 2)

    def test_alter_user_standard_with_drop_two_factors(self):
        """测试标准 ALTER USER 语句，删除两个认证因子"""
        node = parse_statement("ALTER USER user_name DROP 2 FACTOR DROP 3 FACTOR")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertFalse(node.if_exists)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserDropTwoFactors)
        self.assertEqual(node.user_list[0].user.user_name.value, "user_name")
        self.assertEqual(node.user_list[0].first_factor, 2)
        self.assertEqual(node.user_list[0].second_factor, 3)

    def test_alter_user_standard_with_multiple_users(self):
        """测试标准 ALTER USER 语句，多个用户"""
        node = parse_statement("ALTER USER user1 IDENTIFIED BY 'password1', user2 IDENTIFIED BY 'password2'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertFalse(node.if_exists)
        self.assertEqual(len(node.user_list), 2)
        
        # 验证第一个用户
        self.assertIsInstance(node.user_list[0], ast.AlterUserIdentifiedByPassword)
        self.assertEqual(node.user_list[0].user.user_name.value, "user1")
        self.assertEqual(node.user_list[0].identification.password, "password1")
        
        # 验证第二个用户
        self.assertIsInstance(node.user_list[1], ast.AlterUserIdentifiedByPassword)
        self.assertEqual(node.user_list[1].user.user_name.value, "user2")
        self.assertEqual(node.user_list[1].identification.password, "password2")

    def test_alter_user_standard_with_if_exists(self):
        """测试标准 ALTER USER 语句，包含 IF EXISTS"""
        node = parse_statement("ALTER USER IF EXISTS user_name IDENTIFIED BY 'password123'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertTrue(node.if_exists)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserIdentifiedByPassword)
        self.assertEqual(node.user_list[0].user.user_name.value, "user_name")

    def test_alter_user_current_user_random_password(self):
        """测试当前用户随机密码 ALTER USER 语句"""
        node = parse_statement("ALTER USER USER() IDENTIFIED BY RANDOM PASSWORD")
        self.assertIsInstance(node, ast.AlterUserCurrentUserRandomPasswordStatement)
        self.assertFalse(node.if_exists)
        self.assertIsInstance(node.identification, ast.IdentifiedByRandomPassword)
        self.assertIsNone(node.replace_password)
        self.assertFalse(node.retain_current_password)

    def test_alter_user_current_user_random_password_with_replace(self):
        """测试当前用户随机密码 ALTER USER 语句，替换当前密码"""
        node = parse_statement("ALTER USER USER() IDENTIFIED BY RANDOM PASSWORD REPLACE 'currentpassword'")
        self.assertIsInstance(node, ast.AlterUserCurrentUserRandomPasswordStatement)
        self.assertFalse(node.if_exists)
        self.assertIsInstance(node.identification, ast.IdentifiedByRandomPassword)
        self.assertEqual(node.replace_password, "currentpassword")
        self.assertFalse(node.retain_current_password)

    def test_alter_user_current_user_random_password_with_retain(self):
        """测试当前用户随机密码 ALTER USER 语句，保留当前密码"""
        node = parse_statement("ALTER USER USER() IDENTIFIED BY RANDOM PASSWORD RETAIN CURRENT PASSWORD")
        self.assertIsInstance(node, ast.AlterUserCurrentUserRandomPasswordStatement)
        self.assertFalse(node.if_exists)
        self.assertIsInstance(node.identification, ast.IdentifiedByRandomPassword)
        self.assertIsNone(node.replace_password)
        self.assertTrue(node.retain_current_password)

    def test_alter_user_current_user_password(self):
        """测试当前用户密码 ALTER USER 语句"""
        node = parse_statement("ALTER USER USER() IDENTIFIED BY 'newpassword'")
        self.assertIsInstance(node, ast.AlterUserCurrentUserPasswordStatement)
        self.assertFalse(node.if_exists)
        self.assertIsInstance(node.identification, ast.IdentifiedByPassword)
        self.assertEqual(node.identification.password, "newpassword")
        self.assertIsNone(node.replace_password)
        self.assertFalse(node.retain_current_password)

    def test_alter_user_current_user_password_with_replace(self):
        """测试当前用户密码 ALTER USER 语句，替换当前密码"""
        node = parse_statement("ALTER USER USER() IDENTIFIED BY 'newpassword' REPLACE 'oldpassword'")
        self.assertIsInstance(node, ast.AlterUserCurrentUserPasswordStatement)
        self.assertFalse(node.if_exists)
        self.assertIsInstance(node.identification, ast.IdentifiedByPassword)
        self.assertEqual(node.identification.password, "newpassword")
        self.assertEqual(node.replace_password, "oldpassword")
        self.assertFalse(node.retain_current_password)

    def test_alter_user_current_user_password_with_retain(self):
        """测试当前用户密码 ALTER USER 语句，保留当前密码"""
        node = parse_statement("ALTER USER USER() IDENTIFIED BY 'newpassword' RETAIN CURRENT PASSWORD")
        self.assertIsInstance(node, ast.AlterUserCurrentUserPasswordStatement)
        self.assertFalse(node.if_exists)
        self.assertIsInstance(node.identification, ast.IdentifiedByPassword)
        self.assertEqual(node.identification.password, "newpassword")
        self.assertIsNone(node.replace_password)
        self.assertTrue(node.retain_current_password)

    def test_alter_user_current_user_discard_password(self):
        """测试当前用户丢弃密码 ALTER USER 语句"""
        node = parse_statement("ALTER USER USER() DISCARD OLD PASSWORD")
        self.assertIsInstance(node, ast.AlterUserCurrentUserDiscardPasswordStatement)
        self.assertFalse(node.if_exists)

    def test_alter_user_current_user_discard_password_with_if_exists(self):
        """测试当前用户丢弃密码 ALTER USER 语句，包含 IF EXISTS"""
        node = parse_statement("ALTER USER IF EXISTS USER() DISCARD OLD PASSWORD")
        self.assertIsInstance(node, ast.AlterUserCurrentUserDiscardPasswordStatement)
        self.assertTrue(node.if_exists)

    def test_alter_user_default_role_all(self):
        """测试设置用户默认角色为全部"""
        node = parse_statement("ALTER USER user_name DEFAULT ROLE ALL")
        self.assertIsInstance(node, ast.AlterUserDefaultRoleAllStatement)
        self.assertFalse(node.if_exists)
        self.assertEqual(node.user.user_name.value, "user_name")

    def test_alter_user_default_role_all_with_if_exists(self):
        """测试设置用户默认角色为全部，包含 IF EXISTS"""
        node = parse_statement("ALTER USER IF EXISTS user_name DEFAULT ROLE ALL")
        self.assertIsInstance(node, ast.AlterUserDefaultRoleAllStatement)
        self.assertTrue(node.if_exists)
        self.assertEqual(node.user.user_name.value, "user_name")

    def test_alter_user_default_role_none(self):
        """测试设置用户默认角色为无"""
        node = parse_statement("ALTER USER user_name DEFAULT ROLE NONE")
        self.assertIsInstance(node, ast.AlterUserDefaultRoleNoneStatement)
        self.assertFalse(node.if_exists)
        self.assertEqual(node.user.user_name.value, "user_name")

    def test_alter_user_default_role_none_with_if_exists(self):
        """测试设置用户默认角色为无，包含 IF EXISTS"""
        node = parse_statement("ALTER USER IF EXISTS user_name DEFAULT ROLE NONE")
        self.assertIsInstance(node, ast.AlterUserDefaultRoleNoneStatement)
        self.assertTrue(node.if_exists)
        self.assertEqual(node.user.user_name.value, "user_name")

    def test_alter_user_default_role_list(self):
        """测试设置用户默认角色列表"""
        node = parse_statement("ALTER USER user_name DEFAULT ROLE role1, role2, role3")
        self.assertIsInstance(node, ast.AlterUserDefaultRoleListStatement)
        self.assertFalse(node.if_exists)
        self.assertEqual(node.user.user_name.value, "user_name")
        self.assertEqual(len(node.role_list), 3)
        self.assertEqual(node.role_list[0].role_name, "role1")
        self.assertEqual(node.role_list[1].role_name, "role2")
        self.assertEqual(node.role_list[2].role_name, "role3")

    def test_alter_user_default_role_list_with_if_exists(self):
        """测试设置用户默认角色列表，包含 IF EXISTS"""
        node = parse_statement("ALTER USER IF EXISTS user_name DEFAULT ROLE role1, role2")
        self.assertIsInstance(node, ast.AlterUserDefaultRoleListStatement)
        self.assertTrue(node.if_exists)
        self.assertEqual(node.user.user_name.value, "user_name")
        self.assertEqual(len(node.role_list), 2)
        self.assertEqual(node.role_list[0].role_name, "role1")
        self.assertEqual(node.role_list[1].role_name, "role2")

    def test_alter_user_with_quoted_user_name(self):
        """测试使用引号的用户名"""
        node = parse_statement("ALTER USER 'user_name'@'localhost' IDENTIFIED BY 'password123'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserIdentifiedByPassword)
        self.assertEqual(node.user_list[0].user.user_name.value, "user_name")
        self.assertEqual(node.user_list[0].user.user_host, "localhost")

    def test_alter_user_with_backtick_user_name(self):
        """测试使用反引号的用户名"""
        node = parse_statement("ALTER USER `user_name`@`localhost` IDENTIFIED BY 'password123'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserIdentifiedByPassword)
        self.assertEqual(node.user_list[0].user.user_name.value, "user_name")

    def test_alter_user_with_complex_plugin_name(self):
        """测试复杂的插件名称"""
        node = parse_statement("ALTER USER user_name IDENTIFIED WITH 'authentication_ldap_sasl'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserIdentifiedWithPlugin)
        self.assertEqual(node.user_list[0].identification.plugin, "authentication_ldap_sasl")

    def test_alter_user_with_hex_auth_string(self):
        """测试使用十六进制认证字符串"""
        node = parse_statement("ALTER USER user_name IDENTIFIED WITH mysql_native_password AS 0x6BB4837EB74329105EE4568DDA7DC67ED2CA2AD9")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserIdentifiedWithPluginAsAuth)
        self.assertEqual(node.user_list[0].identification.plugin, "mysql_native_password")
        self.assertIsNotNone(node.user_list[0].identification.auth_string)

    def test_alter_user_case_insensitive_keywords(self):
        """测试关键字大小写不敏感"""
        node = parse_statement("alter user user_name identified by 'password123' retain current password")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserIdentifiedByPassword)
        self.assertEqual(node.user_list[0].user.user_name.value, "user_name")
        self.assertTrue(node.user_list[0].retain_current_password)

    def test_alter_user_with_whitespace_handling(self):
        """测试空白字符处理"""
        node = parse_statement("ALTER   USER   user_name   IDENTIFIED   BY   'password123'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserIdentifiedByPassword)
        self.assertEqual(node.user_list[0].user.user_name.value, "user_name")
        self.assertEqual(node.user_list[0].identification.password, "password123")

    def test_alter_user_identification_types(self):
        """测试各种认证类型的枚举值"""
        # 测试密码认证
        node = parse_statement("ALTER USER user_name IDENTIFIED BY 'password123'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertEqual(node.user_list[0].identification.identification_type, IdentificationType.BY_PASSWORD)
        
        # 测试随机密码认证
        node = parse_statement("ALTER USER user_name IDENTIFIED BY RANDOM PASSWORD")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertEqual(node.user_list[0].identification.identification_type, IdentificationType.BY_RANDOM_PASSWORD)
        
        # 测试插件认证
        node = parse_statement("ALTER USER user_name IDENTIFIED WITH mysql_native_password")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertEqual(node.user_list[0].identification.identification_type, IdentificationType.WITH_PLUGIN)
        
        # 测试插件和认证字符串
        node = parse_statement("ALTER USER user_name IDENTIFIED WITH mysql_native_password AS 'auth_string'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertEqual(node.user_list[0].identification.identification_type, IdentificationType.WITH_PLUGIN_AS_AUTH)
        
        # 测试插件和密码认证
        node = parse_statement("ALTER USER user_name IDENTIFIED WITH mysql_native_password BY 'password123'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertEqual(node.user_list[0].identification.identification_type, IdentificationType.WITH_PLUGIN_BY_PASSWORD)
        
        # 测试插件和随机密码认证
        node = parse_statement("ALTER USER user_name IDENTIFIED WITH mysql_native_password BY RANDOM PASSWORD")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertEqual(node.user_list[0].identification.identification_type, IdentificationType.WITH_PLUGIN_BY_RANDOM_PASSWORD)

    def test_alter_user_factor_numbers(self):
        """测试认证因子编号"""
        # 测试因子 2
        node = parse_statement("ALTER USER user_name ADD 2 FACTOR IDENTIFIED BY 'factor2_password'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertEqual(node.user_list[0].factor, 2)
        
        # 测试因子 3
        node = parse_statement("ALTER USER user_name ADD 3 FACTOR IDENTIFIED BY 'factor3_password'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertEqual(node.user_list[0].factor, 3)
        
        # 测试删除因子 2
        node = parse_statement("ALTER USER user_name DROP 2 FACTOR")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertEqual(node.user_list[0].factor, 2)
        
        # 测试删除因子 3
        node = parse_statement("ALTER USER user_name DROP 3 FACTOR")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertEqual(node.user_list[0].factor, 3)

    def test_alter_user_complex_scenarios(self):
        """测试复杂场景组合"""
        # 测试多用户、多种认证方式的组合
        node = parse_statement("""
            ALTER USER IF EXISTS 
                user1 IDENTIFIED BY 'password1' RETAIN CURRENT PASSWORD,
                user2 IDENTIFIED BY RANDOM PASSWORD,
                user3 IDENTIFIED WITH mysql_native_password BY 'password3',
                user4 DISCARD OLD PASSWORD
        """)
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        self.assertTrue(node.if_exists)
        self.assertEqual(len(node.user_list), 4)
        
        # 验证第一个用户：密码认证 + 保留当前密码
        self.assertIsInstance(node.user_list[0], ast.AlterUserIdentifiedByPassword)
        self.assertEqual(node.user_list[0].user.user_name.value, "user1")
        self.assertTrue(node.user_list[0].retain_current_password)
        
        # 验证第二个用户：随机密码认证
        self.assertIsInstance(node.user_list[1], ast.AlterUserIdentifiedByRandomPassword)
        self.assertEqual(node.user_list[1].user.user_name.value, "user2")
        
        # 验证第三个用户：插件和密码认证
        self.assertIsInstance(node.user_list[2], ast.AlterUserIdentifiedWithPluginByPassword)
        self.assertEqual(node.user_list[2].user.user_name.value, "user3")
        
        # 验证第四个用户：丢弃旧密码
        self.assertIsInstance(node.user_list[3], ast.AlterUserDiscardOldPassword)
        self.assertEqual(node.user_list[3].user.user_name.value, "user4")

    def test_alter_user_attribute_access(self):
        """测试 ALTER USER 语句的属性访问"""
        node = parse_statement("ALTER USER user_name IDENTIFIED BY 'password123'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        
        # 测试基类属性
        self.assertFalse(node.if_exists)
        
        # 测试用户列表属性
        self.assertEqual(len(node.user_list), 1)
        self.assertIsInstance(node.user_list[0], ast.AlterUserIdentifiedByPassword)
        
        # 测试用户认证信息
        alter_user = node.user_list[0]
        self.assertEqual(alter_user.user.user_name.value, "user_name")
        self.assertIsInstance(alter_user.identification, ast.IdentifiedByPassword)
        self.assertEqual(alter_user.identification.password, "password123")
        self.assertEqual(alter_user.identification.identification_type, IdentificationType.BY_PASSWORD)
        self.assertFalse(alter_user.retain_current_password)

    def test_alter_user_require_clause_empty(self):
        """测试 REQUIRE 子句为空的情况"""
        node = parse_statement("ALTER USER user_name IDENTIFIED BY 'password123'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        # REQUIRE 子句应该为 None 或空
        self.assertIsNone(node.require_clause)

    def test_alter_user_connect_options_empty(self):
        """测试连接选项为空的情况"""
        node = parse_statement("ALTER USER user_name IDENTIFIED BY 'password123'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        # 连接选项列表应该为空
        self.assertEqual(len(node.connect_options), 0)

    def test_alter_user_account_lock_expire_options_empty(self):
        """测试账户锁定和密码过期选项为空的情况"""
        node = parse_statement("ALTER USER user_name IDENTIFIED BY 'password123'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        # 账户锁定和密码过期选项列表应该为空
        self.assertEqual(len(node.account_lock_expire_options), 0)

    def test_alter_user_user_attribute_empty(self):
        """测试用户属性为空的情况"""
        node = parse_statement("ALTER USER user_name IDENTIFIED BY 'password123'")
        self.assertIsInstance(node, ast.AlterUserStandardStatement)
        # 用户属性应该为 None
        self.assertIsNone(node.user_attribute) 