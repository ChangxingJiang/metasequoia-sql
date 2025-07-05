"""
ALTER FUNCTION 语句（alter_function_statement）单元测试

测试 alter_function_statement.py 中的语义组：
- alter_function_statement: ALTER FUNCTION 语句
"""

from unittest import TestCase

from metasequoia_sql import ast, parse_statement


class TestAlterFunctionStatement(TestCase):
    """测试 alter_function_statement 语义组
    
    测试 ALTER FUNCTION 语句的解析，包括函数名称和各种选项的不同组合
    """

    def test_alter_function_with_comment(self):
        """测试带有注释的 ALTER FUNCTION 语句"""
        node = parse_statement("ALTER FUNCTION function_name COMMENT 'This is a test function'")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[0].comment, "This is a test function")

    def test_alter_function_with_language_sql(self):
        """测试带有 LANGUAGE SQL 的 ALTER FUNCTION 语句"""
        node = parse_statement("ALTER FUNCTION function_name LANGUAGE SQL")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionLanguageSql)

    def test_alter_function_with_language_identifier(self):
        """测试带有 LANGUAGE 标识符的 ALTER FUNCTION 语句"""
        node = parse_statement("ALTER FUNCTION function_name LANGUAGE C")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionLanguageIdent)
        self.assertEqual(node.option_list[0].language, "C")

    def test_alter_function_with_no_sql(self):
        """测试带有 NO SQL 的 ALTER FUNCTION 语句"""
        node = parse_statement("ALTER FUNCTION function_name NO SQL")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionNoSql)

    def test_alter_function_with_contains_sql(self):
        """测试带有 CONTAINS SQL 的 ALTER FUNCTION 语句"""
        node = parse_statement("ALTER FUNCTION function_name CONTAINS SQL")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionContainsSql)

    def test_alter_function_with_reads_sql_data(self):
        """测试带有 READS SQL DATA 的 ALTER FUNCTION 语句"""
        node = parse_statement("ALTER FUNCTION function_name READS SQL DATA")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionReadsSqlData)

    def test_alter_function_with_modifies_sql_data(self):
        """测试带有 MODIFIES SQL DATA 的 ALTER FUNCTION 语句"""
        node = parse_statement("ALTER FUNCTION function_name MODIFIES SQL DATA")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionModifiesSqlData)

    def test_alter_function_with_sql_security_definer(self):
        """测试带有 SQL SECURITY DEFINER 的 ALTER FUNCTION 语句"""
        node = parse_statement("ALTER FUNCTION function_name SQL SECURITY DEFINER")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionSqlSecurity)
        self.assertEqual(node.option_list[0].security, ast.EnumSqlSecurity.DEFINER)

    def test_alter_function_with_sql_security_invoker(self):
        """测试带有 SQL SECURITY INVOKER 的 ALTER FUNCTION 语句"""
        node = parse_statement("ALTER FUNCTION function_name SQL SECURITY INVOKER")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionSqlSecurity)
        self.assertEqual(node.option_list[0].security, ast.EnumSqlSecurity.INVOKER)

    def test_alter_function_with_multiple_options(self):
        """测试包含多个选项的 ALTER FUNCTION 语句"""
        node = parse_statement("ALTER FUNCTION function_name COMMENT 'Test function' LANGUAGE SQL CONTAINS SQL")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 3)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[0].comment, "Test function")
        self.assertIsInstance(node.option_list[1], ast.FunctionOptionLanguageSql)
        self.assertIsInstance(node.option_list[2], ast.FunctionOptionContainsSql)

    def test_alter_function_with_all_options(self):
        """测试包含所有选项的 ALTER FUNCTION 语句"""
        node = parse_statement("ALTER FUNCTION function_name COMMENT 'Complete function' LANGUAGE SQL READS SQL DATA SQL SECURITY DEFINER")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 4)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[0].comment, "Complete function")
        self.assertIsInstance(node.option_list[1], ast.FunctionOptionLanguageSql)
        self.assertIsInstance(node.option_list[2], ast.FunctionOptionReadsSqlData)
        self.assertIsInstance(node.option_list[3], ast.FunctionOptionSqlSecurity)
        self.assertEqual(node.option_list[3].security, ast.EnumSqlSecurity.DEFINER)

    def test_alter_function_with_schema_qualified_name(self):
        """测试使用模式限定名称的 ALTER FUNCTION 语句"""
        node = parse_statement("ALTER FUNCTION database_name.function_name COMMENT 'Function in schema'")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.schema_name, "database_name")
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[0].comment, "Function in schema")

    def test_alter_function_with_quoted_name(self):
        """测试使用引号的函数名称"""
        node = parse_statement("ALTER FUNCTION `function_name` COMMENT 'Quoted function name'")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[0].comment, "Quoted function name")

    def test_alter_function_with_different_languages(self):
        """测试不同语言的 ALTER FUNCTION 语句"""
        # 测试 C 语言
        node = parse_statement("ALTER FUNCTION function_name LANGUAGE C")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionLanguageIdent)
        self.assertEqual(node.option_list[0].language, "C")

        # 测试 Python 语言
        node = parse_statement("ALTER FUNCTION function_name LANGUAGE Python")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionLanguageIdent)
        self.assertEqual(node.option_list[0].language, "Python")

    def test_alter_function_with_sql_data_access_options(self):
        """测试 SQL 数据访问选项的组合"""
        # 测试 NO SQL 和 COMMENT
        node = parse_statement("ALTER FUNCTION function_name NO SQL COMMENT 'No SQL function'")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 2)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionNoSql)
        self.assertIsInstance(node.option_list[1], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[1].comment, "No SQL function")

        # 测试 READS SQL DATA 和 SQL SECURITY
        node = parse_statement("ALTER FUNCTION function_name READS SQL DATA SQL SECURITY INVOKER")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 2)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionReadsSqlData)
        self.assertIsInstance(node.option_list[1], ast.FunctionOptionSqlSecurity)
        self.assertEqual(node.option_list[1].security, ast.EnumSqlSecurity.INVOKER)

    def test_alter_function_with_comment_variations(self):
        """测试注释选项的不同变体"""
        # 测试单引号注释
        node = parse_statement("ALTER FUNCTION function_name COMMENT 'Single quote comment'")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[0].comment, "Single quote comment")

        # 测试双引号注释
        node = parse_statement('ALTER FUNCTION function_name COMMENT "Double quote comment"')
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[0].comment, "Double quote comment")

    def test_alter_function_with_complex_combinations(self):
        """测试复杂的选项组合"""
        # 测试数据访问和安全性组合
        node = parse_statement("ALTER FUNCTION function_name MODIFIES SQL DATA SQL SECURITY DEFINER COMMENT 'Complex function'")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 3)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionModifiesSqlData)
        self.assertIsInstance(node.option_list[1], ast.FunctionOptionSqlSecurity)
        self.assertEqual(node.option_list[1].security, ast.EnumSqlSecurity.DEFINER)
        self.assertIsInstance(node.option_list[2], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[2].comment, "Complex function")

    def test_alter_function_with_language_and_data_access(self):
        """测试语言和数据访问选项的组合"""
        node = parse_statement("ALTER FUNCTION function_name LANGUAGE SQL CONTAINS SQL")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 2)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionLanguageSql)
        self.assertIsInstance(node.option_list[1], ast.FunctionOptionContainsSql)

    def test_alter_function_with_empty_comment(self):
        """测试空注释的 ALTER FUNCTION 语句"""
        node = parse_statement("ALTER FUNCTION function_name COMMENT ''")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[0].comment, "")

    def test_alter_function_security_variations(self):
        """测试安全性选项的变体"""
        # 测试 DEFINER 安全性
        node = parse_statement("ALTER FUNCTION function_name SQL SECURITY DEFINER")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionSqlSecurity)
        self.assertEqual(node.option_list[0].security, ast.EnumSqlSecurity.DEFINER)

        # 测试 INVOKER 安全性
        node = parse_statement("ALTER FUNCTION function_name SQL SECURITY INVOKER")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionSqlSecurity)
        self.assertEqual(node.option_list[0].security, ast.EnumSqlSecurity.INVOKER)

    def test_alter_function_with_mixed_order_options(self):
        """测试不同顺序的选项组合"""
        node = parse_statement("ALTER FUNCTION function_name SQL SECURITY INVOKER COMMENT 'Mixed order' LANGUAGE SQL")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 3)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionSqlSecurity)
        self.assertEqual(node.option_list[0].security, ast.EnumSqlSecurity.INVOKER)
        self.assertIsInstance(node.option_list[1], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[1].comment, "Mixed order")
        self.assertIsInstance(node.option_list[2], ast.FunctionOptionLanguageSql)

    def test_alter_function_with_long_comment(self):
        """测试长注释的 ALTER FUNCTION 语句"""
        long_comment = "This is a very long comment that describes the function in detail and explains its purpose and functionality"
        node = parse_statement(f"ALTER FUNCTION function_name COMMENT '{long_comment}'")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[0].comment, long_comment)

    def test_alter_function_with_special_characters_in_name(self):
        """测试包含特殊字符的函数名称"""
        node = parse_statement("ALTER FUNCTION `function_name_with_123` COMMENT 'Special name'")
        self.assertIsInstance(node, ast.AlterFunctionStatement)
        self.assertIsInstance(node.function_name, ast.Identifier)
        self.assertEqual(node.function_name.object_name, "function_name_with_123")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[0].comment, "Special name") 