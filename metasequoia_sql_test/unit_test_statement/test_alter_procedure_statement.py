"""
ALTER PROCEDURE 语句（alter_procedure_statement）单元测试

测试 alter_procedure_statement.py 中的语义组：
- alter_procedure_statement: ALTER PROCEDURE 语句
"""

from unittest import TestCase

from metasequoia_sql import ast, parse_statement


class TestAlterProcedureStatement(TestCase):
    """测试 alter_procedure_statement 语义组
    
    测试 ALTER PROCEDURE 语句的解析，包括存储过程名称和各种选项的不同组合
    """

    def test_alter_procedure_with_comment(self):
        """测试带有注释的 ALTER PROCEDURE 语句"""
        node = parse_statement("ALTER PROCEDURE procedure_name COMMENT 'This is a test procedure'")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[0].comment, "This is a test procedure")

    def test_alter_procedure_with_language_sql(self):
        """测试带有 LANGUAGE SQL 的 ALTER PROCEDURE 语句"""
        node = parse_statement("ALTER PROCEDURE procedure_name LANGUAGE SQL")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionLanguageSql)

    def test_alter_procedure_with_language_identifier(self):
        """测试带有 LANGUAGE 标识符的 ALTER PROCEDURE 语句"""
        node = parse_statement("ALTER PROCEDURE procedure_name LANGUAGE C")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionLanguageIdent)
        self.assertEqual(node.option_list[0].language, "C")

    def test_alter_procedure_with_no_sql(self):
        """测试带有 NO SQL 的 ALTER PROCEDURE 语句"""
        node = parse_statement("ALTER PROCEDURE procedure_name NO SQL")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionNoSql)

    def test_alter_procedure_with_contains_sql(self):
        """测试带有 CONTAINS SQL 的 ALTER PROCEDURE 语句"""
        node = parse_statement("ALTER PROCEDURE procedure_name CONTAINS SQL")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionContainsSql)

    def test_alter_procedure_with_reads_sql_data(self):
        """测试带有 READS SQL DATA 的 ALTER PROCEDURE 语句"""
        node = parse_statement("ALTER PROCEDURE procedure_name READS SQL DATA")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionReadsSqlData)

    def test_alter_procedure_with_modifies_sql_data(self):
        """测试带有 MODIFIES SQL DATA 的 ALTER PROCEDURE 语句"""
        node = parse_statement("ALTER PROCEDURE procedure_name MODIFIES SQL DATA")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionModifiesSqlData)

    def test_alter_procedure_with_sql_security_definer(self):
        """测试带有 SQL SECURITY DEFINER 的 ALTER PROCEDURE 语句"""
        node = parse_statement("ALTER PROCEDURE procedure_name SQL SECURITY DEFINER")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionSqlSecurity)
        self.assertEqual(node.option_list[0].security, ast.EnumSqlSecurity.DEFINER)

    def test_alter_procedure_with_sql_security_invoker(self):
        """测试带有 SQL SECURITY INVOKER 的 ALTER PROCEDURE 语句"""
        node = parse_statement("ALTER PROCEDURE procedure_name SQL SECURITY INVOKER")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionSqlSecurity)
        self.assertEqual(node.option_list[0].security, ast.EnumSqlSecurity.INVOKER)

    def test_alter_procedure_with_multiple_options(self):
        """测试包含多个选项的 ALTER PROCEDURE 语句"""
        node = parse_statement("ALTER PROCEDURE procedure_name COMMENT 'Test procedure' LANGUAGE SQL CONTAINS SQL")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 3)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[0].comment, "Test procedure")
        self.assertIsInstance(node.option_list[1], ast.FunctionOptionLanguageSql)
        self.assertIsInstance(node.option_list[2], ast.FunctionOptionContainsSql)

    def test_alter_procedure_with_all_options(self):
        """测试包含所有选项的 ALTER PROCEDURE 语句"""
        node = parse_statement("ALTER PROCEDURE procedure_name COMMENT 'Complete procedure' LANGUAGE SQL READS SQL DATA SQL SECURITY DEFINER")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 4)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[0].comment, "Complete procedure")
        self.assertIsInstance(node.option_list[1], ast.FunctionOptionLanguageSql)
        self.assertIsInstance(node.option_list[2], ast.FunctionOptionReadsSqlData)
        self.assertIsInstance(node.option_list[3], ast.FunctionOptionSqlSecurity)
        self.assertEqual(node.option_list[3].security, ast.EnumSqlSecurity.DEFINER)

    def test_alter_procedure_with_schema_qualified_name(self):
        """测试使用模式限定名称的 ALTER PROCEDURE 语句"""
        node = parse_statement("ALTER PROCEDURE database_name.procedure_name COMMENT 'Procedure in schema'")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.schema_name, "database_name")
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[0].comment, "Procedure in schema")

    def test_alter_procedure_with_quoted_name(self):
        """测试使用引号的存储过程名称"""
        node = parse_statement("ALTER PROCEDURE `procedure_name` COMMENT 'Quoted procedure name'")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[0].comment, "Quoted procedure name")

    def test_alter_procedure_with_different_languages(self):
        """测试不同语言的 ALTER PROCEDURE 语句"""
        # 测试 C 语言
        node = parse_statement("ALTER PROCEDURE procedure_name LANGUAGE C")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionLanguageIdent)
        self.assertEqual(node.option_list[0].language, "C")

        # 测试 Python 语言
        node = parse_statement("ALTER PROCEDURE procedure_name LANGUAGE Python")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionLanguageIdent)
        self.assertEqual(node.option_list[0].language, "Python")

    def test_alter_procedure_with_sql_data_access_options(self):
        """测试 SQL 数据访问选项的组合"""
        # 测试 NO SQL 和 COMMENT
        node = parse_statement("ALTER PROCEDURE procedure_name NO SQL COMMENT 'No SQL procedure'")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 2)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionNoSql)
        self.assertIsInstance(node.option_list[1], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[1].comment, "No SQL procedure")

        # 测试 READS SQL DATA 和 SQL SECURITY
        node = parse_statement("ALTER PROCEDURE procedure_name READS SQL DATA SQL SECURITY INVOKER")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 2)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionReadsSqlData)
        self.assertIsInstance(node.option_list[1], ast.FunctionOptionSqlSecurity)
        self.assertEqual(node.option_list[1].security, ast.EnumSqlSecurity.INVOKER)

    def test_alter_procedure_with_comment_variations(self):
        """测试注释选项的不同变体"""
        # 测试单引号注释
        node = parse_statement("ALTER PROCEDURE procedure_name COMMENT 'Single quote comment'")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[0].comment, "Single quote comment")

        # 测试双引号注释
        node = parse_statement('ALTER PROCEDURE procedure_name COMMENT "Double quote comment"')
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[0].comment, "Double quote comment")

    def test_alter_procedure_with_complex_combinations(self):
        """测试复杂的选项组合"""
        # 测试数据访问和安全性组合
        node = parse_statement("ALTER PROCEDURE procedure_name MODIFIES SQL DATA SQL SECURITY DEFINER COMMENT 'Complex procedure'")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 3)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionModifiesSqlData)
        self.assertIsInstance(node.option_list[1], ast.FunctionOptionSqlSecurity)
        self.assertEqual(node.option_list[1].security, ast.EnumSqlSecurity.DEFINER)
        self.assertIsInstance(node.option_list[2], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[2].comment, "Complex procedure")

    def test_alter_procedure_with_language_and_data_access(self):
        """测试语言和数据访问选项的组合"""
        node = parse_statement("ALTER PROCEDURE procedure_name LANGUAGE SQL CONTAINS SQL")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 2)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionLanguageSql)
        self.assertIsInstance(node.option_list[1], ast.FunctionOptionContainsSql)

    def test_alter_procedure_with_empty_comment(self):
        """测试空注释的 ALTER PROCEDURE 语句"""
        node = parse_statement("ALTER PROCEDURE procedure_name COMMENT ''")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[0].comment, "")

    def test_alter_procedure_security_variations(self):
        """测试安全性选项的变体"""
        # 测试 DEFINER 安全性
        node = parse_statement("ALTER PROCEDURE procedure_name SQL SECURITY DEFINER")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionSqlSecurity)
        self.assertEqual(node.option_list[0].security, ast.EnumSqlSecurity.DEFINER)

        # 测试 INVOKER 安全性
        node = parse_statement("ALTER PROCEDURE procedure_name SQL SECURITY INVOKER")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionSqlSecurity)
        self.assertEqual(node.option_list[0].security, ast.EnumSqlSecurity.INVOKER)

    def test_alter_procedure_with_mixed_order_options(self):
        """测试不同顺序的选项组合"""
        node = parse_statement("ALTER PROCEDURE procedure_name SQL SECURITY INVOKER COMMENT 'Mixed order' LANGUAGE SQL")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 3)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionSqlSecurity)
        self.assertEqual(node.option_list[0].security, ast.EnumSqlSecurity.INVOKER)
        self.assertIsInstance(node.option_list[1], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[1].comment, "Mixed order")
        self.assertIsInstance(node.option_list[2], ast.FunctionOptionLanguageSql)

    def test_alter_procedure_with_long_comment(self):
        """测试长注释的 ALTER PROCEDURE 语句"""
        long_comment = "This is a very long comment that describes the procedure in detail and explains its purpose and functionality"
        node = parse_statement(f"ALTER PROCEDURE procedure_name COMMENT '{long_comment}'")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[0].comment, long_comment)

    def test_alter_procedure_with_special_characters_in_name(self):
        """测试包含特殊字符的存储过程名称"""
        node = parse_statement("ALTER PROCEDURE `procedure_name_with_123` COMMENT 'Special name'")
        self.assertIsInstance(node, ast.AlterProcedureStatement)
        self.assertIsInstance(node.procedure_name, ast.Identifier)
        self.assertEqual(node.procedure_name.object_name, "procedure_name_with_123")
        self.assertEqual(len(node.option_list), 1)
        self.assertIsInstance(node.option_list[0], ast.FunctionOptionComment)
        self.assertEqual(node.option_list[0].comment, "Special name")

    def test_alter_procedure_comprehensive_scenarios(self):
        """测试综合场景"""
        # 测试所有主要选项类型
        test_cases = [
            ("ALTER PROCEDURE proc1 COMMENT 'Test procedure'", 1),
            ("ALTER PROCEDURE proc1 LANGUAGE SQL", 1),
            ("ALTER PROCEDURE proc1 CONTAINS SQL", 1),
            ("ALTER PROCEDURE proc1 READS SQL DATA", 1),
            ("ALTER PROCEDURE proc1 MODIFIES SQL DATA", 1),
            ("ALTER PROCEDURE proc1 SQL SECURITY DEFINER", 1),
            ("ALTER PROCEDURE proc1 SQL SECURITY INVOKER", 1),
            ("ALTER PROCEDURE proc1 NO SQL", 1),
            ("ALTER PROCEDURE proc1 LANGUAGE SQL CONTAINS SQL READS SQL DATA", 3),
        ]

        for sql, expected_option_count in test_cases:
            with self.subTest(sql=sql):
                node = parse_statement(sql)
                self.assertIsInstance(node, ast.AlterProcedureStatement)
                self.assertEqual(len(node.option_list), expected_option_count) 