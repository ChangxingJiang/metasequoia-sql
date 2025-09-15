"""
ALTER VIEW 语句（alter_view_statement）单元测试

测试 alter_view_statement.py 中的语义组：
- alter_view_statement: ALTER VIEW 语句
"""

from unittest import TestCase

from metasequoia_sql import ast, parse_statement


class TestAlterViewStatement(TestCase):
    """测试 alter_view_statement 语义组
    
    测试 ALTER VIEW 语句的解析，包括算法类型、定义者、安全模式、列列表等不同组合
    """

    def test_alter_view_basic(self):
        """测试基本的 ALTER VIEW 语句"""
        node = parse_statement("ALTER VIEW view_name AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertIsNotNone(node.algorithm)
        self.assertIsNone(node.definer)
        self.assertIsNotNone(node.suid)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertEqual(len(node.column_list), 0)
        self.assertIsInstance(node.query_expression, ast.QueryExpression)
        self.assertIsNotNone(node.check_option)

    def test_alter_view_with_algorithm_undefined(self):
        """测试指定 ALGORITHM = UNDEFINED 的 ALTER VIEW 语句"""
        node = parse_statement("ALTER ALGORITHM = UNDEFINED VIEW view_name AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertIsNotNone(node.algorithm)
        self.assertEqual(node.algorithm, ast.EnumViewAlgorithmType.UNDEFINED)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_alter_view_with_algorithm_merge(self):
        """测试指定 ALGORITHM = MERGE 的 ALTER VIEW 语句"""
        node = parse_statement("ALTER ALGORITHM = MERGE VIEW view_name AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertIsNotNone(node.algorithm)
        self.assertEqual(node.algorithm, ast.EnumViewAlgorithmType.MERGE)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_alter_view_with_algorithm_temptable(self):
        """测试指定 ALGORITHM = TEMPTABLE 的 ALTER VIEW 语句"""
        node = parse_statement("ALTER ALGORITHM = TEMPTABLE VIEW view_name AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertIsNotNone(node.algorithm)
        self.assertEqual(node.algorithm, ast.EnumViewAlgorithmType.TEMPTABLE)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_alter_view_with_definer_user(self):
        """测试指定 DEFINER = user 的 ALTER VIEW 语句"""
        node = parse_statement("ALTER DEFINER = 'user'@'localhost' VIEW view_name AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertIsNotNone(node.definer)
        self.assertIsInstance(node.definer, ast.UserName)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_alter_view_with_definer_current_user(self):
        """测试指定 DEFINER = CURRENT_USER 的 ALTER VIEW 语句"""
        node = parse_statement("ALTER DEFINER = CURRENT_USER VIEW view_name AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertIsNotNone(node.definer)
        self.assertIsInstance(node.definer, ast.UserName)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_alter_view_with_sql_security_definer(self):
        """测试指定 SQL SECURITY DEFINER 的 ALTER VIEW 语句"""
        node = parse_statement("ALTER SQL SECURITY DEFINER VIEW view_name AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertIsNotNone(node.suid)
        self.assertEqual(node.suid, ast.EnumViewSuidType.DEFINER)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_alter_view_with_sql_security_invoker(self):
        """测试指定 SQL SECURITY INVOKER 的 ALTER VIEW 语句"""
        node = parse_statement("ALTER SQL SECURITY INVOKER VIEW view_name AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertIsNotNone(node.suid)
        self.assertEqual(node.suid, ast.EnumViewSuidType.INVOKER)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_alter_view_with_column_list(self):
        """测试指定列列表的 ALTER VIEW 语句"""
        node = parse_statement("ALTER VIEW view_name (column_name_1, column_name_2) AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertEqual(len(node.column_list), 2)
        self.assertEqual(node.column_list[0], "column_name_1")
        self.assertEqual(node.column_list[1], "column_name_2")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_alter_view_with_single_column(self):
        """测试指定单个列的 ALTER VIEW 语句"""
        node = parse_statement("ALTER VIEW view_name (column_name) AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertEqual(len(node.column_list), 1)
        self.assertEqual(node.column_list[0], "column_name")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_alter_view_with_check_option_cascaded(self):
        """测试指定 WITH CASCADED CHECK OPTION 的 ALTER VIEW 语句"""
        node = parse_statement("ALTER VIEW view_name AS SELECT * FROM table_name WITH CASCADED CHECK OPTION")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)
        self.assertIsNotNone(node.check_option)
        self.assertEqual(node.check_option, ast.EnumViewCheckOption.CASCADED)

    def test_alter_view_with_check_option_local(self):
        """测试指定 WITH LOCAL CHECK OPTION 的 ALTER VIEW 语句"""
        node = parse_statement("ALTER VIEW view_name AS SELECT * FROM table_name WITH LOCAL CHECK OPTION")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)
        self.assertIsNotNone(node.check_option)
        self.assertEqual(node.check_option, ast.EnumViewCheckOption.LOCAL)

    def test_alter_view_with_check_option_default(self):
        """测试指定 WITH CHECK OPTION 的 ALTER VIEW 语句（默认形式）"""
        node = parse_statement("ALTER VIEW view_name AS SELECT * FROM table_name WITH CHECK OPTION")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)
        self.assertIsNotNone(node.check_option)
        self.assertEqual(node.check_option, ast.EnumViewCheckOption.CASCADED)

    def test_alter_view_with_all_options(self):
        """测试包含所有选项的 ALTER VIEW 语句"""
        node = parse_statement(
            "ALTER ALGORITHM = MERGE DEFINER = 'user'@'localhost' SQL SECURITY DEFINER VIEW view_name "
            "(column_name_1, column_name_2) AS SELECT * FROM table_name WITH CASCADED CHECK OPTION"
        )
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(node.algorithm, ast.EnumViewAlgorithmType.MERGE)
        self.assertIsNotNone(node.definer)
        self.assertIsInstance(node.definer, ast.UserName)
        self.assertEqual(node.suid, ast.EnumViewSuidType.DEFINER)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertEqual(len(node.column_list), 2)
        self.assertEqual(node.column_list[0], "column_name_1")
        self.assertEqual(node.column_list[1], "column_name_2")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)
        self.assertEqual(node.check_option, ast.EnumViewCheckOption.CASCADED)

    def test_alter_view_with_quoted_view_name(self):
        """测试使用引号的视图名称"""
        node = parse_statement("ALTER VIEW `view_name` AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_alter_view_with_database_qualified_name(self):
        """测试使用数据库限定名称的视图"""
        node = parse_statement("ALTER VIEW database_name.view_name AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertIsInstance(node.table_ident, ast.Identifier)
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_alter_view_with_complex_query(self):
        """测试复杂查询的 ALTER VIEW 语句"""
        node = parse_statement(
            "ALTER VIEW view_name AS SELECT column_name_1, column_name_2 FROM table_name WHERE column_name_1 > 0"
        )
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_alter_view_with_join_query(self):
        """测试包含连接的查询的 ALTER VIEW 语句"""
        node = parse_statement(
            "ALTER VIEW view_name AS SELECT t1.column_name, t2.column_name FROM table_name_1 t1 "
            "JOIN table_name_2 t2 ON t1.id = t2.id"
        )
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_alter_view_with_subquery(self):
        """测试包含子查询的 ALTER VIEW 语句"""
        node = parse_statement(
            "ALTER VIEW view_name AS SELECT * FROM table_name WHERE column_name IN "
            "(SELECT column_name FROM table_name_2)"
        )
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_alter_view_with_order_by_and_limit(self):
        """测试包含 ORDER BY 和 LIMIT 的 ALTER VIEW 语句"""
        node = parse_statement(
            "ALTER VIEW view_name AS SELECT * FROM table_name ORDER BY column_name LIMIT 10"
        )
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_alter_view_algorithm_without_equal_sign(self):
        """测试不使用等号的算法选项"""
        node = parse_statement("ALTER ALGORITHM UNDEFINED VIEW view_name AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertIsNotNone(node.algorithm)
        self.assertEqual(node.algorithm, ast.EnumViewAlgorithmType.UNDEFINED)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_alter_view_definer_without_equal_sign(self):
        """测试不使用等号的定义者选项"""
        node = parse_statement("ALTER DEFINER CURRENT_USER VIEW view_name AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertIsNotNone(node.definer)
        self.assertIsInstance(node.definer, ast.UserName)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_alter_view_with_union_query(self):
        """测试包含 UNION 的查询的 ALTER VIEW 语句"""
        node = parse_statement(
            "ALTER VIEW view_name AS SELECT * FROM table_name_1 UNION SELECT * FROM table_name_2"
        )
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_alter_view_with_group_by_and_having(self):
        """测试包含 GROUP BY 和 HAVING 的 ALTER VIEW 语句"""
        node = parse_statement(
            "ALTER VIEW view_name AS SELECT column_name, COUNT(*) FROM table_name "
            "GROUP BY column_name HAVING COUNT(*) > 1"
        )
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(node.table_ident.object_name, "view_name")
        self.assertIsInstance(node.query_expression, ast.QueryExpression)

    def test_alter_view_multiple_algorithms(self):
        """测试不同算法类型的组合"""
        # 测试 MERGE 算法
        node = parse_statement("ALTER ALGORITHM = MERGE VIEW view_name AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(node.algorithm, ast.EnumViewAlgorithmType.MERGE)
        
        # 测试 TEMPTABLE 算法
        node = parse_statement("ALTER ALGORITHM = TEMPTABLE VIEW view_name AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(node.algorithm, ast.EnumViewAlgorithmType.TEMPTABLE)

    def test_alter_view_multiple_security_modes(self):
        """测试不同安全模式的组合"""
        # 测试 DEFINER 模式
        node = parse_statement("ALTER SQL SECURITY DEFINER VIEW view_name AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(node.suid, ast.EnumViewSuidType.DEFINER)
        
        # 测试 INVOKER 模式
        node = parse_statement("ALTER SQL SECURITY INVOKER VIEW view_name AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(node.suid, ast.EnumViewSuidType.INVOKER)

    def test_alter_view_different_check_options(self):
        """测试不同检查选项的组合"""
        # 测试 CASCADED CHECK OPTION
        node = parse_statement("ALTER VIEW view_name AS SELECT * FROM table_name WITH CASCADED CHECK OPTION")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(node.check_option, ast.EnumViewCheckOption.CASCADED)
        
        # 测试 LOCAL CHECK OPTION
        node = parse_statement("ALTER VIEW view_name AS SELECT * FROM table_name WITH LOCAL CHECK OPTION")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(node.check_option, ast.EnumViewCheckOption.LOCAL)

    def test_alter_view_with_different_user_formats(self):
        """测试不同用户格式的定义者"""
        # 测试带引号的用户名
        node = parse_statement("ALTER DEFINER = 'user'@'localhost' VIEW view_name AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertIsInstance(node.definer, ast.UserName)
        
        # 测试不带引号的用户名
        node = parse_statement("ALTER DEFINER = user@localhost VIEW view_name AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertIsInstance(node.definer, ast.UserName)

    def test_alter_view_with_varying_column_count(self):
        """测试不同列数量的视图"""
        # 测试三个列
        node = parse_statement("ALTER VIEW view_name (column_name_1, column_name_2, column_name_3) AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(len(node.column_list), 3)
        self.assertEqual(node.column_list[0], "column_name_1")
        self.assertEqual(node.column_list[1], "column_name_2")
        self.assertEqual(node.column_list[2], "column_name_3")
        
        # 测试四个列
        node = parse_statement("ALTER VIEW view_name (column_name_1, column_name_2, column_name_3, column_name_4) AS SELECT * FROM table_name")
        self.assertIsInstance(node, ast.AlterViewStatement)
        self.assertEqual(len(node.column_list), 4)
        self.assertEqual(node.column_list[0], "column_name_1")
        self.assertEqual(node.column_list[1], "column_name_2")
        self.assertEqual(node.column_list[2], "column_name_3")
        self.assertEqual(node.column_list[3], "column_name_4") 